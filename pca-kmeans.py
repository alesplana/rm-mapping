import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from scipy.signal import savgol_filter
from sklearn.decomposition import PCA as sk_pca
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.cluster import KMeans
from matplotlib import colors as c


data = pd.read_csv('new_file2.csv')

lab = data.values[:, 3].astype('uint8')

# Read the features (scans) and transform data from reflectance to absorbance
feat = (data.values[:,4:]).astype('float32')

# Calculate first derivative applying a Savitzky-Golay filter
dfeat = savgol_filter(feat, 25, polyorder = 5, deriv=1)

# Initialise
skpca1 = sk_pca(n_components=20)
skpca2 = sk_pca(n_components=20)

# Scale the features to have zero mean and standard devisation of 1
# This is important when correlating data with very different variances
nfeat1 = StandardScaler().fit_transform(feat)
nfeat2 = StandardScaler().fit_transform(dfeat)

# Fit the spectral data and extract the explained variance ratio
X1 = skpca1.fit(nfeat1)
expl_var_1 = X1.explained_variance_ratio_

# Fit the first data and extract the explained variance ratio
X2 = skpca2.fit(nfeat2)
expl_var_2 = X2.explained_variance_ratio_

# Plot data
plt.bar(range(ncom),expl_var_1, label="Explained Variance %", color='blue')
plt.plot(np.cumsum(expl_var_1),'-o', label = 'Cumulative variance %')
plt.xlabel("PC number")
# plt.title('Absorbance data')
plt.legend()
plt.show()

skpca1 = sk_pca(n_components=2)
# Transform on the scaled features
Xt1 = skpca1.fit_transform(nfeat1)


score_1 = skpca1.score_samples(nfeat1)

scores = pd.DataFrame(Xt1)

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
plt.savefig('test.png', transparent=True)