import hashlib
import os
import time

global baseline
baseline = "baseline.txt"


def main():
    print("File Integrity Monitor")
    directory = input("Enter Directory Name: ")
    while True:
        print("A) Establish Baseline")
        print("B) Start Monitor")
        print("C) Close Monitor")
        answer = input("Select Option: ")
        if answer == "A" or answer == "a":
            establish(directory)
            print("Baseline Established")
        elif answer == "B" or answer == "b":
            start(directory)
        elif answer == "C" or answer == "c":
            break
        else:
            print("invalid input")


# Creates the baseline.txt file and dictionary to compare against during the monitoring
def establish(directory):
    try:
        os.remove(baseline)  # removes old baseline file
    except Exception:
        print("Couldn't Find An Old baseline.txt File")
    hasher = hashlib.sha3_512()
    for file in os.scandir(directory):  # scans through the given directory
        if file.is_file():  # only includes files in the baseline
            with open(file, "r") as f:
                lines = f.read().splitlines()  # read file contents into list
                for l in lines:
                    hasher.update(l.encode("utf-8"))  # adds each list item into the hasher and converts string to bytes
                    with open(baseline, "a") as b:
                        b.write("{} -> {}\n".format(file.name,
                                                    hasher.digest()))  # writes file name and hash into baseline.txt
                    b.close()
            f.close()


def start(directory):
    if os.path.exists(baseline):  # makes sure that baseline has been established
        baseline_dic = read_baseline()  # reads baseline file into a dictionary to be compared with easily
        while True:
            hasher = hashlib.sha3_512()
            for file in os.scandir(directory):  # scans through the given directory
                if file.is_file():  # only includes files in the baseline
                    with open(file, "r") as f:
                        lines = f.read().splitlines()  # read file contents into list
                        for l in lines:
                            hasher.update(
                                l.encode("utf-8"))  # adds each list item into the hasher and converts string to bytes
                    f.close()
                    hashcode = hasher.digest()
                    if file.name not in baseline_dic.keys():  # makes sure that file isn't a new file
                        print("{}'s name has been changed or not established in baseline.".format(file.name))
                    elif baseline_dic[file.name] == str(hashcode):  # checks if new hash is equal to baseline
                        print("{} integrity intact.".format(file.name))
                    else:  # reports that the hash is different and therefore file has been changed
                        print("{} HAS BEEN COMPROMISED!".format(file.name))
                time.sleep(3)  # to slow down the loop
    else:
        print("Baseline has not been established.")


def read_baseline():
    baseline_dic = {}  # clears dictionary
    with open(baseline, "r") as b:
        line = b.read().splitlines()  # reads baseline content into list
        for i in line:
            x = i.split(" -> ")  # splits strings by personal dividing indicator
            baseline_dic[x[0]] = x[1]  # keys = file name, values = hashcode
    b.close()
    return baseline_dic  # returns dictionary to start method


main()
