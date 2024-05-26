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
                {'timestamp': 1581608700000, 'value': 1000},    # 2020 4:45:00 PM GMT+01:00
                {'timestamp': 1581609600000, 'value': 1},       # 2020 5:00:00 PM GMT+01:00
                {'timestamp': 1581609960000, 'value': 0},       # 2020 5:06:00 PM GMT+01:00
                {'timestamp': 1581611400000, 'value': 1},       # 2020 5:30:00 PM GMT+01:00
                {'timestamp': 1581612000000, 'value': 4},       # 2020 5:40:00 PM GMT+01:00
                {'timestamp': 1581613200000, 'value': 5},       # 6:00:00 PM GMT+01:00
                {'timestamp': 1581613800000, 'value': 8},       # 6:10:00 PM GMT+01:00
                {'timestamp': 1581614400000, 'value': 14},      # 6:20:00 PM GMT+01:00
                {'timestamp': 1581615000000, 'value': None}
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

        self.assertEqual(result_timestamps, expected_timestamps, "The result timeseries does not have all 30-minute timestamps between min and max dates of the input.")


    # def test_inputD(self):
    #     #GIVEN
    #     inputD:GranularityOperationsDict = {
    #         "turbine": "Freudenau Turbine 2",
    #         "power_unit": "MW",
    #         "timeseries": [
    #     {
    #         "timestamp": 1586901600000,
    #         "value": 12
    #     },
    #     {
    #         "timestamp": 1586902200000,
    #         "value": 5.01
    #     },
    #     {
    #         "timestamp": 1586923200000,
    #         "value": 20.043
    #     },
    #     {
    #         "timestamp": 1586940600000,
    #         "value": 32.01
    #     },
    #     {
    #         "timestamp": 1586957400000,
    #         "value": 23.4
    #     },
    #     {
    #         "timestamp": 1586958000000,
    #         "value": 23.5
    #     },
    #     {
    #         "timestamp": 1586958600000,
    #         "value": 24.92
    #     },
    #     {
    #         "timestamp": 1586958720000,
    #         "value": 26.7
    #     },
    #     {
    #         "timestamp": 1586959080000,
    #         "value": 32.034
    #     },
    #     {
    #         "timestamp": 1586959200000,
    #         "value": 32.000001
    #     },
    #     {
    #         "timestamp": 1586964000000,
    #         "value": 29.95665
    #     },
    #     {
    #         "timestamp": 1586966400000,
    #         "value": 30.2
    #     },
    #     {
    #         "timestamp": 1586977200000,
    #         "value": 0.001
    #     },
    #     {
    #         "timestamp": 1586994600000,
    #         "value": -0.0002
    #     },
    #     {
    #         "timestamp": 1586996400000,
    #         "value": 0
    #     },
    #     {
    #         "timestamp": 1586998800000,
    #         "value": 2.0
    #     },
    #     {
    #         "timestamp": 1587002400000,
    #         "value": 2.5
    #     },
    #     {
    #         "timestamp": 1587006000000,
    #         "value": 3.3
    #     },
    #     {
    #         "timestamp": 1587009600000,
    #         "value": 4.4
    #     },
    #     {
    #         "timestamp": 1587013200000,
    #         "value": 5.5
    #     },
    #     {
    #         "timestamp": 1587016800000,
    #         "value": 6.6
    #     },
    #     {
    #         "timestamp": 1587020400000,
    #         "value": 7.7
    #     },
    #     {
    #         "timestamp": 1587056400000,
    #         "value": 0.0
    #     },
    #     {
    #         "timestamp": 1587074400000,
    #         "value": None
    #     }
    # ]
    #     }

    #     #WHEN
    #     equalizer = TimeseriesEqualizer()
    #     result = equalizer.equalize_timeseries(inputD)


    #     #THEN
    #     outputD:GranularityOperationsDict = {
    #         "turbine": "Freudenau Turbine 2",
    #         "power_unit": "MW",
    #         "timeseries": [
    #             {
    #                 "timestamp": 1586901600000,
    #                 "value": 12.0
    #             },
    #             {
    #                 "timestamp": 1586903400000,
    #                 "value": 12.67025
    #             },
    #             {
    #                 "timestamp": 1586905200000,
    #                 "value": 13.3405
    #             },
    #             {
    #                 "timestamp": 1586907000000,
    #                 "value": 14.01075
    #             },
    #             {
    #                 "timestamp": 1586908800000,
    #                 "value": 14.681
    #             },
    #             {
    #                 "timestamp": 1586910600000,
    #                 "value": 15.35125
    #             },
    #             {
    #                 "timestamp": 1586912400000,
    #                 "value": 16.0215
    #             },
    #             {
    #                 "timestamp": 1586914200000,
    #                 "value": 16.69175
    #             },
    #             {
    #                 "timestamp": 1586916000000,
    #                 "value": 17.362
    #             },
    #             {
    #                 "timestamp": 1586917800000,
    #                 "value": 18.032249999999998
    #             },
    #             {
    #                 "timestamp": 1586919600000,
    #                 "value": 18.7025
    #             },
    #             {
    #                 "timestamp": 1586921400000,
    #                 "value": 19.37275
    #             },
    #             {
    #                 "timestamp": 1586923200000,
    #                 "value": 20.043
    #             },
    #             {
    #                 "timestamp": 1586925000000,
    #                 "value": 20.219684210526314
    #             },
    #             {
    #                 "timestamp": 1586926800000,
    #                 "value": 20.39636842105263
    #             },
    #             {
    #                 "timestamp": 1586928600000,
    #                 "value": 20.573052631578946
    #             },
    #             {
    #                 "timestamp": 1586930400000,
    #                 "value": 20.74973684210526
    #             },
    #             {
    #                 "timestamp": 1586932200000,
    #                 "value": 20.92642105263158
    #             },
    #             {
    #                 "timestamp": 1586934000000,
    #                 "value": 21.103105263157893
    #             },
    #             {
    #                 "timestamp": 1586935800000,
    #                 "value": 21.27978947368421
    #             },
    #             {
    #                 "timestamp": 1586937600000,
    #                 "value": 21.456473684210525
    #             },
    #             {
    #                 "timestamp": 1586939400000,
    #                 "value": 21.63315789473684
    #             },
    #             {
    #                 "timestamp": 1586941200000,
    #                 "value": 21.809842105263158
    #             },
    #             {
    #                 "timestamp": 1586943000000,
    #                 "value": 21.986526315789472
    #             },
    #             {
    #                 "timestamp": 1586944800000,
    #                 "value": 22.163210526315787
    #             },
    #             {
    #                 "timestamp": 1586946600000,
    #                 "value": 22.339894736842105
    #             },
    #             {
    #                 "timestamp": 1586948400000,
    #                 "value": 22.51657894736842
    #             },
    #             {
    #                 "timestamp": 1586950200000,
    #                 "value": 22.693263157894734
    #             },
    #             {
    #                 "timestamp": 1586952000000,
    #                 "value": 22.86994736842105
    #             },
    #             {
    #                 "timestamp": 1586953800000,
    #                 "value": 23.046631578947366
    #             },
    #             {
    #                 "timestamp": 1586955600000,
    #                 "value": 23.223315789473684
    #             },
    #             {
    #                 "timestamp": 1586957400000,
    #                 "value": 23.4
    #             },
    #             {
    #                 "timestamp": 1586959200000,
    #                 "value": 32.000001
    #             },
    #             {
    #                 "timestamp": 1586961000000,
    #                 "value": 31.55000075
    #             },
    #             {
    #                 "timestamp": 1586962800000,
    #                 "value": 31.1000005
    #             },
    #             {
    #                 "timestamp": 1586964600000,
    #                 "value": 30.650000249999998
    #             },
    #             {
    #                 "timestamp": 1586966400000,
    #                 "value": 30.2
    #             },
    #             {
    #                 "timestamp": 1586968200000,
    #                 "value": 25.166833333333333
    #             },
    #             {
    #                 "timestamp": 1586970000000,
    #                 "value": 20.133666666666667
    #             },
    #             {
    #                 "timestamp": 1586971800000,
    #                 "value": 15.1005
    #             },
    #             {
    #                 "timestamp": 1586973600000,
    #                 "value": 10.067333333333334
    #             },
    #             {
    #                 "timestamp": 1586975400000,
    #                 "value": 5.034166666666668
    #             },
    #             {
    #                 "timestamp": 1586977200000,
    #                 "value": 0.001
    #             },
    #             {
    #                 "timestamp": 1586979000000,
    #                 "value": 0.16758333333333333
    #             },
    #             {
    #                 "timestamp": 1586980800000,
    #                 "value": 0.33416666666666667
    #             },
    #             {
    #                 "timestamp": 1586982600000,
    #                 "value": 0.50075
    #             },
    #             {
    #                 "timestamp": 1586984400000,
    #                 "value": 0.6673333333333333
    #             },
    #             {
    #                 "timestamp": 1586986200000,
    #                 "value": 0.8339166666666666
    #             },
    #             {
    #                 "timestamp": 1586988000000,
    #                 "value": 1.0005
    #             },
    #             {
    #                 "timestamp": 1586989800000,
    #                 "value": 1.1670833333333333
    #             },
    #             {
    #                 "timestamp": 1586991600000,
    #                 "value": 1.3336666666666666
    #             },
    #             {
    #                 "timestamp": 1586993400000,
    #                 "value": 1.5002499999999999
    #             },
    #             {
    #                 "timestamp": 1586995200000,
    #                 "value": 1.6668333333333332
    #             },
    #             {
    #                 "timestamp": 1586997000000,
    #                 "value": 1.8334166666666665
    #             },
    #             {
    #                 "timestamp": 1586998800000,
    #                 "value": 2.0
    #             },
    #             {
    #                 "timestamp": 1587000600000,
    #                 "value": 2.25
    #             },
    #             {
    #                 "timestamp": 1587002400000,
    #                 "value": 2.5
    #             },
    #             {
    #                 "timestamp": 1587004200000,
    #                 "value": 2.9
    #             },
    #             {
    #                 "timestamp": 1587006000000,
    #                 "value": 3.3
    #             },
    #             {
    #                 "timestamp": 1587007800000,
    #                 "value": 3.85
    #             },
    #             {
    #                 "timestamp": 1587009600000,
    #                 "value": 4.4
    #             },
    #             {
    #                 "timestamp": 1587011400000,
    #                 "value": 4.95
    #             },
    #             {
    #                 "timestamp": 1587013200000,
    #                 "value": 5.5
    #             },
    #             {
    #                 "timestamp": 1587015000000,
    #                 "value": 6.05
    #             },
    #             {
    #                 "timestamp": 1587016800000,
    #                 "value": 6.6
    #             },
    #             {
    #                 "timestamp": 1587018600000,
    #                 "value": 7.15
    #             },
    #             {
    #                 "timestamp": 1587020400000,
    #                 "value": 7.7
    #             },
    #             {
    #                 "timestamp": 1587022200000,
    #                 "value": 7.315
    #             },
    #             {
    #                 "timestamp": 1587024000000,
    #                 "value": 6.93
    #             },
    #             {
    #                 "timestamp": 1587025800000,
    #                 "value": 6.545
    #             },
    #             {
    #                 "timestamp": 1587027600000,
    #                 "value": 6.16
    #             },
    #             {
    #                 "timestamp": 1587029400000,
    #                 "value": 5.775
    #             },
    #             {
    #                 "timestamp": 1587031200000,
    #                 "value": 5.390000000000001
    #             },
    #             {
    #                 "timestamp": 1587033000000,
    #                 "value": 5.005
    #             },
    #             {
    #                 "timestamp": 1587034800000,
    #                 "value": 4.62
    #             },
    #             {
    #                 "timestamp": 1587036600000,
    #                 "value": 4.235
    #             },
    #             {
    #                 "timestamp": 1587038400000,
    #                 "value": 3.85
    #             },
    #             {
    #                 "timestamp": 1587040200000,
    #                 "value": 3.465
    #             },
    #             {
    #                 "timestamp": 1587042000000,
    #                 "value": 3.08
    #             },
    #             {
    #                 "timestamp": 1587043800000,
    #                 "value": 2.6950000000000003
    #             },
    #             {
    #                 "timestamp": 1587045600000,
    #                 "value": 2.3099999999999996
    #             },
    #             {
    #                 "timestamp": 1587047400000,
    #                 "value": 1.9249999999999998
    #             },
    #             {
    #                 "timestamp": 1587049200000,
    #                 "value": 1.54
    #             },
    #             {
    #                 "timestamp": 1587051000000,
    #                 "value": 1.1550000000000002
    #             },
    #             {
    #                 "timestamp": 1587052800000,
    #                 "value": 0.7700000000000005
    #             },
    #             {
    #                 "timestamp": 1587054600000,
    #                 "value": 0.3849999999999998
    #             },
    #             {
    #                 "timestamp": 1587056400000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587058200000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587060000000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587061800000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587063600000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587065400000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587067200000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587069000000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587070800000,
    #                 "value": 0.0
    #             },
    #             {
    #                 "timestamp": 1587072600000,
    #                 "value": 0.0
    #             }
    #         ]
    #     }
    #     self.assertEqual(result, outputD)


if __name__ == '__main__':
    unittest.main()