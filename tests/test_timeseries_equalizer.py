import unittest
from src.timeseries_equalizer import TimeseriesEqualizer, GranularityOperationsDict


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
            "turbine": "A", "power_unit": "MW",  
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
            "turbine": "A", "power_unit": "MW",  
            "timeseries": [] 
        }
        self.assertEqual(result, outputA)
    

    def test_inputB(self):
        #GIVEN
        inputB:GranularityOperationsDict = {
        "turbine": "B", "power_unit": "MW",  
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
            "turbine": "B", "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 8.0}, 
                {"timestamp": 1581611400000, "value": 32.0} 
            ] 
        }
        self.assertEqual(result, outputB)

    def test_inputC(self):
        #GIVEN
        inputC:GranularityOperationsDict = {
            "turbine": "So_long_and_thanks_for_all_the_fish", "power_unit": "MW",  
            "timeseries": [ 
                {'timestamp': 1581608700000, 'value': 1000},  
                {'timestamp': 1581609600000, 'value': 1},  
                {'timestamp': 1581609960000, 'value': 0}, 
                {'timestamp': 1581611400000, 'value': 1},  
                {'timestamp': 1581612000000, 'value': 4},  
                {'timestamp': 1581613200000, 'value': 5},  
                {'timestamp': 1581613800000, 'value': 8},  
                {'timestamp': 1581614400000, 'value': 14},  
                {'timestamp': 1581615000000, 'value': None}
            ] 
        }

        #WHEN
        equalizer = TimeseriesEqualizer()
        result = equalizer.equalize_timeseries(inputC)


        #THEN
        outputC:GranularityOperationsDict = {
            "turbine": "So_long_and_thanks_for_all_the_fish", "power_unit": "MW",  
            "timeseries": [ 
                {"timestamp": 1581609600000, "value": 0.2},  
                {"timestamp": 1581611400000, "value": 3.0},  
                {"timestamp": 1581613200000, "value": 9.0} 
            ] 
        }
        self.assertEqual(result, outputC)


if __name__ == '__main__':
    unittest.main()