from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
import pandas as pd
import time
from datetime import datetime

class SelectTimeseries(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
        else:
            output_data = input_data
        #print(type(output_data))
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
    def run_acf(self, inputDataSets, params,time_):
        input_data = inputDataSets.get(0)
        #print(input_data['root.test.d2.s2'][0])
        timeseries = params.get("timeseries", None)
        #print(params.values())
        
        count = 0
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
            for i in range(len(output_data)):
                if (datetime.strptime(output_data.Time[i], '%Y-%m-%d %H:%M:%S')
                        <= datetime.strptime(time_, '%Y-%m-%d %H:%M:%S')):
                    count += 1
        else:
            output_data = input_data
        output_data.fillna(0, inplace=True)
        a = output_data[column][0:count]
        xcorr = np.correlate(a, a, mode='full')/output_data[column].values[count-1]
        Time = []
        for i in range(1, 2*count):
            if i < 10:
                q = time_[0:-1]+str(i)
                Time.append(q)
            if i >= 10:
                q = time_[0:-2]+str(i)
                Time.append(q)
        j='acf('+column+')'       
        data = {'Time': Time, j: xcorr}
        output_data = pd.DataFrame(data)
        #print(output_data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result

    def run_distinct(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
        else:
            output_data = input_data
        # print(type(output_data))
        q = len(set(output_data[column]))
        j='dictinct('+column+')'
        data = {'Time': (output_data['Time'][0:q]), j: list(
            set(output_data[column]))}
        output_data = pd.DataFrame(data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result

    def run_histogram(self, inputDataSets, params, min=0, max=0, count=1):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
        else:
            output_data = input_data
        # print(type(output_data))
        
        max_value=np.max(output_data[column])
        
        if min:
            pass
        else:
            min = -max_value
        if max:
            pass
        else:
            max = max_value
        
        bucket = [0]*count
        Time = []

        # print(len(output_data['root.test.d2.s2']))
        for j in range(len(output_data[column])):
            if output_data[column][j] < min:
                bucket[0] += 1
            elif output_data[column][j] >= max:
                # print(output_data['root.test.d2.s2'][j])
                bucket[-1] += 1
            else:
                for i in range(1, count+1):
                    if (output_data[column][j] >= min+(i-1)*(max-min)/count
                            and output_data[column][j] < min+i*(max-min)/count):
                        bucket[i-1] += 1
        for i in range(0, count):
            Time.append(output_data['Time'][i])
        z='histogram('+column+',min='+str(min)+',max='+str(max)+',count='+str(count)+')'
        data = {'Time': Time, z: bucket}
        output_data = pd.DataFrame(data)
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
    #result = algorithm.run_acf(dataSet, params,'2022-01-01 00:00:05')
    #result = algorithm.run_distinct(dataSet, params)
    result = algorithm.run_histogram(dataSet, params,count=10)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)


