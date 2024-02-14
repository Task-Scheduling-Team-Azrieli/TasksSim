from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Processor import Processor


class Task:
    def __init__(
        self,
        name: str,
        duration: int,
        processor_type: int,
        blocking: List["Task"],
        blocked_by: List["Task"],
    ):
        self.name = name
        self.processor_type = processor_type
        self.duration = duration
        self.end_time = 0
        self.done = False
        self.processed_by: Processor = None
        self.blocking = blocking
        self.blocked_by = blocked_by

    def is_ready(self):
        return not self.blocked_by and not self.done and self.processed_by == None

    def is_blocked(self):
        return self.blocked_by and not self.done
    
    # insert a task that i am (self) blocking
    def insert_blocking(self, task: "Task"):
        self.blocking.append(task)
        if (self not in task.blocked_by):
            task.blocked_by.append(self)

    # insert a task that i am (self) blocked by
    def insert_blocked_by(self, task: "Task"):
        self.blocked_by.append(task)
        if (self not in task.blocking):
            task.blocking.append(self)
