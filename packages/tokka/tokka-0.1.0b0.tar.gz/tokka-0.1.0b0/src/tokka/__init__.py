from typing import Any
from typing import Awaitable
from typing import Literal
from typing import Unpack

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo import ReturnDocument
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult

from tokka.kwargs import FindKwargs
from tokka.kwargs import ModelDumpKwargs


# TODO: 'Intersection' PEP is under development
#        it will possible be the best and most accurate to type Pydantic`s model_dump
#        and Pymongo's Kwargs.
#
# ? Related issues:
#        https://github.com/python/typing/issues/213
#        https://github.com/python/typing/issues/1445


class Collection:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    @staticmethod
    def _pop_model_dump_kwargs(
        kwargs: dict[str, Any],
    ) -> tuple[dict[str, Any], ModelDumpKwargs]:
        model_dump_kwargs: ModelDumpKwargs = {
            "mode": kwargs.pop("mode", "python"),
            "include": kwargs.pop("include", None),
            "exclude": kwargs.pop("exclude", None),
            "by_alias": kwargs.pop("by_alias", False),
            "exclude_unset": kwargs.pop("exclude_unset", False),
            "exclude_defaults": kwargs.pop("exclude_defaults", False),
            "exclude_none": kwargs.pop("exclude_none", False),
            "round_trip": kwargs.pop("round_trip", False),
            "warnings": kwargs.pop("warnings", True),
        }

        if isinstance(model_dump_kwargs["include"], str):
            model_dump_kwargs["include"] = set([model_dump_kwargs["include"]])

        if isinstance(model_dump_kwargs["exclude"], str):
            model_dump_kwargs["exclude"] = set([model_dump_kwargs["exclude"]])

        return kwargs, model_dump_kwargs

    @staticmethod
    def _make_filter(
        model: BaseModel, by: None | str | list[str] = None
    ) -> dict[str, Any]:
        match by:
            case x if isinstance(x, str):
                _filter = {x: getattr(model, x)}
            case xx if isinstance(xx, list):
                _filter = {x: getattr(model, x) for x in xx}
            case _:
                _filter = model.model_dump()

        return _filter

    @staticmethod
    def _make_projection(exclude_keys: set[str]) -> dict[str, Literal[0]]:
        return {key: 0 for key in exclude_keys}

    def find_one(
        self,
        model: BaseModel,
        *,
        hide: set[str] = set("_id"),
        filter_by: None | str | list[str] = None,
        **kwargs: Unpack[FindKwargs],
    ) -> Awaitable[Cursor] | Awaitable[None]:
        _filter = self._make_filter(model, filter_by)
        _projection = self._make_projection(hide)
        kwargs.pop("projection", None)
        return self.collection.find_one(_filter, _projection, **kwargs)

    def find_one_and_replace(
        self,
        model: BaseModel,
        replacement: BaseModel,
        *,
        upsert: bool = False,
        return_old: bool = False,
        filter_by: None | str | list[str] = None,
        hide: set[str] = set("_id"),
        **kwargs: Any,
    ) -> Awaitable[ReturnDocument]:
        _filter = self._make_filter(model, filter_by)
        pymongo_kwargs, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        pymongo_kwargs.pop("projection", None)
        pymongo_kwargs.pop("filter", None)
        pymongo_kwargs.pop("replacement", None)
        pymongo_kwargs.pop("upsert", None)
        pymongo_kwargs.pop("return_document", None)

        # ? see pymongo.collection.ReturnDocument.BEFORE
        # ? at https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#
        # pymongo.collection.ReturnDocument = False returns the old document
        # pymongo.collection.ReturnDocument = True returns the new document
        # Therefore, we need to invert the return_old value to obtain a more
        # intuitive behavior
        return_old = not return_old

        pymongo_kwargs.pop("return_document", None)

        _replacement = replacement.model_dump(**model_dump_kwargs)
        _projection = self._make_projection(hide)
        return self.collection.find_one_and_replace(
            _filter,
            _replacement,
            _projection,
            upsert=upsert,
            return_document=return_old,
            **pymongo_kwargs,
        )

    def find_one_and_delete(
        self,
        model: BaseModel,
        *,
        filter_by: None | str | list[str] = None,
        hide: set[str] = set("_id"),
        **kwargs: Any,
    ) -> Awaitable[dict[str, Any]]:
        _filter = self._make_filter(model, filter_by)
        _projection = self._make_projection(hide)
        return self.collection.find_one_and_delete(_filter, _projection, **kwargs)

    def find_one_and_update(
        self,
        model: BaseModel,
        update: dict[str, Any],
        *,
        upsert: bool = False,
        return_old: bool = False,
        filter_by: None | str | list[str] = None,
        hide: set[str] = set("_id"),
        **kwargs: Any,
    ) -> Awaitable[ReturnDocument]:
        _filter = self._make_filter(model, filter_by)
        kwargs.pop("projection", None)
        kwargs.pop("filter", None)
        kwargs.pop("replacement", None)
        kwargs.pop("upsert", None)
        kwargs.pop("return_document", None)

        # NOTE: see find_one_and_replace method for more details
        return_old = not return_old

        kwargs.pop("return_document", None)

        _projection = self._make_projection(hide)
        return self.collection.find_one_and_update(
            _filter,
            update,
            _projection,
            upsert=upsert,
            return_document=return_old,
            **kwargs,
        )

    def find_one_and_set(
        self,
        model: BaseModel,
        *,
        upsert: bool = False,
        return_old: bool = False,
        filter_by: None | str | list[str] = None,
        hide: set[str] = set("_id"),
        **kwargs: Any,
    ) -> Awaitable[ReturnDocument]:
        _, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        _update = {"$set": model.model_dump(**model_dump_kwargs)}
        return self.find_one_and_update(
            model,
            _update,
            upsert=upsert,
            return_old=return_old,
            filter_by=filter_by,
            hide=hide,
            **kwargs,
        )

    def insert_one(self, model: BaseModel, **kwargs: Any) -> Awaitable[InsertOneResult]:
        insert_one_kwargs, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        document = model.model_dump(**model_dump_kwargs)
        return self.collection.insert_one(document, **insert_one_kwargs)

    def replace_one(
        self,
        model: BaseModel,
        replacement: BaseModel,
        *,
        upsert: bool = False,
        return_old: bool = False,
        filter_by: None | str | list[str] = None,
        **kwargs: Any,
    ) -> Awaitable[UpdateResult]:
        _filter = self._make_filter(model, filter_by)
        pymongo_kwargs, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        pymongo_kwargs.pop("projection", None)
        pymongo_kwargs.pop("filter", None)
        pymongo_kwargs.pop("replacement", None)
        pymongo_kwargs.pop("upsert", None)
        pymongo_kwargs.pop("return_document", None)

        # ? see pymongo.collection.ReturnDocument.BEFORE
        # ? at https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#
        # pymongo.collection.ReturnDocument = False returns the old document
        # pymongo.collection.ReturnDocument = True returns the new document
        # Therefore, we need to invert the return_old value to obtain a more
        # intuitive behavior
        return_old = not return_old

        pymongo_kwargs.pop("return_document", None)

        _replacement = replacement.model_dump(**model_dump_kwargs)

        return self.collection.replace_one(
            _filter, _replacement, upsert=upsert, **pymongo_kwargs
        )

    def update_one(
        self,
        model: BaseModel,
        *,
        filter_by: None | str | list[str] = None,
        upsert: bool = False,
        **kwargs: dict[str, Any],
    ) -> Awaitable[UpdateResult]:
        _, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        _update = model.model_dump(*model_dump_kwargs)
        _filter = self._make_filter(model, filter_by)
        return self.collection.update_one(_filter, _update, upsert)

    def set(
        self,
        model: BaseModel,
        *,
        match: None | str | list[str],
        upsert: bool = False,
        **kwargs: Any,
    ) -> Awaitable[UpdateResult]:
        update_one_kwargs, model_dump_kwargs = self._pop_model_dump_kwargs(kwargs)
        _filter = self._make_filter(model, match)
        _update = {"$set": model.model_dump(**model_dump_kwargs)}

        return self.collection.update_one(_filter, _update, upsert, **update_one_kwargs)

    def delete_one(self) -> Awaitable[DeleteResult]:
        raise NotImplementedError


class Database:
    def __init__(self, name: str, *, connection: str | AsyncIOMotorClient) -> None:
        match connection:
            case str():
                self.client = AsyncIOMotorClient(connection)
            case AsyncIOMotorClient():
                self.client = connection

        self._connection = self.client.get_database(name)

    def get_collection(self, name: str) -> Collection:
        return Collection(self._connection.get_collection(name))

    def close(self) -> None:
        self.client.close()


class Client:
    def __init__(self, uri: str) -> None:
        self.client = AsyncIOMotorClient(uri)

    def get_database(self, name: str) -> Database:
        return Database(name, connection=self.client)

    def close(self) -> None:
        self.client.close()
