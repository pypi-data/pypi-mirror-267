from collections.abc import Sequence
from typing import TypedDict

from mango.drive import Database
from mango.encoder import EncodeType
from mango.index import Index, IndexTuple


class MetaConfig(TypedDict, total=False):
    name: str | None
    database: Database | str | None
    indexes: Sequence[str | Index | Sequence[IndexTuple]]
    bson_encoders: EncodeType
    by_alias: bool
