import json
from typing import Any, Callable, Optional, Type, Generic, Union
from uuid import uuid4
from axabc.db.async_repository import AbstractAsyncRepository
from async_redis_uow.session_maker.session import LazySession 
from .types import TIModel, TOModel


class BaseRepoCreator(AbstractAsyncRepository, Generic[TIModel, TOModel]):
    Schema: Type[TIModel]
    OSchema: Type[TOModel]

    __hname__: Optional[str] = None
    __abstract__ = True

    def __init__(self, session: LazySession) -> None:
        self.session = session

    def __init_subclass__(cls) -> None:
        if cls.__abstract__ and '__abstract__' in cls.__dict__:
            return

        types = getattr(cls, "__orig_bases__")[0].__args__
        cls.Schema, cls.OSchema = types

    def get_obj_id(self, obj: Union[TIModel, TOModel]):
        return _ if hasattr(obj, 'id') and (_ := getattr(obj, 'id')) else str(uuid4())

    @staticmethod
    def _isnt_last_level_list(objs: list[TIModel]):
        return objs and len(objs) == 1 and isinstance(objs[-1], list)

    @staticmethod
    def _is_non_empty_list(objs: list[TIModel]):
        return isinstance(objs, list) and objs
    
    def _unwrap_till(self, objs, *, condition_func: Callable[[list[TIModel]], Any] = _isnt_last_level_list):
        while condition_func(objs):
            objs = objs[-1]

        return objs

    @property
    def hname(self):
        return self.__hname__ or self.Schema.__name__.lower()

    def dumps(self, obj: dict) -> str:
        return json.dumps(obj)

    def loads(self, obj: str) -> dict:
        return json.loads(obj)

