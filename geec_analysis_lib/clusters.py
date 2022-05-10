from geec_analysis_lib.labels import int_label_to_letter_label
from itertools import *

class Clusters(dict):
    def __init__(self, *args):
        super(Clusters, self).__init__(*args)
        self.clusters_ref = {file_name:cl
                             for cl in self.itervalues()
                             for file_name in cl.get_file_names()}

    def get_file_names(self):
        return self.clusters_ref.keys()

    def obtain_cluster_name(self, file_name):
        return self.clusters_ref[file_name].get_name()

    @staticmethod
    def make_clusters(cluster_ids, file_names):
        if len(cluster_ids) != len(file_names):
            raise Exception('The length of the two list aren\'t matching!')

        clusters_file_names = {cluster_id:[] for cluster_id in set(cluster_ids)}

        for cluster_id, file_name in izip(cluster_ids, file_names):
            clusters_file_names[cluster_id].append(file_name)

        return Clusters({cls_id:Cluster.make_cluster(cls_id, md5s)
                         for cls_id, md5s in clusters_file_names.iteritems()})

class Cluster:
    def __init__(self, cluster_id, cluster_name, file_names):
        self.cluster_id = cluster_id
        self.name = cluster_name
        self.file_names = file_names

    def get_id(self):
        return self.cluster_id

    def get_name(self):
        return self.name

    def get_file_names(self):
        return self.file_names

    def __len__(self):
        return len(self.file_names)

    @staticmethod
    def make_cluster(cluster_id, file_names):
        return Cluster(cluster_id,
                       int_label_to_letter_label(cluster_id),
                       file_names)
