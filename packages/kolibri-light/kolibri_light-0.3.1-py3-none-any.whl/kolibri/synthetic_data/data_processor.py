"""Single table data processing."""

import json
import logging
import warnings
from copy import deepcopy
from pathlib import Path

import pandas as pd
import rdt
from pandas.api.types import is_float_dtype, is_integer_dtype
from rdt.transformers import AnonymizedFaker, RegexGenerator

from kolibri.synthetic_data.base_contraint import Constraint
from kolibri.synthetic_data.base_contraint import get_subclasses
from kolibri.errors import (
    AggregateConstraintsError, FunctionError, MissingConstraintColumnError)
from kdmt.df import DatetimeFormatter
from kolibri.errors import InvalidConstraintsError, NotFittedError
from kdmt.df import NumericalFormatter
from kdmt.lib import load_module_from_path
from kolibri.errors import SynthesizerInputError
from kolibri.synthetic_data.anonymization import get_anonymized_transformer
from kolibri.synthetic_data.metadata import TableMetadata

LOGGER = logging.getLogger(__name__)


class DataProcessor:
    """Single table data processor.

    This class handles all pre and post processing that is done to a single table to get it ready
    for modeling and finalize sampling. These processes include formatting, transformations,
    anonymization and constraint handling.

    Args:
        metadata (metadata.TableMetadata):
            The single table metadata instance that will be used to apply constraints and
            transformations to the data.
        enforce_rounding (bool):
            Define rounding scheme for FloatFormatter. If True, the data returned by
            reverse_transform will be rounded to that place. Defaults to True.
        enforce_min_max_values (bool):
            Specify whether or not to clip the data returned by reverse_transform of the numerical
            transformer, FloatFormatter, to the min and max values seen during fit.
            Defaults to True.
        model_kwargs (dict):
            Dictionary specifying the kwargs that need to be used in each tabular
            model when working on this table. This dictionary contains as keys the name of the
            TabularModel class and as values a dictionary containing the keyword arguments to use.
            This argument exists mostly to ensure that the models are fitted using the same
            arguments when the same DataProcessor is used to fit different model instances on
            different slices of the same table.
        table_name (str):
            Name of table this processor is for. Optional.
        locales (str or list):
            Default locales to use for AnonymizedFaker transformers. Optional, defaults to using
            Faker's default locale.
    """

    _DEFAULT_TRANSFORMERS_BY_SDTYPE = {
        'numerical': rdt.transformers.FloatFormatter(
            learn_rounding_scheme=True,
            enforce_min_max_values=True,
            missing_value_replacement='mean',
            missing_value_generation='random',
        ),
        'int': rdt.transformers.FloatFormatter(
            learn_rounding_scheme=True,
            enforce_min_max_values=True,
            missing_value_replacement='mean',
            missing_value_generation='random',
        ),
        'float': rdt.transformers.FloatFormatter(
            learn_rounding_scheme=True,
            enforce_min_max_values=True,
            missing_value_replacement='mean',
            missing_value_generation='random',
        ),
        'category': rdt.transformers.FloatFormatter(
            learn_rounding_scheme=True,
            enforce_min_max_values=True,
            missing_value_replacement='mean',
            missing_value_generation='random',
        ),
        'categorical': rdt.transformers.LabelEncoder(add_noise=True),
        'boolean': rdt.transformers.LabelEncoder(add_noise=True),
        'datetime': rdt.transformers.UnixTimestampEncoder(
            missing_value_replacement='mean',
            missing_value_generation='random',
        ),
        'id': rdt.transformers.RegexGenerator()
    }
    _DTYPE_TO_SDTYPE = {
        'i': 'numerical',
        'f': 'numerical',
        'O': 'categorical',
        'b': 'boolean',
        'M': 'datetime',
    }

    def _update_numerical_transformer(self, enforce_rounding, enforce_min_max_values):
        custom_float_formatter = rdt.transformers.FloatFormatter(
            missing_value_replacement='mean',
            missing_value_generation='random',
            learn_rounding_scheme=enforce_rounding,
            enforce_min_max_values=enforce_min_max_values
        )
        self._transformers_by_sdtype.update({'numerical': custom_float_formatter})

    def __init__(self, metadata, enforce_rounding=True, enforce_min_max_values=True,
                 model_kwargs=None, table_name=None, locales=None):
        self.metadata = metadata
        self._enforce_rounding = enforce_rounding
        self._enforce_min_max_values = enforce_min_max_values
        self._model_kwargs = model_kwargs or {}
        self._locales = locales
        self._constraints_list = []
        self._constraints = []
        self._constraints_to_reverse = []
        self._custom_constraint_classes = {}
        self._transformers_by_sdtype = self._DEFAULT_TRANSFORMERS_BY_SDTYPE.copy()
        self._update_numerical_transformer(enforce_rounding, enforce_min_max_values)
        self._hyper_transformer = rdt.HyperTransformer()
        self.table_name = table_name
        self._dtypes = None
        self.fitted = False
        self.formatters = {}
        self._primary_key = self.metadata.primary_key
        self._prepared_for_fitting = False
        self._keys = deepcopy(self.metadata.alternate_keys)
        if self._primary_key:
            self._keys.append(self._primary_key)

    def get_model_kwargs(self, model_name):
        """Return the required model kwargs for the indicated model.

        Args:
            model_name (str):
                Qualified Name of the model for which model kwargs
                are needed.

        Returns:
            dict:
                Keyword arguments to use on the indicated model.
        """
        return deepcopy(self._model_kwargs.get(model_name))

    def set_model_kwargs(self, model_name, model_kwargs):
        """Set the model kwargs used for the indicated model.

        Args:
            model_name (str):
                Qualified Name of the model for which the kwargs will be set.
            model_kwargs (dict):
                The key word arguments for the model.
        """
        self._model_kwargs[model_name] = model_kwargs

    def get_sdtypes(self, primary_keys=False):
        """Get a ``dict`` with the ``sdtypes`` for each column of the table.

        Args:
            primary_keys (bool):
                Whether or not to include the primary key fields. Defaults to ``False``.

        Returns:
            dict:
                Dictionary that contains the column names and ``sdtypes``.
        """
        sdtypes = {}
        for name, column_metadata in self.metadata.columns.items():
            sdtype = column_metadata['sdtype']

            if primary_keys or (name not in self._keys):
                sdtypes[name] = sdtype

        return sdtypes

    def _validate_custom_constraint_name(self, class_name):
        reserved_class_names = list(get_subclasses(Constraint))
        if class_name in reserved_class_names:
            error_message = (
                f"The name '{class_name}' is a reserved constraint name. "
                'Please use a different one for the custom constraint.'
            )
            raise InvalidConstraintsError(error_message)

    def _validate_custom_constraints(self, filepath, class_names, module):
        errors = []
        for class_name in class_names:
            try:
                self._validate_custom_constraint_name(class_name)
            except InvalidConstraintsError as err:
                errors += err.errors

            if not hasattr(module, class_name):
                errors.append(f"The constraint '{class_name}' is not defined in '{filepath}'.")

        if errors:
            raise InvalidConstraintsError(errors)

    def load_custom_constraint_classes(self, filepath, class_names):
        """Load a custom constraint class for the current synthesizer_name.

        Args:
            filepath (str):
                String representing the absolute or relative path to the python file where
                the custom constraints are declared.
            class_names (list):
                A list of custom constraint classes to be imported.
        """
        path = Path(filepath)
        module = load_module_from_path(path)
        self._validate_custom_constraints(filepath, class_names, module)
        for class_name in class_names:
            constraint_class = getattr(module, class_name)
            self._custom_constraint_classes[class_name] = constraint_class

    def add_custom_constraint_class(self, class_object, class_name):
        """Add a custom constraint class for the synthesizer_name to use.

        Args:
            class_object (sdv.constraints.Constraint):
                A custom constraint class object.
            class_name (str):
                The name to assign this custom constraint class. This will be the name to use
                when writing a constraint dictionary for ``add_constraints``.
        """
        self._validate_custom_constraint_name(class_name)
        self._custom_constraint_classes[class_name] = class_object

    def _validate_constraint_dict(self, constraint_dict):
        """Validate a constraint against the single table metadata.

        Args:
            constraint_dict (dict):
                A dictionary containing:
                    * ``constraint_class``: Name of the constraint to apply.
                    * ``constraint_parameters``: A dictionary with the constraint parameters.
        """
        params = {'constraint_class', 'constraint_parameters'}
        keys = constraint_dict.keys()
        missing_params = params - keys
        if missing_params:
            raise SynthesizerInputError(
                f'A constraint is missing required parameters {missing_params}. '
                'Please add these parameters to your constraint definition.'
            )

        extra_params = keys - params
        if extra_params:
            raise SynthesizerInputError(
                f'Unrecognized constraint parameter {extra_params}. '
                'Please remove these parameters from your constraint definition.'
            )

        constraint_class = constraint_dict['constraint_class']
        constraint_parameters = constraint_dict['constraint_parameters']
        try:
            if constraint_class in self._custom_constraint_classes:
                constraint_class = self._custom_constraint_classes[constraint_class]

            else:
                constraint_class = Constraint._get_class_from_dict(constraint_class)

        except KeyError:
            raise InvalidConstraintsError(f"Invalid constraint class ('{constraint_class}').")

        constraint_class._validate_metadata(self.metadata, **constraint_parameters)

    def add_constraints(self, constraints):
        """Add constraints to the data processor.

        Args:
            constraints (list):
                List of constraints described as dictionaries in the following format:
                    * ``constraint_class``: Name of the constraint to apply.
                    * ``constraint_parameters``: A dictionary with the constraint parameters.
        """
        errors = []
        validated_constraints = []
        for constraint_dict in constraints:
            constraint_dict = deepcopy(constraint_dict)
            try:
                self._validate_constraint_dict(constraint_dict)
                validated_constraints.append(constraint_dict)
            except (AggregateConstraintsError, InvalidConstraintsError) as e:
                reformated_errors = '\n'.join(map(str, e.errors))
                errors.append(reformated_errors)

        if errors:
            raise InvalidConstraintsError(errors)

        self._constraints_list.extend(validated_constraints)
        self._prepared_for_fitting = False

    def get_constraints(self):
        """Get a list of the current constraints that will be used.

        Returns:
            list:
                List of dictionaries describing the constraints for this data processor.
        """
        return deepcopy(self._constraints_list)

    def _load_constraints(self):
        loaded_constraints = []
        default_constraints_classes = list(get_subclasses(Constraint))
        for constraint in self._constraints_list:
            if constraint['constraint_class'] in default_constraints_classes:
                loaded_constraints.append(Constraint.from_dict(constraint))

            else:
                constraint_class = self._custom_constraint_classes[constraint['constraint_class']]
                loaded_constraints.append(
                    constraint_class(**constraint.get('constraint_parameters', {}))
                )

        return loaded_constraints

    def _fit_constraints(self, data):
        self._constraints = self._load_constraints()
        errors = []
        for constraint in self._constraints:
            try:
                constraint.fit(data)
            except Exception as e:
                errors.append(e)

        if errors:
            raise AggregateConstraintsError(errors)

    def _transform_constraints(self, data, is_condition=False):
        errors = []
        if not is_condition:
            self._constraints_to_reverse = []

        for constraint in self._constraints:
            try:
                data = constraint.transform(data)
                if not is_condition:
                    self._constraints_to_reverse.append(constraint)

            except (MissingConstraintColumnError, FunctionError) as error:
                if isinstance(error, MissingConstraintColumnError):
                    LOGGER.info(
                        f'{constraint.__class__.__name__} cannot be transformed because columns: '
                        f'{error.missing_columns} were not found. Using the reject sampling '
                        'approach instead.'
                    )
                else:
                    LOGGER.info(
                        f'Error transforming {constraint.__class__.__name__}. '
                        'Using the reject sampling approach instead.'
                    )
                if is_condition:
                    indices_to_drop = data.columns.isin(constraint.constraint_columns)
                    columns_to_drop = data.columns.where(indices_to_drop).dropna()
                    data = data.drop(columns_to_drop, axis=1)

            except Exception as error:
                errors.append(error)

        if errors:
            raise AggregateConstraintsError(errors)

        return data

    def _update_transformers_by_sdtypes(self, sdtype, transformer):
        self._transformers_by_sdtype[sdtype] = transformer

    @staticmethod
    def create_anonymized_transformer(sdtype, column_metadata, enforce_uniqueness, locales=None):
        """Create an instance of an ``AnonymizedFaker``.

        Read the extra keyword arguments from the ``column_metadata`` and use them to create
        an instance of an ``AnonymizedFaker`` transformer.

        Args:
            sdtype (str):
                Sematic data type or a ``Faker`` function name.
            column_metadata (dict):
                A dictionary representing the rest of the metadata for the given ``sdtype``.
            enforce_uniqueness (bool):
                If ``True`` overwrite ``enforce_uniqueness`` with ``True`` to ensure unique
                generation for primary keys.
            locales (str or list):
                Locale or list of locales to use for the AnonymizedFaker transfomer. Optional,
                defaults to using Faker's default locale.

        Returns:
            Instance of ``rdt.transformers.pii.AnonymizedFaker``.
        """
        kwargs = {'locales': locales}
        for key, value in column_metadata.items():
            if key not in ['pii', 'sdtype']:
                kwargs[key] = value

        if enforce_uniqueness:
            kwargs['enforce_uniqueness'] = True

        return get_anonymized_transformer(sdtype, kwargs)

    def create_regex_generator(self, column_name, sdtype, column_metadata, is_numeric):
        """Create a ``RegexGenerator`` for the ``id`` columns.

        Read the keyword arguments from the ``column_metadata`` and use them to create
        an instance of a ``RegexGenerator``. If ``regex_format`` is not present in the
        metadata a default ``[0-1a-z]{5}`` will be used for object like data and an increasing
        integer from ``0`` will be used for numerical data. Also if the column name is a primary
        key or alternate key this will enforce the values to be unique.

        Args:
            column_name (str):
                Name of the column.
            sdtype (str):
                Sematic data type or a ``Faker`` function name.
            column_metadata (dict):
                A dictionary representing the rest of the metadata for the given ``sdtype``.
            is_numeric (boolean):
                A boolean representing whether or not data type is numeric or not.

        Returns:
            transformer:
                Instance of ``rdt.transformers.text.RegexGenerator`` or
                ``rdt.transformers.pii.AnonymizedFaker`` with ``enforce_uniqueness`` set to
                ``True``.
        """
        default_regex_format = r'\d{30}' if is_numeric else '[0-1a-z]{5}'
        regex_format = column_metadata.get('regex_format', default_regex_format)
        transformer = rdt.transformers.RegexGenerator(
            regex_format=regex_format,
            enforce_uniqueness=(column_name in self._keys)
        )

        return transformer

    def _get_transformer_instance(self, sdtype, column_metadata):
        kwargs = {
            key: value for key, value in column_metadata.items()
            if key not in ['pii', 'sdtype']
        }
        if kwargs and self._transformers_by_sdtype[sdtype] is not None:
            transformer_class = self._transformers_by_sdtype[sdtype].__class__
            return transformer_class(**kwargs)

        return deepcopy(self._transformers_by_sdtype[sdtype])

    def _update_constraint_transformers(self, data, columns_created_by_constraints, config):
        missing_columns = set(columns_created_by_constraints) - config['transformers'].keys()
        for column in missing_columns:
            dtype_kind = data[column].dtype.kind
            if dtype_kind in ('i', 'f'):
                config['sdtypes'][column] = 'numerical'
                config['transformers'][column] = rdt.transformers.FloatFormatter(
                    missing_value_replacement='mean',
                    missing_value_generation='random',
                    enforce_min_max_values=self._enforce_min_max_values
                )
            else:
                sdtype = self._DTYPE_TO_SDTYPE.get(dtype_kind, 'categorical')
                config['sdtypes'][column] = sdtype
                config['transformers'][column] = self._get_transformer_instance(sdtype, {})

        # Remove columns that have been dropped by the constraint
        for column in list(config['sdtypes'].keys()):
            if column not in data:
                LOGGER.info(
                    f"A constraint has dropped the column '{column}', removing the transformer "
                    "from the 'HyperTransformer'."
                )
                config['sdtypes'].pop(column)
                config['transformers'].pop(column)

        return config

    def _create_config(self, data, columns_created_by_constraints):
        sdtypes = {}
        transformers = {}

        for column in set(data.columns) - columns_created_by_constraints:
            column_metadata = self.metadata.columns.get(column)
            sdtype = column_metadata.get('sdtype')
            pii = column_metadata.get('pii', sdtype not in self._DEFAULT_TRANSFORMERS_BY_SDTYPE)
            sdtypes[column] = 'pii' if pii else sdtype

            if sdtype == 'id':
                is_numeric = pd.api.types.is_numeric_dtype(data[column].dtype)
                transformers[column] = self.create_regex_generator(
                    column,
                    sdtype,
                    column_metadata,
                    is_numeric
                )
                sdtypes[column] = 'text'

            elif pii:
                enforce_uniqueness = bool(column in self._keys)
                transformers[column] = self.create_anonymized_transformer(
                    sdtype,
                    column_metadata,
                    enforce_uniqueness,
                    self._locales
                )

            elif sdtype in self._transformers_by_sdtype:
                transformers[column] = self._get_transformer_instance(sdtype, column_metadata)

            else:
                sdtypes[column] = 'categorical'
                transformers[column] = self._get_transformer_instance(
                    'categorical',
                    column_metadata
                )

        config = {'transformers': transformers, 'sdtypes': sdtypes}
        config = self._update_constraint_transformers(data, columns_created_by_constraints, config)

        return config

    def update_transformers(self, column_name_to_transformer):
        """Update any of the transformers assigned to each of the column names.

        Args:
            column_name_to_transformer (dict):
                Dict mapping column names to transformers to be used for that column.
        """
        if self._hyper_transformer.field_transformers == {}:
            raise NotFittedError(
                'The DataProcessor must be prepared for fitting before the transformers can be '
                'updated.'
            )

        for column, transformer in column_name_to_transformer.items():
            if column in self._keys and not type(transformer) in (AnonymizedFaker, RegexGenerator):
                raise SynthesizerInputError(
                    f"Invalid transformer '{transformer.__class__.__name__}' for a primary "
                    f"or alternate key '{column}'. Please use 'AnonymizedFaker' or "
                    "'RegexGenerator' instead."
                )

        warnings.filterwarnings('ignore', module='rdt')
        self._hyper_transformer.update_transformers(column_name_to_transformer)
        warnings.resetwarnings()

    def _fit_hyper_transformer(self, data):
        """Create and return a new ``rdt.HyperTransformer`` instance.

        First get the ``dtypes`` and then use them to build a transformer dictionary
        to be used by the ``HyperTransformer``.

        Args:
            data (pandas.DataFrame):
                Data to transform.

        Returns:
            rdt.HyperTransformer
        """
        if not data.empty:
            self._hyper_transformer.fit(data)

    def _fit_formatters(self, data):
        """Fit ``NumericalFormatter`` and ``DatetimeFormatter`` for each column in the data."""
        for column_name in data:
            column_metadata = self.metadata.columns.get(column_name)
            sdtype = column_metadata.get('sdtype')
            if sdtype == 'numerical' and column_name != self._primary_key:
                representation = column_metadata.get('computer_representation', 'Float')
                self.formatters[column_name] = NumericalFormatter(
                    enforce_rounding=self._enforce_rounding,
                    enforce_min_max_values=self._enforce_min_max_values,
                    computer_representation=representation
                )
                self.formatters[column_name].learn_format(data[column_name])

            elif sdtype == 'datetime' and column_name != self._primary_key:
                datetime_format = column_metadata.get('datetime_format')
                self.formatters[column_name] = DatetimeFormatter(datetime_format=datetime_format)
                self.formatters[column_name].learn_format(data[column_name])

    def prepare_for_fitting(self, data):
        """Prepare the ``DataProcessor`` for fitting.

        This method will learn the ``dtypes`` of the data, fit the numerical formatters,
        fit the constraints and create the configuration for the ``rdt.HyperTransformer``.
        If the ``rdt.HyperTransformer`` has already been updated, this will not perform the
        actions again.

        Args:
            data (pandas.DataFrame):
                Table data to be learnt.
        """
        if not self._prepared_for_fitting:
            LOGGER.info(f'Fitting table {self.table_name} metadata')
            self._dtypes = data[list(data.columns)].dtypes

            self.formatters = {}
            LOGGER.info(f'Fitting formatters for table {self.table_name}')
            self._fit_formatters(data)

            LOGGER.info(f'Fitting constraints for table {self.table_name}')
            if len(self._constraints_list) != len(self._constraints):
                self._fit_constraints(data)

            constrained = self._transform_constraints(data)
            columns_created_by_constraints = set(constrained.columns) - set(data.columns)

            config = self._hyper_transformer.get_config()
            missing_columns = columns_created_by_constraints - config.get('sdtypes').keys()
            if not config.get('sdtypes'):
                LOGGER.info((
                    'Setting the configuration for the ``HyperTransformer`` '
                    f'for table {self.table_name}'
                ))
                config = self._create_config(constrained, columns_created_by_constraints)
                self._hyper_transformer.set_config(config)

            elif missing_columns:
                config = self._update_constraint_transformers(
                    constrained,
                    missing_columns,
                    config
                )
                self._hyper_transformer = rdt.HyperTransformer()
                self._hyper_transformer.set_config(config)

            self._prepared_for_fitting = True

    def fit(self, data):
        """Fit this metadata to the given data.

        Args:
            data (pandas.DataFrame):
                Table to be analyzed.
        """
        self._prepared_for_fitting = False
        self.prepare_for_fitting(data)
        constrained = self._transform_constraints(data)
        LOGGER.info(f'Fitting HyperTransformer for table {self.table_name}')
        self._fit_hyper_transformer(constrained)
        self.fitted = True

    def reset_sampling(self):
        """Reset the sampling state for the anonymized columns and primary keys."""
        self._hyper_transformer.reset_randomization()

    def generate_keys(self, num_rows, reset_keys=False):
        """Generate the columns that are identified as ``keys``.

        Args:
            num_rows (int):
                Number of rows to be created. Must be an integer greater than 0.
            reset_keys (bool):
                Whether or not to reset the keys generators. Defaults to ``False``.

        Returns:
            pandas.DataFrame:
                A dataframe with the newly generated primary keys of the size ``num_rows``.
        """
        generated_keys = self._hyper_transformer.create_anonymized_columns(
            num_rows=num_rows,
            column_names=self._keys,
        )
        return generated_keys

    def transform(self, data, is_condition=False):
        """Transform the given data.

        Args:
            data (pandas.DataFrame):
                Table data.

        Returns:
            pandas.DataFrame:
                Transformed data.
        """
        data = data.copy()
        if not self.fitted:
            raise NotFittedError()

        # Filter columns that can be transformed
        columns = [
            column for column in self.get_sdtypes(primary_keys=not is_condition)
            if column in data.columns
        ]
        LOGGER.debug(f'Transforming constraints for table {self.table_name}')
        data = self._transform_constraints(data[columns], is_condition)

        LOGGER.debug(f'Transforming table {self.table_name}')
        if self._keys and not is_condition:
            data = data.set_index(self._primary_key, drop=False)

        try:
            transformed = self._hyper_transformer.transform_subset(data)
        except (rdt.errors.NotFittedError, rdt.errors.ConfigNotSetError):
            transformed = data

        return transformed

    def reverse_transform(self, data, reset_keys=False):
        """Reverse the transformed data to the original format.

        Args:
            data (pandas.DataFrame):
                Data to be reverse transformed.
            reset_keys (bool):
                Whether or not to reset the keys generators. Defaults to ``False``.

        Returns:
            pandas.DataFrame
        """
        if not self.fitted:
            raise NotFittedError()

        reversible_columns = [
            column
            for column in self._hyper_transformer._output_columns
            if column in data.columns
        ]

        reversed_data = data
        try:
            if not data.empty:
                reversed_data = self._hyper_transformer.reverse_transform_subset(
                    data[reversible_columns]
                )
        except rdt.errors.NotFittedError:
            LOGGER.info(f'HyperTransformer has not been fitted for table {self.table_name}')

        for constraint in reversed(self._constraints_to_reverse):
            reversed_data = constraint.reverse_transform(reversed_data)

        num_rows = len(reversed_data)
        sampled_columns = list(reversed_data.columns)
        missing_columns = [
            column
            for column in self.metadata.columns.keys() - set(sampled_columns + self._keys)
            if self._hyper_transformer.field_transformers.get(column)
        ]
        if missing_columns and num_rows:
            anonymized_data = self._hyper_transformer.create_anonymized_columns(
                num_rows=num_rows,
                column_names=missing_columns
            )
            sampled_columns.extend(missing_columns)

        if self._keys and num_rows:
            generated_keys = self.generate_keys(num_rows, reset_keys)
            sampled_columns.extend(self._keys)

        # Sort the sampled columns in the order of the metadata
        # In multitable there may be missing columns in the sample such as foreign keys
        # And alternate keys. Thats the reason of ensuring that the metadata column is within
        # The sampled columns.
        sampled_columns = [
            column for column in self.metadata.columns.keys()
            if column in sampled_columns
        ]
        for column_name in sampled_columns:
            if column_name in missing_columns:
                column_data = anonymized_data[column_name]
            elif column_name in self._keys:
                column_data = generated_keys[column_name]
            else:
                column_data = reversed_data[column_name]

            dtype = self._dtypes[column_name]
            if is_integer_dtype(dtype) and is_float_dtype(column_data.dtype):
                column_data = column_data.round()

            reversed_data[column_name] = column_data[column_data.notna()]
            try:
                reversed_data[column_name] = reversed_data[column_name].astype(dtype)
            except ValueError as e:
                column_metadata = self.metadata.columns.get(column_name)
                sdtype = column_metadata.get('sdtype')
                if sdtype not in self._DTYPE_TO_SDTYPE.values():
                    LOGGER.info(
                        f"The real data in '{column_name}' was stored as '{dtype}' but the "
                        'synthetic data could not be cast back to this type. If this is a '
                        'problem, please check your input data and metadata settings.'
                    )
                    if column_name in self.formatters:
                        self.formatters.pop(column_name)

                else:
                    raise ValueError(e)

        # reformat columns using the formatters
        for column in sampled_columns:
            if column in self.formatters:
                data_to_format = reversed_data[column]
                reversed_data[column] = self.formatters[column].format_data(data_to_format)

        return reversed_data[sampled_columns]

    def filter_valid(self, data):
        """Filter the data using the constraints and return only the valid rows.

        Args:
            data (pandas.DataFrame):
                Table data.

        Returns:
            pandas.DataFrame:
                Table containing only the valid rows.
        """
        for constraint in self._constraints:
            data = constraint.filter_valid(data)

        return data

    def to_dict(self):
        """Get a dict representation of this DataProcessor.

        Returns:
            dict:
                Dict representation of this DataProcessor.
        """
        constraints_to_reverse = [cnt.to_dict() for cnt in self._constraints_to_reverse]
        return {
            'metadata': deepcopy(self.metadata.to_dict()),
            'constraints_list': deepcopy(self._constraints_list),
            'constraints_to_reverse': constraints_to_reverse,
            'model_kwargs': deepcopy(self._model_kwargs)
        }

    @classmethod
    def from_dict(cls, metadata_dict, enforce_rounding=True, enforce_min_max_values=True):
        """Load a DataProcessor from a metadata dict.

        Args:
            metadata_dict (dict):
                Dict metadata to load.
            enforce_rounding (bool):
                If passed, set the ``enforce_rounding`` on the new instance.
            enforce_min_max_values (bool):
                If passed, set the ``enforce_min_max_values`` on the new instance.
        """
        instance = cls(
            metadata=TableMetadata.load_from_dict(metadata_dict['metadata']),
            enforce_rounding=enforce_rounding,
            enforce_min_max_values=enforce_min_max_values,
            model_kwargs=metadata_dict.get('model_kwargs')
        )

        instance._constraints_to_reverse = [
            Constraint.from_dict(cnt) for cnt in metadata_dict.get('constraints_to_reverse', [])
        ]
        instance._constraints_list = metadata_dict.get('constraints_list', [])

        return instance

    def to_json(self, filepath):
        """Dump this DataProcessor into a JSON file.

        Args:
            filepath (str):
                Path of the JSON file where this metadata will be stored.
        """
        with open(filepath, 'w') as out_file:
            json.dump(self.to_dict(), out_file, indent=4)

    @classmethod
    def from_json(cls, filepath):
        """Load a DataProcessor from a JSON.

        Args:
            filepath (str):
                Path of the JSON file to load
        """
        with open(filepath, 'r') as in_file:
            return cls.from_dict(json.load(in_file))
