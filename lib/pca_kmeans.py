# last edited: 02/17/2021
#
# The functions pca_initial, pca_initial_, pca_final, and pca_final_ are adapted
# from a post by Daniel Pelliccia here:
# https://nirpyresearch.com/classification-nir-spectra-principal-component-analysis-python/
#
# Retrieved in December 2020 and is licensed under Creative Commons Attribution 4.0
# International License. (https://creativecommons.org/licenses/by/4.0/)
#
#
# The function cluster_variance is adapted from a post by Cagri Aydogdu here:
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
    lab = data.values[:, 2].astype('uint8')

    # Read the features
    feat = (data.values[:, 3:]).astype('float32')

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

    return fig


def pca_initial_(data):  # Initial PCA function (no standardscaler)
    feat = (data.values[:, 3:]).astype('float64')
    ncom = 20

    # Initialise
    skpca1 = sk_pca(n_components=ncom)

    # Scale the features to have zero mean and standard devisation of 1
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

    return fig


def pca_final(data, ncomp):  # PCA fitting with scores as result

    # read spectra id
    lab = data.values[:, 2].astype('uint8')

    # Read the features
    feat = (data.values[:, 3:]).astype('float32')

    # Scale the features to have zero mean and standard devisation of 1
    # This is important when correlating data with very different variances
    nfeat1 = StandardScaler().fit_transform(feat)

    skpca1 = sk_pca(n_components=ncomp)

    # Transform on the scaled features
    Xt1 = skpca1.fit_transform(nfeat1)
    scores = pd.DataFrame(Xt1)

    return scores


def pca_final_(data, ncomp):  # PCA fitting with scores as result (no standardscaler)
    # Read the features
    feat = (data.values[:, 3:]).astype('float32')

    # Scale the features to have zero mean and standard devisation of 1
    # This is important when correlating data with very different variances

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

    fig = plt.figure(dpi=100)
    plt.plot(K, variances)
    plt.ylabel("Inertia ( Total Distance )")
    plt.xlabel("K Value")
    plt.xticks([i for i in range(1, n + 1)])

    return fig


def kmeans_(k, data):
    km_res = KMeans(n_clusters=k).fit(data)
    y_km = km_res.labels_
    clusters = km_res.cluster_centers_

    result = pd.DataFrame(y_km)

    return result, clusters


def gen_map(data, res_, cmap, dpi_):
    coord = pd.DataFrame(data[data.columns[0:2]])
    coord_cluster = coord.join(res_)
    coord_cluster.columns = ['x', 'y', 'c']

    grid_base = coord_cluster.pivot('y', 'x').values

    X = coord_cluster.x.unique()
    X.sort()

    Y = coord_cluster.y.unique()
    Y.sort()

    cMap = c.ListedColormap(cmap)

    fig = plt.figure(dpi=dpi_)
    plt.pcolormesh(X, Y, grid_base, shading='auto', cmap=cMap, alpha=0.7, figure=fig)
    plt.clim(0, np.max(grid_base))
    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    # plt.savefig('test.png', transparent=True)

    return fig


def res_vbose(data, res_):
    res_.columns = ['cluster']
    coord = pd.DataFrame(data)
    coord_cluster_ = coord.join(res_)

    return coord_cluster_


def clavg_fig(coord_cluster_, k, cmap, dpi_):
    mean_cl = []

    for i in range(k):
        mean_cl.append(np.mean(coord_cluster_.loc[coord_cluster_['cluster'] == i].iloc[:, 3:-1]) + 1 + (i * 2))

    fig = plt.figure(figsize=(15, 8), dpi=dpi_)
    for i in range(k):
        plt.plot(mean_cl[i].index.astype('float64'), mean_cl[i], label='Cluster ' + str(i), color=cmap[i], figure=fig)
    plt.xticks(np.arange(np.min(mean_cl[0].index.astype('float64')), np.max(mean_cl[0].index.astype('float64')), 70))
    plt.yticks([])
    plt.ylabel("Raman Intensity (a.u.)")
    plt.xlabel("Raman Shift (cm$^{-1}$)")
    plt.subplots_adjust(right=0.8)
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

    return fig

if __name__ == "__main__":
    print('Program not meant to run independently.')
