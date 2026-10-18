"""Shared helpers: dates, deterministic randomness and a tiny in-memory repository.

Swap `Repository` for a real database adapter later — only services talk to it."""
from datetime import date, timedelta
from random import Random

from fastapi import HTTPException

TODAY = date.today()
rng = Random(42)


def days(offset: int) -> str:
    return (TODAY + timedelta(days=offset)).isoformat()


class Repository:
    def __init__(self, rows: list[dict], key: str = "id"):
        self.rows = rows
        self.key = key

    def all(self) -> list[dict]:
        return self.rows

    def get(self, value):
        return next((r for r in self.rows if r[self.key] == value), None)

    def get_or_404(self, value) -> dict:
        row = self.get(value)
        if row is None:
            raise HTTPException(404, f"{value} not found")
        return row

    def add(self, row: dict) -> dict:
        self.rows.insert(0, row)
        return row
