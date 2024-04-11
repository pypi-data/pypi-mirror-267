import logging
import time
from collections import defaultdict
from scipy.sparse import issparse, hstack, vstack, csr_matrix
from abc import ABC
import pandas

from kolibri.core import modules
#from kolibri.core.component import ComponentMetaclass
import numpy as np

LOGGER = logging.getLogger(__name__)


def validate_arguments(pipeline, context, allow_empty_pipeline=False):
    """Validates a pipeline before it is run. Ensures, that all
    arguments are present to train the pipeline."""

    # Ensure the pipeline is not empty
    if not allow_empty_pipeline and len(pipeline) == 0:
        raise ValueError("Can not train an empty pipeline. "
                         "Make sure to specify a proper pipeline in "
                         "the configuration using the `pipeline` key." +
                         "The `backend` configuration key is "
                         "NOT supported anymore.")

    provided_properties = set(context.keys())

    for component in pipeline:
        for r in component.requires:
            if r not in provided_properties:
                raise Exception("Failed to validate at component "
                                "'{}'. Missing property: '{}'"
                                "".format(component.my_name, r))
        provided_properties.update(component.provides)

class Pipeline(ABC):
    """Pipeline Class.

    The **Pipeline** class represents a Machine Learning Pipeline, which
    is an ordered collection of Machine Learning tools or Primitives,
    represented by **Component instances**, that will be executed
    sequentially in order to produce results.

    The Pipeline has two working modes or phases: **fitting** and
    **predicting**.

    During the **fitting** phase, each Component instance, or **component** will be
    fitted and immediately after used to produce results on the same
    fitting data.
    This results will be then passed to the next componenet of the sequence
    as its fitting data, and this process will be repeated until the last
    component is fitted.

    During the **predicting** phase, each component will be used to produce results
    on the output of the previous one, until the last one has produce its
    results, which will be returned as the prediction of the pipelines.
    """

    def _get_tunable_hyperparameters(self):
        """Get the tunable hyperperparameters from all the blocks in this pipelines."""
        tunable = {}
        for step_name, step in self.steps.items():
            tunable[step_name] = step.get_tunable_hyperparameters()

        return tunable

    def _validate_components(self, steps=None):
        if steps is None:
            steps = self.steps
        if not steps:
            return

        self.active = True

        for step in steps:
            if isinstance(step, tuple):
                if step[1].component_type == "estimator":
                    if hasattr(self, 'estimator') and self.estimator is not None:
                        raise ValueError("Only one estimator allowed")
                    self.estimator=step[1]
                if not (hasattr(step[1], "fit") or hasattr(step[1], "fit_transform")) or not hasattr(step[1],
                                                                                                     "transform"):
                    self.active = False
                    raise TypeError(f"Component {step[1]} should implement fit and transform.")
            elif isinstance(step, list):
                # If the step is a list, recursively validate its components
                self._validate_components(step)

    def __init__(self, steps=None, parameters={}):
        self.steps = []
        if steps is not None:
            for step in steps:
                self.steps.append(step)

        self.estimator=None
        self._validate_components()

        self.verbose = parameters.get("verbose", False)

        super(Pipeline, self).__init__()

    @staticmethod
    def from_configs(params):
        """Transform the passed names of the pipeline components into classes"""

        branches = []
        # Transform the passed names of the pipeline components into classes
        for branch_name, branch_params in params.items():
            branch = []
            for component_name, param_val in branch_params.items():
                component = modules.create_component_by_name(
                    component_name, param_val)
                branch.append((component_name, component))
            branches.append(branch)

        return Pipeline(branches)

    @staticmethod
    def _flatten_dict(hyperparameters):
        return {
            (block, name): value
            for block, block_hyperparameters in hyperparameters.items()
            for name, value in block_hyperparameters.items()
        }

    def get_tunable_hyperparameters(self, flat=False):
        """Get the tunable hyperparamters of each block.

        Args:
            flat (bool): If True, return a flattened dictionary where each key
                is a two elements tuple containing the name of the block as the first
                element and the name of the hyperparameter as the second one.
                If False (default), return a dictionary where each key is the name of
                a block and each value is a dictionary containing the complete
                hyperparameter specification of that block.

        Returns:
            dict:
                A dictionary containing the block names as keys and
                the block tunable configs dictionary as values.
        """
        tunables = self._tunable_hyperparameters.copy()
        if flat:
            tunables = self._flatten_dict(tunables)

        return tunables

    @classmethod
    def _sanitize_value(cls, value):
        """Convert numpy values to their python primitive type equivalent.

        If a value is a dict, recursively sanitize its values.

        Args:
            value:
                value to sanitize.

        Returns:
            sanitized value.
        """
        if isinstance(value, dict):
            return {
                key: cls._sanitize_value(value)
                for key, value in value.items()
            }
        if isinstance(value, np.integer):
            return int(value)
        elif isinstance(value, np.floating):
            return float(value)
        elif isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, np.bool_):
            return bool(value)
        elif value == 'None':
            return None

        return value

    @classmethod
    def _sanitize(cls, hyperparameters):
        """Convert tuple hyperparameter keys to nested dicts.

        Also convert numpy types to primary python types.

        The input configs dict can specify them in two formats:

        One is the native MLBlocks format, where each key is the name of a block and each value
        is a dict containing a complete hyperparameter specification for that block::

            {
                'block_name': {
                    'hyperparameter_name': 'hyperparameter_value',
                    ...
                },
                ...
            }

        The other one is an alternative format where each key is a two element tuple containing
        the name of the block as the first element and the name of the hyperparameter as the
        second one::

            {
                ('block_name', 'hyperparameter_name'): 'hyperparameter_value',
                ...
            }


        Args:
            hyperparaeters (dict):
                configs dict to sanitize.

        Returns:
            dict:
                Sanitized dict.
        """
        params_tree = defaultdict(dict)
        for key, value in hyperparameters.items():
            value = cls._sanitize_value(value)
            if isinstance(key, tuple):
                block, hyperparameter = key
                params_tree[block][hyperparameter] = value
            else:
                params_tree[key] = value

        return params_tree

    def flatten_config(self, config):
        flat_config = []

        for item in config:
            if isinstance(item, list):
                flat_config.extend(self. flatten_config(item))
            else:
                flat_config.append(item)

        return flat_config


    @property
    def parameters(self):
        """Get the current hyperparamters of each block.

        Args:
            flat (bool): If True, return a flattened dictionary where each key
                is a two elements tuple containing the name of the block as the first
                element and the name of the hyperparameter as the second one.
                If False (default), return a dictionary where each key is the name of
                a block and each value is a dictionary containing the complete
                hyperparameter specification of that block.

        Returns:
            dict:
                A dictionary containing the block names as keys and
                the current block configs dictionary as values.
        """
        hyperparameters = dict()
        for block_name, block in self.flatten_config(self.steps):
            hyperparameters[block_name] = block.get_hyperparameters()

        return hyperparameters

    def set_hyperparameters(self, hyperparameters):
        """Set new hyperparameter values for some blocks.

        Args:
            hyperparameters (dict):
                A dictionary containing the block names as keys and the new configs
                dictionary as values.
        """
        hyperparameters = self._sanitize(hyperparameters)
        for block_name, block_hyperparams in hyperparameters.items():
            self.steps[block_name].hyperparameters=block_hyperparams

    def fit(self, X, y, X_val=None, y_val=None):

        """ fit
        Sequentially fit and transformer texts in all but last step, then fit
        the model_type in last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            The texts upon which the transforms/estimator will create their
            model_type.
        y: An array_like object of length_train n_samples
            Contains the true class y_values for all the samples in data.
        Returns
        -------
        Pipeline
            self
        """

        Xt, y, Xt_val, y_val=self.fit_transformers(self.steps, X, y, X_val,y_val)

        return self.fit_estimator(Xt, y, Xt_val, y_val)



    def _is_transformer(self, component):
        return (hasattr(component, 'component_type') and component.component_type == "transformer") and (hasattr(component, 'transform') or hasattr(component, 'fit_transform'))



    def _is_estimator(self, component):
        return  (hasattr(component, 'component_type') and component.component_type == "estimator") or hasattr(component, 'fit') and (hasattr(component, 'predict') or hasattr(component, 'predict_proba'))


    def fit_transformers(self, steps, X, y, X_val=None, y_val=None, fitted_config=[], fitted_config_transformed=[]):
        for step in steps:
            if isinstance(step, list):
                # A branch is a list of stages
                X_transformed, y, X_val_transformed, y_val = self.fit_transformers(step, X, y, X_val, y_val, fitted_config, fitted_config_transformed)
                fitted_config.append(X_transformed)
                if X_val_transformed is not None:
                    fitted_config_transformed.append(X_val_transformed)
            elif step[0] == 'join':
                # A join operation
                X= self.concatenate_matrices([branch_transformed for branch_transformed in fitted_config], axis=1)
                if fitted_config_transformed:
                    X_val = self.concatenate_matrices([branch_transformed for branch_transformed in fitted_config], axis=1)

                if self._is_transformer(step[1]):
                    X, y, X_val, y_val=self.fit_transformer(step[1], X, y, X_val, y_val)
            else:
                if self._is_transformer(step[1]):
                    X, y, X_val, y_val=self.fit_transformer(step[1], X, y, X_val, y_val)

        return X, y, X_val, y_val

    def concatenate_matrices(self, mat_array, axis=1):
        # Convert all matrices in array to csr format if they're not already
        mat_array = [mat if issparse(mat) else csr_matrix(mat) for mat in mat_array]

        if axis == 0:
            return vstack(mat_array)
        else:
            return hstack(mat_array)

    def fit_transformer(self, transformer, Xt, y, Xt_val=None, y_val=None):

        start=time.time()
        if transformer is None:
            pass
        if hasattr(transformer, "fit_transform"):
            Xt = transformer.fit_transform(Xt, y)
            if Xt_val is not None:
                Xt_val = transformer.fit_transform(Xt_val, y_val)
        else:
            Xt = transformer.fit(Xt, y).transform(Xt)
            if Xt_val is not None:
                Xt_val = transformer.transform(Xt_val)
        print('fitted component ' + transformer.name + '. Elapsed time ' + str(time.time() - start))

        return Xt, y, Xt_val, y_val

    def fit_estimator(self, Xt, y, Xt_val=None, y_val=None):
        if self.estimator is not None:
            print('fitting estimator '+ self.estimator.name)
            try:
                return self.estimator.fit(Xt, y, Xt_val, y_val)
            except Exception as e:
                return self.estimator.fit(Xt, y)

    def predict(self, X):
        """ predict
        Sequentially applies all transforms and then predict with last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            All the samples we want to predict the label for.
        Returns
        -------
        list
            The predicted class label for all the samples in data.
        """

        if isinstance(X, np.ndarray):
            X=X.tolist()
        if isinstance(X, list) or isinstance(X, pandas.DataFrame):
            Xt = X
        else:
            Xt=[X]

        Xt= self._predict_transform(self.steps, Xt, [])
        if self.estimator is not None:
            return self.estimator.predict(Xt)
        else:
            return Xt


    def _predict_transform(self, stages, X, fitted_config=[]):
        for stage in stages:
            if isinstance(stage, list):
                # A branch is a list of stages
                X_transformed = self._predict_transform(stage, X, fitted_config)
                fitted_config.append(X_transformed)
            elif stage[0] == 'join':
                # A join operation
                # A join operation
                X= self.concatenate_matrices([branch_transformed for branch_transformed in fitted_config], axis=1)

                if self._is_transformer(stage[1]):
                    X =stage[1].transform(stage[1], X)
            else:
                if self._is_transformer(stage[1]):
                    X= stage[1].transform(X)
        return X

    def predict_proba(self, X):
        if isinstance(X, np.ndarray):
            X=X.tolist()
        if isinstance(X, list) or isinstance(X, pandas.DataFrame):
            Xt = X
        else:
            Xt=[X]

        for transform in self.transformers:
            if transform is not None:
                Xt = transform.transform(Xt)
        if self.estimator is not None:
            return self.estimator.predict_proba(Xt)
        else:
            return Xt

    def get_info(self):
        info = "Pipeline:\n["
        names, estimators = zip(*self.steps)
        learner = estimators[-1]
        transforms = estimators[:-1]
        i = 0
        for t in transforms:
            try:
                if t.get_info() is not None:
                    info += t.get_info()
                    info += "\n"
                else:
                    info += 'Transform: no info available'
            except NotImplementedError:
                info += 'Transform: no info available'
            i += 1

        if learner is not None:
            try:
                if hasattr(learner, 'get_info'):
                    info += learner.get_info()
                else:
                    info += 'Learner: no info available'
            except NotImplementedError:
                info += 'Learner: no info available'
        info += "]"
        return info

    def plot(self):
            import matplotlib.pyplot as plt

            base_plot_filename = f"pipeline.png"
            from schemdraw import Drawing
            from schemdraw.flow import Arrow, Data, RoundBox, Subroutine

            # Create schematic drawing
            d = Drawing(backend="matplotlib")
            d += Subroutine(w=10, h=5, s=1).label("Raw data").drop("E")
            for est in self.transformers:
               name = est.__class__.__name__
               d += Arrow().right()
               d += RoundBox(w=max(len(name), 7), h=5, cornerradius=1).label( name)

            # Add the model box
            name = self.estimator.__class__.__name__
            d += Arrow().right()
            d += Data(w=max(len(name), 7), h=5).label(name)

            fig, ax = plt.subplots(
                figsize=((2 + len(self.steps) * 5), 6)
               )

            d.draw(ax=ax, showframe=False, show=False)
            ax.set_aspect("equal")
            plt.axis("off")
            plt.tight_layout()

            return plt
