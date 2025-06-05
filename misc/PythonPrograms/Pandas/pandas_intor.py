import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt # For basic visualizations later

df1 = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv')

print("DataFrame 1: Description")
print(df1.describe())

print("\nDataFrame 2: Description")
print(df2.describe())

