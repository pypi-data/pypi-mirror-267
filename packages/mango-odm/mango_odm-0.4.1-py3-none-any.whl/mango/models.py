import contextlib
from collections.abc import Mapping, MutableMapping, Sequence
from functools import reduce
from typing import TYPE_CHECKING, Any, ClassVar

import bson
from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass
from typing_extensions import Self, dataclass_transform

from mango.encoder import Encoder
from mango.expression import Expression, ExpressionField, Operators
from mango.fields import Field, FieldInfo, ObjectIdField
from mango.meta import MetaConfig
from mango.result import AggregateResult, FindMapping, FindResult
from mango.source import Mango
from mango.stage import Pipeline
from mango.utils import add_fields, all_check, validate_fields

if TYPE_CHECKING:
    from bson.codec_options import CodecOptions
    from pymongo.results import DeleteResult, UpdateResult

    from mango.drive import Collection, Database

operators = tuple(str(i) for i in Operators)


def is_need_default_pk(
    bases: tuple[type[Any], ...], annotate: dict[str, Any] | None = None
) -> bool:
    # 未定义任何字段
    if not annotate:
        return False

    # 存在 id 字段但未定义主键
    if "id" in annotate:
        return False

    # 存在 id 字段但未定义主键，且其被继承
    return not any(getattr(base, "id", None) for base in bases)


def set_default_pk(model: type["Document"]) -> None:
    add_fields(
        model,
        id=(
            ObjectIdField,
            {
                "default_factory": ObjectId,
                "primary_key": True,
                "frozen": True,
                "init": False,
            },
        ),
    )
    model.__primary_key__ = "id"


def flat_filter(data: Mapping[str, Any]) -> dict[str, Any]:
    flatted = {}
    for key, value in data.items():
        if key.startswith(operators):
            flatted |= flat_filter(reduce(lambda x, y: x | y, value))
        elif "." in key:
            parent, child = key.split(".", maxsplit=1)
            flatted[parent] = flat_filter({child: value})
        else:
            for operator in operators:
                if isinstance(value, dict) and operator in value:
                    flatted[key] = value[operator]
    return flatted


def merge_map(data: MutableMapping[Any, Any], into: Mapping[Any, Any]) -> None:
    for k, v in into.items():
        k = str(k)  # noqa: PLW2901
        if isinstance(data.get(k), dict) and isinstance(v, dict | EmbeddedDocument):
            merge_map(data[k], v if isinstance(v, dict) else v.model_dump())
        else:
            data[k] = v


config_keys = set(MetaConfig.__annotations__.keys())


def merge_config(
    bases: tuple[type[Any], ...], attrs: dict[str, Any], kwargs: dict[str, Any]
) -> MetaConfig:
    config = MetaConfig()

    for base in bases:
        if cfg := getattr(base, "meta_config", None):
            config.update(cfg.copy())

    config.update(attrs.get("meta_config", MetaConfig()))

    for k in list(kwargs.keys()):
        if k in config_keys:
            config[k] = kwargs.pop(k)
        if k == "db":
            config["database"] = kwargs.pop(k)

    return config


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, FieldInfo))
class MetaDocument(ModelMetaclass):
    def __new__(
        cls,
        cname: str,
        bases: tuple[type[Any], ...],
        attrs: dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        # 跳过基类
        if bases == (BaseModel,):
            return super().__new__(cls, cname, bases, attrs, **kwargs)

        # 合并配置
        attrs["meta_config"] = merge_config(bases, attrs, kwargs)

        # 创建编码器
        attrs["__encoder__"] = Encoder.create(attrs["meta_config"].get("bson_encoders"))

        scls = super().__new__(cls, cname, bases, attrs, **kwargs)

        # 设置模型字段
        annotations = attrs.get("__annotations__", {})
        for fname in annotations:
            field = scls.model_fields[fname]
            setattr(scls, fname, ExpressionField(fname, field, []))

        # 检查主键是否唯一
        pk_fields = {
            fname: field
            for fname, field in scls.model_fields.items()
            if isinstance(field, FieldInfo) and field.primary_key
        }
        if len(pk_fields) > 1:
            raise ValueError(
                f"文档的主键应唯一, 当前有主键字段: {', '.join(pk_fields.keys())}"
            )

        # 设置显式主键
        if len(pk_fields) == 1:
            pk_name, pk_filed = next(iter(pk_fields.items()))
            scls.__primary_key__ = pk_filed.alias or pk_name

        # 设置默认主键
        if not pk_fields and is_need_default_pk(bases, annotations):
            set_default_pk(scls)

        # 注册模型
        Mango.register_model(scls)

        return scls


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, FieldInfo))
class MetaEmbeddedDocument(ModelMetaclass):
    def __new__(
        cls,
        name: str,
        bases: tuple[type[Any], ...],
        attrs: dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        scls = super().__new__(cls, name, bases, attrs, **kwargs)
        for fname, field in scls.model_fields.items():
            setattr(scls, fname, ExpressionField(fname, field, []))
            if isinstance(field, FieldInfo) and field.primary_key:
                raise ValueError("内嵌文档不可设置主键")
        return scls


class Document(BaseModel, metaclass=MetaDocument):
    if TYPE_CHECKING:  # pragma: no cover
        id: ClassVar[ObjectId]
        model_fields: ClassVar[dict[str, FieldInfo]]
        __encoder__: ClassVar[CodecOptions]
        __collection__: ClassVar[Collection]
        __primary_key__: ClassVar[str]

        def __init_subclass__(
            cls,
            *,
            name: str | None = None,
            db: Database | str | None = None,
            **kwargs: Any,
        ) -> None: ...

    meta_config: ClassVar[MetaConfig] = MetaConfig()
    model_config = ConfigDict(validate_assignment=True)

    @property
    def pk(self) -> Any:
        """主键值"""
        return getattr(self, self.__primary_key__)

    async def insert(self) -> Self:
        """插入文档"""
        await self.__collection__.insert_one(self.doc())
        return self

    async def update(self, **kwargs: Any) -> bool:
        """更新文档"""
        if kwargs:
            values = validate_fields(self.__class__, kwargs)
            for field, value in values.items():
                setattr(self, field, value)
        result: UpdateResult = await self.__collection__.update_one(
            {"_id": self.pk}, {"$set": self.doc(exclude={self.__primary_key__})}
        )
        return bool(result.modified_count)

    async def save(self, **kwargs: Any) -> Self:
        """保存文档，如果文档不存在，则插入，否则更新它。"""
        existing_doc = await self.__collection__.find_one({"_id": self.pk})
        if existing_doc:
            await self.update(**kwargs)
        else:
            await self.insert()
        return self

    async def delete(self) -> bool:
        """删除文档"""
        result: DeleteResult = await self.__collection__.delete_one({"_id": self.pk})
        return bool(result.deleted_count)

    def doc(self, **kwargs: Any) -> dict[str, Any]:
        """转换为 MongoDB 文档"""
        if by_alias := self.meta_config.get("by_alias"):
            kwargs.setdefault("by_alias", by_alias)
        data = self.model_dump(**kwargs)
        pk = self.__primary_key__
        exclude = kwargs.get("exclude")
        if not (exclude and pk in exclude):
            data["_id"] = data.pop(pk)
        return bson.decode(bson.encode(data, codec_options=self.__encoder__))

    @classmethod
    def from_doc(cls, document: Mapping[str, Any]) -> Self:
        """从文档构建模型实例"""
        doc = dict(document)
        with contextlib.suppress(KeyError):
            doc[cls.__primary_key__] = doc.pop("_id")
        return cls(**doc)

    @classmethod
    async def save_all(cls, *documents: Self) -> None:
        """保存全部文档"""
        await cls.__collection__.insert_many(doc.doc() for doc in documents)

    @classmethod
    def aggregate(
        cls, pipeline: Pipeline | Sequence[Mapping[str, Any]], *args: Any, **kwargs: Any
    ) -> AggregateResult:
        """聚合查询"""
        cursor = cls.__collection__.aggregate(pipeline, *args, **kwargs)
        return AggregateResult(cursor)

    @classmethod
    def find(
        cls,
        *args: FindMapping | Expression | bool,
    ) -> FindResult[Self]:
        """使用表达式查询文档"""
        if all_check(args, Expression | Mapping):
            return FindResult(cls, *args)  # type: ignore
        raise TypeError("查询表达式类型不正确")

    @classmethod
    async def get(cls, _id: Any) -> Self | None:
        """通过主键查询文档"""
        return await cls.find({"_id": _id}).get()

    @classmethod
    async def get_or_create(
        cls,
        *args: FindMapping | Expression | bool,
        defaults: FindMapping | Self | None = None,
    ) -> Self:
        """获取文档, 如果不存在, 则创建"""
        result: FindResult[Self] = FindResult(cls, *args)  # type: ignore
        if model := await result.get():
            return model
        default = defaults.doc() if isinstance(defaults, Document) else defaults or {}
        data = flat_filter(result.filter)
        merge_map(data, default)
        model = cls.from_doc(data)
        return await model.save()


class EmbeddedDocument(BaseModel, metaclass=MetaEmbeddedDocument):
    model_config = ConfigDict(validate_assignment=True)
