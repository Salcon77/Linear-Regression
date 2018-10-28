import math
import pandas as pd
import quandl
import numpy as np
from sklearn import preprocessing, model_selection,svm
from sklearn.linear_model import LinearRegression


pd.set_option('display.max_columns', 10)


# Daily High and Low prices from WIKI prices using free Quandl
df = quandl.get('WIKI/GOOGL')

# Display only the following columns
df = df[["Adj. Open", "Adj. High", "Adj. Low", "Adj. Close"]]

# Create a column that displays the percent change from the the highest price of the day and the lowest price of the day
df['HL_PCT'] = (df['Adj. High']-df['Adj. Low'])/df['Adj. Low']*100.0

# Create a column that displays the percent change from the opening price of the day and the closing price of the day
df['OC_PCT']=(df['Adj. Open']-df['Adj. Close'])/df['Adj. Close']*100.0

# Assigning the Adj. Close column to the variable forcast_col
forcast_col = 'Adj. Close'

# replace nand data with -99999 it will be treated as an outlier
df.fillna(-99999, inplace=True)

# set forcast_out to be a 1% of the len of the dataframe.
forcast_out = int(math.ceil(0.01*len(df)))

# create a label column that returns forcasted values shifted by forcast_out days ahead
df['label']=df[forcast_col].shift(-forcast_out)
df.dropna(inplace=True)


# SELF NOTE: read more into scikit-learn and its built in functions
x = np.array(df.drop(['label'],1))
y = np.array(df['label'])
x= preprocessing.scale(x)
df.dropna(inplace=True)
y = np.array(df['label'])


x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.2)

clf = LinearRegression()
clf.fit(x_train, y_train)
clf.score(x_test, y_test)
accuracy = clf.score(x_test,y_test)

print(accuracy)

