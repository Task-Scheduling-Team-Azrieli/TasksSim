from Task import Task
from Processor import Processor
from Algorithms.Algorithm import Algorithm
from Algorithms.Greedy import Greedy, MobileyeGreedy
from Algorithms.GreedyHeuristics import (
    OutDegreesFirst,
    MinRuntimeFirst,
    MaxRuntimeFirst,
    FromCriticalPath,
    OutDegreesLast,
)
from queue import PriorityQueue
from TimeLineIlustration import TimeLineIlustartion

from typing import List, Tuple, Dict
import json
import os
import random

# excel
import openpyxl
from openpyxl import Workbook


class Sim:
    def __init__(self):
        self.tasks: List["Task"] = []
        self.processors: List["Processor"] = []

        self.algorithm = None

        self.total_time = 0
        self.final_end_time = 0

    def read_data(self, file_path: str):
        """reads data from a json file to objects (tasks, processors) in this class

        Args:
            file_path (str): full path to the file to read the data from
        """
        input_file = open(file_path)
        data = json.load(input_file)

        tasks_json = data["Tasks"]
        processors_json: List[str] = data["Processors"]

        # to connect a task name to its object, improves efficiency
        # when adding in and out degrees
        temp: Dict[str, Task] = {}

        # create all tasks
        for task_name in tasks_json:
            task_info = tasks_json[task_name]
            task = Task(
                task_name,
                task_info["duration"],
                task_info["processor_type"],
                task_info["priority"],
                [],
                [],
            )
            self.tasks.append(task)
            temp[task_name] = task

        # add in and out degrees to the tasks
        for task_name in tasks_json:
            # add out-degrees
            task_info = tasks_json[task_name]

            blocking = [
                temp[task_name_blocking] for task_name_blocking in task_info["blocking"]
            ]
            temp[task_name].blocking = blocking

            # add in-degrees
            for task in temp[task_name].blocking:
                task.blocked_by.append(temp[task_name])
                task.len_blocked_by += 1

        # read processors
        for processor_str in processors_json:
            processor_name = processor_str.split(":")[0]
            processor_type = int(processor_str.split(":")[1])
            processor = Processor(processor_name, processor_type)

            if processor not in self.processors:
                self.processors.append(processor)

        self.timeLineIlustartor = TimeLineIlustartion(self.processors)

    def start(self, algorithm: Algorithm, illustration=False):
        """starts the simulation, matches tasks for processors

        Args:
            algorithm (Algorithm): the algorithm to apply the order of tasks
            illustration (bool, optional): adds an illustration to the sim. Defaults to False.

        Returns:
            (float, int): total duration of all tasks, final end time of all tasks
        """
        self.algorithm = algorithm
        working_processors = []
        idle_processors: List["Processor"] = self.processors.copy()

        current_tasks: PriorityQueue[Tuple[float, Task]] = PriorityQueue()
        ready_tasks = [task for task in self.tasks if task.is_ready()]

        # for offline algorithms
        if algorithm.offline:
            order = algorithm.calculate()

        def match_ready_tasks(current_time, ready_tasks):
            if len(ready_tasks) == 0:
                return []
            algorithm.update_lists(idle_processors, ready_tasks, self.tasks)
            if algorithm.offline:
                ready_tasks_order = algorithm.decide(order)
            else:
                ready_tasks_order = algorithm.decide()

            threshold_index = 0
            if algorithm.is_mobileye:
                threshold_index = algorithm.order_by_priority(
                    ready_tasks_order, algorithm.decide_attribute
                )

            unmatched_tasks = set()
            task_index = (
                threshold_index if random.random() >= algorithm.priority_rate else 0
            )
            task = ready_tasks[task_index]

            while len(ready_tasks) > 0:
                match_found = False
                for processor in self.processors:
                    if processor.type == task.processor_type and processor.idle:
                        # work on the task
                        processor.work_on_task(task)
                        task.end_time = current_time + task.duration

                        # update processor lists
                        working_processors.append(processor)
                        idle_processors.remove(processor)

                        # update task lists
                        current_tasks.put((task.end_time, task))

                        # a task can only run on one processor
                        match_found = True
                        break

                if not match_found:
                    unmatched_tasks.add(task)
                ready_tasks.remove(task)

                # remove from

                if len(ready_tasks) == 0:
                    break

                rand_value = random.random() if self.algorithm.is_mobileye else 0
                task = ready_tasks[0]
                if rand_value < algorithm.priority_rate and threshold_index > 0:
                    threshold_index -= 1
                else:
                    if len(ready_tasks) == threshold_index:
                        threshold_index = 0
                    task = ready_tasks[threshold_index]

            return list(unmatched_tasks)

        # init - assign all the tasks you can
        ready_tasks = match_ready_tasks(0, ready_tasks)

        # main loop
        while len(self.tasks) > 0:
            # pop the first task to finish
            current_time, done_task = current_tasks.get()
            self.total_time += done_task.duration
            self.final_end_time = done_task.end_time

            # free the processor and update in-degrees
            processor = done_task.processed_by
            processor.task_finished(ready_tasks)

            # add to time line
            if illustration:
                self.timeLineIlustartor.add_to_timeline(
                    processor, done_task, current_time - done_task.duration
                )

            # update working/idle processors
            working_processors.remove(processor)
            idle_processors.append(processor)

            self.tasks.remove(done_task)

            ready_tasks = match_ready_tasks(current_time, ready_tasks)

        return self.total_time, self.final_end_time

    def find_critical_path(self):
        # perform topological sort to get the tasks in order
        sorted_tasks = self._topological_sort()

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

    def show_illustration(self):
        self.timeLineIlustartor.show()

    def set_critical_path(self, critical_path):
        self.timeLineIlustartor.set_critical_path(critical_path)

    # helper function for find_critical_path
    def _topological_sort(self):
        stack = []
        visited = set()

        def dfs(task):
            if task in visited:
                return
            visited.add(task)
            for dependency in task.blocked_by:
                dfs(dependency)
            stack.append(task)

        for task in self.tasks:
            dfs(task)

        # Reverse the stack to get the correct topological order
        return stack

    def __str__(self):
        return (
            f"{self.algorithm.__class__.__qualname__} End Time: {self.final_end_time}\n"
        )


def run_sim_once(
    algorithm: Algorithm,
    file_path: str,
    illustration=False,
    offline=False,
    is_mobileye=False,
    priority_threshold=-1,
    priority_rate=-1,
):
    sim = Sim()
    sim.read_data(file_path)

    critical_path = sim.find_critical_path()
    critical_path = [task.name for task in critical_path]

    sim.start(
        algorithm(
            sim.tasks,
            sim.processors,
            sim.tasks,
            offline,
            is_mobileye,
            priority_threshold,
            priority_rate,
        ),
        illustration=illustration,
    )

    if illustration:
        sim.set_critical_path(critical_path)
        sim.show_illustration()

    return sim


def run_sim_all(
    algorithm: Algorithm,
    folder_path: str,
    output_file: str,
    illustration=False,
    offline=False,
    is_mobileye=False,
    priority_threshold=-1,
    priority_rate=-1,
):
    total_end_time = 0
    count = 0
    for filename in os.listdir(folder_path):
        sim = run_sim_once(
            algorithm,
            f"{folder_path}/{filename}",
            illustration=illustration,
            offline=offline,
            is_mobileye=is_mobileye,
            priority_threshold=priority_threshold,
            priority_rate=priority_rate,
        )
        print(f"done with {filename}")
        total_end_time += sim.final_end_time
        count += 1

    average_end_time = total_end_time / count

    print(f"Average End Time For {algorithm.__qualname__}: {average_end_time}")

    write_results(is_mobileye, priority_rate, priority_threshold)

    with open(output_file, "a") as file:
        file.write(
            f"Average End Time For {algorithm.__qualname__}: {average_end_time}\n"
        )

    return average_end_time


# writes the results to an excel spreadsheet
def write_results(
    output_file:str , algorithm: Algorithm, average_end_time: int, is_mobileye: bool, priority_rate: float, priority_threshold: float
):
    workbook: Workbook = openpyxl.load_workbook(output_file)

    sheet = workbook[algorithm.__qualname__]
    if sheet is None:
        sheet = workbook.create_sheet(algorithm.__qualname__)

    # rows = priority thresholds
    # columns = priority rates
    # cell = average end time for a certain threshold and rate
    # if threshold and rate are -1 that means the algorithm is non-mobileye
    sheet["A2"] = -1
    sheet["B"]
    # if (not is_mobileye):
    pass


def main():
    # output_file = "Results.txt"
    # run_sim_all(MaxRuntimeFirst, "Parser/Data/parsed", output_file, offline=False)

    # print(
    #     run_sim_once(
    #         FromCriticalPath,
    #         "Parser/Data/parsed/gsf.000390.prof.json",
    #         illustration=True,
    #         offline=True,
    #     )
    # )
    # print(
    #     run_sim_once(
    #         MinRuntimeFirst,
    #         "Parser/Data/parsed/gsf.000390.prof.json",
    #         illustration=False,
    #     )
    # )
    # print(
    #     run_sim_once(
    #         OutDegreesFirst, "Parser/Data/parsed/gsf.000390.prof.json", illustration=False
    #     )
    # )
    print(
        run_sim_once(
            MaxRuntimeFirst,
            "Parser/Data/parsed/gsf.000390.prof.json",
            illustration=False,
            is_mobileye=True,
            priority_threshold=23984732848326487,
            priority_rate=0.5,
        )
    )

    # run_sim_all(MinRuntimeFirst, "Parser/Data/parsed", output_file)

    # print(
    #     run_sim_once(
    #         OutDegreesFirst,
    #         "Parser/Data/parsed/gsf.000390.prof.json",
    #         illustration=False,
    #     )
    # )


if __name__ == "__main__":
    main()
