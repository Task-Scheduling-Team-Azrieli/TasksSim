from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Task import Task
    from Processor import Processor


class Algorithm:
    def __init__(self, ready_tasks: List["Task"], processors: List["Processor"]):
        self.processors = processors
        self.ready_tasks = ready_tasks

    def update_lists(self, processors, ready_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self) -> List["Task"]:
        pass
