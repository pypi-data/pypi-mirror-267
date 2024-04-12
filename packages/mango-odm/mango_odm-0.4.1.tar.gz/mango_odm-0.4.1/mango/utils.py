import re
from collections.abc import Callable, Generator, Iterable, Sequence
from types import UnionType
from typing import TYPE_CHECKING, Any

import pydantic

from mango.fields import FieldInfo
from mango.index import Index, IndexType

if TYPE_CHECKING:  # pragma: no cover
    from pydantic import BaseModel

    from mango.models import Document


def to_snake_case(string: str) -> str:
    """将字符串转换为蛇形命名法"""
    tmp = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", tmp).lower()


def all_check(
    iter_obj: Iterable[object],
    type_or_func: type
    | UnionType
    | Callable
    | tuple[type | UnionType | tuple[Any, ...], ...],
) -> bool:
    """
    如果可迭代对象中的所有元素为指定类型，则返回True。
    如果可迭代对象为空，则返回True。
    """
    if isinstance(type_or_func, Callable):
        return all(type_or_func(obj) for obj in iter_obj)
    return all(isinstance(obj, type_or_func) for obj in iter_obj)


def any_check(
    iter_obj: Iterable[object],
    type_or_func: type
    | UnionType
    | Callable
    | tuple[type | UnionType | tuple[Any, ...], ...],
) -> bool:
    """
    如果可迭代对象中的任意元素为指定类型，则返回True。
    如果可迭代对象为空，则返回False。
    """
    if isinstance(type_or_func, Callable):
        return any(type_or_func(obj) for obj in iter_obj)
    return any(isinstance(obj, type_or_func) for obj in iter_obj)


def is_sequence(
    iter_obj: Sequence[object],
) -> bool:
    """判断是否为非字符串的序列对象"""
    return isinstance(iter_obj, Sequence) and not isinstance(iter_obj, bytes | str)


def validate_fields(
    model: type["Document"], input_data: dict[str, Any]
) -> dict[str, Any]:
    """验证模型的指定字段"""
    if miss := set(input_data) - set(model.model_fields):
        raise ValueError(f"这些字段在 {model.__name__} 中不存在: {miss}")

    fields = {
        k: (v.annotation, v.get_default())
        for k, v in model.model_fields.items()
        if k in input_data
    }
    new_model: "BaseModel" = pydantic.create_model(model.__name__, **fields)  # type: ignore
    new_model.model_validate(input_data)

    return input_data


def add_fields(model: type["Document"], **field_definitions: Any) -> None:
    """动态添加字段

    来源见: https://github.com/pydantic/pydantic/issues/1937
    """
    new_fields: dict[str, FieldInfo] = {}
    new_annotations: dict[str, type | None] = {}

    for f_name, f_def in field_definitions.items():
        if isinstance(f_def, tuple):
            try:
                f_annotation, f_value = f_def
            except ValueError as e:
                raise ValueError(
                    "field definitions should either be a tuple of (<type>, <default>) "
                    "or just a default value, unfortunately this means tuples as "
                    "default values are not allowed"
                ) from e
        else:
            f_annotation, f_value = None, f_def

        if not isinstance(f_value, dict):
            f_value = {"default": f_value}

        if f_annotation:
            new_annotations[f_name] = f_annotation

        new_fields[f_name] = FieldInfo(annotation=f_annotation, **f_value)

    model.model_fields.update(new_fields)
    model.__annotations__.update(new_annotations)
    model.model_rebuild(force=True)


def get_indexes(model: type["Document"]) -> Generator[Index, None, None]:
    """获取模型中定义的索引, 包括字段与元配置"""
    for name, field in model.model_fields.items():
        if isinstance(field, FieldInfo):
            if index := field.index:
                if index is True:
                    yield Index(name)
                elif isinstance(index, IndexType):
                    yield Index((name, index))
                else:
                    yield index
            elif (expire := field.expire) is not None:
                yield Index(name, expireAfterSeconds=expire)

    for index in model.meta_config.get("indexes", []):
        if isinstance(index, str):
            yield Index(index)
        elif isinstance(index, Sequence):
            yield Index(*index)
        else:
            yield index
