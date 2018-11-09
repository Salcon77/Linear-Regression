import math, datetime
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import quandl
import numpy as np
from sklearn import preprocessing, model_selection,svm
from sklearn.linear_model import LinearRegression

style.use('ggplot')
# Allows pandas to display up to 10 columns fo data to the console
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



# SELF NOTE: read more into sk-learn and its built in functions
# Standardize the data set using sk-learn pre-processing
# https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
x = np.array(df.drop(['label'],1))
x = preprocessing.scale(x)
x_lately = x[-forcast_out:]
x = x[:-forcast_out]



df.dropna(inplace=True)
y = np.array(df['label'])
y = np.array(df['label'])

# Create a test sets to test out 20% of given data stored in the arrays
# https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.2)

# apply the linearrefression model to the sets
clf = LinearRegression()
clf.fit(x_train, y_train)

# The score function on linear regression returns the variance between the independent variable and dependant variable
# In this case it is daily high and low price volatility to daily opening and closing price volatility
# The close the score is to 1.0 the better the regression model is

clf.score(x_test, y_test)

accuracy = clf.score(x_test,y_test)
#print(accuracy)

forcast_set = clf.predict(x_lately)

#print(forcast_set, accuracy, forcast_out)

df['Forcast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day=86400
next_unix=last_unix + one_day

for i in forcast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix = next_unix + one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]
df['Adj. Close'].plot()
df['Forcast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
