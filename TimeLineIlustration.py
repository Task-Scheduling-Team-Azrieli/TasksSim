import numpy as np
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
        self.showTimelines(self.timeLines)    
        
        
    def showTimelines(self, timeLines):
        if len(timeLines) >= 7:
            for tl in split_dict(timeLines, len(timeLines)//7 + 1):
                self.showTimelines(tl)
            return
        
        plt.figure(figsize=(10, len(timeLines) * 2))  # Adjust figure size based on number of timelines
            
        # Generate a color map with enough colors for all tasks
        colors = plt.cm.tab10(np.linspace(0, 1, len(timeLines)))

        for i, (processor, timeline) in enumerate(timeLines.items(), 1):
            plt.subplot(len(timeLines), 1, i)
            #plt.title(f'Timeline for {processor}')
            #plt.xlabel('Time')
            #plt.ylabel('Tasks')

            # Calculate y-coordinate for the current timeline
            y = len(timeLines) - i

            for j, (task_name, start_time, end_time) in enumerate(timeline):
                # Plot a rectangle for each task with a different color
                plt.fill_betweenx([y - 0.4, y + 0.4], start_time, end_time, color=colors[j % len(colors)], alpha=0.5)
                # Add text for the task name
                plt.text((start_time + end_time) / 2, y, task_name[0:0], ha='center', va='center')

            # Set y-ticks and y-tick labels
            plt.yticks([y], [processor])

        plt.tight_layout()
        plt.show()
        

def split_dict(original_dict, n):
    sub_dicts = [{} for _ in range(n)]
    keys = list(original_dict.keys())
    num_keys = len(keys)
    for i, key in enumerate(keys):
        sub_dicts[i % n][key] = original_dict[key]
    return sub_dicts