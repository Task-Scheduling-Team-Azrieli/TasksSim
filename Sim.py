import random
import threading
import tkinter
from tkinter import ttk
from typing import List, Tuple
import sv_ttk
from Greedy import Greedy
from Task import Task
from Processor import Processor
from Algorithm import Algorithm
import time
from queue import PriorityQueue


class Sim:
    def __init__(self):
        self.tasks: List["Task"] = []
        self.processors: List["Processor"] = []

    def read_data(self):
        pass

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
        for processor in self.processors_list:
            print(processor.name + ":\t")
            for task in processor.work_order:
                print(task.name + "\t")
            print("\n")


def main():
    sim = Sim()
    sim.read_data()
    sim.start()


if __name__ == "__main__":
    main()
