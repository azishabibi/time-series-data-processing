from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
import pandas as pd
import time
from datetime import datetime

class acf(FlokAlgorithmLocal):
    def run(self, inputDataSets, params,time_=0):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        count=0
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            
            for i in range(len(output_data)):
                if (datetime.strptime(output_data.Time[i], '%Y-%m-%d %H:%M:%S') 
                <= datetime.strptime(time_, '%Y-%m-%d %H:%M:%S')):
                    count+=1
            output_data.fillna(0, inplace=True)
            a = output_data[timeseries_list[1]][0:count]
            c = np.correlate(a, a, mode='full') / \
                output_data[timeseries_list[1]].values[count-1]
            Time = []
            for i in range(1, 2*count):
                if i < 10:
                    q = time_[0:-1]+str(i)
                    Time.append(q)
                if i >= 10:
                    q = time_[0:-2]+str(i)
                    Time.append(q)
            j = 'acf({f})'.format(f=timeseries_list[1])
            data = {'Time': Time, j: c}
            output_data = pd.DataFrame(data)
        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result

       
        

if __name__ == "__main__":
    algorithm = acf()

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
    result = algorithm.run(dataSet, params,'2022-01-01 00:00:05')
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
