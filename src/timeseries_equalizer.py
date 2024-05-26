from typing import Dict, List, TypedDict
import json
from collections import Counter

class TimeseriesEntry(TypedDict):
    timestamp: int
    value: float

class GranularityOperationsDict(TypedDict):
    turbine: str
    power_unit: str
    timeseries: List[TimeseriesEntry]

class TimeseriesEqualizer:
    def equalize_timeseries(self, granularity_operations_input: GranularityOperationsDict) -> GranularityOperationsDict:
        self._validate_input(granularity_operations_input)
        self._validate_unique_timestamps(granularity_operations_input)
        return None
        # TODO
        # The provided data is in json format and consists of 2 days of power telemetry of a turbine.
        # The timestamps are irregular and should be mapped to full granularities.
        # This code should be used as a core part of our backend to resample and unify telemetry coming from the customers systems.
        # The output timeseries should be equally time spaced and on full (half hourly) granularities, so there has to be a datapoint for every 30 minutes (full hours and half hours, e.g., 12:00, 12:30, 13:00,...)
        # The input is provided as JSON file: a turbine telemetry timeseries of power data. A combination of timestamp and value is a "datapoint".
        # The output should also be a power timeseries and can also be JSON
        # Each datapoint is valid until the next datapoint.
        # The last value can be null or NaN and only marks the end,
        #       its value is meaningless and should be ignored 
        # The input will not contain multiple values with the same timestamps (should be rejected if so)
        pass
    
    def _validate_unique_timestamps(self, granularity_operations_input: GranularityOperationsDict):
        timestamp_counts = Counter(entry.get("timestamp") for entry in granularity_operations_input.get("timeseries", []))
        duplicates = [timestamp for timestamp, count in timestamp_counts.items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate timestamps found in timeseries data: {duplicates}")

    def _validate_input(self, granularity_operations_input: GranularityOperationsDict):
        if not isinstance(granularity_operations_input.get("turbine"), str):
            raise TypeError("Turbine must be a string.")
        
        if not isinstance(granularity_operations_input.get("power_unit"), str):
            raise TypeError("Power unit must be a string.")
        
        if not isinstance(granularity_operations_input.get("timeseries"), list):
            raise TypeError("Timeseries must be a list.")

        for entry in granularity_operations_input.get("timeseries", []):
            if not isinstance(entry, dict):
                raise TypeError("Each timeseries entry must be a dictionary.")
                
            if not isinstance(entry.get("timestamp"), int):
                raise TypeError("Timestamp must be an integer.")
            
            if not isinstance(entry.get("value"), (float, int)) and entry.get("value") is not None:
                raise TypeError("Value must be a float or an integer or None.")