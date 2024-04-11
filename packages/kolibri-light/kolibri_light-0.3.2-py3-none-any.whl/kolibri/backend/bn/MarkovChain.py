#!/usr/bin/env python3
from collections import defaultdict
from warnings import warn

import numpy as np
from pandas import DataFrame
from scipy.linalg import eig

from kolibri.backend.bn.DiscreteFactor import State
from kolibri.utils.mathext import sample_discrete


class MarkovChain(object):
    """
    Class to represent a Markov Chain with multiple kernels for factored state space,
    along with methods to simulate a run.

    Examples
    --------
    """

    def __init__(self, variables=None, card=None, start_state=None):
        """
        Parameters
        ----------
        variables: array-like iterable object
            A list of variables of the model.

        card: array-like iterable object
            A list of cardinalities of the variables.

        start_state: array-like iterable object
            List of tuples representing the starting states of the variables.
        """
        if variables is None:
            variables = []
        if card is None:
            card = []
        if not hasattr(variables, "__iter__") or isinstance(variables, str):
            raise ValueError("variables must be a non-string iterable.")
        if not hasattr(card, "__iter__") or isinstance(card, str):
            raise ValueError("card must be a non-string iterable.")
        self.variables = variables
        self.cardinalities = {v: c for v, c in zip(variables, card)}
        self.transition_models = {var: {} for var in variables}
        if start_state is None or self._check_state(start_state):
            self.state = start_state

    def set_start_state(self, start_state):
        """
        Set the start state of the Markov Chain. If the start_state is given as an array-like iterable, its contents
        are reordered in the internal representation.

        Parameters
        ----------
        start_state: dict or array-like iterable object
            Dict (or list) of tuples representing the starting states of the variables.

        Examples
        --------

        """
        if start_state is not None:
            if not hasattr(start_state, "__iter__") or isinstance(start_state, str):
                raise ValueError("start_state must be a non-string iterable.")
            # Must be an array-like iterable. Reorder according to self.variables.
            state_dict = {var: st for var, st in start_state}
            start_state = [State(var, state_dict[var]) for var in self.variables]
        if start_state is None or self._check_state(start_state):
            self.state = start_state

    def _check_state(self, state):
        """
        Checks if a list representing the state of the variables is valid.
        """
        if not hasattr(state, "__iter__") or isinstance(state, str):
            raise ValueError("Start state must be a non-string iterable object.")
        state_vars = {s.var for s in state}
        if not state_vars == set(self.variables):
            raise ValueError(
                f"Start state must represent a complete assignment to all variables."
                f"Expected variables in state: {state_vars}, Got: {set(self.variables)}."
            )
        for var, val in state:
            if val >= self.cardinalities[var]:
                raise ValueError(f"Assignment {val} to {var} invalid.")
        return True

    def add_variable(self, variable, card=0):
        """
        Add a variable to the model.

        Parameters
        ----------
        variable: any hashable python object

        card: int
            Representing the cardinality of the variable to be added.

        Examples
        --------
        """
        if variable not in self.variables:
            self.variables.append(variable)
        else:
            warn(f"Variable {variable} already exists.")
        self.cardinalities[variable] = card
        self.transition_models[variable] = {}

    def add_variables_from(self, variables, cards):
        """
        Add several variables to the model at once.

        Parameters
        ----------
        variables: array-like iterable object
            List of variables to be added.

        cards: array-like iterable object
            List of cardinalities of the variables to be added.

        Examples
        --------

        """
        for var, card in zip(variables, cards):
            self.add_variable(var, card)

    def add_transition_model(self, variable, transition_model):
        """
        Adds a transition model for a particular variable.

        Parameters
        ----------
        variable: any hashable python object
            must be an existing variable of the model.

        transition_model: dict or 2d array
            dict representing valid transition probabilities defined for every possible state of the variable.
            array represent a square matrix where every row sums to 1,
            array[i,j] indicates the transition probalities from State i to State j

        Examples
        --------


        """
        if isinstance(transition_model, list):
            transition_model = np.array(transition_model, dtype=float)

        # check if the transition model is valid
        if not isinstance(transition_model, dict):
            if not isinstance(transition_model, np.ndarray):
                raise ValueError("Transition model must be a dict or numpy array")
            elif len(transition_model.shape) != 2:
                raise ValueError(
                    f"Transition model must be 2d array.given {transition_model.shape}"
                )
            elif transition_model.shape[0] != transition_model.shape[1]:
                raise ValueError(
                    f"Dimension mismatch {transition_model.shape[0]}!={transition_model.shape[1]}"
                )
            else:
                # convert the matrix to dict
                size = transition_model.shape[0]
                transition_model = dict(
                    (
                        i,
                        dict(
                            (j, float(transition_model[i][j])) for j in range(0, size)
                        ),
                    )
                    for i in range(0, size)
                )

        exp_states = set(range(self.cardinalities[variable]))
        tm_states = set(transition_model.keys())
        if not exp_states == tm_states:
            raise ValueError(
                f"Transitions must be defined for all states of variable {variable}. Expected states: {exp_states}, Got: {tm_states}."
            )

        for _, transition in transition_model.items():
            if not isinstance(transition, dict):
                raise ValueError("Each transition must be a dict.")
            prob_sum = 0

            for _, prob in transition.items():
                if prob < 0 or prob > 1:
                    raise ValueError(
                        "Transitions must represent valid probability weights."
                    )
                prob_sum += prob

            if not np.allclose(prob_sum, 1):
                raise ValueError("Transition probabilities must sum to 1.")

        self.transition_models[variable] = transition_model

    def sample(self, start_state=None, size=1, seed=None):
        """
        Sample from the Markov Chain.

        Parameters
        ----------
        start_state: dict or array-like iterable
            Representing the starting states of the variables. If None is passed, a random start_state is chosen.
        size: int
            Number of samples to be generated.

        Returns
        -------
        pandas.DataFrame

        Examples
        --------

        """
        if start_state is None:
            if self.state is None:
                self.state = self.random_state()
            # else use previously-set state
        else:
            self.set_start_state(start_state)

        sampled = DataFrame(index=range(size), columns=self.variables)
        sampled.loc[0] = [st for var, st in self.state]

        var_states = defaultdict(dict)
        var_values = defaultdict(dict)
        samples = defaultdict(dict)
        for var in self.transition_models.keys():
            for st in self.transition_models[var]:
                var_states[var][st] = list(self.transition_models[var][st].keys())
                var_values[var][st] = list(self.transition_models[var][st].values())
                samples[var][st] = sample_discrete(
                    var_states[var][st], var_values[var][st], size=size, seed=seed
                )

        for i in range(size - 1):
            for j, (var, st) in enumerate(self.state):
                next_st = samples[var][st][i]
                self.state[j] = State(var, next_st)
            sampled.loc[i + 1] = [st for var, st in self.state]

        return sampled

    def prob_from_sample(self, state, sample=None, window_size=None):
        """
        Given an instantiation (partial or complete) of the variables of the model,
        compute the probability of observing it over multiple windows in a given sample.

        If 'sample' is not passed as an argument, generate the statistic by sampling from the
        Markov Chain, starting with a random initial state.

        Examples
        --------

        """
        if sample is None:
            # generate sample of size 10000
            sample = self.sample(self.random_state(), size=10000)
        if window_size is None:
            window_size = len(sample) // 100  # default window size is 100
        windows = len(sample) // window_size
        probabilities = np.zeros(windows)

        for i in range(windows):
            for j in range(window_size):
                ind = i * window_size + j
                state_eq = [sample.loc[ind, v] == s for v, s in state]
                if all(state_eq):
                    probabilities[i] += 1

        return probabilities / window_size

    def generate_sample(self, start_state=None, size=1, seed=None):
        """
        Generator version of self.sample

        Returns
        -------
        List of State namedtuples, representing the assignment to all variables of the model.

        Examples
        --------

        """
        if start_state is None:
            if self.state is None:
                self.state = self.random_state()
            # else use previously-set state
        else:
            self.set_start_state(start_state)
        # sampled.loc[0] = [self.state[var] for var in self.variables]

        for i in range(size):
            for j, (var, st) in enumerate(self.state):
                next_st = sample_discrete(
                    list(self.transition_models[var][st].keys()),
                    list(self.transition_models[var][st].values()),
                    seed=seed,
                )[0]
                self.state[j] = State(var, next_st)
            yield self.state[:]

    def is_stationarity(self, tolerance=0.2, sample=None):
        """
        Checks if the given markov chain is stationary and checks the steady state
        probability values for the state are consistent.

        Parameters
        ----------
        tolerance: float
            represents the diff between actual steady state value and the computed value
        sample: [State(i,j)]
            represents the list of state which the markov chain has sampled

        Returns
        -------
        Boolean:
            True, if the markov chain converges to steady state distribution within the tolerance
            False, if the markov chain does not converge to steady state distribution within tolerance

        Examples
        --------

        """
        keys = self.transition_models.keys()
        return_val = True
        for k in keys:
            # convert dict to numpy matrix
            transition_mat = np.array(
                [
                    np.array(list(self.transition_models[k][i].values()))
                    for i in self.transition_models[k].keys()
                ],
                dtype=float,
            )
            S, U = eig(transition_mat.T)
            stationary = np.array(U[:, np.where(np.abs(S - 1.0) < 1e-8)[0][0]].flat)
            stationary = (stationary / np.sum(stationary)).real

            probabilities = []
            window_size = 10000 if sample is None else len(sample)
            for i in range(0, transition_mat.shape[0]):
                probabilities.extend(
                    self.prob_from_sample([State(k, i)], window_size=window_size)
                )
            if any(
                np.abs(i) > tolerance for i in np.subtract(probabilities, stationary)
            ):
                return_val = return_val and False
            else:
                return_val = return_val and True

        return return_val

    def random_state(self):
        """
        Generates a random state of the Markov Chain.

        Returns
        -------
        List of namedtuples, representing a random assignment to all variables of the model.

        Examples
        --------

        """
        return [
            State(var, np.random.randint(self.cardinalities[var]))
            for var in self.variables
        ]

    def copy(self):
        """
        Returns a copy of Markov Chain Model.

        Returns
        -------
        MarkovChain : Copy of MarkovChain.

        Examples
        --------

        """
        markovchain_copy = MarkovChain(
            variables=list(self.cardinalities.keys()),
            card=list(self.cardinalities.values()),
            start_state=self.state,
        )
        if self.transition_models:
            markovchain_copy.transition_models = self.transition_models.copy()

        return markovchain_copy
