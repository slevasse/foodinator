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

    def sort_items_alphabetically(self, reverse=False):
        """Sort the item in alphabetical order based on their name. If the optional parameter 'reverse' is set to
        True, the list will be sorted in anti-alphabetical order."""
        self.library.sort(key=lambda x: x['Name'], reverse=reverse)

    def find(self, search_form: list) -> list:
        method_library = {"item_name": self.check_name,
                          "item_type": self.check_type,
                          "item_season": self.check_type}
        result = []
        test = False
        for item in self.library:
            for form in search_form:
                test = method_library[form['search_mode']](form['key'], item)
                if not test:
                    break  # if we get there, this recipe is not matching all criteria and we can move on
            if test:
                result.append(item)
        return result

    def check_name(self, key: str, item: dict):
        if re.search(key, item['Name'], re.IGNORECASE):
            return True
        return False

    def check_type(self, key: str, item: dict):
        if re.search(key, item['Type'], re.IGNORECASE):
            return True
        return False

    def check_season(self, key: str, item: dict):
        if re.search(key, item['Season'], re.IGNORECASE):
            return True
        return False

    def does_it_exist(self, food_item: dict):
        """Return True if the given food_item exit in the library."""
        for item in self.library:
            if food_item == item:
                return True
        return False
