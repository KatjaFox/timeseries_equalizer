from typing import List, TypedDict
from collections import Counter
from datetime import datetime, timedelta


class TimeseriesEntry(TypedDict):
    timestamp: int | datetime
    value: float


class GranularityOperationsDict(TypedDict):
    turbine: str
    power_unit: str
    timeseries: List[TimeseriesEntry]


class TimeseriesEqualizer:
    """
    A class for equalizing timeseries data.

    Methods:
    equalize_timeseries(granularity_operations_input: GranularityOperationsDict) -> GranularityOperationsDict:
        Equalizes the input timeseries data by resampling to regular 30 min intervals.

    """

    def equalize_timeseries(self, granularity_operations_input: GranularityOperationsDict) -> GranularityOperationsDict:
        """
        Equalizes the input timeseries data by resampling to regular 30 min intervals.

        Args:
        granularity_operations_input (GranularityOperationsDict): The input data json containing timeseries to be equalized.

        Returns:
        GranularityOperationsDict: The equalized timeseries data in json.
        """

        self._validate_input(granularity_operations_input)
        self._validate_unique_timestamps(granularity_operations_input)
        granularity_operations_output_dict = granularity_operations_input

        timeseries = self._remove_last_entry(granularity_operations_input.get("timeseries", []))

        granularity_operations_output_dict["timeseries"] = self._resample_timeseries_data(timeseries=timeseries)

        return granularity_operations_output_dict

    def _resample_timeseries_data(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        """
        Resamples the timeseries data to regular intervals of 30 minutes using time-weighted average.

        Args:
        timeseries (List[TimeseriesEntry]): The input timeseries data.

        Returns:
        List[TimeseriesEntry]: The resampled timeseries data.
        """
        if len(timeseries) > 1:
            minute_interval = 30
            delta = timedelta(minute_interval)
            datetime_timeseries: List[TimeseriesEntry] = self._convert_timestamp_to_datetime(timeseries=timeseries)
            first_time = self._get_first_rounded_datetime(datetime_timeseries=datetime_timeseries)
            last_time = self._get_last_rounded_datetime(datetime_timeseries=datetime_timeseries)

            num_intervals = int((last_time - first_time) / timedelta(minutes=30)) + 1
            # Create an array with 30-minute intervals using list comprehension
            intervals = [{"time": first_time + timedelta(minutes=30 * i), "weighted_average": 0.00} for i in
                         range(num_intervals)]

            current_interval_index = 0
            weighted_sum = 0
            total_duration = 0
            weighted_average = 0
            resampled_output_new = []

            if len(intervals) == 0:
                return []
            for i, entry in enumerate(datetime_timeseries):
                if intervals[current_interval_index]["time"] <= entry["timestamp"] and (
                        current_interval_index + 1 >= len(intervals) or entry["timestamp"] <
                        intervals[current_interval_index + 1]["time"]):
                    if i + 1 >= len(datetime_timeseries) or i + 1 < len(
                            datetime_timeseries) and current_interval_index + 1 < len(intervals) and \
                            datetime_timeseries[i + 1]["timestamp"] >= intervals[current_interval_index + 1]["time"]:
                        duration = (intervals[current_interval_index]["time"] + timedelta(minutes=30) - entry[
                            "timestamp"]).total_seconds()
                    else:
                        duration = (datetime_timeseries[i + 1]["timestamp"] -
                                    entry["timestamp"]).total_seconds()
                    weighted_sum += entry["value"] * duration
                    total_duration += duration
                    weighted_average = weighted_sum / total_duration
                    intervals[current_interval_index]["weighted_average"] = 0 if total_duration == 0 \
                        else weighted_average

                    if i + 1 < len(datetime_timeseries) and current_interval_index + 1 < len(intervals) and \
                            datetime_timeseries[i + 1]["timestamp"] >= intervals[current_interval_index + 1]["time"]:
                        weighted_sum = 0
                        total_duration = 0
                        previous_index = current_interval_index
                        if i + 1 >= len(datetime_timeseries) - 1:
                            current_interval_index = len(intervals) - 1
                        else:
                            current_interval_index = next((idx - 1 for idx, interval in
                                                           enumerate(intervals[current_interval_index + 1:],
                                                                     start=current_interval_index + 1)
                                                           if
                                                           interval["time"] > datetime_timeseries[i + 1]["timestamp"]),
                                                          current_interval_index + 1)
                        intervals[previous_index:current_interval_index] = [
                            {**interval, "weighted_average": weighted_average}
                            for interval in intervals[previous_index:current_interval_index]
                        ]

            resampled_output_new = [
                {"timestamp": int(interval["time"].timestamp() * 1000), "value": interval["weighted_average"]}
                for interval in intervals
            ]
            return resampled_output_new
        return []

    def _remove_last_entry(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        if timeseries and timeseries[-1]["value"] is None:
            return timeseries[0:-1]
        return timeseries

    def _convert_timestamp_to_datetime(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        datetime_timeseries = []
        for entry in timeseries:
            new_entry = datetime.fromtimestamp(entry.get("timestamp") / 1000)
            datetime_timeseries.append({"timestamp": new_entry, "value": entry.get("value")})
        return datetime_timeseries

    def _get_first_rounded_datetime(self, datetime_timeseries: List[TimeseriesEntry]) -> datetime:
        return self._round_up([entry["timestamp"] for entry in datetime_timeseries][0])

    def _get_last_rounded_datetime(self, datetime_timeseries: List[TimeseriesEntry]) -> datetime:
        return self._round_down(datetime_timeseries[-1]["timestamp"])

    def _round_up(self, dt: datetime, delta: timedelta = timedelta(minutes=30)) -> datetime:
        return dt + (datetime.min - dt) % delta

    def _round_down(self, dt: datetime, delta: timedelta = timedelta(minutes=30)) -> datetime:
        secs = delta.total_seconds()
        return datetime.fromtimestamp(dt.timestamp() - dt.timestamp() % secs)

    def _validate_unique_timestamps(self, granularity_operations_input: GranularityOperationsDict):
        """
        Validates that the timestamps in the timeseries data are unique.

        Args:
        granularity_operations_input (GranularityOperationsDict): The input data containing timeseries to be validated.

        Raises:
        ValueError: If duplicate timestamps are found in the timeseries data.
        """
        timestamp_counts = Counter(
            entry.get("timestamp") for entry in granularity_operations_input.get("timeseries", []))
        duplicates = [timestamp for timestamp, count in timestamp_counts.items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate timestamps found in timeseries data: {duplicates}")

    def _validate_input(self, granularity_operations_input: GranularityOperationsDict):
        """
        Validates the format of the input data.

        Args:
        granularity_operations_input (GranularityOperationsDict): The input data to be validated.

        Raises:
        TypeError: If the input data does not meet the required format.
        """
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
