from typing import List, TypedDict
import json
from collections import Counter
from datetime import datetime,timedelta

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
        granularity_operations_output_dict = granularity_operations_input

        timeseries = self._remove_last_entry(granularity_operations_input.get("timeseries", []))

        granularity_operations_output_dict["timeseries"] = self._resample_timeseries_data(timeseries=timeseries)
        
        self._save_to_json(granularity_operations_output_dict)

        return granularity_operations_output_dict

    def _resample_timeseries_data(self, timeseries:List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        if len(timeseries) > 1:
            datetime_timeseries =self._convert_to_datetime(timeseries=timeseries)
            current_time = self._get_first_rounded_datetime(datetime_timeseries=datetime_timeseries)
            resampled_output = []

            while current_time <= datetime_timeseries[-1]["timestamp"]:
                next_time = current_time + timedelta(minutes=30)
                relevant_points_for_time_period = [entry for entry in datetime_timeseries if current_time <= entry["timestamp"] < next_time]

                if relevant_points_for_time_period:
                    weighted_sum = 0
                    total_duration = 0

                    for i in range(len(relevant_points_for_time_period) - 1):
                        duration = (relevant_points_for_time_period[i + 1]["timestamp"] - relevant_points_for_time_period[i]["timestamp"]).total_seconds()
                        weighted_sum += relevant_points_for_time_period[i]["value"] * duration
                        total_duration += duration

                    if relevant_points_for_time_period:
                        last_point_duration = (next_time - relevant_points_for_time_period[-1]["timestamp"]).total_seconds()
                        weighted_sum += relevant_points_for_time_period[-1]["value"] * last_point_duration
                        total_duration += last_point_duration

                    if total_duration > 0:
                        weighted_avg = weighted_sum / total_duration
                resampled_output.append({"timestamp": int(current_time.timestamp() * 1000), "value": weighted_avg})

                current_time = next_time

            return resampled_output
        return []
        
    def _remove_last_entry(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        if timeseries and timeseries[-1]["value"] is None:
            timeseries.pop()
        return timeseries
    
    def _convert_to_datetime(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        datetime_timeseries = []
        for entry in timeseries:
            new_entry = datetime.fromtimestamp(entry.get("timestamp")/1000)
            datetime_timeseries.append({"timestamp":new_entry, "value": entry.get("value")})
        return datetime_timeseries
    
    def _save_to_json(self, data: GranularityOperationsDict) -> None:
        file_path = "output.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    def _get_first_rounded_datetime(self, datetime_timeseries:List[TimeseriesEntry]) -> datetime:
        datetimes = [entry["timestamp"] for entry in datetime_timeseries]
        first_date = datetimes[0]
        rounded_first_date = self._round_up(first_date) 
        return rounded_first_date
    
    def _round_up(self, dt, delta=timedelta(minutes=30)) -> datetime:
        return dt + (datetime.min - dt) % delta

        
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
            

if __name__ == '__main__':
    inputTest = {
        "turbine": "Freudenau Turbine 2",
        "power_unit": "MW",
        "timeseries": [
            {
                "timestamp": 1586901600000,
                "value": 12
            },
            {
                "timestamp": 1586902200000,
                "value": 5.01
            },
            {
                "timestamp": 1586923200000,
                "value": 20.043
            },
            {
                "timestamp": 1586940600000,
                "value": 32.01
            },
            {
                "timestamp": 1586957400000,
                "value": 23.4
            },
            {
                "timestamp": 1586958000000,
                "value": 23.5
            },
            {
                "timestamp": 1586958600000,
                "value": 24.92
            },
            {
                "timestamp": 1586958720000,
                "value": 26.7
            },
            {
                "timestamp": 1586959080000,
                "value": 32.034
            },
            {
                "timestamp": 1586959200000,
                "value": 32.000001
            },
            {
                "timestamp": 1586964000000,
                "value": 29.95665
            },
            {
                "timestamp": 1586966400000,
                "value": 30.2
            },
            {
                "timestamp": 1586977200000,
                "value": 0.001
            },
            {
                "timestamp": 1586994600000,
                "value": -0.0002
            },
            {
                "timestamp": 1586996400000,
                "value": 0
            },
            {
                "timestamp": 1586998800000,
                "value": 2.0
            },
            {
                "timestamp": 1587002400000,
                "value": 2.5
            },
            {
                "timestamp": 1587006000000,
                "value": 3.3
            },
            {
                "timestamp": 1587009600000,
                "value": 4.4
            },
            {
                "timestamp": 1587013200000,
                "value": 5.5
            },
            {
                "timestamp": 1587016800000,
                "value": 6.6
            },
            {
                "timestamp": 1587020400000,
                "value": 7.7
            },
            {
                "timestamp": 1587056400000,
                "value": 0.0
            },
            {
                "timestamp": 1587074400000,
                "value": None
            }
        ]
    }
    
    equalizer = TimeseriesEqualizer()
    result = equalizer.equalize_timeseries(inputTest)