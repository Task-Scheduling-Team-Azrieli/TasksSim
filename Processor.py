from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Task import Task


class Processor:
    def __init__(self, name: str, processor_type: int):
        self.name = name
        self.type = processor_type
        self.idle = True
        self.current_task = None
        self.work_order: List["Task"] = []

    def work_on_task(self, task: "Task"):
        self.idle = False
        self.work_order.append(task)
        self.current_task = task
        self.current_task.processed_by = self
        self.current_task.being_processed = True

    def task_finished(self, ready_tasks):
        self.current_task.done = True
        self.current_task.processed_by = None

        # remove current task from all blocked_by lists of the tasks its blocking
        # and update ready_tasks
        for task in self.current_task.blocking:
            task.blocked_by.remove(self.current_task)
            if len(task.blocked_by) == 0:
                ready_tasks.append(task)

        self.idle = True
        self.current_task = None
