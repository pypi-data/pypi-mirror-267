def dbscan():
    code = """

    from sklearn.cluster import DBSCAN
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_circles
    # Sample data
    X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])

    # Visualize sample data
    plt.scatter(X[:, 0], X[:, 1])
    plt.show()

    # DBSCAN clustering
    db = DBSCAN(eps=10, min_samples=2)
    db.fit(X)
    db.labels_

    # Create a concentric circle dataset
    X, _ = make_circles(n_samples=500, factor=.5, noise=.03, random_state=4)

    # Apply DBSCAN to the dataset
    dbscan = DBSCAN(eps=0.1, min_samples=5)
    clusters = dbscan.fit_predict(X)

    # Plotting
    plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.title("DBSCAN Clustering of Concentric Circles")
    plt.xlabel("Feature 0")
    plt.ylabel("Feature 1")
    plt.show()
    """
    print(code)




def hierarchical():
    code = """

    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import scipy.cluster.hierarchy as shc
    from sklearn.cluster import AgglomerativeClustering

    # Load customer data
    customer_data = pd.read_csv('.csv')

    # Extract relevant columns
    data = customer_data.iloc[:, 3:5].values

    # Visualize dendrogram
    plt.figure(figsize=(10, 7))
    plt.title("Customer Dendograms")
    dend = shc.dendrogram(shc.linkage(data, method='ward'))

    # Perform Agglomerative Clustering
    cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
    labels_ = cluster.fit_predict(data)

    # Visualize clustered data
    plt.figure(figsize=(10, 7))
    plt.scatter(data[:, 0], data[:, 1], c=cluster.labels_, cmap='rainbow')
    plt.show()
    """
    print(code)


def kmeans():

    code = """

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans

    # Loading data
    data = pd.read_csv('.csv')
    data = data.drop([''], axis=1)

    # Handling missing values
    data.isna().sum()

    # Encoding categorical variables
    mapping = {'': 0, '': 1, '': 2, '': 3}
    data[''] = data[''].map(mapping)

    # KMeans clustering
    kmeans = KMeans(n_clusters=2, random_state=42)

    def plot_data(X):
        plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2)

    def plot_centroids(centroids, weights=None, circle_color='w', cross_color='k'):
        if weights is not None:
            centroids = centroids[weights > weights.max() / 10]
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='o', s=35, linewidths=8,
                    color=circle_color, zorder=10, alpha=0.9)
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=2, linewidths=12,
                    color=cross_color, zorder=11, alpha=1)

    def plot_decision_boundaries(clusterer, X, resolution=1000, show_centroids=True,
                                 show_xlabels=True, show_ylabels=True):
        mins = X.min(axis=0) - 0.1
        maxs = X.max(axis=0) + 0.1
        xx, yy = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                             np.linspace(mins[1], maxs[1], resolution))
        Z = clusterer.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        plt.contourf(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                    cmap="Pastel2")
        plt.contour(Z, extent=(mins[0], maxs[0], mins[1], maxs[1]),
                    linewidths=1, colors='k')
        plot_data(X)
        if show_centroids:
            plot_centroids(clusterer.cluster_centers_)

        if show_xlabels:
            plt.xlabel("$x_1$", fontsize=14)
        else:
            plt.tick_params(labelbottom=False)
        if show_ylabels:
            plt.ylabel("$x_2$", fontsize=14, rotation=0)
        else:
            plt.tick_params(labelleft=False)

    def plot_clusterer_comparison(clusterer1, clusterer2, X, title1=None, title2=None):
        clusterer1.fit(X)
        clusterer2.fit(X)

        plt.figure(figsize=(12, 8))

        plt.subplot(121)
        plot_decision_boundaries(clusterer1, X)
        if title1:
            plt.title(title1, fontsize=14)

        plt.subplot(122)
        plot_decision_boundaries(clusterer2, X, show_ylabels=False)
        if title2:
            plt.title(title2, fontsize=14)

    # Fit the model to the data
    kmeans.fit(data)

    # Get cluster centroids
    centroids = kmeans.cluster_centers_
    print("Cluster centroids:")
    print(centroids)

    # Get cluster labels for each data point
    labels = kmeans.labels_
    print("\nCluster labels:")
    print(labels)

    plt.figure(figsize=(12, 8))
    plot_decision_boundaries(kmeans, data)
    plt.title('K-Means decision boundaries (Voronoi tessellation)')
    plt.show()

    # Plotting cluster comparison
    kmeans_k3 = KMeans(n_clusters=3, random_state=42)
    kmeans_k8 = KMeans(n_clusters=8, random_state=42)

    plot_clusterer_comparison(kmeans_k3, kmeans_k8, data, "$k=3$", "$k=8$")
    plt.show()

    # Elbow method
    kmeans_per_k = [KMeans(n_clusters=k, random_state=42).fit(data) for k in range(1, 10)]
    inertias = [model.inertia_ for model in kmeans_per_k]

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 10), inertias, "bo-")
    plt.xlabel("$k$", fontsize=14)
    plt.ylabel("Inertia", fontsize=14)
    plt.annotate('Elbow',
                 xy=(4, inertias[3]),
                 xytext=(0.55, 0.55),
                 textcoords='figure fraction',
                 fontsize=16,
                 arrowprops=dict(facecolor='black', shrink=0.1)
                )
    plt.axis([1, 8.5, 0, 1300])
    plt.title('The Elbow Diagram')
    plt.show()
    """
    print(code)

