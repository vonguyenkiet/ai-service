from __future__ import annotations

from typing import Protocol, Sequence


class TextEmbedder(Protocol):
    @property
    def name(self) -> str: ...

    async def embed(self, *, text: str) -> Sequence[float]: ...
