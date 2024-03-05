from Task import Task
from Processor import Processor
from Algorithms.Algorithm import Algorithm
from Algorithms.Greedy import Greedy
from Algorithms.GreedyHeuristics import OutDegreesFirst
from queue import PriorityQueue
from TimeLineIlustration import TimeLineIlustartion

from typing import List, Tuple, Dict
import json
import os


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
        print(file_path)
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
        if illustration:
            timeLineIlustartor = TimeLineIlustartion(self.processors)

        def match_ready_tasks(current_time):
            algorithm.update_lists(idle_processors, ready_tasks)
            ready_tasks_order = algorithm.decide()
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
                timeLineIlustartor.add_to_timeline(
                    processor, done_task, current_time - done_task.duration
                )

            # update working/idle processors
            working_processors.remove(processor)
            idle_processors.append(processor)

            self.tasks.remove(done_task)

            match_ready_tasks(current_time)

        if illustration:
            timeLineIlustartor.show()

        return self.total_time, self.final_end_time

    def __str__(self):
        return (
            f"{self.algorithm.__class__.__qualname__} End Time: {self.final_end_time}\n"
        )


def run_sim_once(
    algorithm: Algorithm, file_path: str, print_results=False, illustration=False
):
    sim = Sim()
    sim.read_data(file_path)
    sim.start(algorithm(sim.tasks, sim.processors), illustration=illustration)
    if print_results:
        sim.print_results()

    return sim


def run_sim_all(
    algorithm: Algorithm,
    folder_path: str,
    output_file: str,
    print_average=True,
    print_results=False,
    illustration=False,
):
    total_end_time = 0
    count = 0
    for filename in os.listdir(folder_path):
        sim = run_sim_once(
            algorithm,
            f"{folder_path}/{filename}",
            print_results=print_results,
            illustration=illustration,
        )
        total_end_time += sim.final_end_time
        count += 1

    average_end_time = total_end_time / count

    print(f"Average End Time For {algorithm.__qualname__}: {average_end_time}")

    with open("Results.txt", "a") as file:
        file.write(
            f"Average End Time For {algorithm.__qualname__}: {average_end_time}\n"
        )

    return average_end_time


def main():
    # output_file = "Results.txt"
    # print("OutDegreesFirst:")
    # run_sim_all(OutDegreesFirst, "Parser/Data/parsed", output_file)

    print(
        run_sim_once(
            Greedy, "Parser/Data/parsed/gsf.000390.prof.json", illustration=False
        )
    )
    print(
        run_sim_once(
            OutDegreesFirst,
            "Parser/Data/parsed/gsf.000390.prof.json",
            illustration=False,
        )
    )


if __name__ == "__main__":
    main()
