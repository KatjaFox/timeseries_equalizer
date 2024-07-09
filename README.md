# Timeseries Equalizer

## Project Overview
This project involves creating a timeseries equalizer that transforms an irregular timeseries into an equally spaced timeseries. The primary use case is for resampling and unifying telemetry data from customer systems.

## Input Format
- The input is a JSON file containing power telemetry data.
- Each entry in the JSON file consists of a timestamp and a corresponding value.

## Output Format
- The output is in JSON format and represents a resampled timeseries.
- The timeseries is equally spaced with datapoints at every 30-minute interval (e.g., 12:00, 12:30, 13:00, etc.).

## Granularity Mapping
- The timestamps in the input file are irregular and should be mapped to full granularities (30-minute intervals).
- Each datapoint is valid until the next datapoint.
- If a timestamp falls between two intervals, the time-weighted average of the surrounding data points is used.

## Data Integrity
- The input file should not contain multiple values with the same timestamp. If such a case is encountered, it should be rejected.
- Only the last value in the series is allowed to be "null" or "NaN".

## How the Program Works

### Reading Input
- The program reads the JSON input file containing the irregular timeseries data.

### Generating Full Granularities
- The program generates timestamps for every 30 minutes within the given range of timestamps.

### Transforming Timeseries
- For each generated timestamp, the program uses the time-weighted average of the surrounding data points.

### Output Generation
- The program saves the transformed timeseries to an output JSON file.

## Usage

### The class containing the timeseuence equalizer logic is in:
/src/ProcessTelemetryData/domain/TimeSeriesEqualizer/timesequence_equalizer.py

### To find the required output.json to provided input.json check the root directory: 
output.json


### To start the unittests run:
> python -m unittest discover tests

### To run the timeseries equalizer in the command line:
> python run_timeseries_equalizer.py "path/to/input.json"

the output file will be saved in the same plaxe as input with *_output.json in the end

### To run a local flask server:
> pip install -r requirements.txt
> 
> python run_server.py

### To upload json file and get the equalized result through the API:
send a post request to localhost:5000/process-data with the json 


### To access OpenAPi documentation with Swagger go to:
http://localhost:5000/apidocs/

### To access the API documentation for /process-data and and get the equalized result:
### copy paste json as data param in body
http://localhost:5000/apidocs/#/Telemetry/post_process_data
