import ParallelFileReader

import csv


exe_name_map = {}

def populate_exe_name_map():
    with open('name_map.csv', newline='') as csvfile:
        name_map_reader = csv.DictReader(csvfile, delimiter=';')
        for row in name_map_reader:
            exe_name_map[row["exe_name"]] = row["name"]

def get_name(line, previous_line):
    name = line.split(",")[1].strip().split(" ")[1].split(".")[0]
    if exe_name_map.get(name):
        name = exe_name_map[name]
    if previous_line.find("low") != -1:
        name = f"{name} Low settings"
    if previous_line.find("high") != -1:
        name = f"{name} High settings"
    if len(previous_line.split(" ")) > 1:
        name = "%s %s" % (name, previous_line.split(" ")[1])
    name = name.strip()
    return name


def get_fps(line):
    fps = line.split(":")[1].strip().split(" ")[0]
    fps = float(fps)
    fps = round(fps, 0)
    fps = int(fps)
    return fps


def get_data(filename):
    data = {}
    name = ""
    previous_line = ""
    with open(filename, 'r') as f:
        for line in f:
            if line.find("benchmark completed") != -1:
                name = get_name(line, previous_line)
                data[name] = [0]*3
            else:
                if line.find("Average framerate") != -1:
                    data[name][2] = get_fps(line)
                elif line.find("0.1% low framerate") != -1:
                    data[name][0] = get_fps(line)
                elif line.find("1% low framerate") != -1:
                    data[name][1] = get_fps(line)
            previous_line = line
    return data

def get_benchmark_data():
    populate_exe_name_map()
    dir = "benchmarks"
    results = ParallelFileReader.get_data_from_files(get_data, dir)
    files = ParallelFileReader.get_file_names(dir)
    data = {}
    x = 0
    for result in results:
        for key, value in result.items():
            value.insert(0, files[x].split("/")[1].split(".")[0])
            if data.get(key):
                data[key].append(value)
            else:
                data[key] = [value]
        x += 1
    return data

get_benchmark_data()