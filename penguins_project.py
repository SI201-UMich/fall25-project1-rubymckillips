# Name: Ruby McKillips
# UM ID: 41668989
# Email: rubymck@umich.edu
# Who I worked with: No one; utilized ChatGPT for assistance (see below)
# How I used AI: 

import os
os.chdir(os.path.dirname(__file__))

def read_penguins_data(filename):
    import csv
    infile = open(filename, "r")
    csv_file = csv.reader(infile)
    headers = next(csv_file)
    
    print("Variables (columns):", headers)
    
    data = []
    for row in csv_file:
        data.append(row)

    print("\nSample entry (first row):", data[0])

    print("\nNumber of rows:", len(data))

    infile.close()
    return data

# Part 3 calculation 1
def calculate_species_averages(data):
    """
    Calculates average flipper length and body mass for each species.
    """
    species_data = {}
    species_index = 0
    flipper_index = 4
    mass_index = 5

    for row in data:
        species = row[species_index]
        flipper = row[flipper_index]
        mass = row[mass_index]

        if flipper == "" or flipper == "NA" or mass == "" or mass == "NA":
            continue

        flipper = float(flipper)
        mass = float(mass)

        if species not in species_data:
            species_data[species] = {"flipper_total": 0, "mass_total": 0, "count": 0}

        species_data[species]["flipper_total"] += flipper
        species_data[species]["mass_total"] += mass
        species_data[species]["count"] += 1

    # calculate averages
    for species, values in species_data.items():
        avg_flipper = values["flipper_total"] / values["count"]
        avg_mass = values["mass_total"] / values["count"]
        print(f"{species}: average flipper = {avg_flipper:.2f} mm, average mass = {avg_mass:.2f} g")

# Part 3 calculation 2
def calculate_above_average_mass(data):
    """
    Calculates the percentage of penguins in each species
    whose body mass is above the average body mass for that species.
    """
    species_index = 1
    mass_index = 5

    species_data = {}
    for row in data:
        species = row[species_index]
        mass = row[mass_index]

        if mass == "" or mass == "NA":
            continue

        mass = float(mass)

        if species not in species_data:
            species_data[species] = {"mass_total": 0, "count": 0}

        species_data[species]["mass_total"] += mass
        species_data[species]["count"] += 1

    averages = {}
    for species, values in species_data.items():
        averages[species] = values["mass_total"] / values["count"]

    # Step 2: Count penguins above average
    above_average_counts = {species: 0 for species in averages}
    total_counts = {species: 0 for species in averages}

    for row in data:
        species = row[species_index]
        mass = row[mass_index]

        if mass == "" or mass == "NA" or species not in averages:
            continue

        mass = float(mass)
        total_counts[species] += 1

        if mass > averages[species]:
            above_average_counts[species] += 1

    print("\nPercentage of penguins above their species average mass:")
    for species in averages:
        if total_counts[species] == 0:
            continue
        percentage = (above_average_counts[species] / total_counts[species]) * 100
        print(f"{species}: {percentage:.2f}% above average body mass")




if __name__ == "__main__":
    data = read_penguins_data("penguins.csv")
    calculate_species_averages(data)
    calculate_above_average_mass(data)