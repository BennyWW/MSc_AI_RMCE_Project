# Libraries
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


# region Load Cluster results
def loadData():
    # Load the dataset from CSV file
    df = pd.read_csv('cluster_results.csv')
    x = df.iloc[:, :50]
    y = df['Cluster']
    print(f'X:\n{x}')
    print(f'Y:\n{y}')

    # Encode the target variable using LabelEncoder
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    return x, y


# endregion

# region Train an Artificial Neural Network model
def TrainModel(ANN_PredictionModel_path, modelAccuracy_path):
    # Step 1: Load the data
    DataVar, targetVar = loadData()
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(DataVar, targetVar, test_size=0.2, random_state=42)

    # Step 2: Build the Artificial Neural Network
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(50,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')  # 4 output neurons for cluster numbers
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Step 3: Train the model
    model.fit(X_train, y_train, epochs=100, batch_size=64, validation_split=0.2)

    # Step 4: Evaluate the model
    # Predict cluster numbers for the testing set
    y_pred = model.predict(X_test)

    # Convert the predicted probabilities to cluster numbers
    predicted_clusters = tf.argmax(y_pred, axis=1).numpy()

    # Calculate the model accuracy
    accuracy = accuracy_score(y_test, predicted_clusters)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    accuracyStats = f"ANN Model prediction accuracy: {accuracy * 100:.2f}%"
    with open(modelAccuracy_path, 'w') as file:
        file.write(accuracyStats)

    # Step 5: Save the model
    model.save(ANN_PredictionModel_path + '.h5')


# endregion

# region Prediction
def PredictCluster(ANN_PredictionModel_path, newData):
    # Define testData if newData is empty (provides a default test data)
    if not newData:
        # Use a default
        testData = np.array([4.0, 1.0, 5.0, 2.0, 5.0, 1.0, 5.0, 2.0, 4.0, 1.0,
                             1.0, 4.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 2.0,
                             2.0, 5.0, 2.0, 4.0, 2.0, 3.0, 2.0, 4.0, 3.0, 4.0,
                             3.0, 4.0, 3.0, 2.0, 2.0, 4.0, 4.0, 2.0, 4.0, 4.0,
                             5.0, 1.0, 4.0, 1.0, 4.0, 1.0, 5.0, 3.0, 4.0, 5.0])
    else:
        testData = np.array(newData)

    # Define the columns for the new data
    column_names = ['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10',
                    'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10',
                    'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10',
                    'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10',
                    'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10']

    # Convert the NumPy array to a DataFrame with the column names
    newData = pd.DataFrame(testData.reshape(1, -1), columns=column_names)

    # Display the DataFrame
    print(newData)

    # Load the prediction model
    loaded_model = tf.keras.models.load_model(ANN_PredictionModel_path)

    # Show model summary/architecture
    loaded_model.summary()

    # Make predictions on the new data
    predictions = loaded_model.predict(newData)

    # Get the predicted class for each data point
    predicted_classes = tf.argmax(predictions, axis=1).numpy()

    # Print predicted cluster
    print(f'Predicted Cluster: Cluster {predicted_classes[0]}')

    return predicted_classes[0]


# region Testing
def Testing():
    newData = [1.0, 5.0, 3.0, 5.0, 2.0, 3.0, 2.0, 4.0, 5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 5.0,
               3.0, 5.0, 1.0, 5.0, 3.0, 4.0, 2.0, 3.0, 2.0, 2.0, 5.0, 1.0, 5.0, 1.0, 4.0, 3.0, 4.0, 2.0, 2.0, 3.0, 1.0,
               3.0, 1.0, 3.0, 3.0, 4.0, 3.0, 3.0, 3.0]

    random_list = [random.randint(1, 5) for _ in range(50)]
    # print(random_list)

    PredictCluster('ANN_PredictionModel.h5', newData)
    # PredictCluster('ANN_PredictionModel.h5', random_list)
    return


# endregion

if __name__ == "__main__":
    # TrainModel('ANN_PredictionModel', 'ANN_ModelAccuracy')
    Testing()
