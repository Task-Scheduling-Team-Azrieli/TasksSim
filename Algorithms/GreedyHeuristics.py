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

class FromCriticalPath(Algorithm):
    def __init__(self, ready_tasks: List["Task"], processors: List["Processor"]):
        super().__init__(ready_tasks, processors)

    def decide(self):
        def update_critical_time(node: Task):
            node.critical_time = (max([n.critical_time for n in node.out_tasks]) if len(node.blocking) > 0 else 0) + node.duration
            if len(node.blocked_by) == 0:
                return
            for n in node.in_task:
                update_critical_time(n)
        
        end_tasks = [task for task in self.ready_tasks if len(task.blocking) == 0]
        for t in end_tasks:
            update_critical_time(t)
        
        result = sorted(self.ready_tasks, key=lambda task: -task.critical_time)
        return result
