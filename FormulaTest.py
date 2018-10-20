import math
import pandas as pd
import quandl
pd.set_option('display.max_columns', 10)


# Daily High and Low prices from WIKI prices using free Quandl
df = quandl.get('WIKI/GOOGL')

# Display only the following columns
df = df[["Adj. Open", "Adj. High", "Adj. Low", "Adj. Close"]]

# Percent change from the the highest price of the day and the lowest price of the day
df['HL_PCT'] = (df['Adj. High']-df['Adj. Low'])/df['Adj. Low']*100.0

# Percent change from the opening price of the day and the closing price of the day
df['OC_PCT']=(df['Adj. Open']-df['Adj. Close'])/df['Adj. Close']*100.0

# Assigning the Adj. Close column to the variable forcast_col
forcast_col = 'Adj. Close'

# replace nand data with -99999 it will be treated as an outlier
df.fillna(-99999, inplace=True)

#!
forcast_out = int(math.ceil(0.01*len(df)))

#!
df['label']=df[forcast_col].shift(-forcast_out)
df.dropna(inplace=True)

print(df.tail())
