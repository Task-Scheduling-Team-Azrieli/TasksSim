from typing import Callable, List, TYPE_CHECKING

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
        is_mobileye: bool = False,
    ):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks
        self.offline = offline
        self.is_mobileye = is_mobileye

    def update_lists(self, processors, ready_tasks, all_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks

    # finds the threshold for a specific heuristic
    def find_thresholds(
        self,
        recurtion_depth: int,
        task_list: List[Task],
        attribute_extractor: Callable[[Task], float],
    ) -> List[float]:

        n = len(task_list)
        if recurtion_depth == 0 or n <= 1:
            return []

        # use the extractor to get the threshold value
        thresh_value = attribute_extractor(task_list[n // 2])
        return (
            [thresh_value]
            + self.find_thresholds(
                recurtion_depth - 1, task_list[: n // 2], attribute_extractor
            )
            + self.find_thresholds(
                recurtion_depth - 1, task_list[n // 2 :], attribute_extractor
            )
        )

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self) -> List["Task"]:
        pass

    def calculate(self) -> List["Task"]:
        pass
