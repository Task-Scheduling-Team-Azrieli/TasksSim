from typing import List
from Task import Task
import random
from Algorithm import Algorithm
from Processor import Processor


class Greedy(Algorithm):
    def __init__(self, task_list: List["Task"], processors_list: List["Processor"]):
        super().__init__(task_list, processors_list)

    # returns a pair (task, processor) that the algorithm decided upon
    def init(self):
        ready_tasks: List["Task"] = [
            task for task in self.task_list if task.is_ready()
        ]
        random.shuffle(ready_tasks)

        # randomly pick a task, and search for a processor to run it
        for task in ready_tasks:
            for processor in self.processors_list:
                if processor.type == task.processor_type and processor.idle:
                    #TODO: run task on processor
                    pass

    def decide(self):
        # TODO: will work only on ready tasks
        pass

