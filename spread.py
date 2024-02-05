from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from datetime import datetime
import pandas as pd
import time
class SelectTimeseries(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result

    def spread(self, inputDataSets, params,time_):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            count = int(time.mktime(time.strptime(
                time_, "%Y-%m-%d %H:%M:%S"))-time.mktime(time.strptime(output_data['Time'][0], "%Y-%m-%d %H:%M:%S")))
            a = output_data[timeseries_list[1]][0:count+1]
            spread=max(a)-min(a)
            j = 'spread({})'.format(timeseries_list[1])
            output_data = pd.DataFrame(
                {'Time': '1970-01-01 08:00:00.000', j: spread}, index=[0])
        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = SelectTimeseries()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {}
    }

    params = all_info_1["parameters"]
    inputPaths = all_info_1["input"]
    inputTypes = all_info_1["inputFormat"]
    inputLocation = all_info_1["inputLocation"]
    outputPaths = all_info_1["output"]
    outputTypes = all_info_1["outputFormat"]
    outputLocation = all_info_1["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)

    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,root.test.d2.s2"}
    }

    params = all_info_2["parameters"]
    inputPaths = all_info_2["input"]
    inputTypes = all_info_2["inputFormat"]
    inputLocation = all_info_2["inputLocation"]
    outputPaths = all_info_2["output"]
    outputTypes = all_info_2["outputFormat"]
    outputLocation = all_info_2["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    result = algorithm.spread(dataSet, params, '2022-01-01 00:00:10')
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
