# The functions pca_initial, pca_initial_, pca_final, and pca_final_ are adapted
# from a post by Daniel Pelliccia here:
# https://nirpyresearch.com/classification-nir-spectra-principal-component-analysis-python/
#
# Retrieved in December 2020 and is licensed under Creative Commons Attribution 4.0
# International License. (https://creativecommons.org/licenses/by/4.0/)
#
#
# The function cluster_variance is adapted from a post by Çağrı Aydoğdu here:
# https://medium.com/analytics-vidhya/choosing-the-best-k-value-for-k-means-clustering-d8b4616f8b86
#
# Retrieved in December 2020.



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA as sk_pca
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import colors as c


def pca_initial(data):  # Initial PCA function

    # read spectra id
    lab = data.values[:, 3].astype('uint8')

    # Read the features
    feat = (data.values[:, 4:]).astype('float32')

    # Initialise
    skpca1 = sk_pca(n_components=20)

    # Scale the features to have zero mean and standard deviation of 1
    # This is important when correlating data with very different variances
    nfeat1 = StandardScaler().fit_transform(feat)

    # Fit the spectral data and extract the explained variance ratio
    X1 = skpca1.fit(nfeat1)
    expl_var_1 = X1.explained_variance_ratio_

    # create scree plot

    fig = plt.figure(dpi=100)
    plt.bar(range(20), expl_var_1, label="Explained Variance %", color='blue', figure=fig)
    plt.xticks(np.arange(len(expl_var_1)), np.arange(1, len(expl_var_1) + 1))
    plt.plot(np.cumsum(expl_var_1), '-o', label='Cumulative variance %', color='green', figure=fig)
    plt.xlabel('PC Number')
    plt.legend()
    '''
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).bar(range(20), expl_var_1, label="Explained Variance %", color='blue')
    fig.add_subplot(111).plot(np.cumsum(expl_var_1), '-o', label='Cumulative variance %', color='green')
    fig.add_subplot(111).set_xlabel("PC number")
    fig.add_subplot(111).legend()
    '''
    return fig


def pca_initial_(data):  # Initial PCA function (no standardscaler)

    # read spectra id
    lab = data.values[:, 3].astype('uint8')

    # Read the features
    feat = (data.values[:, 4:]).astype('float32')

    # Initialise
    skpca1 = sk_pca(n_components=20)

    # Scale the features to have zero mean and standard deviation of 1
    # This is important when correlating data with very different variances
    # nfeat1 = StandardScaler().fit_transform(feat)

    # Fit the spectral data and extract the explained variance ratio
    X1 = skpca1.fit(feat)
    expl_var_1 = X1.explained_variance_ratio_

    # create scree plot

    fig = plt.figure(dpi=100)
    plt.bar(range(20), expl_var_1, label="Explained Variance %", color='blue', figure=fig)
    plt.xticks(np.arange(len(expl_var_1)), np.arange(1, len(expl_var_1) + 1))
    plt.plot(np.cumsum(expl_var_1), '-o', label='Cumulative variance %', color='green', figure=fig)
    plt.xlabel('PC Number')
    plt.legend()
    '''
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).bar(range(20), expl_var_1, label="Explained Variance %", color='blue')
    fig.add_subplot(111).plot(np.cumsum(expl_var_1), '-o', label='Cumulative variance %', color='green')
    fig.add_subplot(111).set_xlabel("PC number")
    fig.add_subplot(111).legend()
    '''
    return fig


def pca_final(data, ncomp):  # PCA fitting with scores as result

    # read spectra id
    lab = data.values[:, 3].astype('uint8')

    # Read the features
    feat = (data.values[:, 4:]).astype('float32')

    # Scale the features to have zero mean and standard devisation of 1
    # This is important when correlating data with very different variances
    nfeat1 = StandardScaler().fit_transform(feat)

    skpca1 = sk_pca(n_components=ncomp)

    # Transform on the scaled features
    Xt1 = skpca1.fit_transform(nfeat1)
    scores = pd.DataFrame(Xt1)

    return scores


def pca_final_(data, ncomp):  # PCA fitting with scores as result (no standardscaler)

    # read spectra id
    lab = data.values[:, 3].astype('uint8')

    # Read the features
    feat = (data.values[:, 4:]).astype('float32')

    # Scale the features to have zero mean and standard devisation of 1
    # This is important when correlating data with very different variances
    # nfeat1 = StandardScaler().fit_transform(feat)

    skpca1 = sk_pca(n_components=ncomp)

    # Transform on the scaled features
    Xt1 = skpca1.fit_transform(feat)
    scores = pd.DataFrame(Xt1)

    return scores


def cluster_variance(data_):
    n = 10
    variances = []
    kmeans = []
    outputs = []
    K = [i for i in range(1, n + 1)]

    for i in range(1, n + 1):
        variance = 0
        model = KMeans(n_clusters=i, random_state=82, verbose=0).fit(data_)
        kmeans.append(model)
        variances.append(model.inertia_)
    # variances,K,n=cluster_variance(10)

    plt.plot(K, variances)
    plt.ylabel("Inertia ( Total Distance )")
    plt.xlabel("K Value")
    plt.xticks([i for i in range(1, n + 1)])
    plt.show()


def kmeans_(k, data):
    km_res = KMeans(n_clusters=k).fit(data)
    y_km = km_res.labels_
    clusters = km_res.cluster_centers_

    result = pd.DataFrame(y_km)

    return result, clusters


def gen_map(data, res_, cmap):
    coord = pd.DataFrame(data[data.columns[1:3]])
    coord_cluster = coord.join(res_)
    coord_cluster.columns = ['x', 'y', 'c']

    grid_base = coord_cluster.pivot('y', 'x').values

    X = coord_cluster.x.unique()
    X.sort()

    Y = coord_cluster.y.unique()
    Y.sort()

    cMap = c.ListedColormap(cmap)
    fig = plt.figure(dpi=100)
    plt.pcolormesh(X, Y, grid_base, shading='auto', cmap=cMap, alpha=0.5, figure=fig)
    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    # plt.savefig('test.png', transparent=True)

    return fig


'''
km_res = KMeans(n_clusters=2).fit(scores)
clusters = km_res.cluster_centers_

plt.scatter(scores[0],scores[1])
plt.scatter(clusters[:,0],clusters[:,1],s=10000,alpha=0.7)

y_km = KMeans(n_clusters=2).fit_predict(scores)
plt.scatter(scores[y_km == 0][0], scores[y_km == 0][1], s=80, color='red')
plt.scatter(scores[y_km == 1][0], scores[y_km == 1][1], s=80, color='blue')

result = pd.DataFrame(y_km)
result.to_csv('res.csv', index=True)


# convert to grid type data
coord = pd.DataFrame(data[data.columns[1:3]])
coord_cluster = coord.join(result)
coord_cluster.columns = ['x','y','c']

grid_base = coord_cluster.pivot('y','x').values

X = coord_cluster.x.unique()
X.sort()

Y = coord_cluster.y.unique()
Y.sort()

cMap = c.ListedColormap(['gray', 'blue'])
plt.pcolormesh(X, Y, grid_base, shading='auto', cmap=cMap, alpha=0.5)
plt.gca().set_aspect('equal')
plt.gca().invert_yaxis()
plt.savefig('test.png', transparent=True)

'''
