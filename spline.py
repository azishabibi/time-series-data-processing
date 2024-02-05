from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import time
import numpy as np
from scipy import interpolate
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class spline(FlokAlgorithmLocal):
    def run(self, inputDataSets, params, points=0):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            if len(output_data) >= 4:
                column = timeseries_list[1]
                #output_data[column] = output_data[column]**3
                Time = []
                time0 = time.mktime(time.strptime(
                    output_data['Time'][0], "%Y-%m-%d %H:%M:%S"))
                for i in range(len(output_data)):
                    Time.append(time.mktime(time.strptime(
                        output_data['Time'][i], "%Y-%m-%d %H:%M:%S"))-time0)
                value = output_data[column]
                # （t，c，k）包含节点向量、B样条曲线系数和样条曲线阶数的元组。
                tck = interpolate.splrep(Time, value, k=3)
                x = (np.linspace(min(Time), max(Time), points)).tolist()
                y = (interpolate.splev(x, tck, der=0)).tolist()
                for i in range(0, len(x)):
                    x[i] = datetime.fromtimestamp(x[i]+time0)
                j = 'spline({})'.format(column)
                data = {'Time': x, j: y}
                output_data = pd.DataFrame(data)
                plt.plot(x, y)
                plt.show()
            else:
                pass
        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = spline()
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
    result = algorithm.run(dataSet, params, points=200)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
