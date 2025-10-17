# Name: Ruby McKillips
# UM ID: 41668989
# Email: rubymck@umich.edu
# Collaborators: None; utilized ChatGPT for assistance (see below)
# How I used AI: code assistance, explanations, and adding os.chdir() for directory management

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
    species_index = 1
    flipper_index = 5
    mass_index = 6
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

    averages = {}
    for species, values in species_data.items():
        avg_flipper = values["flipper_total"] / values["count"]
        avg_mass = values["mass_total"] / values["count"]
        averages[species] = {"avg_flipper": avg_flipper, "avg_mass": avg_mass}
        print(f"{species}: average flipper = {avg_flipper:.2f} mm, average mass = {avg_mass:.2f} g")

    return averages
    

# Part 3 calculation 2
def calculate_above_average_mass(data, averages):
    """
    Calculates the percentage of penguins in each species
    whose body mass is above the average body mass for that species.
    """
    species_index = 1
    mass_index = 6

    above_average_counts = {species: 0 for species in averages}
    total_counts = {species: 0 for species in averages}

    for row in data:
        species = row[species_index]
        mass = row[mass_index]

        if mass == "" or mass == "NA" or species not in averages:
            continue

        mass = float(mass)
        total_counts[species] += 1

        if mass > averages[species]["avg_mass"]:
            above_average_counts[species] += 1

    percentages = {}
    print("\nPercentage of penguins above their species average mass:")
    for species in averages:
        if total_counts[species] == 0:
            continue
        percentage = (above_average_counts[species] / total_counts[species]) * 100
        percentages[species] = percentage
        print(f"{species}: {percentage:.2f}% above average body mass")

    return percentages


def write_results_to_file(filename, averages, percentages):
    """
    Writes the calculated averages and percentages to a text file.
    """
    with open(filename, "w") as outfile:
        outfile.write("Penguin Data Analysis Results\n")
        outfile.write("===============================\n\n")

        outfile.write("Average flipper length and body mass per species:\n")
        for species, values in averages.items():
            outfile.write(f"{species}: average flipper = {values['avg_flipper']:.2f} mm, "
                          f"average mass = {values['avg_mass']:.2f} g\n")

        outfile.write("\nPercentage of penguins above their species average body mass:\n")
        for species, percent in percentages.items():
            outfile.write(f"{species}: {percent:.2f}% above average body mass\n")

    print(f"\nResults written to {filename}")

sample_data = [
    ['1', 'Adelie', 'Torgersen', '39.1', '18.7', '181', '3750', 'male', '2007'],
    ['2', 'Adelie', 'Torgersen', '40.3', '18.0', '195', '3800', 'female', '2007'],
    ['3', 'Gentoo', 'Biscoe', '46.1', '13.2', '211', '4500', 'male', '2008'],
    ['4', 'Gentoo', 'Biscoe', '45.2', '14.8', '214', 'NA', 'female', '2008'],
    ['5', 'Chinstrap', 'Dream', '50.5', '19.7', '205', 'NA', 'male', '2009'],
    ['6', 'Chinstrap', 'Dream', '49.0', '19.5', '210', '3800', 'female', '2009']
]

def test_calculate_species_averages():
    print("\nRunning tests for calculate_species_averages()...")
    averages = calculate_species_averages(sample_data)

    # General test cases
    assert 3700 < averages['Adelie']['avg_mass'] < 3800, "Adelie avg mass seems off."
    assert 210 < averages['Gentoo']['avg_flipper'] < 215, "Gentoo avg flipper seems off."

    # Edge test cases 
    try:
        calculate_species_averages([['1', 'Adelie', 'Torgersen', '39.1', '18.7', 'NA', '3750', 'male', '2007']])
    except Exception:
        assert False, "Function failed on missing flipper data."

    new_data = sample_data + [['7', 'Unknown', 'IslandX', '40.0', '17.5', '180', '3500', 'female', '2007']]
    result = calculate_species_averages(new_data)
    assert 'Unknown' in result, "Function failed to include new species."

    assert 'Gentoo' in averages, "Gentoo species missing from averages."
    assert 'Chinstrap' in averages, "Chinstrap species missing from averages."
    assert len(averages) > 0, "Averages dictionary is empty."

    print("All tests for calculate_species_averages() passed!")

def test_calculate_above_average_mass():
    print("\nRunning tests for calculate_above_average_mass()...")
    averages = calculate_species_averages(sample_data)
    percentages = calculate_above_average_mass(sample_data, averages)

    # General test cases
    for p in percentages.values():
        assert 0 <= p <= 100, "Percentage out of range."

    assert 'Adelie' in percentages, "Adelie not found in percentage results."
    assert 'Gentoo' in percentages, "Gentoo missing despite partial NA data."

    # Edge test cases
    bad_data = [['1', 'Adelie', 'Torgersen', '39.1', '18.7', '181', 'NA', 'male', '2007']]
    try:
        calculate_above_average_mass(bad_data, averages)
    except Exception:
        assert False, "Function crashed with all NA mass values."

    empty_result = calculate_above_average_mass([], averages)
    assert isinstance(empty_result, dict), "Result should still be a dictionary."
    assert len(empty_result) == 0, "Empty dataset should produce empty percentages."
    assert len(percentages) > 0, "Percentages dictionary is empty."

    print("All tests for calculate_above_average_mass() passed!")


if __name__ == "__main__":
    data = read_penguins_data("penguins.csv")
    averages = calculate_species_averages(data)
    percentages = calculate_above_average_mass(data, averages)
    write_results_to_file("penguin_results.txt", averages, percentages)

    test_calculate_species_averages()
    test_calculate_above_average_mass()