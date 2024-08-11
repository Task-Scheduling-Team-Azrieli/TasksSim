import numpy as np
from typing import List, TYPE_CHECKING
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

if TYPE_CHECKING:
    from Processor import Processor
    from Task import Task


class TimeLineIlustartion:
    def __init__(self, processors):
        self.timeLines = {}
        for processor in processors:
            self.timeLines.update({processor.name: []})

        self.start_time = 0
        self.end_time = 100  # Default end time, adjust as needed

        self.critical_path = None

    def add_to_timeline(self, processor, task, start_time):
        self.timeLines[processor.name].append(
            (task.name, start_time, start_time + task.duration)
        )

    def show(self):
        self.showTimelines()

    def set_critical_path(self, critical_path):
        self.critical_path = critical_path

    def showTimelines(self):
        fig, ax = plt.subplots(figsize=(10, len(self.timeLines) * 2))
        plt.subplots_adjust(bottom=0.25)

        # Generate a color map with enough colors for all tasks
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.timeLines)))

        for i, (processor, timeline) in enumerate(self.timeLines.items(), 1):
            # Calculate y-coordinate for the current timeline
            y = len(self.timeLines) - i

            for j, (task_name, start_time, end_time) in enumerate(timeline):
                # Plot a rectangle for each task with a different color if within time range
                if (
                    self.start_time <= start_time <= self.end_time
                    or self.start_time <= end_time <= self.end_time
                ):

                    color = colors[j % len(colors)]
                    edge_color = "#000000"
                    # color critical path with black
                    if task_name in self.critical_path:
                        color = "black"
                        edge_color = "red"

                    plt.fill_betweenx(
                        [y - 0.4, y + 0.4],
                        max(start_time, self.start_time),
                        min(end_time, self.end_time),
                        color=color,
                        alpha=0.5,
                        edgecolor=edge_color,
                    )
                    # Add text for the task name
                    # plt.text((max(start_time, self.start_time) + min(end_time, self.end_time)) / 2, y, task_name, ha='center', va='center')

            # Set y-ticks and y-tick labels
            plt.yticks([y], [processor])

        ax_start = plt.axes([0.1, 0.1, 0.65, 0.03])
        ax_end = plt.axes([0.1, 0.05, 0.65, 0.03])

        val_max = max(
            [
                end_time
                for _, timeline in self.timeLines.items()
                for _, _, end_time in timeline
            ]
        )

        slider_start = Slider(
            ax_start,
            "Start Time",
            valmin=0,
            valmax=val_max,
            valinit=0,
        )
        slider_end = Slider(
            ax_end,
            "End Time",
            valmin=0,
            valmax=val_max,
            valinit=val_max,
        )

        def update(val):
            self.start_time = slider_start.val
            self.end_time = slider_end.val
            ax.clear()
            for i, (processor, timeline) in enumerate(self.timeLines.items(), 1):
                y = len(self.timeLines) - i
                for j, (task_name, start_time, end_time) in enumerate(timeline):
                    if (
                        self.start_time <= start_time <= self.end_time
                        or self.start_time <= end_time <= self.end_time
                    ):
                        color = colors[j % len(colors)]
                        edge_color = "#000000"
                        # color critical path with black
                        if task_name in self.critical_path:
                            color = "black"
                            edge_color = "red"

                        ax.fill_betweenx(
                            [y - 0.4, y + 0.4],
                            max(start_time, self.start_time),
                            min(end_time, self.end_time),
                            color=color,
                            alpha=0.5,
                            edgecolor=edge_color,
                        )
                        # ax.text((max(start_time, self.start_time) + min(end_time, self.end_time)) / 2, y, task_name, ha='center', va='center')
                plt.yticks([y], [processor])
            fig.canvas.draw_idle()

        slider_end.set_val(val_max)
        update(val_max)

        slider_start.on_changed(update)
        slider_end.on_changed(update)

        plt.show()
