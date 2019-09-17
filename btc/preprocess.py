

ser = hist_price_dl() # Not passing any argument since they are set by default
price_matrix = price_matrix_creator(ser) # Creating a matrix using the dataframe
price_matrix = normalize_windows(price_matrix) # Normalizing its values to fit to RNN
row, X_train, y_train, X_test, y_test = train_test_split_(price_matrix) # Applying train-test splitting, also returning the splitting-point


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
    for index in range(0, len(preds)):
        pred = (preds[index]+1)* X_test[index][0]
        preds_original.append(pred)
    preds_original = np.array(preds_original)
    if train_phase:
        return [date, y_test, preds_original]
    else:
        import datetime
        return [date+datetime.timedelta(days=1),y_test]