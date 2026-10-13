#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(slots=True)
class Task:
    title: str
    desc: str
    priority: str
    is_completed: bool
    is_pinned: bool