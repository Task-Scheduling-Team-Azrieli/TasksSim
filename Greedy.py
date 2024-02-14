from typing import List
from Task import Task
from Algorithm import Algorithm
from Processor import Processor


class Greedy(Algorithm):
    def __init__(self, ready_tasks: List["Task"], processors: List["Processor"]):
        super().__init__(ready_tasks, processors)

    # simply returns the order that was given, since the greedy doesn't care
    def decide(self):
        result = self.ready_tasks.copy()
        return result
