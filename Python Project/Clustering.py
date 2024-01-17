# Libraries
from keras.layers import Input, Dense
from keras.models import Model
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf


# region Read Excel file, convert to csv and save csv file
def convertExcelToCsv(fileDirectory, saveDirectory):
    data = pd.read_excel(fileDirectory)
    # Save the DataFrame to a CSV file
    data.to_csv(saveDirectory, index=False)


# endregion

# region Prepare csv file
def PrepareData(saveDirectory):
    data = pd.read_csv(filepath_or_buffer=saveDirectory, usecols=range(0, 50))
    data = data.dropna()
    data.to_csv(saveDirectory, index=False)


# endregion

# region Read CSV file
def readData_CheckForNA(filePath):
    data = pd.read_csv(filePath)
    print(data)
    rows_with_na = data[data.isna().any(axis=1)]

    num_rows_with_na = len(rows_with_na)
    print("Number of rows with missing values:", num_rows_with_na)
    return data


# endregion

# region Identify Clusters (K-Means)
def Clustering_Kmeans(dataset, num_clusters=4):
    # Standardize the data (mean=0, std=1) to ensure equal importance to all questions
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataset)

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    dataset['Cluster'] = kmeans.fit_predict(scaled_data)

    # Print cluster assignments and save results
    print(dataset[['Cluster']])  # Print cluster assignments
    dataset.to_csv('cluster_results_Kmeans.csv', index=False)  # Save cluster assignments


# endregion

# region Identify clusters (Cluster analysis with autoencoders)
def ClustersAnalysis(data, cluster_No, epoch_No, batchSize_No, activationFn, optimizerFn):
    # Normalize the data between 0 and 1
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data)

    # Create an autoencoder
    input_layer = Input(shape=(normalized_data.shape[1],))
    encoded_layer1 = Dense(128, activation=activationFn)(input_layer)  # Adjust layer size as needed
    encoded_layer2 = Dense(32, activation=activationFn)(encoded_layer1)  # Adjust layer size as needed
    encoded_layer3 = Dense(8, activation=activationFn)(encoded_layer2)  # Adjust layer size as needed
    # encoded_layer4 = Dense(32, activation=activationFn)(encoded_layer3)   # Adjust layer size as needed
    decoded = Dense(normalized_data.shape[1], activation='linear')(encoded_layer3)
    autoencoder = Model(input_layer, decoded)
    autoencoder.compile(optimizer=optimizerFn, loss='mean_squared_error')

    # Train the autoencoder
    history = autoencoder.fit(normalized_data, normalized_data, epochs=epoch_No, batch_size=batchSize_No, verbose=1)

    # Extract encoded features from the autoencoder
    encoded_features = autoencoder.predict(normalized_data)

    # Perform K-means clustering on the encoded features
    num_clusters = cluster_No  # Adjust as needed
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    cluster_assignments = kmeans.fit_predict(encoded_features)

    # Add the cluster assignments to the subset_data DataFrame
    data['Cluster'] = cluster_assignments

    # Print cluster assignments and save results
    print(data[['Cluster']])  # Print cluster assignments
    data.to_csv('cluster_results_autoencoder.csv', index=False)  # Save cluster assignments


def ClusterAnalysis2(data, cluster_No, epoch_No, batchSize_No, activationFn, optimizerFn):
    # Normalize the data
    scaler = StandardScaler()
    normalized_Data = scaler.fit_transform(data)

    # Build the neural network model
    # activation functions: relu, sigmoid, softmax (for output layer)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(normalized_Data.shape[1],)),  # 5 features for OCEAN
        tf.keras.layers.Dense(16, activation=activationFn),
        tf.keras.layers.Dense(8, activation=activationFn),
        tf.keras.layers.Dense(cluster_No, activation=activationFn),  # 4 clusters
    ])

    # Compile the model
    # Optimizers: adam, SGD,
    model.compile(optimizer=optimizerFn, loss='mse')  # Using MSE loss for unsupervised learning

    # Train the model
    model.fit(normalized_Data, normalized_Data, epochs=epoch_No, batch_size=batchSize_No)

    # Extract embeddings from the hidden layers
    embeddings = model.predict(normalized_Data)

    # Apply clustering algorithm to the embeddings (e.g., KMeans)
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(embeddings)
    print(cluster_labels)

    # Add the cluster assignments to the subset_data DataFrame
    data['Cluster'] = cluster_labels

    # Print cluster assignments and save results
    print(data[['Cluster']])  # Print cluster assignments
    data.to_csv('cluster_results.csv', index=False)  # Save cluster assignments


# endregion


# region Analyze clusters
def generateTotals(data):
    def Totals(colName):
        dataX = data[[col for col in data.columns if colName in col]].astype(int)
        dataX['Total'] = dataX.sum(axis=1)
        dataX['Cluster'] = data['Cluster']
        return dataX

    def Totals_ClusterMean(dataX, clusterNum):
        fData = dataX[dataX['Cluster'] == clusterNum]
        return fData['Total'].mean()

    OPN_data = Totals('OPN')
    CSN_data = Totals('CSN')
    EXT_data = Totals('EXT')
    AGR_data = Totals('AGR')
    EST_data = Totals('EST')
    print(f"OPN:\n{OPN_data}\n"
          f"CSN:\n{CSN_data}\n"
          f"EXT:\n{EXT_data}\n"
          f"AGR:\n{AGR_data}\n"
          f"EST:\n{EST_data}\n")

    C1_TotalsMeans = [Totals_ClusterMean(OPN_data, 0),
                      Totals_ClusterMean(CSN_data, 0),
                      Totals_ClusterMean(EXT_data, 0),
                      Totals_ClusterMean(AGR_data, 0),
                      Totals_ClusterMean(EST_data, 0)]
    C2_TotalsMeans = [Totals_ClusterMean(OPN_data, 1),
                      Totals_ClusterMean(CSN_data, 1),
                      Totals_ClusterMean(EXT_data, 1),
                      Totals_ClusterMean(AGR_data, 1),
                      Totals_ClusterMean(EST_data, 1)]
    C3_TotalsMeans = [Totals_ClusterMean(OPN_data, 2),
                      Totals_ClusterMean(CSN_data, 2),
                      Totals_ClusterMean(EXT_data, 2),
                      Totals_ClusterMean(AGR_data, 2),
                      Totals_ClusterMean(EST_data, 2)]
    C4_TotalsMeans = [Totals_ClusterMean(OPN_data, 3),
                      Totals_ClusterMean(CSN_data, 3),
                      Totals_ClusterMean(EXT_data, 3),
                      Totals_ClusterMean(AGR_data, 3),
                      Totals_ClusterMean(EST_data, 3)]

    print(C1_TotalsMeans, '\n',
          C2_TotalsMeans, '\n',
          C3_TotalsMeans, '\n',
          C4_TotalsMeans, '\n')

    clusterMeans = pd.DataFrame({
        'Trait': ['OPN', 'CSN', 'EXT', 'AGR', 'EST'],
        'C1': C1_TotalsMeans,
        'C2': C2_TotalsMeans,
        'C3': C3_TotalsMeans,
        'C4': C4_TotalsMeans,
    })
    return clusterMeans


def determineTraitScores(data):
    opn = ['OPN3', 'AGR2', 'OPN5', 'OPN7', 'OPN9', 'OPN10']
    csn = ['CSN1', 'CSN3', 'CSN5', 'CSN7', 'CSN9', 'CSN10', 'OPN9']
    ext = ['EXT1', 'EXT3', 'EXT5', 'EXT7', 'EXT9', 'AGR2', 'AGR10', 'CSN6', 'CSN9', 'OPN10']
    agr = ['AGR2', 'AGR4', 'AGR6', 'AGR8', 'AGR10']
    nrt = ['EST1', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10']

    data['OPN_Score'] = data[opn].sum(axis=1)
    data['CSN_Score'] = data[csn].sum(axis=1)
    data['EXT_Score'] = data[ext].sum(axis=1)
    data['AGR_Score'] = data[agr].sum(axis=1)
    data['N_Score'] = data[nrt].sum(axis=1)

    c1_opnMean = (data[data['Cluster'] == 0].mean())['OPN_Score']
    c2_opnMean = (data[data['Cluster'] == 1].mean())['OPN_Score']
    c3_opnMean = (data[data['Cluster'] == 2].mean())['OPN_Score']
    c4_opnMean = (data[data['Cluster'] == 3].mean())['OPN_Score']

    c1_csnMean = (data[data['Cluster'] == 0].mean())['CSN_Score']
    c2_csnMean = (data[data['Cluster'] == 1].mean())['CSN_Score']
    c3_csnMean = (data[data['Cluster'] == 2].mean())['CSN_Score']
    c4_csnMean = (data[data['Cluster'] == 3].mean())['CSN_Score']

    c1_extMean = (data[data['Cluster'] == 0].mean())['EXT_Score']
    c2_extMean = (data[data['Cluster'] == 1].mean())['EXT_Score']
    c3_extMean = (data[data['Cluster'] == 2].mean())['EXT_Score']
    c4_extMean = (data[data['Cluster'] == 3].mean())['EXT_Score']

    c1_agrMean = (data[data['Cluster'] == 0].mean())['AGR_Score']
    c2_agrMean = (data[data['Cluster'] == 1].mean())['AGR_Score']
    c3_agrMean = (data[data['Cluster'] == 2].mean())['AGR_Score']
    c4_agrMean = (data[data['Cluster'] == 3].mean())['AGR_Score']

    c1_nMean = (data[data['Cluster'] == 0].mean())['N_Score']
    c2_nMean = (data[data['Cluster'] == 1].mean())['N_Score']
    c3_nMean = (data[data['Cluster'] == 2].mean())['N_Score']
    c4_nMean = (data[data['Cluster'] == 3].mean())['N_Score']

    summary = (
        f'Cluster 1: \tOPN {int(c1_opnMean / (len(opn) * 5) * 100)}%\t\tCSN {int(c1_csnMean / (len(csn) * 5) * 100)}%\t\tEXT 'f'{int(c1_extMean / (len(ext) * 5) * 100)}%\t\tAGR {int(c1_agrMean / (len(agr) * 5) * 100)}%\t\tN {int(c1_nMean / (len(nrt) * 5) * 100)}%\n'
        f'Cluster 2: \tOPN {int(c2_opnMean / (len(opn) * 5) * 100)}%\t\tCSN {int(c2_csnMean / (len(csn) * 5) * 100)}%\t\tEXT 'f'{int(c2_extMean / (len(ext) * 5) * 100)}%\t\tAGR {int(c2_agrMean / (len(agr) * 5) * 100)}%\t\tN {int(c2_nMean / (len(nrt) * 5) * 100)}%\n'
        f'Cluster 3: \tOPN {int(c3_opnMean / (len(opn) * 5) * 100)}%\t\tCSN {int(c3_csnMean / (len(csn) * 5) * 100)}%\t\tEXT 'f'{int(c3_extMean / (len(ext) * 5) * 100)}%\t\tAGR {int(c3_agrMean / (len(agr) * 5) * 100)}%\t\tN {int(c3_nMean / (len(nrt) * 5) * 100)}%\n'
        f'Cluster 4: \tOPN {int(c4_opnMean / (len(opn) * 5) * 100)}%\t\tCSN {int(c4_csnMean / (len(csn) * 5) * 100)}%\t\tEXT 'f'{int(c4_extMean / (len(ext) * 5) * 100)}%\t\tAGR {int(c4_agrMean / (len(agr) * 5) * 100)}%\t\tN {int(c4_nMean / (len(nrt) * 5) * 100)}%\n'
    )

    print(summary)

    return data, summary


# endregion


if __name__ == "__main__":
    # --------------------Data Pre-processing---------------------------------------------------------------------------
    convertExcelToCsv('Big5PersonalityTraits.xlsx', 'Big5PersonalityTraits.csv')
    PrepareData('Big5PersonalityTraits.csv')

    # --------------------Cluster Analysis------------------------------------------------------------------------------
    # read pre-processed data and check for NA values if any
    pData = readData_CheckForNA('Big5PersonalityTraits.csv')

    # K-means clustering
    Clustering_Kmeans(pData, 4)
    # Autoencoder clustering
    ClustersAnalysis(pData, 4, 50, 32, 'relu', 'SGD')
    # Simple Neural Network Clustering
    ClusterAnalysis2(pData, 4, 50, 32, 'relu', 'SGD')

    # ----------------------Analyse results-----------------------------------------------------------------------------
    # Approach 1: Generate totals regardless of - or + scores
    # read saved clusters
    clusters_results_Kmeans = pd.read_csv('cluster_results_Kmeans.csv')
    clusters_results_autoencoder = pd.read_csv('cluster_results_autoencoder.csv')
    clusters_results = pd.read_csv('cluster_results.csv')
    # Generate totals
    Kmeans_Cluster_means = generateTotals(clusters_results_Kmeans)
    Autoencoder_Cluster_means = generateTotals(clusters_results_autoencoder)
    SimpleNN_Cluster_means = generateTotals(clusters_results)
    # Print Results
    print('\n\nApproach 1:')
    print('K-means cluster totals:')
    print(Kmeans_Cluster_means)
    print('\nAutoencoder cluster totals:')
    print(Autoencoder_Cluster_means)
    print('\nSimple Neural Network cluster totals:')
    print(SimpleNN_Cluster_means)

    # Approach 2: Totals considering - and + scores
    # Print cluster results
    print('\n\nApproach 2: ')
    print('K-Means:')
    clusters_results_Kmeans_withScores, summary_kmeans = determineTraitScores(clusters_results_Kmeans)
    with open('Clusters Summary_Kmeans', 'w') as file:
        file.write(summary_kmeans)

    print('\nAutoencoder: ')
    clusters_results_autoencoder_withScores, summary_autoencoder = determineTraitScores(clusters_results_autoencoder)
    with open('Clusters Summary_Autoencoder', 'w') as file:
        file.write(summary_autoencoder)

    print('\nSimple Neural Network: ')
    clusters_results_withScores, summary_autoencoder = determineTraitScores(clusters_results)
    with open('Clusters Summary', 'w') as file:
        file.write(summary_autoencoder)

    # print(clusters_results_Kmeans_withScores)
    # print(clusters_results_withScores)
    # clusters_results_withScores.to_csv('cluster_results_withScores.csv', index=False)
    # clusters_results_Kmeans_withScores.to_csv('cluster_results_Kmeans_withScores.csv', index=False)
