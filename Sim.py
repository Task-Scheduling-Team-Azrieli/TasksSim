import random
import threading
import tkinter
from tkinter import ttk
from typing import List
import sv_ttk
from Greedy import Greedy
from Task import Task
from Processor import Processor
from Algorithm import Algorithm
import time
from queue import PriorityQueue


class Sim:
    def __init__(self):
        self.task_list: List["Task"] = []
        self.processors_list: List["Processor"] = []

    def read_data(self):
        pass

    def start(self, algorithm: Algorithm):
        working_processors = []
        idle_processors = self.processors_list.copy()
        priority_queue = PriorityQueue()
        ready_tasks = []

        # init
        # assign tasks until you can't assign anymore
        algorithm.update_lists()
        task, processor = algorithm.decide()

        # main loop
        while len(self.task_list) > 0:
            pass

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
