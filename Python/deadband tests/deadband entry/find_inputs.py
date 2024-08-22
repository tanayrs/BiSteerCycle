import pandas as pd

constants_path = './Python/deadband tests/deadband entry/plotting_constants.csv'

df = pd.read_csv(constants_path)

for index,row in df.iterrows():
    data = pd.read_csv(row['path'])
    data['Relative Time'] = data['Time'] - data['Time'].iloc[0]
    
    print(row['path'])

    start1 = data.iloc[(data['Relative Time']-row['deadband_start1']).abs().argsort()[:1]]['Relative Time'].values[0]
    start2 = data.iloc[(data['Relative Time']-row['deadband_start2']).abs().argsort()[:1]]['Relative Time'].values[0]
    start3 = data.iloc[(data['Relative Time']-row['deadband_start3']).abs().argsort()[:1]]['Relative Time'].values[0]
    start4 = data.iloc[(data['Relative Time']-row['deadband_start4']).abs().argsort()[:1]]['Relative Time'].values[0]
    print(data.loc[data['Relative Time'] == start1,'Wheel Input'].values[0],end=',')
    print(data.loc[data['Relative Time'] == start2,'Wheel Input'].values[0],end=',')
    print(data.loc[data['Relative Time'] == start3,'Wheel Input'].values[0],end=',')
    print(data.loc[data['Relative Time'] == start4,'Wheel Input'].values[0])
    print()