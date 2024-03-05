import re
from typing import List
import json
import os


class Task:
    def __init__(self, name, duration, priority, processor_type, blocking):
        self.name = name
        self.duration = duration
        self.processor_type = processor_type
        self.blocking = blocking
        self.priority = priority


class Processor:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Parser:
    PRIORITY_ZERO = 0
    PRIORITY_ONE = 1
    PRIORITY_BOTH = 2

    def __init__(self):
        self.tasks: List[Task] = []
        self.processors: List[Processor] = []
        self.processor_types: List[str] = []

    def read_prof(self, file_path: str):
        """reads a .prof file and stores all the information
          about tasks and processors as objects inside this class

        Args:
            file_path (str): full path to the .prof file to read
        """
        file = open(file_path, "r")
        for line in file.readlines():
            split = line.split("|")
            processor = self.extract_processor_info(split[1])

            # add only unique processors
            processor_exists = False
            for p in self.processors:
                if p.name == processor.name and p.type == processor.type:
                    processor_exists = True
                    break

            if not processor_exists:
                self.processors.append(processor)

            # add task
            task = Task(
                split[0],
                float(split[2]),
                int(split[3]),
                processor.type,
                self.extract_blocking_tasks(split[-1]),
            )
            self.tasks.append(task)

        file.close()

    def to_json(self, file_path: str, priority: int):
        """extracts all the tasks and processors
        info from objects in this class to a json file

        Args:
            file_path (str): full path to the output file (including .json at the end)
            priority (int): tasks priority, whether to include just priority 0, just 1 or 2=both (leave it on both for stability)
        """
        # create dictionary data
        data = {"Tasks": {}, "Processors": []}

        # tasks
        if priority == self.PRIORITY_BOTH:
            tasks = self.tasks
        else:
            tasks = [t for t in self.tasks if t.priority == priority]

        for task in tasks:
            data["Tasks"][task.name] = {}
            data["Tasks"][task.name]["duration"] = task.duration
            data["Tasks"][task.name]["processor_type"] = task.processor_type
            data["Tasks"][task.name]["blocking"] = task.blocking
            data["Tasks"][task.name]["priority"] = task.priority

        # processors
        for processor in self.processors:
            data["Processors"].append(f"{processor.name}:{processor.type}")

        # dump dictionary to json file
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    def extract_processor_info(self, text: str) -> Processor:
        """helper function for read_prof, reads the processor name and type and extracts to an object

        Args:
            text (str): text to extract the information from

        Returns:
            Processor: the processor object with the info extracted to it
        """
        match = re.match(r"\('(\w+)', (\d+)\)", text)
        processor_type = match.group(1)
        processor_name = match.group(2)

        # add unique processor types
        if processor_type not in self.processor_types:
            self.processor_types.append(processor_type)

        return Processor(
            f"{processor_type}{processor_name}",
            self.processor_types.index(processor_type),
        )

    def extract_blocking_tasks(self, text:str):
        """helper function for read_prof, extracts all the tasks
        the current one we're reading is blocking, and returns all the matches

        Args:
            text (str): the text to search the tasks in

        Returns:
            List[str]: list of all the task names
        """
        pattern = re.compile(r"'(.*?)'")
        matches = pattern.findall(text)
        return matches


def main():
    folder_path = "Parser/Data"
    for filename in os.listdir(f"{folder_path}/gsf-profs"):
        parser = Parser()
        parser.read_prof(f"{folder_path}/gsf-profs/{filename}")
        parser.to_json(f"{folder_path}/parsed/{filename}.json", Parser.PRIORITY_BOTH)


if __name__ == "__main__":
    main()
