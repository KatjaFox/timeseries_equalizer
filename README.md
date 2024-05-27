# The class containing the timeseuence equalizer logic is in:
/src/ProcessTelemetryData/domain/TimeSeriesEqualizer/timesequence_equalizer.py

# To find the required output.json to provided input.json check the root directory: 
output.json


# To start the unittests run:
> python -m unittest discover tests

# To run the timeseries equalizer in the command line:
> python run_timeseries_equalizer.py "path/to/input.json"

the output file will be saved in the same plaxe as input with *_output.json in the end

# To run a local flask server:
> pip install -r requirements.txt
> 
> python run_server.py

# To upload json file and get the equalized result through the API:
send a post request to localhost:5000/process-data with the json 


# To access OpenAPi documentation with Swagger go to:
http://localhost:5000/apidocs/

# To access the API documentation for /process-data and and get the equalized result:
# copy paste json as data param in body
http://localhost:5000/apidocs/#/Telemetry/post_process_data
