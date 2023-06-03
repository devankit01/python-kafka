import pandas as pd
import time
from river import metrics



def predict_model(model, data):
        
        df = pd.DataFrame(data, index=[0])    
        
        df = df.drop(["notes"], axis=1)
        df['StartDate'] = pd.to_datetime(df['StartDate'])
        df['Year'] = df['StartDate'].dt.year
        df['Month'] = df['StartDate'].dt.month
        df['Day'] = df['StartDate'].dt.day
        df['Hour'] = df['StartDate'].dt.hour
        df['Minute'] = df['StartDate'].dt.minute
        
        
        # # Split the dataset into features and target
        y = df['kwh']
        x = df.drop(['StartDate', 'kwh'], axis=1)
        
        
        # Use the loaded model for predictions
        try:
            data_point = x.iloc[0].to_dict()

            y_pred = model.predict_one(data_point)
            print("Predicted value:", y_pred)
            return y_pred
            
        except Exception as e:
            print(e)
        