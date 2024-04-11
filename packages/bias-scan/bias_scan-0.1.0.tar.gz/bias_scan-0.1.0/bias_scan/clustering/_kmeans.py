from ._bahc import BiasAwareHierarchicalClustering
from sklearn.cluster import KMeans


class BiasAwareHierarchicalKMeans(BiasAwareHierarchicalClustering):
    """Bias-Aware Hierarchical k-Means Clustering.

    Parameters
    ----------
    max_iter : int
        Maximum number of iterations.
    min_cluster_size : int
        Minimum size of a cluster.
    kmeans_params : dict
        k-means parameters
    
    Attributes
    ----------
    n_clusters_ : int
        The number of clusters found by the algorithm.
    labels_ : ndarray of shape (n_samples,)
        Cluster labels for each point.
    biases_ : ndarray of shape (n_clusters_,)
        ???
    
    References
    ----------
    .. [1] J. Misztal-Radecka, B. Indurkhya, "Bias-Aware Hierarchical Clustering for detecting the discriminated
           groups of users in recommendation systems", Information Processing & Management, vol. 58, no. 3, May. 2021.
    
    Examples
    --------
    >>> from bias_scan.clustering import BiasAwareHierarchicalKMeans
    """

    def __init__(
        self,
        max_iter,
        min_cluster_size,
        kmeans_params={"n_clusters": 2, "n_init": "auto"},
    ):
        super().__init__(max_iter, min_cluster_size)
        self.kmeans = KMeans(**kmeans_params)

    def _split(self, X):
        return self.kmeans.fit_predict(X)
