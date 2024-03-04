from typing import List, Tuple, Dict
from Task import Task
from Processor import Processor
from Algorithms.Algorithm import Algorithm
from Algorithms.Greedy import Greedy
from Algorithms.GreedyHeuristics import OutDegreesFirst
from queue import PriorityQueue
from TimeLineIlustration import TimeLineIlustartion

import json


class Sim:
    def __init__(self):
        self.tasks: List["Task"] = []
        self.processors: List["Processor"] = []

        self.total_time = 0
        self.final_end_time = 0

    def read_data(self):
        input_file = open("input.json")
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

    def start(self, algorithm: Algorithm):
        working_processors = []
        idle_processors: List["Processor"] = self.processors.copy()

        current_tasks: PriorityQueue[Tuple[int, Task]] = PriorityQueue()
        ready_tasks = [task for task in self.tasks if task.is_ready()]
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
            timeLineIlustartor.add_to_timeline(
                processor, done_task, current_time - done_task.duration
            )
            # update working/idle processors
            working_processors.remove(processor)
            idle_processors.append(processor)

            self.tasks.remove(done_task)

            match_ready_tasks(current_time)

        timeLineIlustartor.show()

        return self.total_time, self.final_end_time

    # temporary, maybe remove later
    def print_results(self):
        for processor in self.processors:
            task_index = 0
            print(f"{processor.name} type {processor.type}\t")
            for task in processor.work_order:
                print(
                    f"task #{task_index}"
                    + ":\t start time: "
                    + f"{task.end_time - task.duration}\t\t"
                    + f"duration: {task.duration}"
                )
                task_index += 1
            print("\n")

    def __str__(self):
        return f"Total Time: {self.total_time}\nEnd Time: {self.final_end_time}\n"


def run_sim(algorithm: Algorithm, print_results=False):
    sim = Sim()
    sim.read_data()
    sim.start(algorithm(sim.tasks, sim.processors))
    if print_results:
        sim.print_results()

    return sim


def main():
    print("Greedy:")
    print(run_sim(Greedy))
    print("Out degrees first:")
    print(run_sim(OutDegreesFirst))


if __name__ == "__main__":
    main()
