from typing import List


class Task:
    def __init__(self, priority, poggers):
        self.priority = priority
        self.runtime = poggers

    def __repr__(self):
        return f"Task(priority={self.priority} poggers={self.runtime})"


# Sample tasks
tasks = [
    Task(1, 2),
    Task(0, 3),
    Task(1, 1),
    Task(0, 8),
    Task(1, 5),
]


# Your complex sorting function
def complex_sort(tasks: List["Task"]):
    # Your complex sorting logic here
    # This function should return a sorted list of tasks
    # For simplicity, let's just reverse the list here
    return sorted(tasks, key=lambda task: task.runtime)


# Sorting function
def custom_sort(tasks):
    return sorted(tasks, key=lambda task: task.priority)


# Sort the tasks using your complex sorting logic
sorted_tasks = complex_sort(tasks)

# Sort the tasks again by priority
sorted_tasks = custom_sort(sorted_tasks)

# Print the sorted tasks
for task in sorted_tasks:
    print(task)
