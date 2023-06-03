from config import BOOTSTRAP_SERVER, GROUP_ID
from river import metrics
import asyncio
from kafka import KafkaConsumer
import pandas as pd
from river import linear_model
import pickle
from my_river.predict import predict_model
import matplotlib.pyplot as plt
import json

accuracy = []

TRAIN_TOPIC = "train"
TEST_TOPIC = "test"
PREDICT_TOPIC = "predict"
EVALUATE_TOPIC = "evaluate"
PREDICTION_TOPIC = "prediction"
filename = "model.pkl"

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9093', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


metric = metrics.Accuracy()
from river import optim

class OnlineML:
    """
    Online model service that consumes from the train, test, and predict topics and produces to the evaluate and
    predictions topics.
    """

    def __init__(self, train_metric, test_metric):
        
         # Load the model from the file if it exists
        try:
            with open(filename, "rb") as f:
                model = pickle.load(f)
        except FileNotFoundError:
            
            # Create a new model if the file doesn't exist
            model = linear_model.BayesianLinearRegression()
            
        self.metric = metrics.MAE()
        self.model = model
        self.train_metric = train_metric
        self.test_metric = test_metric

    def train_model(self, data):
        df = pd.DataFrame(data, index=[0])
        

        df = df.drop(["notes"], axis=1)
        
        df['StartDate'] = pd.to_datetime(df['StartDate'])
        df['Year'] = df['StartDate'].dt.year
        df['Month'] = df['StartDate'].dt.month
        df['Day'] = df['StartDate'].dt.day
        df['Hour'] = df['StartDate'].dt.hour
        df['Minute'] = df['StartDate'].dt.minute

        # Split the dataset into features and target
        y = df['kwh']
        x = df.drop(['StartDate', 'kwh'], axis=1)
                

        self.model.learn_one(x.iloc[0].to_dict(), y.iloc[0])
        
        # Save the model to a file
        with open(filename, "wb") as f:
            pickle.dump(self.model, f)
            print(vars(self.model))
            print("model updated")
        
        
    async def consume_train(self):
        consumer = KafkaConsumer(
            TRAIN_TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVER,
            request_timeout_ms=1000,
            auto_offset_reset="earliest",
            max_poll_interval_ms=1000,
            consumer_timeout_ms=1000,
        )

        # Consume and process data from the Kafka topic
        for message in consumer:
            csv_row = message.value.decode("utf-8")
            csv_row = eval(csv_row)
            self.train_model(csv_row)  # train
            
            
    async def consume_test(self):
        consumer = KafkaConsumer(
            TEST_TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVER,
            request_timeout_ms=1000,
            auto_offset_reset="earliest",
            max_poll_interval_ms=1000,
            consumer_timeout_ms=1000,
        )

        # Consume and process data from the Kafka topic
        accuracy = []
        for message in consumer:
            
            csv_row = message.value.decode("utf-8")
            csv_row = eval(csv_row)
            
            y_pred = predict_model(self.model, csv_row)  # predict
            df = pd.DataFrame(csv_row, index=[0])  
            y = df['kwh']  
            
            # send prediction to topic
            data = {
                "record" : csv_row,
                "predicted_data" : y_pred
            }
            producer.send(PREDICTION_TOPIC, value=data) 
            
            
            # update the metric
            self.metric = self.metric.update(y.iloc[0], y_pred) 
            mae = self.metric.get()
            accuracy.append(self.metric.get())
            
            
            # send the accuracy to evaluate topic
            data = {
                "accuracy" : mae,
                "topic" : "test"
            }
            producer.send(EVALUATE_TOPIC, value=data) 
        

        # plot the mae
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(accuracy)
        ax.set_xlabel("data")
        ax.set_ylabel("MAE")
        fig.savefig("metric.png")
            
            


if __name__ == "__main__":
    # # Load the model from the file if it exists

    test_metric = ""
    train_metric = ""
    online_ml = OnlineML( train_metric, test_metric)
    loop = asyncio.get_event_loop()
    
    # loop.run_until_complete(online_ml.consume_train())
    loop.run_until_complete(online_ml.consume_test())
    loop.close()
