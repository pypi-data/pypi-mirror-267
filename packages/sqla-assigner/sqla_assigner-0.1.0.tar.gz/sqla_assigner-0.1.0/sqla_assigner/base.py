import dataclasses
import enum
from collections.abc import Mapping, Sequence
from types import UnionType
from typing import (
    Any,
    ClassVar,
    Generic,
    TypeVar,
    dataclass_transform,
    get_args,
    get_origin,
    get_type_hints,
)

from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute

TModel = TypeVar("TModel", bound=DeclarativeBase)


class Unset(enum.Enum):
    v = enum.auto()


UNSET = Unset.v


@dataclass_transform(kw_only_default=True)
class BaseAssigner(Generic[TModel]):
    model: type[TModel]

    __sqla_assigner_fields__: ClassVar[Mapping[str, InstrumentedAttribute[Any]]]

    def __class_getitem__(cls, item: type[TModel]) -> "BaseAssigner[TModel]":
        return type(f"BaseAssigner[{item.__name__}]", (cls,), {"model": item})  # type: ignore[return-value]

    def __init_subclass__(cls) -> None:
        wrapped_cls = dataclasses.dataclass(cls)
        class_type_hints = get_type_hints(wrapped_cls, include_extras=True)
        del class_type_hints["__sqla_assigner_fields__"]

        attributes = {}

        for field_name, raw_type in class_type_hints.items():
            args = get_args(raw_type)
            attribute = _get_instrumented_attribute(args)

            if attribute is None:
                continue

            if not issubclass(
                attribute.class_,  # type:ignore[arg-type]
                cls.model,  # pyright: ignore[reportGeneralTypeIssues]
            ):
                msg = f"Attribute `{attribute}` not belongs to class `{cls.model.__qualname__}`"  # pyright: ignore[reportGeneralTypeIssues]
                raise TypeError(msg)

            attributes[field_name] = attribute

        wrapped_cls.__sqla_assigner_fields__ = attributes

    def assign(self, model: TModel) -> TModel:
        for field_name, attribute in self.__sqla_assigner_fields__.items():
            value = getattr(self, field_name)

            if value is UNSET:
                continue

            setattr(model, attribute.key, value)

        return model


def _get_instrumented_attribute(
    annotations: tuple[Any, ...],
) -> InstrumentedAttribute[Any] | None:
    for annotation in annotations:
        if isinstance(annotation, InstrumentedAttribute):
            prev = annotations[0]
            args = [type_ for type_ in prev.__args__ if not issubclass(type_, Unset)]

            attr_type_hints = get_type_hints(annotation.class_)
            attr = attr_type_hints[annotation.key]
            attr_args = get_args(attr)
            expected_type = attr_args[0]
            origin = get_origin(expected_type)

            if origin and issubclass(origin, UnionType):
                expected_types = list(get_args(expected_type))
            else:
                expected_types = [expected_type]

            if args != expected_types:
                msg = f"Got not correct type annotations. For field `{attr}` expected: `{_repr_types(expected_types)}`, got: `{_repr_types(args)}`"
                raise TypeError(msg)

            return annotation  # pyright: ignore[reportUnknownVariableType]

    return None


def _repr_types(types: Sequence[type[Any]]) -> str:
    return " | ".join(str(type_) for type_ in types)
