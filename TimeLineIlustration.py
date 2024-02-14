from typing import List, TYPE_CHECKING
from matplotlib import pyplot as plt
if TYPE_CHECKING:
    from Processor import Processor
    from Task import Task

class TimeLineIlustartion:
    def __init__(self, processors):
        self.timeLines = {}
        for processor in processors:
            self.timeLines.update({processor.name : []})
    

    def add_to_timeline(self, processor, task, start_time):
        self.timeLines[processor.name].append((task.name, start_time, start_time+task.duration))
    
    def show(self):
        print(self.timeLines)
        plt.figure(figsize=(10, len(self.timeLines) * 2))  # Adjust figure size based on number of timelines

        for i, (processor, timeline) in enumerate(self.timeLines.items(), 1):
            plt.subplot(len(self.timeLines), 1, i)
            plt.title(f'Timeline for {processor}')
            plt.xlabel('Time')
            plt.ylabel('Tasks')

            for task_name, start_time, end_time in timeline:
                plt.plot([start_time, end_time], [task_name, task_name], marker='o')

        plt.tight_layout()
        plt.show()