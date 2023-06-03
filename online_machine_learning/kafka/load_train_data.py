import pandas as pd
import json
from kafka import KafkaProducer
from sklearn.model_selection import train_test_split

TRAIN_TOPIC = "train"  # topic to consume to train the model
TEST_TOPIC = "test"  # topic to consume to evaluate the model
PREDICT_TOPIC = "predict"  # topic to consume to make predictions
EVALUATE_TOPIC = "evaluate"  # topic to send metrics to
PREDICTION_TOPIC = "prediction"  # topic to send predictions to

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9093', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read data form csv file
# data = pd.read_csv("data/BostonHousing.csv")
data = pd.read_csv("data/power_usage.csv")



test_proportion = 0.2  #  80% for training and 20% for testing

# Calculate the number of samples to be used for testing
test_size = int(len(data) * test_proportion)

# Split the dataset into train and test sets
train_data = data[:-test_size]
test_data = data[-test_size:]


# sending data to train topic
print("Sending data to train topic 🚀")
for index, row in train_data.iterrows():
    print(row)
    row_data = row.to_dict()
    print(row_data)
    producer.send(TRAIN_TOPIC, value=row_data)
    producer.flush()
print("Sending data completed to train topic 🚀")


# sending data to test topic
print("Sending data to test topic ")
for index, row in test_data.iterrows():
    row_data = row.to_dict()
    print(row_data)
    producer.send(TEST_TOPIC, value=row_data)
    producer.flush()
print("Sending data completed to test topic 🚀")
