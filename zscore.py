from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import math


class zscore(FlokAlgorithmLocal):
    def run(self, inputDataSets, params, compute='batch', avg=0, sd=1):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
            if compute == 'stream':
                for i in range(len(output_data[column])):
                    output_data[column][i] = (output_data[column][i]-avg)/sd
            else:
                mean = sum(output_data[column])/len(output_data[column])
                std = math.sqrt(
                    sum((output_data[column]-mean) ** 2)/len(output_data[column]))
                for i in range(len(output_data[column])):
                    output_data[column][i] = (output_data[column][i]-mean)/std

        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = zscore()

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
    result = algorithm.run(dataSet, params, 'stream', 2.2, 1)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
