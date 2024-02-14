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

            # Calculate y-coordinate for the current timeline
            y = len(self.timeLines) - i

            for task_name, start_time, end_time in timeline:
                # Plot a rectangle for each task
                plt.fill_betweenx([y - 0.4, y + 0.4], start_time, end_time, color='skyblue', alpha=0.5)
                # Add text for the task name
                plt.text((start_time + end_time) / 2, y, task_name, ha='center', va='center')

            # Set y-ticks and y-tick labels
            plt.yticks([y], [processor])

        plt.tight_layout()
        plt.show()