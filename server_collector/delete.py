import csv
import sys
if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Please provide the keywords of AP to delete.")
        exit
    keywords = sys.argv[1:]

with open("wireless_record.csv", "r") as f:
    data = list(csv.reader(f))

with open("wireless_record.csv", "w") as f:
    writer = csv.writer(f)
    for row in data:
        write_bool = True
        for keyword in keywords:
            if (keyword in row[2]):
                write_bool = False
        if write_bool:
            writer.writerow(row)  
