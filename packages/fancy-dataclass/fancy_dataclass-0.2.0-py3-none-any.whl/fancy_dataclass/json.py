from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from io import StringIO, TextIOBase
import json
from json import JSONEncoder
from typing import Any, BinaryIO, TextIO, Type, Union, get_args, get_origin

from typing_extensions import Self

from fancy_dataclass.dict import AnyDict, DictDataclass
from fancy_dataclass.utils import TypeConversionError


AnyIO = Union[BinaryIO, TextIO]


class JSONSerializable(ABC):
    """Mixin class enabling conversion of an object to/from JSON."""

    @abstractmethod
    def to_dict(self, **kwargs: Any) -> AnyDict:
        """Converts an object to a dict that can be readily converted into JSON.

        Returns:
            A JSON-convertible dict"""

    def _json_encoder(self) -> Type[JSONEncoder]:
        """Override this method to create a custom `JSONEncoder` to handle specific data types.
        A skeleton for this looks like:

        ```
        class Encoder(JSONEncoder):
            def default(self, obj):
                return json.JSONEncoder.default(self, obj)
        ```
        """
        return JSONEncoder

    @classmethod
    def _json_key_decoder(cls, key: Any) -> Any:
        """Override this method to decode a JSON key, for use with `from_dict`."""
        return key

    def _to_json(self, fp: TextIO, **kwargs: Any) -> None:
        indent = kwargs.get('indent')
        if (indent is not None) and (indent < 0):
            kwargs['indent'] = None
        kwargs['cls'] = self._json_encoder()
        d = self.to_dict()
        json.dump(d, fp, **kwargs)

    def to_json(self, fp: AnyIO, **kwargs: Any) -> None:
        """Writes the object as JSON to a file-like object (text or binary).
        If binary, applies UTF-8 encoding.

        Args:
            fp: A writable file-like object
            kwargs: Keyword arguments passed to `json.dump`"""
        if isinstance(fp, TextIOBase):  # text stream
            self._to_json(fp, **kwargs)
        else:  # binary
            fp.write(self.to_json_string(**kwargs).encode())  # type: ignore[call-overload]

    def to_json_string(self, **kwargs: Any) -> str:
        """Converts the object into a JSON string.

        Args:
            kwargs: Keyword arguments passed to `json.dump`

        Returns:
            Object rendered as a JSON string"""
        with StringIO() as stream:
            self._to_json(stream, **kwargs)
            return stream.getvalue()

    @classmethod
    @abstractmethod
    def from_dict(cls, d: AnyDict, **kwargs: Any) -> Self:
        """Constructs an object from a dictionary of fields.

        Args:
            d: Dict to convert into an object
            kwargs: Keyword arguments

        Returns:
            Converted object of this class"""

    @classmethod
    def from_json(cls, fp: AnyIO, **kwargs: Any) -> Self:
        """Constructs an object from a JSON file-like object (text or binary).

        Args:
            fp: A readable file-like object
            kwargs: Keyword arguments

        Returns:
            Converted object of this class"""
        # pop off known DictDataclass.from_dict kwargs
        default_dict_kwargs = {'strict': False}
        dict_kwargs = {key: kwargs.get(key, default_dict_kwargs[key]) for key in default_dict_kwargs}
        json_kwargs = {key: val for (key, val) in kwargs.items() if (key not in default_dict_kwargs)}
        return cls.from_dict(json.load(fp, **json_kwargs), **dict_kwargs)

    @classmethod
    def from_json_string(cls, s: str, **kwargs: Any) -> Self:
        """Constructs an object from a JSON string.

        Args:
            s: JSON string
            kwargs: Keyword arguments

        Returns:
            Converted object of this class"""
        default_dict_kwargs = {'strict': False}
        dict_kwargs = {key: kwargs.get(key, default_dict_kwargs[key]) for key in default_dict_kwargs}
        json_kwargs = {key: val for (key, val) in kwargs.items() if (key not in default_dict_kwargs)}
        return cls.from_dict(json.loads(s, **json_kwargs), **dict_kwargs)


class JSONDataclass(DictDataclass, JSONSerializable):  # type: ignore[misc]
    """Dataclass mixin enabling default serialization of dataclass objects to and from JSON."""

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # if the class already inherits from JSONDataclass, raise an error if qualified_type=False
        # this is because resolving the type from a dict may be ambiguous
        if not getattr(cls.__settings__, 'qualified_type', False):
            for base in cls.mro():
                if (base not in [cls, JSONDataclass]) and issubclass(base, JSONDataclass):
                    raise TypeError('when subclassing a JSONDataclass, you must set qualified_type=True or subclass JSONBaseDataclass instead')

    @classmethod
    def _to_dict_value_basic(cls, val: Any) -> Any:
        if isinstance(val, Enum):
            return val.value
        elif isinstance(val, range):  # store the range bounds
            bounds = [val.start, val.stop]
            if val.step != 1:
                bounds.append(val.step)
            return bounds
        elif isinstance(val, datetime):
            return val.isoformat()
        elif isinstance(val, (int, float)):  # handles numpy numeric types
            return val
        elif hasattr(val, 'dtype'):  # assume it's a numpy array of numbers
            return [float(elt) for elt in val]
        return val

    @classmethod
    def _to_dict_value(cls, val: Any, full: bool) -> Any:
        if isinstance(val, tuple) and hasattr(val, '_fields'):
            # if a namedtuple, render as a dict with named fields rather than a tuple
            return {k: cls._to_dict_value(v, full) for (k, v) in zip(val._fields, val)}
        return super()._to_dict_value(val, full)

    @classmethod
    def _from_dict_value_basic(cls, tp: type, val: Any) -> Any:
        if issubclass(tp, float):
            return tp(val)
        if issubclass(tp, range):
            return tp(*val)
        if issubclass(tp, datetime):
            return tp.fromisoformat(val)
        if issubclass(tp, Enum):
            try:
                return tp(val)
            except ValueError as e:
                raise TypeConversionError(tp, val) from e
        return super()._from_dict_value_basic(tp, val)

    @classmethod
    def _from_dict_value(cls, tp: type, val: Any, strict: bool = False) -> Any:
        # customize behavior for JSONSerializable
        origin_type = get_origin(tp)
        if (origin_type is None) and issubclass(tp, tuple) and isinstance(val, dict) and hasattr(tp, '_fields'):  # namedtuple
            try:
                vals = []
                for key in tp._fields:
                    # if NamedTuple's types are annotated, check them
                    valtype = tp.__annotations__.get(key)
                    vals.append(val[key] if (valtype is None) else cls._from_dict_value(valtype, val[key], strict=strict))
                return tp(*vals)
            except KeyError as e:
                raise TypeConversionError(tp, val) from e
        if origin_type == dict:  # decode keys to be valid JSON
            (keytype, valtype) = get_args(tp)
            return {cls._json_key_decoder(cls._from_dict_value(keytype, k)) : cls._from_dict_value(valtype, v, strict=strict) for (k, v) in val.items()}
        return super()._from_dict_value(tp, val)


class JSONBaseDataclass(JSONDataclass, qualified_type=True):
    """This class should be used in place of [`JSONDataclass`][fancy_dataclass.json.JSONDataclass] when you intend to inherit from the class.

    When converting a subclass to a dict with [`to_dict`][fancy_dataclass.json.JSONSerializable.to_dict], it will store the subclass's type in the `type` field. It will also resolve this type when calling [`from_dict`][fancy_dataclass.json.JSONSerializable.from_dict]."""
