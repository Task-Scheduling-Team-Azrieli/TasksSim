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
    ):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks
        self.offline = offline

    def update_lists(self, processors, ready_tasks, all_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks

    # threshold = the number to check against the task attribute
    # below = whether priority 0 (more important) should be below the threshold or above
    def decide_priority(
        self, threshold: int, attribute: str, below: bool
    ) -> List["Task"]:
        for task in self.all_tasks:
            task_attr_value = getattr(task, attribute)
            if (below and task_attr_value < threshold) or (
                not below and task_attr_value > threshold
            ):
                task.priority = 0
            else:
                task.priority = 1

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self) -> List["Task"]:
        pass

    def calculate(self) -> List["Task"]:
        pass
