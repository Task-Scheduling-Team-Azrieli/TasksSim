from openpyxl import Workbook
import openpyxl
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

# for writing the results to excel
FILE_TO_INDEX = {}


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

        # read processors
        for processor_str in processors_json:
            processor_name = processor_str.split(":")[0]
            processor_type = int(processor_str.split(":")[1])
            processor = Processor(processor_name, processor_type)

            if processor not in self.processors:
                self.processors.append(processor)

        self.timeLineIlustartor = TimeLineIlustartion(self.processors)

    def start(
        self,
        algorithm: Algorithm,
        illustration=False,
        threshold: int = -1,
    ):
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

        def match_ready_tasks(current_time):
            algorithm.update_lists(idle_processors, ready_tasks, self.tasks)
            if algorithm.offline:
                ready_tasks_order = algorithm.decide(order)
            else:
                ready_tasks_order = algorithm.decide(threshold)
            for task in ready_tasks_order:
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
                        ready_tasks.remove(task)

                        # a task can only run on one processor
                        break

        # init - assign all the tasks you can
        match_ready_tasks(0)

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

            match_ready_tasks(current_time)

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
    is_mobileye: bool = False,
    output_file: str = "Results.xlsx",
):
    sim = Sim()
    sim.read_data(file_path)

    critical_path = sim.find_critical_path()
    critical_path = [task.name for task in critical_path]

    if is_mobileye:
        algorithm_instance = algorithm(
            sim.tasks, sim.processors, sim.tasks, offline, is_mobileye
        )

        thresholds = algorithm_instance.find_thresholds(3)

        init_sheet(output_file, algorithm=algorithm, thresholds=thresholds)

        # get Greedy runtime for this file
        sim2 = Sim()
        sim2.read_data(file_path)
        greedy_runtime, _ = sim2.start(
            Greedy(sim.tasks, sim.processors, sim.tasks, offline)
        )

        for threshold in thresholds:
            # run sim and get total time
            total_time, _ = sim.start(
                algorithm_instance, illustration=False, threshold=threshold
            )
            # write to excel
            write_results(
                output_file,
                input_file=file_path,
                algorithm=algorithm,
                threshold=threshold,
                runtime=total_time,
                greedy_time=greedy_runtime,
            )

    else:

        sim.start(
            algorithm(sim.tasks, sim.processors, sim.tasks, offline, is_mobileye),
            illustration=illustration,
        )

    if illustration:
        sim.set_critical_path(critical_path)
        sim.show_illustration()

    return sim

    # writes the results to an excel spreadsheet


def write_results(
    output_file: str,
    input_file: str,
    algorithm: Algorithm,
    threshold: float,
    runtime: float,
    greedy_time: float,
):
    input_file = input_file.split("/")[-1]
    workbook: Workbook = openpyxl.load_workbook(output_file)

    if algorithm.__qualname__ in workbook.sheetnames:
        sheet = workbook[algorithm.__qualname__]
    else:
        raise Exception("init the sheet before write result (use init_sheet())")

    def same_value(value1, value2):
        return abs(value1 - value2) < 0.001 * value1

    # self.clear_sheet(sheet)
    def find_threshold_column(threshold):
        i = 2
        while i < 12:
            if same_value(sheet.cell(1, i).value, threshold):
                return i
            i += 1
        return -1

    sheet.cell(
        row=FILE_TO_INDEX[input_file], column=find_threshold_column(threshold)
    ).value = (runtime / greedy_time)
    workbook.save(output_file)


def init_dictionary():
    global FILE_TO_INDEX
    files = os.listdir("Parser/Data/parsed")
    files_dict = {file.split("/")[-1]: i + 2 for i, file in enumerate(files)}
    FILE_TO_INDEX = files_dict


def init_sheet(output_file: str, algorithm: Algorithm, thresholds: list["float"]):
    if FILE_TO_INDEX == {}:
        init_dictionary()
    workbook: Workbook = openpyxl.load_workbook(output_file)
    sheet = None
    if algorithm.__qualname__ in workbook.sheetnames:
        sheet = workbook[algorithm.__qualname__]
        clear_sheet(sheet)
    else:
        workbook.create_sheet(algorithm.__qualname__)
        sheet = workbook[algorithm.__qualname__]
    for i, threshold in enumerate(thresholds):
        sheet.cell(1, i + 2).value = threshold
    for key in FILE_TO_INDEX.keys():
        sheet.cell(FILE_TO_INDEX[key], 1).value = key

    workbook.save(output_file)


def clear_sheet(sheet):
    for row in sheet.iter_rows():
        for cell in row:
            cell.value = None
            cell.style = "Normal"


def run_sim_all(
    algorithm: Algorithm,
    folder_path: str,
    output_file: str,
    illustration=False,
    offline=False,
    is_mobileye: bool = False,
):
    total_end_time = 0
    count = 0
    for filename in os.listdir(folder_path):
        if is_mobileye:
            run_sim_once(
                algorithm, f"{folder_path}/{filename}", False, offline, is_mobileye
            )
            print(f"done with {filename}")
        else:
            sim = run_sim_once(
                algorithm,
                f"{folder_path}/{filename}",
                illustration=illustration,
                offline=offline,
            )
            print(f"done with {filename}")
            total_end_time += sim.final_end_time

        count += 1

    average_end_time = total_end_time / count

    print(f"Average End Time For {algorithm.__qualname__}: {average_end_time}")

    with open(output_file, "a") as file:
        file.write(
            f"Average End Time For {algorithm.__qualname__}: {average_end_time}\n"
        )

    return average_end_time


def main():
    output_file = "Results.xlsx"
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
    #         Greedy, "Parser/Data/parsed/gsf.000390.prof.json", illustration=False
    #     )
    # )
    print(
        run_sim_once(
            MinRuntimeFirst,
            "Parser/Data/parsed/gsf.000390.prof.json",
            illustration=False,
            is_mobileye=True,
            output_file="Results.xlsx",
        )
    )
    print(
        run_sim_once(
            MinRuntimeFirst,
            "Parser/Data/parsed/gsf.000391.prof.json",
            illustration=False,
            is_mobileye=True,
            output_file="Results.xlsx",
        )
    )
    # print(
    #     run_sim_once(
    #         MaxRuntimeFirst, "Parser/Data/parsed/gsf.000390.prof.json", illustration=False
    #     )
    # )

    # run_sim_all(MinRuntimeFirst, "Parser/Data/parsed", output_file, is_mobileye=True)
    # run_sim_all(MaxRuntimeFirst, "Parser/Data/parsed", output_file, is_mobileye=True)
    # run_sim_all(OutDegreesFirst, "Parser/Data/parsed", output_file, is_mobileye=True)
    # run_sim_all(OutDegreesLast, "Parser/Data/parsed", output_file, is_mobileye=True)

    # print(
    #     run_sim_once(
    #         OutDegreesFirst,
    #         "Parser/Data/parsed/gsf.000390.prof.json",
    #         illustration=False,
    #     )
    # )


if __name__ == "__main__":
    main()
