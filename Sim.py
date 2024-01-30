from typing import List, Tuple
from Task import Task
from Processor import Processor
from Algorithm import Algorithm
from queue import PriorityQueue

import json


class Sim:
    def __init__(self):
        self.tasks: List["Task"] = []
        self.processors: List["Processor"] = []

    def read_data(self):
        input_file = open("input.json")
        data = json.load(input_file)

        tasks_json = data["Tasks"]
        processors_json = data["Processors"]

        # to connect a task name to its object, improves efficiency
        # when adding in and out degrees
        temp = {}

        # create all tasks
        for task_name in tasks_json:
            task_info = tasks_json[task_name]
            task = Task(
                task_name,
                task_info["duration"],
                task_info["processor_type"],
                [],
                [],
            )
            self.tasks.append(task)
            temp[task_name] = task

        # add in and out degrees to the tasks
        for task_name in tasks_json:
            task_info = tasks_json[task_name]
            blocking = [
                temp[task_name_blocking] for task_name_blocking in task_info["blocking"]
            ]
            temp[task_name].blocking = blocking
            # TODO: continue here

        for task in self.tasks:
            print(task.blocking)

    def start(self, algorithm: Algorithm):
        total_time = 0
        working_processors = []
        idle_processors: List["Processor"] = self.processors_list.copy()

        current_tasks: PriorityQueue[Tuple[int, Task]] = PriorityQueue()
        ready_tasks = [task for task in self.tasks if task.is_ready()]

        def match_ready_tasks():
            for task in ready_tasks_order:
                for processor in idle_processors:
                    if processor.type == task.processor_type:
                        # work on the task
                        processor.work_on_task(task)

                        # update processor lists
                        working_processors.append(processor)
                        idle_processors.remove(processor)

                        # update task lists
                        current_tasks.put((task.duration, task))
                        ready_tasks.remove(task)

        # init - assign all the tasks you can
        algorithm.update_lists(self.processors, ready_tasks)
        ready_tasks_order = algorithm.decide()
        match_ready_tasks()

        # main loop
        while len(self.tasks) > 0:
            # pop the first task to finish
            duration, done_task = current_tasks.get()
            total_time += duration

            # free the processor and update in-degrees
            processor = done_task.processed_by
            processor.task_finished()

            # update working/idle processors
            working_processors.remove(processor)
            idle_processors.append(processor)

            self.tasks.remove(done_task)

            match_ready_tasks()

    # temporary, maybe remove later
    def print_results(self):
        for processor in self.processors:
            print(processor.name + ":\t")
            for task in processor.work_order:
                print(task.name + "\t")
            print("\n")


def main():
    sim = Sim()
    sim.read_data()


if __name__ == "__main__":
    main()
