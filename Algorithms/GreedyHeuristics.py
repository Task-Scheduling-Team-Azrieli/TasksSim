from typing import List
from Task import Task
from Algorithms.Algorithm import Algorithm
from Processor import Processor
import random


class OutDegreesFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_mobileye: bool = False,
        is_critical: bool = False,
        threshold: float = -1,
    ):
        super().__init__(
            ready_tasks,
            processors,
            all_tasks,
            offline,
            is_mobileye,
            is_critical,
            threshold,
        )
        if self.is_mobileye:
            self.color_tasks()

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -len(task.blocking))
        if self.is_mobileye:
            result = Algorithm.sort_by_priority(result)
        return result

    def find_thresholds(self, recursion_depth: int) -> List[float]:
        return super()._find_thresholds(
            recursion_depth, self.all_tasks, lambda task: len(task.blocking)
        )

    def color_tasks(self) -> None:
        return super()._color_tasks(lambda task: len(task.blocking) > self.threshold)


class OutDegreesLast(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_mobileye: bool = False,
        is_critical: bool = False,
        threshold: float = -1,
    ):
        super().__init__(
            ready_tasks,
            processors,
            all_tasks,
            offline,
            is_mobileye,
            is_critical,
            threshold,
        )
        if self.is_mobileye:
            self.color_tasks()

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: len(task.blocking))
        if self.is_mobileye:
            result = Algorithm.sort_by_priority(result)
        return result

    def find_thresholds(self, recursion_depth: int) -> int:
        return super()._find_thresholds(
            recursion_depth, self.all_tasks, lambda task: len(task.blocking)
        )

    def color_tasks(self) -> None:
        return super()._color_tasks(lambda task: len(task.blocking) < self.threshold)


class MinRuntimeFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_mobileye: bool = False,
        threshold: float = -1,
        is_critical: bool = False,
    ):
        super().__init__(
            ready_tasks,
            processors,
            all_tasks,
            offline,
            is_mobileye,
            is_critical,
            threshold,
        )
        if self.is_mobileye:
            self.color_tasks()

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: task.duration)
        if self.is_mobileye:
            random.shuffle(self.ready_tasks)
            result = Algorithm.sort_by_priority(self.ready_tasks)
        return result

    def find_thresholds(self, recursion_depth: int) -> int:
        return super()._find_thresholds(
            recursion_depth, self.all_tasks, lambda task: task.duration
        )

    def color_tasks(self) -> None:
        return super()._color_tasks(lambda task: task.duration < self.threshold)


class MaxRuntimeFirst(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Task"],
        offline: bool = False,
        is_mobileye: bool = False,
        is_critical: bool = False,
        threshold: int = -1,
    ):
        super().__init__(
            ready_tasks,
            processors,
            all_tasks,
            offline,
            is_mobileye,
            is_critical,
            threshold,
        )
        if self.is_mobileye:
            self.color_tasks()

    # prioritize tasks with high amount of out-degrees
    def decide(self):
        result = sorted(self.ready_tasks, key=lambda task: -task.duration)
        if self.is_mobileye:
            result = Algorithm.sort_by_priority(random.shuffle(self.ready_tasks))
        return result

    def find_thresholds(self, recursion_depth: int) -> int:
        return super()._find_thresholds(
            recursion_depth, self.all_tasks, lambda task: task.duration
        )

    def color_tasks(self) -> None:
        return super()._color_tasks(lambda task: task.duration > self.threshold)


class FromCriticalPath(Algorithm):
    def __init__(
        self,
        ready_tasks: List["Task"],
        processors: List["Processor"],
        all_tasks: List["Processor"],
        offline: bool = False,
        is_mobileye: bool = False,
    ):
        super().__init__(
            ready_tasks,
            processors,
            all_tasks,
            offline,
            is_mobileye=is_mobileye,
            is_critical=False,
            threshold=-1,
        )

    def decide(self, critical_order):
        return sorted(self.ready_tasks, key=lambda x: critical_order.index(x))

    def calculate(self):
        return (
            self._calc_using_topological_sort()
            if self.is_mobileye
            else self._calc_using_critical_time()
        )

    def _calc_using_critical_time(self):
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

        return sorted(self.all_tasks, key=lambda task: -task.critical_time)

    def _calc_using_topological_sort(self):
        # helper function for find_critical_path
        def _topological_sort():
            stack = []
            visited = set()

            def dfs(task):
                if task in visited:
                    return
                visited.add(task)
                for dependency in task.blocked_by:
                    dfs(dependency)
                stack.append(task)

            for task in self.all_tasks:
                dfs(task)

            # Reverse the stack to get the correct topological order
            return stack

        def find_critical_path():
            # perform topological sort to get the tasks in order
            sorted_tasks = _topological_sort()

            # calculate earliest start time (ES) for each task
            for task in sorted_tasks:
                es = 0
                for dependency in task.blocked_by:
                    es = max(es, dependency.es)
                task.es = es + task.duration

            # calculate latest start time (LS) for each task
            for task in reversed(sorted_tasks):
                ls = float("inf")
                if not task.blocking:  # if task is a sink node
                    ls = task.es
                for predecessor in task.blocked_by:
                    ls = min(ls, predecessor.es - predecessor.duration)
                task.ls = ls

            # identify critical path tasks
            critical_path = [task for task in sorted_tasks if task.es == task.ls]

            return critical_path

        return find_critical_path()

    def color_tasks(self) -> None:
        return super().color_tasks()

    def find_thresholds(self, recursion_depth: int) -> List[float]:
        return super().find_thresholds(recursion_depth)
