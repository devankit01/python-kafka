# Python Kafka Integration Project

This project demonstrates the integration of Kafka with a Python application for streaming and consuming data. The data is used to train and predict using a machine learning model and also plotting MAE on chart.

## Project Structure

The project has the following structure:

```
online_machine_learning/
├── kafka/
│   ├── data/
│   │   ├── BostonHousing.csv
│   │   ├── power_usage.csv
│   ├── create_topics.py
│   ├── load_train_data.py
├── my_river/
│   ├── __init__.py
│   ├── predict.py
├── config.py
├── main.py
├── metric.png
├── model.pkl
├── .gitignore
├── docker-compose.kafka.yaml
```

Explanation of the directory structure:

- `kafka/`: Directory containing Kafka-related files.
  - `data/`: Directory for storing data files used by the application.
    - `BostonHousing.csv`: Sample dataset file.
    - `power_usage.csv`: Sample dataset file.
  - `create_topics.py`: Script for creating Kafka topics.
  - `load_train_data.py`: Script for loading training data.
- `my_river/`: Directory for your custom river module.
  - `__init__.py`: File marking the directory as a Python package.
  - `predict.py`: File containing prediction code using the machine learning model.
- `config.py`: Configuration file for storing constants or environment variables.
- `main.py`: Main script for your Python Kafka integration project.
- `metric.png`: Image file representing a metric chart.
- `model.pkl`: Serialized machine learning model file.
- `.gitignore`: File specifying patterns to ignore during version control (e.g., `.env`, generated files, etc.).
- `docker-compose.kafka.yaml`: Docker Compose file for setting up Kafka and Kafdrop.

Please note that this structure assumes the presence of other required dependencies and files specific to your project. Adjust the structure as needed based on your specific implementation.

## Prerequisites

Before running the project, ensure that you have the following prerequisites installed:

- Python (version >= 3.6)
- Apache Kafka
- Docker Engine
- Docker Compose

## Getting Started

Follow the steps below to get started with the project:

1. Set up and configure Apache Kafka on your system. Ensure that Kafka is running and accessible.

2. Navigate to the `kafka/` directory and run the `create_topics.py` script to create the necessary Kafka topics. Use the script parameters to specify the desired topics.

3. Run the `load_train_data.py` script to load the training data into the Kafka topics. Make sure to provide the correct file paths for the data files.

4. Modify the configuration variables in the `my_river/config.py` file according to your Kafka setup. Update the bootstrap server address and topic names as per your configuration.

5. Open a terminal and navigate to the root directory of the project.

6. Run the following command to start the Kafka and ZooKeeper containers:

   ```
   docker-compose -f docker-compose.kafka.yaml up -d
   ```

   This will create and start the Docker containers based on the configurations defined in `docker-compose.kafka.yaml`.

7. Run the `my_river/main.py` script using the command:

   ```
   python my_river/main.py
   ```

   This will start the data streaming, consuming, and processing using the machine learning model.

8. Monitor the output and logs to observe the streaming and processing of data, as well as the evaluation metric results.

9. When you are done, stop the Docker containers by running the following command in the project directory:

   ```
   docker-compose -f docker-compose.kafka.yaml down
   ```

## Conclusion

This project demonstrates the integration of Apache Kafka with