import threading
from typing import TYPE_CHECKING
from tkinter import Canvas

if TYPE_CHECKING:
    from Task import Task


class Processor:
    def __init__(self, name: str, processor_type: int):
        self.name = name
        self.type = processor_type
        self.idle = True
        self.current_task = None
        work_order = []

    def work_on_task(self, task: "Task"):
        self.idle = False
        self.work_order.append(task)
        self.current_task = task
        self.current_task.being_processed = True

    def finish_task(self):
        self.current_task.done = True
        self.current_task.being_processed = False
        # remove current task from all blocked_by lists of the tasks its blocking
        for task in self.current_task.blocking:
            if self.current_task in task.blocked_by:
                task.blocked_by.remove(self.current_task)

        self.idle = True
        self.current_task = None
