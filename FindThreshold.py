from Task import Task
from Sim import Sim

class FindThershold:
    def __init__(self, tasks: list["Task"]) -> None:
        self.tasks: list["Task"] = tasks

    def find_threshold(
        self, recurtion_depth: int, task_list: list["Task"], attribute: str
    ) -> list["float"]:
        n = len(task_list)
        if recurtion_depth == 0 or n <= 1:
            return []
        thresh_value = getattr(task_list[n // 2], attribute)
        return (
            [thresh_value]
            + self.find_threshold(recurtion_depth - 1, task_list[: n // 2], attribute)
            + self.find_threshold(recurtion_depth - 1, task_list[n // 2 :], attribute)
        )

    def check_find_threshold(self, attribute):
        min_val = getattr(self.tasks[0], attribute)
        max_val = getattr(self.tasks[-1], attribute)
        ranges = [min_val] + sorted(self.find_threshold(3, self.tasks, attribute)) + [max_val]
        
        res = {}
        for r in ranges:
            res[r] = 0
            
        for task in self.tasks:
            for i in range(1, len(ranges)):
                if ranges[i-1] <= getattr(task, attribute) <= ranges[i]:
                    res[ranges[i-1]] += 1
                    break
        return res
            
        


def main():
    sim = Sim()
    sim.read_data("Parser/Data/parsed/gsf.-00001.prof.json")
    th = FindThershold(sorted(sim.tasks, key=lambda x: x.duration))
    print(th.check_find_threshold("duration"))


if __name__ == "__main__":
    main()
