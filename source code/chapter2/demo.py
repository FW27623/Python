import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取exp3_1.csv数据
data = pd.read_csv('exp3_1.csv')
# 检查是否有空值
data.isnull().sum()
# 检查是否有重复值
data.duplicated().sum()
# 设置一列数据，数据内容为年份（1994-2014年），将该year设置为表格索引
data['year'] = range(1994, 2014)
data.set_index('year', inplace=True)
# 进行描述性统计
data.describe()
# 分析每个影响因素的集中趋势与离散趋势
data.plot(kind='box')
plt.show()
# 分析每个影响因素的集中趋势与离散趋势
data.plot(kind='hist')
plt.show()
# 分析每个影响因素的集中趋势与离散趋势
data.plot(kind='kde')
plt.show()
# 计算person的相关系数，并保留两位小数
data.corr()
# 查看person的相关系数
data.corr()['person']
# 分析每个影响因素的集中趋势与离散趋势
data.plot(kind='scatter', x='person', y='year')
plt.show()