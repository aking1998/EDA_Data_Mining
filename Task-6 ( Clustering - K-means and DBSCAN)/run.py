"""
Question 1: K-Means Clustering
The file specs/question_1.csv contains coordinates of 2-dimensional (x and y) points with
their original cluster labels (org_cluster). Write a Python script that:
1. Visualise the original data points with different colours for their original cluster labels in
a scatter plot. Save the plot into output/question_1_1.pdf.
2. Using x and y, use the k-means algorithm to cluster the dataset into x (from 1 to 10)
number of clusters. If you are using sklearn, set a fixed random state to 0. Plot inertia
(within cluster sum of squares) against the number of clusters. What is the best number
of clusters for this data? Save the plot into output/question_1_2.pdf
3. Calculate the Rand Index as an extrinsic measure (i.e. when are know the original/groudtruth
clusters), and Silhouette Score as an intrinsic measure (unsupervised) for the given
dataset with 3 clusters.
2
4. Save the input data with an extra column that contains the labels generated by K-Means
into a file called output/question_1.csv. The new column should be called
cluster_kmeans.
5. Plots the clustering results (including the centroids) as in Q1.1 and save into
output/question_1_5.pdf. Make sure that new clusters are marked with the same
colours of the corresponding original clusters).
"""
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.metrics.cluster import rand_score,silhouette_score


df = pd.read_csv("./specs/question_1.csv")

scaler = MinMaxScaler()
scaler.fit(df[['x']])
df['x'] = scaler.transform(df[['x']])           # Normalising data
scaler.fit(df[['y']])
df['y'] = scaler.transform(df[['y']])
print(df.head())

df1 = df[df.org_cluster==0]
df2 = df[df.org_cluster==1]
df3 = df[df.org_cluster==2]
plt.scatter(df1.x,df1.y,color='green')
plt.scatter(df2.x,df2.y,color='red')
plt.scatter(df3.x,df3.y,color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig("output/question_1_1.pdf",format='pdf')
plt.show()

km = KMeans(n_clusters=3, random_state=0)        # K-means Algorithm
y_predicted = km.fit_predict(df[['x','y']])
df['cluster_kmeans'] = y_predicted
print(df.head())

df1 = df[df.cluster_kmeans==0]
df2 = df[df.cluster_kmeans==1]                   # Plotting graph
df3 = df[df.cluster_kmeans==2]
plt.scatter(df1.x,df1.y,color='green')
plt.scatter(df2.x,df2.y,color='red')
plt.scatter(df3.x,df3.y,color='blue')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig("output/question_1_5.pdf",format='pdf')
plt.show()

sse = []
k_rng = range(1,10)
for k in k_rng:                                 # Elbow Plot
    km = KMeans(n_clusters=k)
    km.fit(df[['x','y']])
    sse.append(km.inertia_)

plt.xlabel('Number of Clusters')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)
plt.savefig("output/question_1_2.pdf",format='pdf')
plt.show()


print(rand_score(df['org_cluster'], df['cluster_kmeans']))                         # Rand Index
 
print(silhouette_score(df[['x','y']],y_predicted))                                 # Silhouette Score

df.to_csv('./output/question_1.csv', index=False)

"""
Question 2: K-Means Clustering
The file specs/question_2.csv contains data related to nutritional content of several cereal
brands.
1. Discard the columns NAME, MANUF, TYPE, and RATING.
2. Run the k-means algorithm using 5 clusters as a target, 5 maximum runs, and 100
maximum optimization steps. Keep the random state to 0. Save the cluster labels in a
new column called config1.
3. Run k-means again, but this time use 100 maximum runs and 100 maximum optimization
steps. Again, use a random state of 0. Save the cluster labels in a new column called
config2.
4. Are the clustering results obtained with the first configuration different from the results
obtained with the second configuration? Explain your answer in your report.
5. Run the clustering algorithm again, but this time use only 3 clusters. Save the generated
cluster labels in a new column called config3.
6. Which clustering solution is better? Discuss it in your report.
7. Save the input data with the newly generated columns into a file called
output/question_2.csv.
"""

df = pd.read_csv("./specs/question_2.csv")

df.drop(['NAME', 'MANUF', 'TYPE', 'RATING'], axis=1, inplace=True)                 # Removing inappropriate columns
print(df.head())


X = np.array(df)


kmeans = KMeans(n_clusters=5,n_init=5, max_iter=100, random_state=0).fit(X)         # k-means execution
df["config1"] = kmeans.labels_ 
print(df.head())
print(silhouette_score(df,df["config1"])) 

kmeans = KMeans(n_clusters=5, n_init=100, max_iter=100, random_state=0).fit(X)
df["config2"] = kmeans.labels_
print(df.head())
print(silhouette_score(df,df["config2"])) 

kmeans = KMeans(n_clusters=3, n_init=100, max_iter=100, random_state=0).fit(X)
df["config3"] = kmeans.labels_
print(df.head())
print(silhouette_score(df,df["config3"])) 

df.to_csv('./output/question_2.csv', index=False)

"""
Question 3: DBSCAN Clustering Algorithm
The file specs/question_3.csv contains coordinates of 2-dimensional points. Write a
Python script to perform the following tasks.
1. Discard the ID column, the use the X and Y coordinates as data input to the K-Means
algorithm to cluster it into 7 clusters. Perform 5 maximum runs, and 100 maximum
optimization steps. Keep a random state to 0. Save the cluster labels into a new column
called k-means. Discuss the results in your report.
2. Plot the generated clusters and save the plot in a file called ./output/question_3_1.pdf.
3. Normalize the X and Y columns in a range between 0 and 1, then use the DBSCAN
algorithm to cluster the points again. Use a value of 0.4 for epsilon, and set the
3
minimum points equals to 4. Save the generated plot in a file, called
./output/question_3_2.pdf, and save the cluster labels into a new column called
dbscan1.
4. Execute DBSCAN again, but this time use a value of 0.08 for epsilon. Plot the generated
clusters in a file called ./output/question_3_3.pdf, and save the cluster labels into a
new column called dbscan2.
5. Save the data with the cluster labels in a file called ./output/question_3.csv.
"""


df = pd.read_csv("./specs/question_3.csv")


df.drop(['ID'], axis=1, inplace=True)
print(df.head())


X = np.array(df)


kmeans = KMeans(n_clusters=7,n_init=5, max_iter=100, random_state=0).fit(X)
df["kmeans"] = kmeans.labels_
print(df.head())

plt.scatter(df.x, df.y , c=df["kmeans"])
plt.xlabel('x')
plt.ylabel('y')
plt.savefig("output/question_3_1.pdf",format='pdf')
plt.show()

scaler = MinMaxScaler()                                              # Normalising data
scaler.fit(df[['x']])
df['x'] = scaler.transform(df[['x']])
scaler.fit(df[['y']])
df['y'] = scaler.transform(df[['y']])



clustering = DBSCAN(eps=0.4, min_samples=4).fit(df[['x','y']])       # Applying DBSCAN Algorithm
df['dbscan1'] = clustering.labels_
print(df.head())

plt.scatter(df.x, df.y , c=clustering.labels_)                       # Plotting graphs 
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("output/question_3_2.pdf",format='pdf')
plt.show()

clustering_new = DBSCAN(eps=0.08, min_samples=4).fit(df[['x','y']])
df['dbscan2'] = clustering_new.labels_
print(df.head())

plt.scatter(df.x, df.y , c=clustering_new.labels_)
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("output/question_3_3.pdf",format='pdf')
plt.show()

df.to_csv('./output/question_3.csv', index=False)


