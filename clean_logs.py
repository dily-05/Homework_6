import csv

INPUT_FILE = "environmental_raw.txt"
OUTPUT_FILE = "clean_logs.csv"

def celsius_converter(f_temp):
    celsius = (float(f_temp) - 32) * 5 / 9
    return round(celsius, 2)

def parse_and_clean(line):
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 5:
        return None
    
    timestamp, station_id, temp, humidity, status = parts
    if not timestamp or not station_id:
        return None

    if status != "ACTIVE":
        return None

    try:
        temp_f = float(temp)
        hum = float(humidity)
    except ValueError:
        return None

    return [timestamp, station_id, temp_f, hum]

def main():
    skipped = 0

    with open(INPUT_FILE, "r") as infile, \
         open(OUTPUT_FILE, "w", newline="") as outfile:

        writer = csv.writer(outfile)
        writer.writerow(["Timestamp", "StationID", "Temp_C", "Humidity_%"])

        for line in infile:
            record = parse_and_clean(line)

            if record is None:
                skipped += 1
                continue

            timestamp, station_id, temp_f, hum = record
            writer.writerow([timestamp, station_id, celsius_converter(temp_f), hum])

    print(f"Done. Corrupted/skipped lines: {skipped}")

if __name__ == "__main__":
    main()       