import unittest
from src.ProcessTelemetryData.domain.TimeSeriesEqualizer.timeseries_equalizer import TimeseriesEqualizer, GranularityOperationsDict


class TimeseriesEqualizerTestCase(unittest.TestCase):

    def test_invalid_input_wrong_input_format(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "x": "A", 
            "y": "MW",  
            "z": [ 
                {"t": 1581609600000, "v": 16},  
                {"t": 1581610500000, "v": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)
    

    def test_invalid_input_wrong_input_format_2(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": 2, 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 16},  
                {"timestamp": 1581610400000, "value": 3}, 
                {"timestamp": 1581610500000, "value": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)
    
    def test_invalid_input_wrong_input_format_3(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": "name", 
            "power_unit": 3,  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 16},  
                {"timestamp": 1581610400000, "value": 3}, 
                {"timestamp": 1581610500000, "value": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)
    
    def test_invalid_input_wrong_input_format_4(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": "name", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": "1581609600000", "value": 16},  
                {"timestamp": "1581610400000", "value": 3}, 
                {"timestamp": "1581610500000", "value": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)
    
    def test_invalid_input_wrong_input_format_5(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": "name", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": "16"},  
                {"timestamp": 1581610400000, "value": "3"}, 
                {"timestamp": 1581610500000, "value": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)
    
    def test_invalid_input_wrong_input_format_6(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": "name", 
            "power_unit": "MW",  
            "timeseries": [ 
                1581609600000, 
                "3", 
                None 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(TypeError):
            equalizer.equalize_timeseries(input)

    def test_invalid_input_dublicated_timestamps(self):
        # GIVEN 
        input:GranularityOperationsDict = {
            "turbine": "A", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 16},  
                {"timestamp": 1581609600000, "value": 7}, 
                {"timestamp": 1581610400000, "value": 3}, 
                {"timestamp": 1581610500000, "value": None} 
            ] 
        }
        # WHEN 
        equalizer = TimeseriesEqualizer()

        # THEN 
        with self.assertRaises(ValueError):
            equalizer.equalize_timeseries(input)

    def test_inputA(self):
        #GIVEN
        inputA:GranularityOperationsDict = {
            "turbine": "A", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 16},  
                {"timestamp": 1581610500000, "value": None} 
            ] 
        }

        #WHEN
        equalizer = TimeseriesEqualizer()
        result = equalizer.equalize_timeseries(inputA)

        #THEN   
        outputA:GranularityOperationsDict = {
            "turbine": "A", 
            "power_unit": "MW",  
            "timeseries": [] 
        }
        self.assertEqual(result, outputA)
    

    def test_inputB(self):
        #GIVEN
        inputB:GranularityOperationsDict = {
        "turbine": "B", 
        "power_unit": "MW",  
        "timeseries": [ 
                {"timestamp": 1581609600000, "value": 16},  
                {"timestamp": 1581610500000, "value": 0},  
                {"timestamp": 1581611400000, "value": 4},  
                {"timestamp": 1581612300000, "value": 60}, 
                {"timestamp": 1581613200000, "value": None} 
            ] 
        }

        #WHEN
        equalizer = TimeseriesEqualizer()
        result = equalizer.equalize_timeseries(inputB)

        #THEN
        outputB:GranularityOperationsDict = {
            "turbine": "B", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 8.0}, 
                {"timestamp": 1581611400000, "value": 32.0} 
            ] 
        }
        self.assertEqual(result, outputB)

    def test_inputC(self):
        #GIVEN
        inputC:GranularityOperationsDict = {
            "turbine": "So_long_and_thanks_for_all_the_fish", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581608700000, "value": 1000},    # 2020 4:45:00 PM GMT+01:00
                {"timestamp": 1581609600000, "value": 1},       # 2020 5:00:00 PM GMT+01:00
                {"timestamp": 1581609960000, "value": 0},       # 2020 5:06:00 PM GMT+01:00
                {"timestamp": 1581611400000, "value": 1},       # 2020 5:30:00 PM GMT+01:00
                {"timestamp": 1581612000000, "value": 4},       # 2020 5:40:00 PM GMT+01:00
                {"timestamp": 1581613200000, "value": 5},       # 6:00:00 PM GMT+01:00
                {"timestamp": 1581613800000, "value": 8},       # 6:10:00 PM GMT+01:00
                {"timestamp": 1581614400000, "value": 14},      # 6:20:00 PM GMT+01:00
                {"timestamp": 1581615000000, "value": None}
            ] 
        }

        #WHEN
        equalizer = TimeseriesEqualizer()
        result = equalizer.equalize_timeseries(inputC)


        #THEN
        outputC:GranularityOperationsDict = {
            "turbine": "So_long_and_thanks_for_all_the_fish", 
            "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 0.2},  # Thursday, February 13, 2020 5:00:00 PM GMT+01:00
                {"timestamp": 1581611400000, "value": 3.0},  # Thursday, February 13, 2020 5:30:00 PM GMT+01:00
                {"timestamp": 1581613200000, "value": 9.0}   # Thursday, February 13, 2020 6:00:00 PM GMT+01:00
            ] 
        }
        self.assertEqual(result, outputC)

    def test_has_all_30_min_timestamps(self):
        # GIVEN
        input_data = {
            "turbine": "Freudenau Turbine 2",
            "power_unit": "MW",
            "timeseries": [
                {"timestamp": 1586901600000, "value": 12},
                {"timestamp": 1586902200000, "value": 5.01},
                {"timestamp": 1586923200000, "value": 20.043},
                {"timestamp": 1586940600000, "value": 32.01},
                {"timestamp": 1586957400000, "value": 23.4},
                {"timestamp": 1586958000000, "value": 23.5},
                {"timestamp": 1586958600000, "value": 24.92},
                {"timestamp": 1586958720000, "value": 26.7},
                {"timestamp": 1586959080000, "value": 32.034},
                {"timestamp": 1586959200000, "value": 32.000001},
                {"timestamp": 1586964000000, "value": 29.95665},
                {"timestamp": 1586966400000, "value": 30.2},
                {"timestamp": 1586977200000, "value": 0.001},
                {"timestamp": 1586994600000, "value": -0.0002},
                {"timestamp": 1586996400000, "value": 0},
                {"timestamp": 1586998800000, "value": 2.0},
                {"timestamp": 1587002400000, "value": 2.5},
                {"timestamp": 1587006000000, "value": 3.3},
                {"timestamp": 1587009600000, "value": 4.4},
                {"timestamp": 1587013200000, "value": 5.5},
                {"timestamp": 1587016800000, "value": 6.6},
                {"timestamp": 1587020400000, "value": 7.7},
                {"timestamp": 1587056400000, "value": 0.0},
                {"timestamp": 1587074400000, "value": None}
            ]
        }

        # Remove the last item if its value is None
        if input_data["timeseries"] and input_data["timeseries"][-1]["value"] is None:
            input_data["timeseries"].pop()

        # WHEN
        equalizer = TimeseriesEqualizer()
        result = equalizer.equalize_timeseries(input_data)

        # THEN
        result_timeseries = result["timeseries"]
        result_timestamps = [entry["timestamp"] for entry in result_timeseries]

        min_timestamp = min(entry["timestamp"] for entry in input_data["timeseries"])
        max_timestamp = max(entry["timestamp"] for entry in input_data["timeseries"])

        current_time = min_timestamp
        expected_timestamps = []

        while current_time <= max_timestamp:
            expected_timestamps.append(current_time)
            current_time += 30 * 60 * 1000  # Increment by 30 minutes in milliseconds

        self.assertEqual(result_timestamps, expected_timestamps, 
                         "The result timeseries does not have all 30-minute timestamps between min and max dates of the input.")


if __name__ == '__main__':
    unittest.main()