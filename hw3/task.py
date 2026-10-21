#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(slots=True)
class Task:
    task_id: int
    title: str
    desc: str
    priority: str | None
    is_completed: bool
    is_pinned: bool