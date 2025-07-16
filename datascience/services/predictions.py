import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from datascience.services.consume import consume_data
from datascience.services.detrend import SMASmoothingDetrendingStrategy


def predict_prices(stockdata):
    raw_data = consume_data(stockdata)
    data = SMASmoothingDetrendingStrategy().detrend(raw_data).dropna()
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1)) # type: ignore
    training_data_len = int(len(scaled_data) * 0.95)
    train_data = scaled_data[:training_data_len]
    valid_data = scaled_data[training_data_len:]

    def create_dataset(dataset, time_step=1):
        X, y = [], []
        for i in range(len(dataset) - time_step):
            X.append(dataset[i:(i + time_step), 0])
            y.append(dataset[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 60
    X_train, y_train = create_dataset(train_data, time_step)
    X_valid, y_valid = create_dataset(valid_data, time_step)

    xgb_model = XGBRegressor(
        objective="reg:squarederror",
        colsample_bytree=0.3,
        learning_rate=0.1,
        max_depth=5,
        alpha=10,
        n_estimators=100
    )
    xgb_model.fit(X_train, y_train)

    future_prices = []

    last_60_days = scaled_data[-time_step:].reshape(1, time_step)

    for i in range(10):
        pred_price = xgb_model.predict(last_60_days)
        future_prices.append(pred_price[0])
        last_60_days = np.append(last_60_days[:, 1:], [[pred_price[0]]], axis=1)

    future_prices = scaler.inverse_transform(
        np.array(future_prices).reshape(-1, 1)
    )

    rolling_mean = raw_data.Close.rolling(window=12).mean().iloc[-1]
    retrended_future_prices = future_prices.flatten() + rolling_mean
    future_dates = pd.date_range(
        start=data.index[-1] + pd.Timedelta(days=1), # type: ignore
        periods=10,
        freq="D"
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        data.index[-100:],
        data.tail(100),
        label="Detrended Prices"
    )
    plt.plot(
        future_dates,
        retrended_future_prices,
        linestyle="dashed",
        color="red",
        label="Future Predictions"
    )
    plt.title("Stock Price Prediction for Next 10 Days using XGBoost")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    # plt.show()
    return {
            "dates": [str(date.date()) for date in future_dates],
            "predictions": retrended_future_prices.tolist()
    }
 
