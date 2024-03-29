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
    ):
        super().__init__(ready_tasks, processors, all_tasks)

    # simply returns the order that was given, since the greedy doesn't care
    # gives priority 0 tasks a precedence
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: task.priority)
        return result
