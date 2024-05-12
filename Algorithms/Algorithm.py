from typing import List, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Task import Task
    from Processor import Processor


class Algorithm:
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        decide_attribute: str,
        offline: bool = False,
        is_mobileye: bool = False,
        priority_threshold: float = -1,
        priority_rate: float = -1,
    ):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks
        self.decide_attribute = decide_attribute
        self.offline = offline
        self.is_mobileye = is_mobileye
        self.priority_threshold = priority_threshold
        self.priority_rate = priority_rate

    def update_lists(self, processors, ready_tasks, all_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks

    # sort such that to the left of self.priority_threshold are tasks of
    #  priority 0, and to the right are tasks of priority 1
    # (this is where the priority is decided)
    def order_by_priority(
        self, sorted_ready_tasks: List["Task"], attribute: str
    ) -> List["Task"]:
        # check extremes
        if self.priority_threshold < getattr(
            sorted_ready_tasks[0], attribute
        ) or self.priority_threshold > getattr(sorted_ready_tasks[-1], attribute):
            random.shuffle(sorted_ready_tasks)
            self.is_mobileye = False
            return 0

        for task_index in range(1, len(sorted_ready_tasks), 1):
            task = sorted_ready_tasks[task_index]
            previous_task = sorted_ready_tasks[task_index - 1]
            # search for the index where self.priority_threshold fits between two tasks
            if getattr(task, attribute) <= self.priority_threshold <= getattr(
                previous_task, attribute
            ) or getattr(task, attribute) >= self.priority_threshold >= getattr(
                previous_task, attribute
            ):
                random.shuffle(sorted_ready_tasks[:task_index])
                random.shuffle(sorted_ready_tasks[task_index:])
                return task_index

        # if threshold is too big or too small, treat it like a random algorithm
        sorted_ready_tasks = random.shuffle(sorted_ready_tasks)
        return 0

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self) -> List["Task"]:
        pass

    def calculate(self) -> List["Task"]:
        pass
