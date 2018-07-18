from abc import ABC, abstractmethod
from sqlalchemy import select


class Query(ABC):
    def __str__(self):
        return str(self.build().compile(
            compile_kwargs={"literal_binds": True}))

    def __repr__(self):
        return str(self)

    def build(self) -> select:
        query = self._select\
                    .select_from(self._select_from)\
                    .where(self._whereclause)
        if self._order_by is not None:
            query = query.order_by(*self._order_by)
        query = query.group_by(*self._group_by)\
                     .limit(self._limit)
        if self._having is not None:
            query = query.having(self._having)
        return query

    @property
    @abstractmethod
    def _select(self):
        pass

    @property
    @abstractmethod
    def _select_from(self):
        pass

    @property
    def _whereclause(self):
        return True

    @property
    def _order_by(self):
        return None

    @property
    def _group_by(self):
        return []

    @property
    def _having(self):
        return None

    @property
    def _limit(self):
        return None
