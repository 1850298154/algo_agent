import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture

# 1. 生成3个数据集
# 数据集A：3个凸形聚类，无噪声
X_A, y_A = make_blobs(n_samples=200, n_features=2, centers=3, cluster_std=0.6, random_state=42)
# 数据集B：2个非凸环形聚类，含噪声
X_B, y_B = make_circles(n_samples=200, noise=0.05, factor=0.3, random_state=42)
# 数据集C：2个凸形聚类，加10个异常值
X_C, y_C = make_blobs(n_samples=190, n_features=2, centers=2, cluster_std=0.5, random_state=42)
outliers = np.random.uniform(low=-10, high=10, size=(10, 2))  # 异常值
X_C = np.vstack((X_C, outliers))

# 2. 可视化数据集
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].scatter(X_A[:, 0], X_A[:, 1], c='lightblue', edgecolor='black')
axes[0].set_title('数据集A（凸形聚类，无噪声）')
axes[1].scatter(X_B[:, 0], X_B[:, 1], c='lightgreen', edgecolor='black')
axes[1].set_title('数据集B（非凸环形聚类，含噪声）')
axes[2].scatter(X_C[:190, 0], X_C[:190, 1], c='lightcoral', edgecolor='black', label='主簇')
axes[2].scatter(X_C[190:, 0], X_C[190:, 1], c='gray', edgecolor='black', label='异常值')
axes[2].legend()
axes[2].set_title('数据集C（含异常值的凸聚类）')
plt.show()

# 3. 聚类并可视化（以数据集B为例，对比K-Means和DBSCAN）
kmeans = KMeans(n_clusters=2, random_state=42)
dbscan = DBSCAN(eps=0.2, min_samples=5)  # eps：邻域半径，min_samples：核心点最小样本数

y_kmeans_B = kmeans.fit_predict(X_B)
y_dbscan_B = dbscan.fit_predict(X_B)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(X_B[:, 0], X_B[:, 1], c=y_kmeans_B, cmap='coolwarm', edgecolor='black')
axes[0].set_title('K-Means聚类（数据集B）—— 错误划分')
axes[1].scatter(X_B[:, 0], X_B[:, 1], c=y_dbscan_B, cmap='coolwarm', edgecolor='black')
axes[1].set_title('DBSCAN聚类（数据集B）—— 正确划分（灰色为噪声）')
plt.show()