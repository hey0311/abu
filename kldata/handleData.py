import numpy as np
import pandas as pd
from collections import OrderedDict


result = np.loadtxt("ticker4.csv")
dfIndex = ['ticker' + str(i) for i in range(result.shape[0])]
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
df = pd.DataFrame(result, index=dfIndex, columns=columns)
df['time']=pd.to_datetime(df['timestamp'],unit='ms')
df['date']=pd.to_datetime(df['timestamp'],unit='ms')
df=df.set_index('time')
# df.resample('1D').holc()
# print(df.head())
# df=df.drop(columns='timestamp',axis=1)
df=df.resample('1T').agg(
    OrderedDict([
        ('open', 'first'),
        ('high', 'max'),
        ('low', 'min'),
        ('close', 'last'),
        ('volume', 'sum'),
        ('date', 'first'),
    ])
)
df=df[['date','open','high','low','close','volume']]
print(df.head())
np.save("ticker4.npy", df)