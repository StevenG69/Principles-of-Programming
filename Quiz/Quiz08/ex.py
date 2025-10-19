class BuildingError(Exception):
    pass

class Building:
    number_created = 0

    def __init__(self, height, entries):
        Building.number_created += 1
        self.entries = entries.split()
        self.height = height
        # Initialize occupancy dictionary by sector and floor
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
        # Validate input
        if floor < 0 or floor > self.height or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError('That makes no sense!')

        # Update occupancy for specific sector and floor
        self.sector_floor_occupancy[entry][floor] += nb_of_people
        
        # Determine and print lift movement if necessary
        if self.current_floor[entry] > 0:
            print(f"Wait, lift has to go down {self.current_floor[entry]} floor{self.pluralize(self.current_floor[entry])}...")
        # Update the current floor position for the entry
        self.current_floor[entry] = floor

    def leave_floor_from_entry(self, floor, entry, nb_of_people):
        # Validate input
        if floor < 0 or floor > self.height or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError('That makes no sense!')
        
        # Check if enough people are present in the specified sector and floor
        if self.sector_floor_occupancy[entry][floor] < nb_of_people:
            raise BuildingError("There aren't that many people on that floor!")

        # Update occupancy for specific sector and floor
        self.sector_floor_occupancy[entry][floor] -= nb_of_people

        # Determine and print lift movement if necessary
        if self.current_floor[entry] < floor:
            print(f"Wait, lift has to go up {floor - self.current_floor[entry]} floor{self.pluralize(floor - self.current_floor[entry])}...")
        elif self.current_floor[entry] > floor:
            print(f"Wait, lift has to go down {self.current_floor[entry] - floor} floor{self.pluralize(self.current_floor[entry] - floor)}...")

        # Reset the lift to entry level (or another floor, depending on the desired functionality)
        self.current_floor[entry] = 0

def compare_occupancies(building_1: Building, building_2: Building):
    # Calculate total occupancy by summing up all sector-floor combinations
    total_occupancy_1 = sum(sum(floor_occupancy.values()) for floor_occupancy in building_1.sector_floor_occupancy.values())
    total_occupancy_2 = sum(sum(floor_occupancy.values()) for floor_occupancy in building_2.sector_floor_occupancy.values())

    if total_occupancy_1 > total_occupancy_2:
        print("There are more occupants in the first building.")
    elif total_occupancy_1 < total_occupancy_2:
        print("There are more occupants in the second building.")
    else:
        print("There is the same number of occupants in both buildings.")


## TEST CASES ##        
the_horizons = Building(10, 'A B C D')
the_horizons
print(the_horizons)
print(Building.number_created)
print(the_horizons.sector_floor_occupancy)
print(the_horizons.current_floor)

the_spike = Building(37, '1')
the_spike
print(the_spike)
print(Building.number_created)
print(the_spike.sector_floor_occupancy)
print(the_spike.current_floor)

the_seaside = Building(6, 'A B Z')
the_seaside
print(the_seaside)
print(Building.number_created)
print(the_seaside.sector_floor_occupancy)
print(the_seaside.current_floor)


the_horizons.go_to_floor_from_entry(0, 'B', 4)
compare_occupancies(the_horizons, the_spike)
#There are more occupants in the first building.
the_spike.go_to_floor_from_entry(17, '1', 4)
compare_occupancies(the_horizons, the_spike)
#There is the same number of occupants in both buildings.
the_spike.leave_floor_from_entry(17, '1', 3)
the_horizons.leave_floor_from_entry(0, 'B', 1)
the_horizons.leave_floor_from_entry(0, 'B', 1)
the_horizons.leave_floor_from_entry(0, 'B', 1)
compare_occupancies(the_horizons, the_spike)
#There is the same number of occupants in both buildings.
the_horizons.leave_floor_from_entry(0, 'B', 1)
compare_occupancies(the_horizons, the_spike)
#There are more occupants in the second building.
the_seaside.go_to_floor_from_entry(3, 'B', 1)
the_seaside.go_to_floor_from_entry(3, 'B', 1)
#Wait, lift has to go down 3 floors...
the_seaside.go_to_floor_from_entry(3, 'B', 1)
#Wait, lift has to go down 3 floors...
the_seaside.go_to_floor_from_entry(3, 'B', 1)
#Wait, lift has to go down 3 floors...
the_seaside.leave_floor_from_entry(3, 'B', 2)
the_seaside.leave_floor_from_entry(3, 'B', 2)
#Wait, lift has to go up 3 floors...
the_seaside.go_to_floor_from_entry(4, 'A', 10)
the_seaside.go_to_floor_from_entry(5, 'A', 10)
#Wait, lift has to go down 4 floors...
the_seaside.go_to_floor_from_entry(2, 'A', 10)
#Wait, lift has to go down 5 floors...
the_seaside.leave_floor_from_entry(4, 'A', 2)
#Wait, lift has to go up 2 floors...
the_seaside.go_to_floor_from_entry(1, 'A', 10)
the_seaside.leave_floor_from_entry(5, 'A', 2)
#Wait, lift has to go up 4 floors...
the_seaside.go_to_floor_from_entry(5, 'A', 10)
the_seaside.leave_floor_from_entry(2, 'A', 2)
#Wait, lift has to go down 3 floors...