from src.ProcessTelemetryData.domain.TimeSeriesEqualizer.timeseries_equalizer import TimeseriesEqualizer, GranularityOperationsDict
import json

class TimesequenceService:
    def process_data(self, data):
        equalizer = TimeseriesEqualizer()
        equalized_data: GranularityOperationsDict= equalizer.equalize_timeseries(data)
        self._save_to_json(equalized_data)
        return equalized_data
    
    def _save_to_json(self, data: GranularityOperationsDict) -> None:
        file_path = "src/ProcessTelemetryData/domain/storage/output.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)