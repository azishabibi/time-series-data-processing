from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
from scipy.linalg import toeplitz
import math
import pandas as pd
# pacf method in statsmodels
#import statsmodels.tsa.stattools as stattools
#def default_pacf(ts, k):
#    return statools.pacf(ts, nlags=k, unbiased=True)


def yule_walker(ts, order):
    ''' Solve yule walker equation
    '''
    x = np.array(ts) - np.mean(ts)
    n = x.shape[0]

    r = np.zeros(order+1, np.float64)  # to store acf
    r[0] = x.dot(x) / n  # r(0)
    for k in range(1, order+1):
        r[k] = x[:-k].dot(x[k:]) / (n - k)  # r(k)

    R = toeplitz(r[:-1])

    return np.linalg.solve(R, r[1:])  # solve `Rb = r` to get `b`


def pacf(ts, k):
    ''' Compute partial autocorrelation coefficients for given time series，unbiased
    '''
    res = [1.]
    for i in range(1, k+1):
        res.append(yule_walker(ts, i)[-1])
    return (res)


class SelectTimeseries(FlokAlgorithmLocal):
    '''
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
    '''
    def run(self, inputDataSets, params,nlags=0):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
            if nlags:
                pass
            else:
                n = len(output_data)
                nlags = int(min(n-1, 10*(math.log10(n))))
            res = [1.]
            for i in range(1, nlags+1):
                res.append(yule_walker(output_data[column], i)[-1])
            length = len(res)
            j = 'pacf('+column+',lag='+str(nlags)+')'
            data = {'Time': output_data['Time'][0:length], j: res}
            #print(data)
            output_data = pd.DataFrame(data)
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
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
