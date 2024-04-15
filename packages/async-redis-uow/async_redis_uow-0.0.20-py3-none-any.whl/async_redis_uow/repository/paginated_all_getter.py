from typing import Generic, List, Optional
from .types import TIModel, TOModel
from .all_getter import AllGetterRepo


class PaginatedAllGetterRepo(AllGetterRepo[TIModel, TOModel], Generic[TIModel, TOModel]):
    __abstract__ = True

    def _page(self, count, page, objs):
        if count and page:
            start_point = (count or 1) * page - count
            end_point = start_point + count
            return objs[start_point:end_point]

        return objs

    async def page(
        self, 
        filters: Optional[str] = None, 
        count: Optional[int] = None, 
        page: Optional[int] = None,
        *,
        parse: bool = True,
    ) -> List[TOModel]:
        objs = await super().all(filters, parse=parse)
        return self._page(count, page, objs)

