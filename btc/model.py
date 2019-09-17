import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Dropout

def train_test_split_(price_matrix, train_size=0.9, shuffle=False, return_row=True):
    '''
    It makes a custom train test split where the last part is kept as the training set.
    '''
    price_matrix = np.array(price_matrix)
    #print(price_matrix.shape)
    row = int(round(train_size * len(price_matrix)))
    train = price_matrix[:row, :]
    if shuffle==True:
        np.random.shuffle(train)
    X_train, y_train = train[:row,:-1], train[:row,-1]
    X_test, y_test = price_matrix[row:,:-1], price_matrix[row:,-1]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    if return_row:
        return row, X_train, y_train, X_test, y_test
    else:
        X_train, y_train, X_test, y_test

df = pd.read_csv("data/market-price.csv",header=None)
print(df.head())
dates=df[0]
df.drop([0], 1, inplace=True)
print(df.head())

model = Sequential()
model.add(LSTM(units= 100,activation= 'tanh',input_shape=(None, 1)))
model.add(Dropout(rate= 0.2))
model.add(Dense(units= 1,  activation= 'linear'))

model.compile(optimizer= 'adam', loss= 'mse')


model.fit(x=df,y=df,batch_size= 1,epochs= 100,verbose=True );

# Epoch 100/100
# 164/164 [==============================] - 1s 4ms/step - loss: 0.0020

inputs = min_max_scaler.transform(inputs)
inputs = np.reshape(inputs, (len(inputs), 1, 1))
predicted_price = model.predict(inputs)

plt.plot(dates[len(df)-prediction_days:],test_set[:, 0], color='red', label='Real BTC Price')
plt.plot(dates[len(df)-prediction_days:],predicted_price[:, 0], color = 'blue', label = 'Predicted BTC Price')

plt.savefig("plot2.png")
