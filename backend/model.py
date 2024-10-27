import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler    
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

class Model():
    def __init__(self, df):
        # Features and target
        X = df[['lat', 'lon', 'precip']]
        y = df['floods_per_year']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the data
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Build the model
        model = Sequential([
            Dense(8, input_dim=3, activation='relu'),
            Dense(4, activation='relu'),
            Dense(1)
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='mse')

        # Train the model
        history = model.fit(X_train, y_train, epochs=20, batch_size=10, validation_split=0.2)

        # Plot the loss for each epoch
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

        # Plot the accuracy for each epoch
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()
        
        # Evaluate the model
        loss = model.evaluate(X_test, y_test)
        print(f'Test Loss: {loss}')

        # Predict
        predictions = model.predict(X_test)
        print(predictions)

        self.model = model

    def predict_floods(self, data):
        example = pd.DataFrame(data)
        predicted_floods = self.model.predict(example)
        return predicted_floods[0]
