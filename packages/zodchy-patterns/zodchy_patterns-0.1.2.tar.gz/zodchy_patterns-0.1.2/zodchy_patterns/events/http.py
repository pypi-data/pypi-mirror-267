import collections.abc
import dataclasses
from zodchy import codex


@dataclasses.dataclass
class HTTPResponseEvent(codex.ResponseEvent):
    def get_content(self) -> dict:
        data = dataclasses.asdict(self)
        return {
            'data': data or None
        }

    def get_status_code(self) -> int:
        return 200


@dataclasses.dataclass
class ErrorResponseEvent(HTTPResponseEvent):
    def get_status_code(self) -> int:
        return 500


@dataclasses.dataclass
class CreatedResponseEvent(HTTPResponseEvent):
    def get_content(self) -> dict:
        data = dataclasses.asdict(self)
        return {'data': data} if data else None

    def get_status_code(self):
        return 200 if self.get_content() else 201


@dataclasses.dataclass
class ItemResponseEvent(HTTPResponseEvent):
    data: collections.abc.Mapping

    def get_content(self):
        return {'data': self.data} if self.data else None

    def get_status_code(self):
        return 200 if self.data else 404


@dataclasses.dataclass
class ListResponseEvent(HTTPResponseEvent):
    data: collections.abc.Iterable[collections.abc.Mapping]

    def get_content(self):
        return {
            'data': self.data or []
        }


@dataclasses.dataclass
class PaginatedListResponseEvent(ListResponseEvent):
    total: int

    def get_content(self):
        return super().get_content() | {
            'pagination': {
                'quantity': self.total
            }
        }
