from kafka.admin import KafkaAdminClient, NewTopic

# Kafka broker configuration
bootstrap_servers = 'localhost:9093'

# Create an instance of KafkaAdminClient
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

# Define the topic configuration
topic_name = 'my_topic'
partitions = 1
replication_factor = 1

# Create a NewTopic object
new_topic = NewTopic(name=topic_name, num_partitions=partitions, replication_factor=replication_factor)

# Create the topics
new_topics = [
    NewTopic(topic, num_partitions=1, replication_factor=1)
    for topic in ["train", "test", "predict", "prediction", "evaluate"]
]

try:
    admin_client.create_topics(new_topics)
except Exception as e:
    print("Failed to create topics with error {}".format(e))
