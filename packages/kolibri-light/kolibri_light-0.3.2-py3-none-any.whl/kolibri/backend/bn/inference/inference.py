"""Inferences.

Description
-----------
Inference is same as asking conditional probability questions to the models.
"""
# ------------------------------------
# Name        : inference.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Licence     : See licences
# ------------------------------------


# %% Libraries
from kolibri.backend.bn.ExactInference import VariableElimination
import numpy as np
from kolibri.backend.bn.bnlearn import query2df, to_bayesiannetwork

# %% Exact inference using Variable Elimination
def fit(model, variables=None, evidence=None, to_df=True, verbose=3):
    """Inference using using Variable Elimination.

    Parameters
    ----------
    model : dict
        Contains model.
    variables : List, optional
        For exact inference, P(variables | evidence). The default is None.
            * ['Name_of_node_1']
            * ['Name_of_node_1', 'Name_of_node_2']
    evidence : dict, optional
        For exact inference, P(variables | evidence). The default is None.
            * {'Rain':1}
            * {'Rain':1, 'Sprinkler':0, 'Cloudy':1}
    to_df : Bool, (default is True)
        The output is converted in the dataframe [query.df]. Enabling this function may heavily impact the processing speed.
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    query inference object.

    Examples
    --------

    """
    if not isinstance(model, dict): raise Exception('[bnlearn] >Error: Input requires a object that contains the key: model.')
    adjmat = model['adjmat']
    if not np.all(np.isin(variables, adjmat.columns)):
        raise Exception('[bnlearn] >Error: [variables] should match names in the model (Case sensitive!)')
    if not np.all(np.isin([*evidence.keys()], adjmat.columns)):
        raise Exception('[bnlearn] >Error: [evidence] should match names in the model (Case sensitive!)')
    if verbose>=3: print('[bnlearn] >Variable Elimination..')

    # Extract model
    if isinstance(model, dict):
        model = model['model']

    # Check BayesianNetwork
    if 'BayesianNetwork' not in str(type(model)):
        if verbose>=1: print('[bnlearn] >Warning: Inference requires BayesianNetwork. hint: try: parameter_learning.fit(DAG, df, methodtype="bayes") <return>')
        return None

    # Convert to BayesianNetwork
    if 'BayesianNetwork' not in str(type(model)):
        model = to_bayesiannetwork(adjmat, verbose=verbose)

    try:
        model_infer = VariableElimination(model)
    except:
        raise Exception('[bnlearn] >Error: Input model does not contain learned CPDs. hint: did you run parameter_learning.fit?')

    # Computing the probability P(class | evidence)
    query = model_infer.query(variables=variables, evidence=evidence, show_progress=(verbose>0))
    # Store also in dataframe
    query.df = query2df(query, variables=variables, verbose=verbose) if to_df else None
    # Return
    return(query)
