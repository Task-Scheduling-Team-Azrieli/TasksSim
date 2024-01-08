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

    def decide(self):
        pass
