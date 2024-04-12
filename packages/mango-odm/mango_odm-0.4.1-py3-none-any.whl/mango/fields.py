from collections.abc import Callable
from typing import Any, AnyStr, Literal

from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.aliases import AliasChoices, AliasPath
from pydantic.config import JsonDict
from pydantic.fields import FieldInfo as PDFieldInfo
from pydantic.fields import _FromFieldInfoInputs
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import Discriminator
from pydantic_core import CoreSchema, PydanticUndefined, core_schema
from typing_extensions import Self, Unpack

from mango.index import Index, IndexType


class ObjectIdField(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> CoreSchema:
        from_any_str_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.bytes_schema(),
                    ]
                ),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_any_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    from_any_str_schema,
                ],
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str, when_used="json"
            ),
        )

    @classmethod
    def validate(cls, v: AnyStr) -> Self:
        if cls.is_valid(v):
            return cls(v)
        raise ValueError("无效的 ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class FromFieldInfoInputs(_FromFieldInfoInputs, total=False):
    primary_key: bool
    index: bool | IndexType | Index | None
    expire: int | None
    unique: bool


class FieldInfoInputs(FromFieldInfoInputs, total=False):
    default: Any


class FieldInfo(PDFieldInfo):
    def __init__(self, **kwargs: Unpack[FieldInfoInputs]) -> None:
        self.primary_key: bool = kwargs.pop("primary_key", False)
        self.index: bool | IndexType | Index | None = kwargs.pop("index", None)
        self.expire: int | None = kwargs.pop("expire", None)
        self.unique: bool = kwargs.pop("unique", False)
        super().__init__(**kwargs)

    @staticmethod
    def from_field(
        default: Any = PydanticUndefined, **kwargs: Unpack[FromFieldInfoInputs]
    ) -> "FieldInfo":
        if "annotation" in kwargs:
            raise TypeError('"annotation" is not permitted as a Field keyword argument')
        return FieldInfo(default=default, **kwargs)


def Field(
    default: Any = PydanticUndefined,
    *,
    default_factory: Callable[[], Any] | None = None,
    alias: str | None = None,
    alias_priority: int | None = None,
    validation_alias: str | AliasPath | AliasChoices | None = None,
    serialization_alias: str | None = None,
    title: str | None = None,
    description: str | None = None,
    examples: list[Any] | None = None,
    exclude: bool | None = None,
    discriminator: str | Discriminator | None = None,
    json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = None,
    frozen: bool | None = None,
    validate_default: bool | None = None,
    repr: bool = True,
    init: bool | None = None,
    init_var: bool | None = None,
    kw_only: bool | None = None,
    pattern: str | None = None,
    strict: bool | None = None,
    gt: float | None = None,
    ge: float | None = None,
    lt: float | None = None,
    le: float | None = None,
    multiple_of: float | None = None,
    allow_inf_nan: bool | None = None,
    max_digits: int | None = None,
    decimal_places: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    union_mode: Literal["smart", "left_to_right"] | None = None,
    primary_key: bool = False,
    index: bool | IndexType | Index | None = None,
    expire: int | None = None,
    unique: bool = False,
) -> Any:
    """
    primary_key: 主键
    index: 索引
    expire: 到期时间, int 表示创建后多少秒后到期, datetime 表示到期时间
    unique: 唯一索引
    """
    return FieldInfo.from_field(
        default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        json_schema_extra=json_schema_extra,
        frozen=primary_key or frozen,
        pattern=pattern,
        validate_default=validate_default,
        repr=repr,
        init=init,
        init_var=init_var,
        kw_only=kw_only,
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_length=min_length,
        max_length=max_length,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        union_mode=union_mode,
        primary_key=primary_key,
        index=index,
        expire=expire,
        unique=unique,
    )
