from __future__ import annotations

from dataclasses import dataclass
import typing as t

from piccolo.columns.base import Selectable

if t.TYPE_CHECKING:
    from piccolo.columns.base import Column


@dataclass
class Readable(Selectable):
    template: str
    columns: t.Sequence[Column]
    output_name: str = "readable"

    @property
    def _columns_string(self) -> str:
        return ", ".join([
            i._meta.get_full_name(just_alias=True) for i in self.columns
        ])

    def _get_string(self, operator: str):
        return (
            f"{operator}('{self.template}', {self._columns_string}) AS "
            f"{self.output_name}"
        )

    @property
    def sqlite_string(self) -> str:
        return self._get_string(operator="PRINTF")

    @property
    def postgres_string(self) -> str:
        return self._get_string(operator="FORMAT")

    def get_select_string(self, engine_type: str, just_alias=False) -> str:
        try:
            return getattr(self, f"{engine_type}_string")
        except AttributeError:
            raise ValueError(
                f"Unrecognised engine_type - received {engine_type}"
            )
