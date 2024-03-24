from typing import List
from Task import Task
from Algorithms.Algorithm import Algorithm
from Processor import Processor


class OutDegreesFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
    ):
        super().__init__(ready_tasks, processors, all_tasks)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -len(task.blocking))
        return result


class MinRuntimeFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
    ):
        super().__init__(ready_tasks, processors, all_tasks)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: task.duration)
        return result


class MaxRuntimeFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
    ):
        super().__init__(ready_tasks, processors, all_tasks)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -task.duration)
        return result
