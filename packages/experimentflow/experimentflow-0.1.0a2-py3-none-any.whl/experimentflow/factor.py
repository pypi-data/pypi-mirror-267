from enum import Enum, auto
from typing import List, Tuple


class FactorType(Enum):
    """
    Represents the type of a factor in an experiment.
    Factors can be of different types, e.g. categorical, numeric, ordinal, boolean, text.

    - CATEGORICAL: represents a categorical factor, e.g. color (red, green, blue)
    - NUMERIC: represents a numeric factor, e.g. age (30, 25), weight (70.5, 80.0)
    - ORDINAL: represents an ordinal factor, e.g. education level (high school, college, master, phd)
    - BOOLEAN: represents a boolean factor, e.g. smoker (yes, no), married (yes, no)
    - TEXT: represents a text factor, e.g. comments, notes
    """

    CATEGORICAL = auto()
    NUMERIC = auto()
    ORDINAL = auto()
    BOOLEAN = auto()
    TEXT = auto()


class Factor:
    """
    Represents a factor in an experiment.
    A factor is a variable that can take on different values.
    Factors can be of different types, e.g. categorical, numeric, ordinal, boolean, text.

    Attributes:
    - name: the name of the factor
    - description: the description of the factor
    - type: the type of the factor (FactorType)
    - values: the possible values of the factor (list or tuple)

    """

    def __init__(
        self, name: str, description: str, type: FactorType, values: List | Tuple
    ):
        self.__check_name(name)
        self.__check_description(description)
        self.__check_type(type)
        self.__check_values(values, type)
        self.name = name.strip()
        self.description = description.strip()
        self.type = type
        self.values = values

    def __check_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Factor name should be a string")

        if name == "":
            raise ValueError("Factor name should not be empty")

    def __check_description(self, description: str):
        if not isinstance(description, str):
            raise ValueError("Factor description should be a string")

        if description == "":
            raise ValueError("Factor description should not be empty")

    def __check_type(self, type: FactorType):
        if not isinstance(type, FactorType):
            raise ValueError("Factor type should be a FactorType")

    def __check_values(self, values: List | Tuple, type: FactorType):
        if not isinstance(values, (list, tuple)):
            raise ValueError("Factor values should be a list or tuple")

        if not values:
            raise ValueError("Factor values should not be empty")

        if len(values) != len(set(values)):
            raise ValueError("Factor values should not contain duplicate values")

        value_check_methods = {
            FactorType.CATEGORICAL: self.__check_categorical_values,
            FactorType.NUMERIC: self.__check_numeric_values,
            FactorType.ORDINAL: self.__check_ordinal_values,
            FactorType.BOOLEAN: self.__check_boolean_values,
            FactorType.TEXT: self.__check_text_values,
        }

        if type in value_check_methods:
            value_check_methods[type](values)

    def __check_categorical_values(self, values: List | Tuple):
        if not all(isinstance(value, str) for value in values):
            raise ValueError("Factor values should be strings")

    def __check_numeric_values(self, values: List | Tuple):
        if not all(isinstance(value, (int, float)) for value in values):
            raise ValueError("Factor values should be numbers")

    def __check_ordinal_values(self, values: List | Tuple):
        if not all(isinstance(value, str) for value in values):
            raise ValueError("Factor values should be strings")

    def __check_boolean_values(self, values: List | Tuple):
        if not all(isinstance(value, bool) for value in values):
            raise ValueError("Factor values should be booleans")

        if len(values) != 2:
            raise ValueError(
                "Boolean factor should have exactly two values (True, False)"
            )

    def __check_text_values(self, values: List | Tuple):
        if not all(isinstance(value, str) for value in values):
            raise ValueError("Factor values should be strings")
