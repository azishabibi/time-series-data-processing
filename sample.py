from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import random
import pandas as pd
class SelectTimeseries(FlokAlgorithmLocal):

    def run(self, inputDataSets, params,method='reservoir',k=1):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
            if method=='reservoir':
                reservoir = []
                for t, item in enumerate(output_data[column]):
                    if t < k:
                        reservoir.append(item)
                    else:
                        m = random.randint(0, t)
                        if m < k:
                            reservoir[m] = item
                j='sample('+column+',method=\'reservoir\',k='+str(k)
                data={'Time':output_data['Time'][0:len(reservoir)],j:reservoir}
            if method == 'isometric':
                iso=[]
                a = len(output_data[column])
                for i in range(k):
                  iso.append(output_data[column][i*int(a/k)])  
                j = 'sample('+column+',method=\'isometric\',k='+str(k)
                data = {'Time': output_data['Time']
                        [0:len(iso)], j: iso}
            output_data=pd.DataFrame(data)
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
    result = algorithm.run(dataSet, params,method='isometric',k=5)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
