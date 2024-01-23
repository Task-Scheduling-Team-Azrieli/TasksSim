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


class TasksSim:
    def __init__(self):
        # setup window
        self.window = tkinter.Tk()
        self.window.geometry("1200x800")

        # tasks and processors list/databases
        self.task_list: List["Task"] = []
        self.processors_list: List["Processor"] = []
        self.processor_types_list: List["int"] = []

        # TESTING
        two = Task("1", 3, "2", [], [])
        one = Task("2", 3, "1", [], [])
        one_two = Task("12", 3, "1", [], [one, two])
        two.blocking.append(one_two)
        one.blocking.append(one_two)

        three = Task("3", 3, "1", [], [])
        five = Task("5", 3, "1", [], [])
        three_five = Task("35", 3, "1", [], [three, five])
        three.blocking.append(three_five)
        five.blocking.append(three_five)

        one_two_three_five = Task("1235", 3, "1", [], [three_five, one_two])
        three_five.blocking.append(one_two_three_five)
        one_two.blocking.append(one_two_three_five)

        self.task_list.append(one)
        self.task_list.append(two)
        self.task_list.append(three)
        self.task_list.append(five)
        self.task_list.append(one_two)
        self.task_list.append(three_five)
        self.task_list.append(one_two_three_five)

        # set algorithm
        self.algorithm = Greedy(
            task_list=self.task_list, processors_list=self.processors_list
        )

        # setup style
        self.style = ttk.Style()
        # dark theme (change "dark" to "light" if you hate your eyes)
        sv_ttk.set_theme("dark")
        self.style.configure("Thick.TSeparator", background="gray", padding=(20, 0))

        # setup main_frames
        self.main_frame = ttk.Frame(self.window)

        # grid columns for 2:1 ratio
        self.main_frame.rowconfigure(0, weight=5, minsize=1, uniform="row")
        self.main_frame.rowconfigure(1, weight=1, minsize=1, uniform="row")
        self.main_frame.rowconfigure(2, weight=8, minsize=1, uniform="row")

        self.main_frame.columnconfigure(0, minsize=1, weight=1, uniform="col")

        # ready, blocked and done queues/lists
        self.queues_frame = ttk.Frame(self.main_frame, border=4)
        self.queues_frame.columnconfigure(0, weight=1)
        self.queues_frame.columnconfigure(1, weight=1)
        self.queues_frame.columnconfigure(2, weight=1)

        self.queues_frame.rowconfigure(0, weight=10)
        self.queues_frame.rowconfigure(1, weight=1)
        self.display_queues(self.queues_frame)
        self.queues_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # start button
        start_button_frame = ttk.Frame(self.queues_frame)
        self.start_button = ttk.Button(
            start_button_frame,
            text="Start",
            command=lambda: self._start(self.algorithm),
        )
        start_button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.start_button.pack(fill="both", expand=True)

        # add task button
        self.add_task_button = ttk.Button(
            self.queues_frame,
            text="Add Task",
            command=lambda: self._add_task_handler(self.window),
        )
        self.add_task_button.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)

        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.grid(row=2, column=0, pady=10, columnspan=2)

        # processors
        self.processors_frame = ttk.Frame(self.main_frame, border=4)
        self.canvas = tkinter.Canvas(self.processors_frame, background="black")
        self.canvas_is_packed = False
        self.display_processors()
        self.processors_frame.grid(row=2, column=0, sticky="nsew", columnspan=2)

        # add processor button
        self.add_processor_button = ttk.Button(
            self.queues_frame,
            text="Add Processor",
            command=lambda: self._add_processor_handler(self.window),
        )
        self.add_processor_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

    def main_loop(self):
        # start main loop
        self.main_frame.pack(expand=True, fill="both")
        self.window.mainloop()

    def display_processors(self):
        self.canvas.delete("all")

        def get_random_color(seed):
            random.seed(seed)
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            return color

        x_start = 10
        y_start = 40
        length = 40
        gap_x = 20
        gap_y = 50
        outline_width = 4
        for type_ind in range(len(self.processor_types_list)):
            count = 0
            rect_lengths_accumulator = 0
            for processor_ind in range(len(self.processors_list)):
                if (
                    self.processors_list[processor_ind].type
                    == self.processor_types_list[type_ind]
                ):
                    x = rect_lengths_accumulator + x_start + (length + gap_x) * (count)
                    y = y_start + (length + gap_y) * type_ind
                    text_id = self.canvas.create_text(
                        x + length / 2,
                        y + length / 2,
                        text=self.processors_list[processor_ind].name,
                        anchor="center",
                        justify="center",
                        fill="white",
                    )
                    text_bbox = self.canvas.bbox(text_id)
                    text_width = text_bbox[2] - text_bbox[0]
                    rect_lengths_accumulator += length + text_width
                    # adjust text coordinates
                    self.canvas.coords(
                        text_id, x + length / 2 + text_width / 2 - 1, y + length / 2
                    )
                    # the processor's rectangle
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + length + text_width,
                        y + length,
                        outline=get_random_color(self.processor_types_list[type_ind]),
                        tags=(
                            self.processors_list[processor_ind].type
                            + ":"
                            + self.processors_list[processor_ind].name
                        ),
                        width=outline_width,
                    )
                    # the processor's name
                    self.canvas.create_text(
                        x + length / 2 + text_width / 2 - 1,
                        y - length / 2,
                        justify="center",
                        text="",
                        fill="green",
                        font=("Arial", 12),
                        tags=(
                            self.processors_list[processor_ind].type
                            + ":"
                            + self.processors_list[processor_ind].name
                            + "text"
                        ),
                    )
                    count += 1

        # only pack if
        if self.canvas_is_packed:
            self.canvas.update()
        else:
            self.canvas.pack(fill="both", expand=True)
            self.canvas_is_packed = True

    def display_queues(self, window):
        # Ready Queue
        ready_queue_frame = ttk.Frame(window)
        ready_queue_frame.columnconfigure(0, weight=1)
        ready_queue = []
        for task in self.task_list:
            if task.is_ready():
                ready_queue.append(task.name + ": " + str(task.duration))
        self._display_queue(ready_queue_frame, ready_queue, "Ready")

        ready_queue_frame.grid(column=0, row=0, sticky="nsew")

        # Blocked Queue
        blocked_queue_frame = ttk.Frame(window)
        blocked_queue_frame.columnconfigure(0, weight=1)
        blocked_queue = []
        for task in self.task_list:
            if task.is_blocked():
                blocked_queue.append(task.name + ": " + str(task.duration))
        self._display_queue(blocked_queue_frame, blocked_queue, "Blocked")
        blocked_queue_frame.grid(column=1, row=0, sticky="nsew")

        # Done Tasks
        done_queue_frame = ttk.Frame(window)
        done_queue_frame.columnconfigure(0, weight=1)
        done_queue = []
        for task in self.task_list:
            if task.done:
                done_queue.append(task.name + ": " + str(task.duration))
        self._display_queue(done_queue_frame, done_queue, "Done")
        done_queue_frame.grid(column=2, row=0, sticky="nsew")

    def _display_queue(self, window, queue, title):
        queue_title = ttk.Label(window, text=title, font=("Arial", 16))
        queue_list_frame = ttk.Frame(window)
        scrollbar = ttk.Scrollbar(queue_list_frame, orient="vertical")
        queue_list = tkinter.Listbox(
            queue_list_frame, height=10, yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=queue_list.yview)

        for task in queue:
            queue_list.insert(-1, task)

        if queue_list.winfo_ismapped():
            queue_list.update()
            scrollbar.update()
        else:
            queue_title.pack()
            scrollbar.pack(side=tkinter.RIGHT, fill="y")
            queue_list_frame.pack()
            queue_list.pack()

    def _add_task_handler(self, window):
        add_task_window = tkinter.Toplevel(window)
        add_task_window.geometry("500x500")
        add_task_window.grab_set()

        title = ttk.Label(add_task_window, text="Add a new task", font=("Arial", 16))
        title.pack()

        separator = ttk.Separator(
            add_task_window, orient="horizontal", style="Thick.TSeparator"
        )
        separator.pack(fill="x", pady=10)

        info_frame = ttk.Frame(add_task_window)
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=2)
        info_frame.pack(pady=60)

        # Name
        task_name_label = ttk.Label(info_frame, text="Name: ")
        task_name_label.grid(column=0, row=0, sticky="nsew")
        task_name_entry = ttk.Entry(info_frame)
        task_name_entry.grid(column=1, row=0, sticky="nsew")

        # Duration
        task_duration_label = ttk.Label(info_frame, text="Duration: ")

        def is_number(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        validate_cmd = add_task_window.register(is_number)
        task_duration_entry = ttk.Entry(
            info_frame,
            validate="key",
            validatecommand=(
                validate_cmd,
                "%P",
            ),
        )

        task_duration_label.grid(column=0, row=1, sticky="nsew", pady=10)
        task_duration_entry.grid(column=1, row=1, sticky="nsew", pady=10)

        # Processor type
        task_processor_label = ttk.Label(info_frame, text="Processor Type: ")
        task_processor_entry_value = tkinter.StringVar(info_frame)
        # a processor is presented as a string with the format type:name
        # so for example 1:p1 would be a processor of type 1 that's called p1
        options = self.processor_types_list
        task_processor_entry_value.set(options[0] if options else "None")
        task_processor_entry = ttk.OptionMenu(
            info_frame,
            task_processor_entry_value,
            options[0] if options else "None",
            *options,
        )
        task_processor_entry.grid(column=1, row=2, sticky="nsew")
        task_processor_label.grid(column=0, row=2, sticky="nsew")

        # Tasks that this new task will be blocking
        blocking_label = ttk.Label(info_frame, text="Blocking: ")
        self.blocking_selected_tasks = []
        blocking_button = ttk.Button(
            info_frame,
            text="Select",
            command=lambda: self._multiple_selection_window(
                add_task_window, self.task_list, True
            ),
        )
        blocking_label.grid(column=0, row=3, sticky="nsew", pady=10)
        blocking_button.grid(column=1, row=3, sticky="nsew", pady=10)

        # Tasks that this new task will be blocked by
        blocked_by_label = ttk.Label(info_frame, text="Blocked By: ")
        self.blocked_by_selected_tasks = []
        blocked_by_button = ttk.Button(
            info_frame,
            text="Select",
            command=lambda: self._multiple_selection_window(
                add_task_window, self.task_list, False
            ),
        )
        blocked_by_label.grid(column=0, row=4, sticky="nsew")
        blocked_by_button.grid(column=1, row=4, sticky="nsew")

        # Add task button
        add_task_button = ttk.Button(
            info_frame,
            text="Add Task",
            command=lambda: self._add_task(
                task_name_entry.get(),
                task_duration_entry.get(),
                task_processor_entry_value.get(),
                self.blocking_selected_tasks,
                self.blocked_by_selected_tasks,
                add_task_window,
            ),
        )
        add_task_button.grid(column=0, row=5, columnspan=2, pady=40, sticky="nsew")

        # TODO: finish logic to tasks (blocking blocked_by stuff), then canvas then win?

    def _add_processor_handler(self, window):
        add_processor_window = tkinter.Toplevel(window)
        add_processor_window.geometry("500x400")
        add_processor_window.grab_set()

        title = ttk.Label(
            add_processor_window, text="Add a new processor", font=("Arial", 16)
        )
        title.pack()

        separator = ttk.Separator(
            add_processor_window, orient="horizontal", style="Thick.TSeparator"
        )
        separator.pack(fill="x", pady=10)

        info_frame = ttk.Frame(add_processor_window)
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=2)
        info_frame.pack(pady=60)

        # Name
        processor_name_label = ttk.Label(info_frame, text="Name: ")
        processor_name_label.grid(column=0, row=0, sticky="nsew")
        processor_name_entry = ttk.Entry(info_frame)
        processor_name_entry.grid(column=1, row=0, sticky="nsew")

        # Type
        processor_type_label = ttk.Label(info_frame, text="Type: ")

        def is_number(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        validate_cmd = add_processor_window.register(is_number)
        processor_type_entry = ttk.Entry(
            info_frame,
            validate="key",
            validatecommand=(
                validate_cmd,
                "%P",
            ),
        )

        processor_type_label.grid(column=0, row=1, sticky="nsew", pady=10)
        processor_type_entry.grid(column=1, row=1, sticky="nsew", pady=10)

        # Add processor button

        add_processor_button = ttk.Button(
            info_frame,
            text="Add Processor",
            command=lambda: self._add_processor(
                processor_name_entry.get(),
                processor_type_entry.get(),
                add_processor_window,
            ),
        )
        add_processor_button.grid(column=0, row=2, columnspan=2, pady=40, sticky="nsew")

    def _add_processor(self, name: str, type: int, window: tkinter.Toplevel):
        new_processor = Processor(name, type)
        self.processors_list.append(new_processor)
        if type not in self.processor_types_list:
            self.processor_types_list.append(type)

        # update canvas and destroy add_process_window
        self.display_processors()
        window.destroy()

    def _add_task(
        self,
        name: str,
        duration: int,
        processor_type: int,
        blocking: List["Task"],
        blocked_by: List["Task"],
        window: tkinter.Toplevel,
    ):
        # add the new task
        blocking_list:List['Task'] = [self.task_list[task] for task in blocking]
        blocked_by_list:List['Task'] = [self.task_list[task] for task in blocked_by]
        new_task = Task(name, duration, processor_type, blocking_list, blocked_by_list)
        
        self.task_list.append(new_task)

        # update other tasks
        for task in blocking_list:
            task.blocked_by.append(new_task)
        for task in blocked_by_list:
            task.blocking.append(new_task)

        # refresh queues and destroy window
        self.display_queues(self.queues_frame)
        window.destroy()

    # a window that lets you select multiple tasks
    # to be either blocking or blocked by the new task you're creating
    def _multiple_selection_window(self, window, items: List["Task"], blocking):
        select_tasks_window = tkinter.Toplevel(window)
        select_tasks_window.grab_set()
        select_tasks_window.geometry("300x400")

        main_frame = ttk.Frame(select_tasks_window)
        multiple_choice_list = tkinter.Listbox(main_frame, selectmode="multiple")

        def on_select(event):
            if blocking:
                self.blocking_selected_tasks = multiple_choice_list.curselection()
            else:
                self.blocked_by_selected_tasks = multiple_choice_list.curselection()

        multiple_choice_list.bind("<<ListboxSelect>>", on_select)

        main_frame.pack(expand=True, fill="both")

        scrollbar = ttk.Scrollbar(multiple_choice_list, orient="vertical")
        multiple_choice_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=multiple_choice_list.yview)

        scrollbar.pack(fill="y", side="right")

        for item_index in range(len(items)):
            multiple_choice_list.insert(
                "end", items[item_index].name + ": " + str(items[item_index].duration)
            )

        multiple_choice_list.pack(expand=True, fill="both")

        # Call select_set after the Listbox is fully rendered
        for item_index in range(len(items)):
            if blocking and item_index in self.blocking_selected_tasks:
                multiple_choice_list.select_set(item_index)
            elif not blocking and item_index in self.blocked_by_selected_tasks:
                multiple_choice_list.select_set(item_index)

        select_tasks_window.mainloop()

    def _start(self, algorithm: Algorithm):
        def check_all_tasks_done():
            for task in self.task_list:
                if not task.done:
                    return False

            return True

        # callback for when a processor finishes its work on a task
        def work_on_task(processor: Processor, original_outline_color, callback):
            # update canvas
            tag = processor.type + ":" + processor.name
            self.canvas.itemconfig(tag + "text", text="")
            self.canvas.itemconfig(tag, outline=original_outline_color)
            self.canvas.update()

            processor.task_finished()

            # update queues
            self.display_queues(self.queues_frame)

            # call the callback to signal task completion
            callback()

        def process_next_task():
            algorithm.update_lists(
                task_list=self.task_list, processors_list=self.processors_list
            )

            task: Task = None
            processor: Processor = None
            task, processor = algorithm.decide()

            if task is None and processor is None:
                # no available tasks or processors
                return

            processor.work_on_task(task)

            # take care of processor outline color and text above processor
            original_outline_color = self.update_canvas(processor, task)

            # schedule the task completion callback after task duration
            self.canvas.after(
                ms=int(task.duration) * 1000,
                func=lambda: work_on_task(
                    processor, original_outline_color, process_next_task
                ),
            )

        all_tasks_done = check_all_tasks_done()
        while not all_tasks_done:
            process_next_task()
            all_tasks_done = check_all_tasks_done()
            self.canvas.update()

    def _start2(self,algorithm: Algorithm):
        pass

    def update_canvas(self, processor: Processor, task: Task):
        tag = processor.type + ":" + processor.name
        original_outline_color = self.canvas.itemcget(tag, "outline")
        self.canvas.itemconfig(tag, outline="green")
        self.canvas.itemconfig(tag + "text", text=task.name)

        # add a text with the name of the task above the processor
        self.canvas.update()
        self.display_queues(self.queues_frame)
        return original_outline_color


def main():
    # resolution
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

    sim = TasksSim()
    sim.main_loop()


if __name__ == "__main__":
    main()
