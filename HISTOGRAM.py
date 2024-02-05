from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd

class histogram(FlokAlgorithmLocal):
    def run(self, inputDataSets, params, min=0, max_=0, count=1):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column=timeseries_list[1]
            print(output_data[column])
            max_value = max(output_data[column])
            print(max_value)
            if min:
                pass
            else:
                min = -max_value
            if max_:
                pass
            else:
                max_ = max_value
            bucket = [0]*count
            Time = []
            print(min,max_)
            for j in range(len(output_data['root.test.d2.s2'])):
                if output_data['root.test.d2.s2'][j] < min:
                    bucket[0] += 1
                elif output_data['root.test.d2.s2'][j] >= max_:
                    # print(output_data['root.test.d2.s2'][j])
                    bucket[-1] += 1
                else:
                    for i in range(1, count+1):
                        if (output_data['root.test.d2.s2'][j] >= min+(i-1)*(max_-min)/count
                                and output_data['root.test.d2.s2'][j] < min+i*(max_-min)/count):
                            bucket[i-1] += 1
            for i in range(0, count):
                Time.append(output_data['Time'][i])
            j = 'histogram({f})'.format(f=timeseries_list[1])
            data = {'Time': Time, j: bucket}
            output_data = pd.DataFrame(data)
        else:
            output_data = input_data        
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = histogram()

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
    result = algorithm.run(dataSet, params,min=1,max_=20,count=10)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
