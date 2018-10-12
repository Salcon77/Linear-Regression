import quandl

# Daily High and Low prices from GDAX using Quandl API
df = quandl.get('GDAX/BTC_USD')

# Calculate the % change from the daily high and low
df['HL_PCT'] = (df['High']-df['Low'])/df['Low']*100.0

#df = df[['High', 'Low', 'HL_PCT', 'Volume']]

print(df.tail())