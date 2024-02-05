from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
import pandas as pd
from datetime import datetime


class Segment(FlokAlgorithmLocal):
    def calculate_error(st, seq_range):
        x = np.arange(seq_range[0], seq_range[1] + 1)
        y = np.array(st[seq_range[0]:seq_range[1] + 1])
        # 计算error
        x_, y_ = x.mean(), y.mean()
        num = ((x - x_)*(y - y_)).sum()
        den = ((x - x_)**2).sum()
        _m = num/den
        _b = y_ - _m*x_
        error = (abs(_m*x + _b-y)).sum()/len(x)
        return error

    # 线性拟合
    def linear(a):
        x = np.arange(0, len(a))
        y = np.array(a)
        # 返回回归系数
        x_, y_ = x.mean(), y.mean()
        num = ((x - x_)*(y - y_)).sum()
        den = ((x - x_)**2).sum()
        _m = num/den
        _b = y_ - _m*x_
        return list(_m*x + _b)

    # 自下而上的拟合，先把数据分成n/2段，然后合并
    def Bottom_Up(T, max_error):
        seg_piece = []  # 最终返回的分段
        seg = []  # 储存分段两头位置
        merge_cost = []  # 计算合并带来的误差
        for i in range(0, len(T), 2):
            seg_piece += [T[i:i + 2]]
            seg.append((i, i + 1))
        for i in range(0, len(seg_piece) - 2):
            merge_cost.insert(i, Segment.calculate_error(
                T, (seg[i][0], seg[i + 1][1])))
        while min(merge_cost) < max_error:
            index = merge_cost.index(min(merge_cost))  # 每次合并误差最小的片段
            seg_piece[index] = Segment.linear(
                seg_piece[index] + seg_piece[index + 1])
            seg[index] = (seg[index][0], seg[index + 1][1])
            # 合并完成后删除原值
            del seg_piece[index + 1]
            del seg[index + 1]
            # 更新merge_cost
            if index > 1:
                merge_cost[index - 1] = Segment.calculate_error(
                    T, (seg[index - 1][0], seg[index][1]))
            if index + 1 < len(merge_cost):
                merge_cost[index] = Segment.calculate_error(
                    T, (seg[index][0], seg[index + 1][1]))
                del merge_cost[index + 1]
            else:
                del merge_cost[index]
        seg_piece[-2] = Segment.linear(seg_piece[-2] + seg_piece[-1])
        del seg_piece[-1]
        return seg_piece

    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        output = params.get("output", 'first')
        error = params.get("error", 0.1)
        if isinstance(error, str):
            error = float(error)
        str_ = 'segment({a},\'output\'=\'{b}\',\'error\'=\'{c}\')'.format(
            a=column,b=output, c=error)
        # 如果输入是等差数列直接输出
        if all([((output_data[column][i] - output_data[column][i-1])-(output_data[column][1] - output_data[column][0])) < 1e-10 for i in range(1, len(output_data))]):
            if output == 'all':
                output_data = output_data
            else:
                output_data = pd.DataFrame(
                    {'Time': '1970-01-01 08:00:00.000', str_: output_data[column][0]}, index=[0])
        else:
            seg_piece = Segment.Bottom_Up(list(output_data[column]), error)
            data = []
            n = len(seg_piece)
            Time = []
            if output == 'all':
                for i in range(len(seg_piece)):
                    data += seg_piece[i]
                print(data)
                print(len(data))
                for i in range(len(output_data)):
                    Time.append(datetime.fromtimestamp((i+1)/1000.0))
                Time = pd.Series(
                    [t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for t in Time])
                output_data = pd.DataFrame({'Time': Time, str_: data})
            else:
                for i in range(len(seg_piece)):
                    data.append(seg_piece[i][0])
                for i in range(len(data)):
                    Time.append(datetime.fromtimestamp((i+1)/1000.0))
                Time = pd.Series(
                    [t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for t in Time])
                output_data = pd.DataFrame({'Time': Time, str_: data})

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Segment()

    all_info_1 = {
        "input": ["root_test_d1"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'output': 'all', 'error': 0.1}
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
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(
        dataSet, {"timeseries": "Time,s3"})
    result = algorithm.run(dataSet, params)
    print(result.get(0))
    #algorithm.write(outputPaths, result, outputTypes, outputLocation)
'''
    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,root.test.d2.s2",'output':'first','error':0.1}
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
'''
