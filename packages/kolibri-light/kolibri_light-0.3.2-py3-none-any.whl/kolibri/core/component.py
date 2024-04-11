"""@package docstring
Documentation for this module.

More details.
"""

from copy import deepcopy
import time, os
import regex as re


try:
    from kolibri.optimizers.optuna.tuner import OptunaTuner
except:
    pass
from abc import ABC
from kolibri.errors import *
from kdmt.dict import update
import joblib
from kolibri.utils.config import get_parameter
from kdmt.dict import nested_dict_set_key_value, nested_dict_get_key_path
from kdmt.path import expand_path
from kolibri.config import ModelConfig

logger = get_logger(__name__)
from pathlib import Path

# def register(new_class):
#     from kolibri.registry import ModulesRegistry
#     ModulesRegistry.add_module(new_class.name, new_class)

# class ComponentMetaclass(type):
#     """Metaclass with `name` class property"""
#
#     @property
#     def name(cls):
#         """The name property is a function of the class - its __name__."""
#
#         return cls.__name__
#
#     def __new__(cls, clsname, bases, attrs):
#         newclass = super(ComponentMetaclass, cls).__new__(cls, clsname, bases, attrs)
#         register(newclass)  # here is your register function
#         return newclass

class Component(ABC):
    """A component is a document processing unit in a pipeline.
    Components are the base class for most of kolibri classes. it define some of the basic functionalities and properties.
    In Kolibri all components are responsible for updating thier parameters.
    Component define basic functionalities for loading and saving and creating components.
    It also create the necessary interfaces that need to be implemented by children: fit and transform
    Components are collected sequentially in a pipeline. Each component
    is called one after another. This holds for
    initialization, training, persisting and loading the components.
    If a component comes first in a pipeline, its
    methods will be called first.
"""

    @property
    def name(self):
        """Access the class's property name from an instance."""

        return self.__class__.__name__

    component_type = ""
    # Name of the component to be used when integrating it in a
    # pipeline. E.g. ``[ComponentA, ComponentB]``
    # will be a proper pipeline definition where ``ComponentA``
    # is the name of the first component of the pipeline.
    component_name = ""

    # Defines what attributes the pipeline component will
    # provide when called. The listed attributes
    # should be set by the component on the document object
    # during test and train, e.g.
    # ```document.set("entities", [...])```
    provides = []

    # Which attributes on a document are required by this
    # component. e.g. if requires contains "tokens", than a
    # previous component in the pipeline needs to have "tokens"
    # within the above described `provides` property.
    requires = []

    # Defines the default configuration parameters of a component
    # these values can be overwritten in the pipeline configuration
    # of the model_type. The component should choose sensible defaults
    # and should be able to create reasonable results with the defaults.

    inputs = [
        {
            "name": "",
            "type": ""
        }
    ]

    outputs = [
        {
            "name": "",
            "type": ""
        }
    ]

    language_list = None

    modalities = ["text"]

    defaults = {
        "fixed": {
            "language": 'en',
            "opt-metric-name": "f1-score",
            "optimize-estimator": False,
            'max-time-for-optimization': 3600,
            "random-state": 41,
            "output-folder": None,
            "n_jobs": 1,
            "save-base-model": False,
            "target": None,
            "load-path":None,
            "save-patg": None,
            "verbose": False,
            "required-libs":{}
        },

        "tunable": {
            # "example": {
            #     "description": "This is just an example of a tuneable variable",
            #     "value": 1,
            #     "type": "int",
            #     "values": [1, 3, 7, 10],
            #     "range": [1, 10]
            # }
        }
    }

    def __init__(self, parameters=None):

        self.update_default_hyper_parameters()
        self.hyperparameters = {}
        self.hyperparameters = deepcopy(self.defaults)
        self.override_default_parameters(parameters)

        self.model = self
        # add component name to the config
        self.hyperparameters["fixed"]["name"] = self.name

        self.language = self.get_parameter("language")
        self.target = self.get_parameter("target")
        self._tunable = self._get_tunable(self.hyperparameters)

        if self.get_parameter("save-path"):
            self.save_path = expand_path(self.get_parameter("save-path"))
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            self.save_path = None


        # if self.get_parameter("load-path") is not None:
        #     self.load_path = expand_path(self.get_parameter("load-path"))
        #     if mode != 'train' and self.save_path and self.load_path != self.save_path:
        #         log.warning("Load path '{}' differs from save path '{}' in '{}' mode for {}."
        #                     .format(self.load_path, self.save_path, mode, self.__class__.__name__))
        # elif mode != 'train' and self.save_path:
        #     self.load_path = self.save_path
        #     log.warning("No load path is set for {} in '{}' mode. Using save path instead"
        #                 .format(self.__class__.__name__, mode))
        # else:
        #     self.load_path = None
        #     log.warning("No load path is set for {}!".format(self.__class__.__name__))

        super(Component, self).__init__()

    @classmethod
    def required_packages(cls):
        """Specify which python packages need to be installed to use this
        component.`.

        This list of requirements allows us to fail early during training
        if a required package is not installed."""
        return []

    def get_hyperparameters(self):
        """Get configs values that the current Component is using.

        Returns:
            dict:
                the dictionary containing the hyperparameter values that the
                Component is currently using.
        """
        return deepcopy(self.hyperparameters)

    def get_parameter(self, parmeter_name, default=None):
        return get_parameter(self.hyperparameters, parmeter_name, default)

    def override_default_parameters(self, custom_param):

        if isinstance(custom_param, ModelConfig):
            custom = custom_param.as_dict()
        else:
            custom = custom_param

        if custom:
            if isinstance(custom, dict):
                for key in self.hyperparameters["fixed"]:
                    v = custom['fixed'].get(key, None) if 'fixed' in custom else custom.get(key, None)
                    if v:
                        self.hyperparameters["fixed"][key] = v

                for key in self.hyperparameters["tunable"]:
                    if 'tunable' in custom and key not in custom['tunable']:
                        continue
                    v = custom['tunable'].get(key, None)['value'] if 'tunable' in custom else custom.get(key, None)
                    if v:
                        self.hyperparameters["tunable"][key]["value"] = v

            if "fixed" in custom or "tunable" in custom:
                for key in custom['fixed']:
                    p = nested_dict_get_key_path(key, self.hyperparameters)
                    if p is not None:
                        nested_dict_set_key_value(p, self.hyperparameters, custom['fixed'][key])
                for key in custom["tunable"]:
                    p = nested_dict_get_key_path(key, self.hyperparameters)
                    if p is not None:
                        nested_dict_set_key_value(p, self.hyperparameters, custom["tunable"][key])
            else:
                for key in custom:
                    p = nested_dict_get_key_path(key, self.hyperparameters)
                    if p is not None:
                        if 'tunable' in p:
                            p.append('value')
                        nested_dict_set_key_value(p, self.hyperparameters, custom[key])

    def update_default_hyper_parameters(self):
        self.defaults = update(self.defaults, Component.defaults)

    @classmethod
    def create(cls, cfg):
        """Creates this component (e.g. before a training is started).

        Method can access all configuration parameters."""

        # Check language supporting
        if "fixed" in cfg:
            language = cfg["fixed"]["language"]
        else:
            language = cfg["language"]
        if not cls.can_handle_language(language):
            # check failed
            raise UnsupportedLanguageError(cls.name, language)

        return cls(cfg)

    def fit(self, X, y):
        """Train this component.

        This is the components chance to train itself provided
        with the training texts. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        return self

    def objective(self, X, y):
        raise NotImplementedError

    def optimize(self, X, y):
        try:
            optimizer = OptunaTuner(
                self.get_parameter('output-folder'),
                eval_metric=self.get_parameter('opt-metric-name'),
                time_budget=self.get_parameter('max-time-for-optimization'),
                init_params={},
                verbose=True,
                n_jobs=-1,
                random_state=self.get_parameter('random-state'),
            )

            start_time = time.time()
            self.hyperparameters = optimizer.optimize(
                objective=self.objective(X, y),
                learner_params=self.hyperparameters
            )
            self.optimization_time = time.time() - start_time


        except Exception as e:
            raise Exception('Could not optimize model_type. Exception raised: ' + str(e))

    def transform(self, X):
        """Process an incoming document.

        This is the components chance to process an incoming
        document. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.process`
        of components previous to this one."""
        pass

    def persist(self, model_dir):
        """Persist this model_type into the passed directory.
        Returns the metadata necessary to load the model_type again."""

        model_file = os.path.join(model_dir, self.name + ".pkl")
        joblib.dump(self, model_file)

        return {"model_file": self.name + ".pkl", 'folder': None}

    @classmethod
    def get_subclasses(cls, include_parents=False):
        """Recursively find subclasses of this Baseline.

        Args:
            include_parents (bool):
                Whether to include subclasses which are parents to
                other classes. Defaults to ``False``.
        """
        subclasses = {}
        for child in cls.__subclasses__():
            grandchildren = child.get_subclasses(include_parents)
            subclasses.update(grandchildren)
            if include_parents or not grandchildren:
                subclasses[child.__name__] = child

        return subclasses

    @classmethod
    def load_from_azure(cls, container_name=None):
        from kdmt.cloud.azure import get_file_object
        connect_str=os.environ.get("STORAGE_CONTAINER_STRING")

        blob_model_file=cls.__name__+'.model.pkl'

        model_file=get_file_object(connect_str, container_name, blob_model_file)

        model = joblib.load(model_file)

        return model

    def _default_ouptut_file_name(self):
        file_name=self.__class__.__name__+'.model.pkl'

        return re.sub('[^A-Za-z0-9-\.]+', '', file_name)

    def __repr__(self):

        return self.__class__.__name__

    def save_to_azure(self, container_name):
        """
        Save model
        Args:
            model_path:
        """

        connect_str=os.environ.get("STORAGE_CONTAINER_STRING")
        from kdmt.cloud.azure import  upload_file
        import tempfile
        td=tempfile.TemporaryDirectory()
        model_dir=td.name
        local_model_file = tempfile.NamedTemporaryFile(dir=model_dir, delete=True).name
        joblib.dump(self, local_model_file)
        blob_model_file=self._default_ouptut_file_name()
        upload_file(connect_str, container_name, local_model_file, blob_model_file, overwrite=True)

        return container_name


    @classmethod
    def load(cls,
             model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        if model_metadata is not None:
            if model_metadata.get("folder") is not None:
                model_dir = model_metadata.get("folder")
            if model_dir and model_metadata.get("model_file"):
                file_name = model_metadata.get("model_file")
                model_file = os.path.join(model_dir, file_name)
                return joblib.load(model_file)
            else:
                logger.warning("Failed to load component. Maybe path {} "
                               "doesn't exist".format(os.path.abspath(model_dir)))
                return cls(model_metadata)
        else:
            model_file = os.path.join(model_dir, cls.name + ".pkl")
            return joblib.load(model_file)

    @classmethod
    def cache_key(cls, model_metadata):
        """This key is used to cache components.

        If a component is unique to a model_type it should return None.
        Otherwise, an instantiation of the
        component will be reused for all models where the
        metadata creates the same key."""

        return None

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__repr__()==other
        return self.__dict__ == other.__dict__

    @classmethod
    def _get_tunable(cls, hyperparameters):
        tunable = dict()
        for name, param in hyperparameters.get('tunable', dict()).items():
            tunable[name] = param
        return tunable

    def get_tunable_hyperparameters(self):
        """Get the configs that can be tuned for this Component.
        """
        return deepcopy(self._tunable)

    def get_info(self):
        return self.name

    @classmethod
    def can_handle_language(cls, language):
        """Check if component supports a specific language.

        This method can be overwritten when needed. (e.g. dynamically
        determine which language is supported.)"""

        # if language_list is set to `None` it means: support all languages
        if language is None or cls.language_list is None:
            return True

        return language in cls.language_list


class ComponentBuilder(object):
    """Creates trainers and interpreters based on configurations.

    Caches components for reuse."""

    def __init__(self, use_cache=True):
        self.use_cache = use_cache
        # Reuse nlp and featurizers where possible to save memory,
        # every component that implements a cache-key will be cached
        self.component_cache = {}

    def __get_cached_component(self, component_name, model_metadata):
        """Load a component from the cache, if it exists.

        Returns the component, if found, and the cache key."""
        from kolibri.core import modules

        component_class = modules.get_component_class_from_name(component_name)
        cache_key = component_class.cache_key(model_metadata)
        if (cache_key is not None
                and self.use_cache
                and cache_key in self.component_cache):
            return self.component_cache[cache_key], cache_key
        else:
            return None, cache_key

    def __add_to_cache(self, component, cache_key):
        """Add a component to the cache."""

        if cache_key is not None and self.use_cache:
            self.component_cache[cache_key] = component
            logger.info("Added '{}' to component cache. Key '{}'."
                        "".format(component.my_name, cache_key))

    def load_component(self,
                       component_name,
                       model_dir,
                       **context):
        """Tries to retrieve a component from the cache, else calls
        ``load`` to create a new component.

        Args:
            component_name (str): the name of the component to load
            model_dir (str): the directory to read the model from
            model_metadata (Metadata): the model's
            :class:`models.Metadata`

        Returns:
            Component: the loaded component.
        """
        from kolibri.core import modules

        try:
            cached_component, cache_key = self.__get_cached_component(
                component_name['label'], component_name)
            component = modules.load_component_by_name(
                component_name['label'], model_dir, component_name,
                cached_component, **context)
            if not cached_component:
                # If the component wasn't in the cache,
                # let us add it if possible
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to load component '{}'. "
                            "{}".format(component_name, e))

    def create_component(self, component_name, cfg):
        """Tries to retrieve a component from the cache,
        calls `create` to create a new component."""
        from kolibri.core import modules
        from kolibri.metadata import Metadata

        try:
            component, cache_key = self.__get_cached_component(
                component_name, Metadata(cfg.as_dict(), None))
            if component is None:
                component = modules.create_component_by_name(component_name,
                                                             cfg)
                self.__add_to_cache(component, cache_key)
            return component
        except MissingArgumentError as e:  # pragma: no cover
            raise Exception("Failed to create component '{}'. "
                            "{}".format(component_name, e))
