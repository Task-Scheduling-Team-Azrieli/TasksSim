from abc import abstractmethod
import abc
from GreedyHeuristics import FromCriticalPath
from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from Task import Task
    from Processor import Processor


class Algorithm(metaclass=abc.ABCMeta):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_mobileye: bool = False,
        is_critical: bool = False,
        threshold: int = -1
    ):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks
        self.offline = offline
        self.is_mobileye = is_mobileye
        self.threshold = threshold
        self.is_critical = is_critical

    def update_lists(self, processors, ready_tasks, all_tasks):
        self.processors = processors
        self.ready_tasks = ready_tasks
        self.all_tasks = all_tasks

    # finds the threshold for a specific heuristic
    def _find_thresholds(
        self,
        recursion_depth: int,
        task_list: List["Task"],
        attribute_extractor: Callable[["Task"], "float"],
    ) -> List[float]:

        n = len(task_list)
        if recursion_depth == 0 or n <= 1:
            return []

        # use the extractor to get the threshold value
        thresh_value = attribute_extractor(task_list[n // 2])
        return (
            [thresh_value]
            + self._find_thresholds(
                recursion_depth - 1, task_list[: n // 2], attribute_extractor
            )
            + self._find_thresholds(
                recursion_depth - 1, task_list[n // 2 :], attribute_extractor
            )
        )

    def _color_tasks(self, priority_decider: Callable[["Task"], "float"]) -> List[float]:
        for task in self.all_tasks:
            task.priority = priority_decider(task)
        if self.is_critical:
            critical_path_instance = FromCriticalPath(self.ready_tasks, self.processors, self.all_tasks, offline=True)
            critical_path = critical_path_instance.
            
    
    @abstractmethod
    def find_thresholds(self, recursion_depth: int) -> List[float]:
        pass

    @abstractmethod
    def color_tasks(self, recursion_depth: int) -> List[float]:
        pass

    # returns the order of tasks that the algorithm decided we should iterate over
    def decide(self) -> List["Task"]:
        pass

    def calculate(self) -> List["Task"]:
        pass
