import dataclasses
import csv
import re


@dataclasses.dataclass
class FoodLibrary:
    path: str = "food_item_library/all-foods.csv"
    library: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        # open the library and load it into the dict
        self.load_library()

    def __len__(self):
        return len(self.library)

    def __getitem__(self, key):
        return self.library[key]

    def load_library(self):
        self.library.clear()
        with open(self.path, newline='', encoding='utf-8-sig') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            reader = csv.DictReader(csv_file, dialect=dialect, delimiter=',')
            for row in reader:
                self.library.append(row)

    def find_matching_name(self, name: str, perfect_match: bool = False):
        """Return a list of dict with all food item with names matching the name given by the user."""
        temp = []
        for item in self.library:
            if perfect_match:
                if name.lower() == item['Name'].lower():
                    temp.append(item)
            else:
                if re.search(name, item['Name'], re.IGNORECASE):
                    temp.append(item)
        return temp

    def find_matching_type(self, food_type: str, perfect_match: bool = False):
        """Return a list of dict with all food item with type matching the type given by the user."""
        temp = []
        for item in self.library:
            if perfect_match:
                if food_type.lower() == item['Type'].lower():
                    temp.append(item)
            else:
                if re.search(food_type, item['Type'], re.IGNORECASE):
                    temp.append(item)
        return temp

    def find_matching_season(self, season: str, perfect_match: bool = False):
        """Return a list of dict with all food item with season matching the season given by the user."""
        temp = []
        for item in self.library:
            if perfect_match:
                if season.lower() == item['Season'].lower():
                    temp.append(item)
            else:
                if re.search(season, item['Season'], re.IGNORECASE):
                    temp.append(item)
        return temp

    def does_it_exist(self, food_item: dict):
        """Return True if the given food_item exit in the library."""
        for item in self.library:
            if food_item == item:
                return True
        return False
