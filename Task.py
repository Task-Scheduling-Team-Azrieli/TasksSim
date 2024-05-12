from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Processor import Processor


class Task:
    def __init__(
        self,
        name: str,
        duration: float,
        processor_type: int,
        priority: int,
        blocking: List["Task"],
        blocked_by: List["Task"],
        critical_time = 0
    ):
        self.name = name
        self.processor_type = processor_type
        self.duration = duration
        self.end_time = 0
        self.processed_by: Processor = None
        self.priority = priority
        # whether a task has stopped running
        self.done = False
        self.critical_time = critical_time

        # In and Out degrees
        self.blocking = blocking
        self.len_blocking = len(blocking)
        self.blocked_by = blocked_by
        self.len_blocked_by = len(blocked_by)

        # Latest/Earliest start time (LS and ES)
        self.es = 0
        self.ls = 0

    def is_ready(self):
        return not self.blocked_by and not self.done and self.processed_by == None

    def is_blocked(self):
        return self.blocked_by and not self.done

    # insert a task that i am (self) blocking
    def insert_blocking(self, task: "Task"):
        self.blocking.append(task)
        self.len_blocking += 1
        if self not in task.blocked_by:
            task.blocked_by.append(self)
            task.len_blocked_by += 1

    # insert a task that i am (self) blocked by
    def insert_blocked_by(self, task: "Task"):
        self.blocked_by.append(task)
        self.len_blocked_by += 1
        if self not in task.blocking:
            task.blocking.append(self)
            task.len_blocking += 1

    # Define custom comparison logic
    def __lt__(self, other):
        # if priorities are equal, return False to indicate no preference
        # otherwise, compare based on priority
        if self.priority == other.priority:
            return False
        else:
            return self.priority < other.priority
