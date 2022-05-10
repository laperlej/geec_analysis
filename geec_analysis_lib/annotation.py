from itertools import *
from geec_analysis_lib.clusters import Clusters, Cluster
from geec_analysis_lib.categories import Categories, Category, Tags, Tag
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings("ignore")
import scipy.cluster.hierarchy as sch
import numpy
import config
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

DESCRIPTION = '{matrix_description},\nclusteringAlgorithm={clustering_algorithm}, linkageMethod={linkage_method}'

class Annotation:
    def __init__(self, matrix, metadata, nb_clusters, flat_cluster, linkage_matrix, categories, linkage_method, clustering_algorithm):
        self.matrix = matrix
        self.metadata = metadata
        self.nb_clusters = nb_clusters
        self.flat_cluster = flat_cluster
        self.linkage_matrix = linkage_matrix
        self._linkage_method = linkage_method
        self._clustering_algorithm = clustering_algorithm
        self.remapped_clusters = self._remap_clusters()
        self.ordered_matrix = self._reorder_matrix()
        clusters = self._make_clusters()
        self.comparison = _Comparison(clusters, categories)

        if not metadata.key_intersection(matrix.get_file_names()):
            logger.warning("There's no match between the matrix and the metadata.")

    @property
    def description(self):
        return DESCRIPTION.format(
            matrix_description=self.matrix.description,
            clustering_algorithm=self.clustering_algorithm,
            linkage_method=self.linkage_method
        )

    def obtain_size_of_tags_in_category(self, category_name):
        return self.comparison.obtain_size_of_tags_in_category(category_name)

    def obtain_file_names_with_tag_name(self, tag_name):
        return self.comparison.obtain_file_names_with_tag_name(tag_name)

    def obtain_cluster_name(self, cluster_id):
        return self.comparison.obtain_cluster_name(cluster_id)

    def obtain_size_of_tags_from_tag_names(self, cluster_id, category_name, tag_names):
        return self.comparison.obtain_size_of_tags_from_tag_names(cluster_id, category_name, tag_names)

    def obtain_file_names_tag_names(self, category_name):
        return self.comparison.obtain_file_names_tag_names(category_name)

    def obtain_ordered_tag_names(self, category_name):
        file_names_tag_names = self.comparison.obtain_file_names_tag_names(category_name)
        return [file_names_tag_names[file_name]
                for file_name in self.matrix.get_file_names()]

    def obtain_clusters(self):
        return self.comparison.obtain_clusters()

    @property
    def linkage_method(self):
        return self._linkage_method

    @property
    def clustering_algorithm(self):
        return self._clustering_algorithm

    def get_nb_clusters(self):
        return self.nb_clusters

    def get_linkage_matrix(self):
        return self.linkage_matrix

    def get_matrix(self):
        return self.matrix

    def get_ordered_matrix(self):
        return self.ordered_matrix

    def get_file_names(self):
        return self.matrix.get_file_names()

    def get_remapped_clusters(self):
        return self.remapped_clusters

    def get_metadata(self):
        return self.metadata

    def _make_dendrogram(self, flat_cluster):
        return sch.dendrogram(self.linkage_matrix,
                              color_threshold=self.compute_color_threshold(),
                              orientation=config.DENDROGRAM_ORIENTATION,
                              distance_sort='descending',
                              labels=numpy.asarray(flat_cluster))

    def make_dendrogram(self):
        return self._make_dendrogram(self.remapped_clusters)

    def __len__(self):
        return len(self.matrix)

    def compute_color_threshold(self):
        return self.linkage_matrix[-(self.nb_clusters-1),2]

    def _reorder_matrix(self):
        file_names = self.matrix.get_file_names()
        Z = self._make_dendrogram(self.flat_cluster)
        return self.matrix.sub_matrix(reversed([file_names[leaf] for leaf in Z['leaves']]))

    def _remap_clusters(self):
        Z = self._make_dendrogram(self.flat_cluster)

        visual_cluster_order = self._obtain_order(reversed(Z['ivl']))
        flat_cluster_order = range(1, self.nb_clusters + 1) # [1..n]

        remap_dict = {fco:vso for fco,vso in izip(visual_cluster_order, flat_cluster_order)}

        return [remap_dict[x] for x in self.flat_cluster]

    def _obtain_order(self, elements):
        inside = set()

        def add_if_not_inside(x):
            if x in inside:
                return False
            else:
                inside.add(x)
                return True

        return filter(add_if_not_inside, elements)

    def _make_clusters(self):
        return Clusters.make_clusters(self.remapped_clusters, self.matrix.get_file_names())

    def annotation_datagrid_iter(self, categories_names):
        file_names = self.ordered_matrix.get_file_names()
        datasets = self.ordered_matrix.get_file_names()

        for file_name, dataset in izip(file_names, datasets):
            yield ([dataset, self.comparison.obtain_cluster_name_by_file_name(file_name)] + 
                   self.metadata.obtain_formated_dataset(file_name, categories_names))

    @staticmethod
    def make_annotation(matrix, metadata, categories_names, cluster_maker, desired_nb_clusters):
        nb_clusters, flat_cluster, linkage_matrix = cluster_maker.run(desired_nb_clusters)

        file_names = matrix.get_file_names()
        categories = Categories.make_categories(metadata, file_names, categories_names)

        return Annotation(matrix, metadata, nb_clusters, flat_cluster, linkage_matrix, categories, cluster_maker.linkage_method, cluster_maker.clustering_algorithm)

class _Comparison:
    ALL = 0
    def __init__(self, clusters, categories):
        self.clusters = clusters
        self.categories = categories

    def obtain_file_names_with_tag_name(self, tag_name):
        return self.categories.obtain_file_names_with_tag_name(tag_name)

    def obtain_size_of_tags_in_category(self, category_name):
        return self.categories.obtain_size_of_tags_in_category(category_name)

    def obtain_cluster_name(self, cluster_id):
        if cluster_id == self.ALL:
            return 'All'
        else:
            return self.clusters[cluster_id].get_name()

    def obtain_size_of_tags_from_tag_names(self, cluster_id, category_name, tag_names):
        if cluster_id == self.ALL:
            file_names = self.clusters.get_file_names()
        else:
            file_names = self.clusters[cluster_id].get_file_names()
        return self.categories.obtain_size_of_tags_from_tag_names(category_name, tag_names, file_names)

    def obtain_file_names_tag_names(self, category_name):
        return self.categories.obtain_file_names_tag_names(category_name)

    def obtain_clusters(self):
        return self.clusters

    def obtain_cluster_name_by_file_name(self, file_name):
        return self.clusters.obtain_cluster_name(file_name)
