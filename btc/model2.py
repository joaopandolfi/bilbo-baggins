from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
import time
# LSTM Model parameters, I chose
batch_size = 2            # Batch size (you may try different values)
epochs = 15               # Epoch (you may try different values)
seq_len = 30              # 30 sequence data (Representing the last 30 days)
loss='mean_squared_error' # Since the metric is MSE/RMSE
optimizer = 'rmsprop'     # Recommended optimizer for RNN
activation = 'linear'     # Linear activation
input_shape=(None,1)      # Input dimension
output_dim = 30           # Output dimension


# Model defining
model = Sequential()
model.add(LSTM(units=output_dim, return_sequences=True, input_shape=input_shape))
model.add(Dense(units=32,activation=activation))
model.add(LSTM(units=output_dim, return_sequences=False))
model.add(Dense(units=1,activation=activation))
model.compile(optimizer=optimizer,loss=loss)


start_time = time.time()
model.fit(x=X_train,
          y=y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.05)
end_time = time.time()
processing_time = end_time - start_time


model.save('coin_predictor.h5')