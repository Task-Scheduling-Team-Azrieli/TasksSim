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
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -len(task.blocking))
        return result

class OutDegreesLast(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: len(task.blocking))
        return result

class MinRuntimeFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

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
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -task.duration)
        return result


class FromCriticalPath(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Processor"],
        offline: bool = False,
    ):
        super().__init__(ready_tasks, processors, all_tasks, offline)

    def decide(self, critical_order):
        return sorted(self.ready_tasks, key=lambda x: critical_order.index(x))

    def calculate(self):
        def update_critical_time(node: Task):
            node.critical_time = (
                max([n.critical_time for n in node.blocking])
                if len(node.blocking) > 0
                else 0
            ) + node.duration
            if len(node.blocked_by) == 0:
                return
            for n in [n for n in node.blocked_by if n.critical_time > 0]:
                update_critical_time(n)

        end_tasks = [task for task in self.all_tasks if len(task.blocking) == 0]
        for t in end_tasks:
            update_critical_time(t)

        result = sorted(self.all_tasks, key=lambda task: -task.critical_time)
        return result
