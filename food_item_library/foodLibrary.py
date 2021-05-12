import dataclasses
import csv

@dataclasses.dataclass
class FoodLibrary:
    path: str = "food_item_library/all-foods.csv"
    library: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        # open the library and load it into the dict
        with open(self.path, newline='',encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, dialect=dialect, delimiter=',')
            for row in reader:
                self.library.append(row)
