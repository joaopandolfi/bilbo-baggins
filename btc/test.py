import requests,json,numpy as np,pandas as pd

#https://api.coinranking.com/v1/public/coin/:coin_id/history/:timeframe
#https://docs.coinranking.com/
def hist_price_dl(coin_id=1335,timeframe = "5y",currency = "USD"):
    '''It accepts coin_id, timeframe, and currency parameters to clean the historic coin data taken from COINRANKING.COM
    It returns a Pandas Series with daily mean values of the selected coin in which the date is set as the index'''
    r = requests.get("https://api.coinranking.com/v1/public/coin/"+str(coin_id)+"/history/"+timeframe+"?base="+currency)
    coin = json.loads(r.text)['data']['history'] #Reading in json and cleaning the irrelevant parts
    df = pd.DataFrame(coin)
    df['price'] = pd.to_numeric(df['price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms').dt.date
    return df.groupby('timestamp').mean()['price']




def price_matrix_creator(data, seq_len=30):
    '''
    It converts the series into a nested list where every item of the list contains historic prices of 30 days
    '''
    price_matrix = []
    for index in range(len(data)-seq_len+1):
        price_matrix.append(data[index:index+seq_len])
    return price_matrix

def normalize_windows(window_data):
    '''
    It normalizes each value to reflect the percentage changes from starting point
    '''
    normalised_data = []
    for window in window_data:
        if(window[0] == 0):
            window[0] = 0.000001
        
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data


def deserializer(preds, data, train_size=0.9, train_phase=False):
    '''
    Arguments:
    preds : Predictions to be converted back to their original values
    data : It takes the data into account because the normalization was made based on the full historic data
    train_size : Only applicable when used in train_phase
    train_phase : When a train-test split is made, this should be set to True so that a cut point (row) is calculated based on the train_size argument, otherwise cut point is set to 0
    
    Returns:
    A list of deserialized prediction values, original true values, and date values for plotting
    '''
    price_matrix = np.array(price_matrix_creator(ser))
    if train_phase:
        row = int(round(train_size * len(price_matrix)))
    else:
        row=0
    date = ser.index[row+29:]
    date = np.reshape(date, (date.shape[0]))
    X_test = price_matrix[row:,:-1]
    y_test = price_matrix[row:,-1]
    preds_original = []
    preds = np.reshape(preds, (preds.shape[0]))
    for index in range(0, len(preds)-1):
        pred = (preds[index]+1)* X_test[index][0]
        preds_original.append(pred)
    preds_original = np.array(preds_original)
    if train_phase:
        return [date, y_test, preds_original]
    else:
        import datetime
        return [date+datetime.timedelta(days=1),y_test]




# ----------------------------------------------------


#We need ser, preds, row
ser = hist_price_dl(timeframe='30d')[0:31]
price_matrix = price_matrix_creator(ser)
X_test = normalize_windows(price_matrix)
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(X_test)
from keras.models import load_model
model = load_model('coin_predictor.h5')
preds = model.predict(X_test, batch_size=2)
print(preds)
#print(ser)

plotlist = deserializer(preds, ser, train_phase=True)


from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import cufflinks as cf
init_notebook_mode(connected=True)

'''
prices = pd.DataFrame({'Predictions':plotlist[1], 'Real Prices':plotlist[2]},index=plotlist[0])
iplot(prices.iplot(asFigure=True,
                   kind='scatter',
                   xTitle='Date',
                   yTitle='BTC Price',
                   title='BTC Price Predictions'))
'''

print(plotlist[0])
print(plotlist[1])
print(plotlist[2])

import matplotlib.pyplot as plt
plt.style.use("ggplot")
plt.figure()
plt.plot(plotlist[0], plotlist[1], label="Predictions")
plt.plot(plotlist[0], plotlist[2], label="Real Prices")
plt.title("Real X Prediction")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend(loc="lower left")
plt.savefig("plot.png")