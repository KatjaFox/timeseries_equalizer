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

    def create_interval_array(self, first: datetime, last: datetime, minute_interval: int):
        num_intervals = int((last - first) / timedelta(minutes=minute_interval)) + 1
        return [{"timestamp": first + timedelta(minutes=minute_interval * i), "value": 0.00} for i in
                range(num_intervals)]

    def _resample_timeseries_data(self, timeseries: List[TimeseriesEntry]) -> List[TimeseriesEntry]:
        """
        Resamples the timeseries data to regular intervals of 30 minutes using time-weighted average.

        Args:
        timeseries (List[TimeseriesEntry]): The input timeseries data.

        Returns:
        List[TimeseriesEntry]: The resampled timeseries data.
        """

        minute_interval = 30
        datetime_timeseries: List[TimeseriesEntry] = self._convert_timestamp_to_datetime(timeseries=timeseries)
        first_time: datetime = self._get_first_rounded_datetime(datetime_timeseries=datetime_timeseries)
        last_time: datetime = self._get_last_rounded_datetime(datetime_timeseries=datetime_timeseries)
        intervals: [TimeseriesEntry] = self.create_interval_array(first_time, last_time, minute_interval)

        if len(timeseries) <= 1 or len(intervals) == 0:
            return []

        current_interval_index = 0
        weighted_sum = 0
        total_duration = 0
        interval_weighted_average = 0

        for i, entry in enumerate(datetime_timeseries):
            if self.entry_between_current_intervals(current_interval_index, entry, intervals):
                duration = self.calculate_duration(current_interval_index, datetime_timeseries, entry, i,
                                                                 intervals, weighted_sum)
                weighted_sum += self.calculate_time_weighted_sum(duration, entry)
                total_duration += duration
                interval_weighted_average = self.calculate_interval_weighted_average(total_duration, weighted_sum)
                intervals[current_interval_index]["value"] = interval_weighted_average

                if self.next_entry_exists_and_overflow(current_interval_index, datetime_timeseries, i, intervals):
                    weighted_sum = 0
                    total_duration = 0
                    previous_index = current_interval_index

                    current_interval_index = self.calculate_next_interval_index(current_interval_index,
                                                                                datetime_timeseries, i, intervals)
                    self._fill_overflowed_intervals(previous_index, current_interval_index, intervals,
                                                    interval_weighted_average)

        resampled_timeseries_output = [
            {"timestamp": int(interval["timestamp"].timestamp() * 1000), "value": interval["value"]}
            for interval in intervals
        ]
        return resampled_timeseries_output

    def calculate_next_interval_index(self, current_interval_index, datetime_timeseries, i, intervals):
        if i + 1 >= len(datetime_timeseries) - 1:
            current_interval_index = len(intervals) - 1
        else:
            current_interval_index = self._get_next_interval_index(current_interval_index,
                                                                   datetime_timeseries, i, intervals)
        return current_interval_index

    def calculate_time_weighted_sum(self, duration, entry):
        return entry["value"] * duration

    def calculate_duration(self, current_interval_index, datetime_timeseries, entry, i, intervals, weighted_sum):
        if not self.next_entry_exists(datetime_timeseries, i) or self.next_entry_overflow_next_interval(
                current_interval_index, datetime_timeseries, i, intervals):
            duration = (intervals[current_interval_index]["timestamp"] + timedelta(minutes=30) - entry[
                "timestamp"]).total_seconds()
        else:
            duration = (datetime_timeseries[i + 1]["timestamp"] -
                        entry["timestamp"]).total_seconds()
        return duration

    def calculate_interval_weighted_average(self, total_duration, weighted_sum):
        # weighted average based on duration of different data entries inside the interval (30 min)
        return 0 if total_duration == 0 else weighted_sum / total_duration

    def next_entry_exists_and_overflow(self, current_interval_index, datetime_timeseries, i, intervals):
        return self.next_entry_exists(datetime_timeseries, i) and self.next_entry_overflow_next_interval(
            current_interval_index, datetime_timeseries, i, intervals)

    def _get_next_interval_index(self, current_interval_index: int, datetime_timeseries: List[TimeseriesEntry], i: int,
                                 intervals: List[TimeseriesEntry]) -> int:
        return next((idx - 1 for idx, interval in
                     enumerate(intervals[current_interval_index + 1:],
                               start=current_interval_index + 1)
                     if
                     interval["timestamp"] > datetime_timeseries[i + 1]["timestamp"]),
                    current_interval_index + 1)

    def _fill_overflowed_intervals(self, previous_index: int, current_interval_index: int,
                                   intervals: List[TimeseriesEntry], interval_weighted_average: float):
        intervals[previous_index:current_interval_index] = [
            {**interval, "value": interval_weighted_average}
            for interval in intervals[previous_index:current_interval_index]
        ]

    def entry_between_current_intervals(self, current_interval_index, entry, intervals):
        return intervals[current_interval_index]["timestamp"] <= entry["timestamp"] and (
                not self.next_entry_exists(intervals, current_interval_index) or entry["timestamp"] <
                intervals[current_interval_index + 1]["timestamp"])

    def next_entry_exists(self, datetime_timeseries, i):
        return i + 1 < len(datetime_timeseries)

    def next_entry_overflow_next_interval(self, current_interval_index, datetime_timeseries, i, intervals):
        return current_interval_index + 1 < len(intervals) and \
            datetime_timeseries[i + 1]["timestamp"] >= intervals[current_interval_index + 1]["timestamp"]

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
