import re
from typing import List
import json

PRIORITY_ZERO = 0
PRIORITY_ONE = 1


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
    def __init__(self):
        self.tasks: List[Task] = []
        self.processors: List[Processor] = []
        self.processor_types: List[str] = []

    def parse_prof(self, filename):
        file = open(filename, "r")
        for line in file.readlines():
            split = line.split("|")
            processor = self.extract_processor_info(split[1])

            # add unique processor types
            if processor.type not in self.processor_types:
                self.processor_types.append(processor.type)

            # add only unique processors
            processor_exists = False
            for p in self.processors:
                if p.name == processor.name and p.type == processor.type:
                    processor_exists = True
                    break

            if not processor_exists:
                processor.name = f"{processor.type}{processor.name}"
                processor.type = self.processor_types.index(processor.type)
                self.processors.append(processor)

            task = Task(
                split[0],
                split[2],
                int(split[3]),
                processor.type,
                self.extract_blocking_tasks(split[-1]),
            )
            self.tasks.append(task)

        file.close()

    def to_json(self, filename, priority):
        # create dictionary data
        data = {"Tasks": {}, "Processors": {}}
        for task in [t for t in self.tasks if t.priority == priority]:
            data["Tasks"][task.name] = {}
            data["Tasks"][task.name]["duration"] = task.duration
            data["Tasks"][task.name]["processor_type"] = task.processor_type
            data["Tasks"][task.name]["blocking"] = task.blocking

        # dump dictionary to json file
        with open(filename, "w") as json_file:
            json.dump(data, json_file)

    def extract_processor_info(self, text):
        match = re.match(r"\('(\w+)', (\d+)\)", text)
        processor_type = match.group(1)
        processor_name = match.group(2)

        return Processor(processor_name, processor_type)

    def extract_blocking_tasks(self, text):
        pattern = re.compile(r"'(.*?)'")
        matches = pattern.findall(text)
        return matches


def main():
    parser = Parser()
    parser.parse_prof("Parser/Data/gsf.-00001.prof")
    parser.to_json("input.json", PRIORITY_ZERO)


if __name__ == "__main__":
    main()
