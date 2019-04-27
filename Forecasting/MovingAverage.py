import pandas as pd
data = pd.read_csv("data/bucketed/trades.csv.gz", parse_dates=['timestamp'])


class MovingAverage:
    def __init__(self, n):
        self.n = n

    def predict(self, data):
        pred = []
        for i in range(self.n, data.shape[0]):
            pred.append(data[i-self.n:i].mean())
        return pred


mav = MovingAverage(5)
mav.predict(data['close'][:100])
