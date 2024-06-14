from typing import List
from Task import Task
from Algorithms.Algorithm import Algorithm
from Processor import Processor


class Greedy(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    # simply returns the order that was given, since the greedy doesn't care
    # gives priority 0 tasks a precedence
    def decide(self):
        return self.ready_tasks.copy()

    def find_thresholds(self, recursion_depth: int) -> List[float]:
        return []


class MobileyeGreedy(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    # simply returns the order that was given, since the greedy doesn't care
    # gives priority 0 tasks a precedence
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: task.priority)
        return result
