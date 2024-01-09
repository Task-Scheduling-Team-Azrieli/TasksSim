from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Task import Task
    from Processor import Processor


class Algorithm:
    def __init__(self, task_list: List["Task"], processors_list: List["Processor"]):
        self.processors_list = processors_list
        self.task_list = task_list

    def update_lists(self, processors_list, task_list):
        self.processors_list = processors_list
        self.task_list = task_list

    # returns a pair (task, processor) meaning the algorithm made a decision
    # that the task it chose will run on the processor it chose
    def decide(self):
        pass
