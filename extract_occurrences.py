# Antony Kellermann 7/25/19
# Parses a CSV file generated from MDRF data (compiled with -io flag) and outputs a new CSV file with occurrence data.
# Usage: $ extract_occurences.py -d in.csv out.csv
# -d flag is optional and will delete occurrences in input file

import sys  # argv
import re   # regex

def get_occurrence_arr(filename):
    occurrence_arr = []
    with open(filename, "r") as file:
        data_pattern = re.compile("(\[L (\[([\w\d]+) ([\w\d\"\s]+)\])\s(\[([\w\d]+) ([\w\d\.]+)\])\])\s?")
        print("Reading input file...")
        lines = file.readlines()
        for line in lines:
            match = re.match("\$Occurrence ts:(\d+.\d+) ([\d\-:\.T]+) ([\w.]+) (\[L (.*)\])", line)
            if match:
                match_pairs = [["RunTime", match.group(1)], ["DateTime", match.group(2)], ["ServiceEnum", match.group(3)]]

                matches = data_pattern.findall(match.group(5))
                for match in matches:
                    match_pairs.append([match[3], match[6]])

                occurrence_arr.append(match_pairs)

    return occurrence_arr

def get_header_set(occurrence_arr):
    header_set = set()
    for pairs in occurrence_arr:
        for pair in pairs:
            header_set.add(pair[0])

    return header_set

def get_ordered_header_array(header_set):
    header_array = sorted(header_set)
    common_headers = ["DateTime", "RunTime", "ServiceEnum", "serviceName"]
    for i in range(0, len(common_headers)):
        idx = header_array.index(common_headers[i])
        header_array.insert(i, header_array.pop(idx))

    return header_array

def write_occurrences(filename, header_array, occurrence_arr):
    with open(filename, "w") as file:
        print("Writing output file...")
        file.write(','.join(str(s).replace("\"", "") for s in header_array) + '\n')
        for pairs in occurrence_arr:
            dic = dict.fromkeys(header_array, "")
            for pair in pairs:
                dic[pair[0]] = pair[1]

            file.write(','.join(dic[header] for header in header_array) + '\n')

def delete_occurrences(filename):
    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        for line in lines:
            if re.search("\$Occurrence", line) == None:
                file.write(line)

if __name__ == "__main__":
    argv_len = len(sys.argv)
    if argv_len <= 2 or argv_len >= 5:
        print("Usage: $ extract_occurrences.py [flags] in.csv out.csv")
        print("Optional flags: -d\t\tDeletes occurrences in input CSV")
        print("Example: $ extract_occurrences.py -d in.csv out.csv")
        exit(1);

    delete_flag = False
    if argv_len == 4:
        if sys.argv[1] == "-d":
            delete_flag = True
        else:
            print("Unknow flag: " + str(sys.argv[1]))
            exit(1)

    in_filename = str(sys.argv[1 + int(delete_flag)])
    out_filename = str(sys.argv[2 + int(delete_flag)])
    print(in_filename)
    print(out_filename)

    if in_filename.endswith(".csv") == False or out_filename.endswith(".csv") == False:
        print("You must specify filenames with format CSV.")
        exit(1)

    occurrences = get_occurrence_arr(in_filename)
    num_occurrences = len(occurrences)
    print("Found " + str(num_occurrences) + " occurrences.")
    if num_occurrences == 0:
        print("No occurrences were found. Make sure to convert the MDRF file with the -io flag to convert occurrences.")
        exit(0)

    header_set = get_header_set(occurrences)
    print("Found " + str(len(header_set)) + " unique data keys.")

    header_array = get_ordered_header_array(header_set)
    write_occurrences(out_filename, header_array, occurrences)

    if delete_flag:
        print("Deleting occurrences in input file")
        delete_occurrences(in_filename)

    print("Done")
