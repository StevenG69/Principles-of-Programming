# Written by Hongyin Zhou for COMP9021

# Defines a class Building that defines a few special methods,
# as well as the two methods:
# - go_to_floor_from_entry()
# - leave_floor_from_entry()
# and an atribute, number_created, to keep track of
# the number of Building objects that have been created.
#
# Also defines a function compare_occupancies() meant to take
# as arguments two Building objects.
#
# Building objects are created with statements of the form
# Building(height, entries) where height is a positive integer
# (possibly equal to 0) and entries is a nonempty string that
# denotes all access doors to the building, with at least
# one space within the string to separate entries.
# You can assume that height and entries are as expected.
#
# If building denotes a Building object, then
# building.go_to_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised,
# all with the same message, if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive.
# If the lift at that entry has to go down,
# then by how many floors it has to go down is printed out.
#
# If building denotes a Building object, then
# building.leave_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive, or
# - there are not at least nb_of_people on that floor.
# The same error message is used for the first 3 issues,
# and another error message is used for the last issue.
# If the lift at that entry has to go up or down, then
# by how many floors it has to go up or down is printed out.
#
# For the number of floors to go up or down, use
# "1 floor..." or "n floors..." for n > 1.

class BuildingError(Exception):
    pass

class Building:
    number_created = 0
    
    def __init__(self, height, entries):
        Building.number_created += 1
        self.entries = entries.split()
        self.height = height
        self.sector_floor_occupancy = {entry: {floor: 0 for floor in range(height + 1)} for entry in self.entries}
        self.current_floor = {entry: 0 for entry in self.entries}

    def pluralize(self, n):
        return "s" if n > 1 else ""

    def __repr__(self):
        return f"Building({self.height}, '{' '.join(self.entries)}')"

    def __str__(self):
        entry_list = ", ".join(sorted(self.entries))
        return f"Building with {self.height + 1} floor{self.pluralize(self.height + 1)} accessible from entries: {entry_list}"

    def go_to_floor_from_entry(self, floor, entry, nb_of_people):
        if floor < 0 or floor > self.height or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError('That makes no sense!')

        self.sector_floor_occupancy[entry][floor] += nb_of_people
        if self.current_floor[entry] > 0:
            print(f"Wait, lift has to go down {self.current_floor[entry]} floor{self.pluralize(self.current_floor[entry])}...")
        self.current_floor[entry] = floor

    def leave_floor_from_entry(self, floor, entry, nb_of_people):
        if floor < 0 or floor > self.height or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError('That makes no sense!')
        if self.sector_floor_occupancy[entry][floor] < nb_of_people:
            raise BuildingError("There aren't that many people on that floor!")

        self.sector_floor_occupancy[entry][floor] -= nb_of_people
        if self.current_floor[entry] < floor:
            print(f"Wait, lift has to go up {floor - self.current_floor[entry]} floor{self.pluralize(floor - self.current_floor[entry])}...")
        elif self.current_floor[entry] > floor:
            print(f"Wait, lift has to go down {self.current_floor[entry] - floor} floor{self.pluralize(self.current_floor[entry] - floor)}...")
        self.current_floor[entry] = 0

def compare_occupancies(building_1: Building, building_2: Building):
    total_occupancy_1 = sum(sum(floor_occupancy.values()) for floor_occupancy in building_1.sector_floor_occupancy.values())
    total_occupancy_2 = sum(sum(floor_occupancy.values()) for floor_occupancy in building_2.sector_floor_occupancy.values())

    if total_occupancy_1 > total_occupancy_2:
        print("There are more occupants in the first building.")
    elif total_occupancy_1 < total_occupancy_2:
        print("There are more occupants in the second building.")
    else:
        print("There is the same number of occupants in both buildings.")
