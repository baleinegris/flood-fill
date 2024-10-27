import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler    
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.regularizers import L2
import matplotlib.pyplot as plt
import pickle

LAYERS = [32, 8]
EPOCHS = 2
BATCH_SIZE = 64

class Model():
    def __init__(self, df=None):
        self.model = None
        if df is not None:
            self.train(df)
    
    def train(self, df):
        # Features and target
        X = df[['lat', 'lon', 'precip']]
        y = df['floods_per_year']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the data
        self.scaler = StandardScaler()
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        # Build the model
        model = Sequential([
            Dense(LAYERS[0], input_dim=3, activation='relu'),
            Dense(LAYERS[1], activation='relu'),
            Dense(1, activation='softplus')
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='mse')

        # Train the model
        history = model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)

        # Plot the loss for each epoch
        # plt.plot(history.history['loss'], label='Training Loss')
        # plt.plot(history.history['val_loss'], label='Validation Loss')
        # plt.xlabel('Epoch')
        # plt.ylabel('Loss')
        # plt.legend()
        # plt.show()
        
        # Evaluate the model
        loss = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
        print(f'Test Loss: {loss}')

        # Predict
        predictions = model.predict(X_test, batch_size=BATCH_SIZE)
        print(predictions)

        self.model = model

    def predict_floods(self, lat, lon, precips):
        inputs = pd.DataFrame({'lat': [lat]*len(precips), 'lon': [lon]*len(precips), 'precip': precips})
        inputs = tf.convert_to_tensor(inputs)
        inputs = self.scaler.transform(inputs)
        print(inputs)
        predicted_floods = self.model.predict(inputs, batch_size=BATCH_SIZE)
        return predicted_floods
    
    def load(self, path):
        self.model = tf.keras.models.load_model(f'{path}/model.keras')
        with open(f'{path}/scaler.pkl', 'rb') as pkl:
            self.scaler = pickle.load(pkl)

    def save(self, path):
        self.model.save(f'{path}/model.keras')
        with open(f'{path}/scaler.pkl', 'wb') as pkl:
            pickle.dump(self.scaler, pkl)
