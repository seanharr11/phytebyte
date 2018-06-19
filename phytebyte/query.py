from abc import ABC, abstractmethod
from sqlalchemy import select


class Query(ABC):
    def __str__(self):
        return self.build().compile(compile_kwargs={"literal_binds": True})

    def __repr__(self):
        return str(self)

    def build(self) -> select:
        query = self._select\
                    .select_from(self._select_from)\
                    .where(self._whereclause)\
                    .order_by(self._order_by)\
                    .group_by(*self._group_by)
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
