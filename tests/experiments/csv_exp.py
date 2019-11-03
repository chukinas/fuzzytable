import csv
import names as names_generator
from pathlib import Path
from tests.conftest import fields_to_records


person_count = 3
names_fields = {
    'first_name': [
        names_generator.get_first_name()
        for i in range(person_count)
    ],
    'last_name': [
        names_generator.get_last_name()
        for i in range(person_count)
    ]
}
names_records = fields_to_records(names_fields)


names_path = Path('names.csv')
names_path.touch()
with open(names_path, "w", newline='') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames='first_name last_name'.split())
    csvwriter.writeheader()
    csvwriter.writerows(names_records)


with open(names_path) as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        string = repr(row)
        print(string)
        for cell in row:
            print(cell)

names_path.unlink()
