import sys
import json
import os
from src.ProcessTelemetryData.domain.TimeSeriesEqualizer.timeseries_equalizer import TimeseriesEqualizer


def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Error: python run_timeseries_equalizer.py <json_file_path>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    try:
        with open(json_file_path, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_file_path}'.")
        sys.exit(1)

    equalizer = TimeseriesEqualizer()
    modified_data = equalizer.equalize_timeseries(json_data)

    directory, filename = os.path.split(json_file_path)
    output_file_path = os.path.join(directory, filename.split('.')[0] + '_output.json')

    with open(output_file_path, "w") as outfile:
        json.dump(modified_data, outfile, indent=4)

    print(f"Output JSON saved as: {output_file_path}")

if __name__ == "__main__":
    main()