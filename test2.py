from zscore import zscore
from pandasql import sqldf
algorithm=zscore()
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
result = algorithm.run(dataSet, params, 'batch')
algorithm.write(outputPaths, result, outputTypes, outputLocation)

df=algorithm.run(dataSet, params, 'batch').next()
data_sql = sqldf("select Time, \"root.test.d2.s2\" from df where Time <= '2022-01-01 00:00:12';")
print(data_sql)

