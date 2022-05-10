import matrix as mtx
import csv
from itertools import *
import rendering
import pdf
import metadata as md
import hierarchical_clustering as hc
import annotation as annot
from geec_analysis_lib.annotate_tsv import *

version = "epiGeEC-Annotate version 1.0.0"

class Annotate:
    def __init__(self, params):
        self.matrix_filename = params['matrix_filename']
        self.metadata_filename = params['metadata_filename']
        self.groups = params['groups']
        self.title = params['title']
        self.linkage_method = params['linkage_method']
        self.desired_nb_clusters = params['desired_nb_clusters']
        self.pdf_file = params['pdf_file']
        self.tsv_file = params['tsv_file']
        self.reordered_matrix_filename = params['reordered_matrix_filename']
        self.seed = params['seed']
        self.mds = params['mds']

    def run(self):
        #load files
        matrix = self._load_matrix()
        data = self._load_metadata()

        #base data
        restrictions = ['md5sum', 'file_path', 'file_name', 'id', 'virtual', 'assembly']
        ordered_categories = ['assay', 'publishing_group', 'cell_type']
        groups = data.make_usable_categories(matrix.get_file_names(),
                                             self.groups,
                                             restrictions,
                                             ordered_categories)

        # clustering
        cluster_maker = hc.HierarchicalClustering(matrix, self.linkage_method)

        # Annotation
        annotation = annot.Annotation.make_annotation(matrix, data, groups, cluster_maker, self.desired_nb_clusters)

        # pdf export
        if self.pdf_file is not None:
            self._export_pdf(groups, annotation)

        # tsv export
        if self.tsv_file is not None:
            self._export_tsv(annotation)

        if self.reordered_matrix_filename is not None:
            self._write_reordered_matrix(annotation)

    def _export_pdf(self, groups, annotation):
        cr = rendering.Rendering(version)

        self.title.set('nb_clusters', annotation.get_nb_clusters())
        files = cr.render(annotation, self.title.build(), self.seed, self.mds, groups)

        pdf.create_pdf(self.pdf_file, files)

    def _export_tsv(self, annotation):
        metadata = annotation.get_metadata()

        restrictions = ['file_path', 'id', 'virtual']
        ordered_categories = ['assay', 'cell_type', 'publishing_group', 'assembly']
        categories_names = metadata.make_usable_categories(annotation.get_file_names(),
                                                          None,
                                                          restrictions,
                                                          ordered_categories)

        with open(self.tsv_file, 'w') as tsv_file:
            AnnotateTsv.annotation_to_tsv(annotation, categories_names, tsv_file)

    def _write_reordered_matrix(self, annotation):
        matrix = annotation.get_ordered_matrix()
        with open(self.reordered_matrix_filename, 'w') as rmat_f: 
            matrix.write(rmat_f)

    def _load_matrix(self):
        return mtx.Matrix.parse_matrixfile(self.matrix_filename)

    def _load_metadata(self):
        return md.Metadata.parse_metadatafile(self.metadata_filename)
