import pandas as pd

df = pd.read_csv('./Python/deadband coeff/SourceData/FrontSlope10CompData_1.csv')

df['Wheel Speed'] = df['Wheel Speed']*8

df.to_csv('./Python/deadband coeff/FrontSlope10CompData_1.csv')