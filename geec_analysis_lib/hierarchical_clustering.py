import numpy
import clustering
import warnings
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score

class HierarchicalClustering(clustering.Clustering):
    def __init__(self, matrix, linkage_method):
        self.matrix = matrix
        self.linkage_method = linkage_method
        self.fcluster_criterion = 'maxclust'

        if len(matrix) > 1:
            self.linkage_matrix = self._linkage(matrix, linkage_method)
        else:
            self.linkage_matrix = numpy.array([])

    @property
    def clustering_algorithm(self):
        return 'hierarchical'

    def run(self, wanted_nb_clusters=None):
        if len(self.linkage_matrix) == 0:
            return 1, [1], self.linkage_matrix

        if wanted_nb_clusters is None:
            flat_cluster = self._find_best_flat_clusters(self.linkage_matrix)
        else:
            flat_cluster = self._fcluster(self.linkage_matrix, wanted_nb_clusters, self.fcluster_criterion)

        nb_clusters = len(set(flat_cluster))

        return nb_clusters, flat_cluster, self.linkage_matrix

    def _find_best_flat_clusters(self, linkage_matrix):
        maximum = 21
        if maximum > len(self.matrix):
            maximum = len(self.matrix)

        best_nb_clusters = (-1.0, 2, range(len(self.matrix)))
        for i in xrange(2, maximum):
            flat_cluster = self._fcluster(linkage_matrix, i, self.fcluster_criterion)
            silhouette_avg = silhouette_score(self.matrix.get_matrix(), flat_cluster)
            if best_nb_clusters[0] < silhouette_avg:
                best_nb_clusters = (silhouette_avg, i, flat_cluster)

        return best_nb_clusters[2]

    def _linkage(self, matrix, linkage_method):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return linkage(matrix.to_distance().get_matrix(), linkage_method)

    def _fcluster(self, linkage_matrix, asked_nb_clusters, fcluster_criterion):
        return fcluster(linkage_matrix, asked_nb_clusters, fcluster_criterion)