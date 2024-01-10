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
        self.ready = False
        self.done = False
        self.being_processed = False
        self.blocking = blocking
        self.blocked_by = blocked_by

    def remove_from_blocks(self, task: "Task"):
        self.blocks = [t for t in self.blocks if t.name != task.name]

    def remove_from_blocked_by(self, task):
        self.blocked_by = [t for t in self.blocked_by if t.name != task.name]
