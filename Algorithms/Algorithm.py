from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Task import Task
    from Processor import Processor


class Algorithm:
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_priority: bool = False,
    ):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks
        self.offline = offline
        self.is_priority = is_priority

    def update_lists(self, processors, ready_tasks, all_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self, order=[], threshold=-1) -> List["Task"]:
        pass

    def calculate(self) -> List["Task"]:
        pass
