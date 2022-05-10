import unittest
from StringIO import StringIO

from tests.context import geec_analysis_lib
from geec_analysis_lib.metadata import Metadata
from geec_analysis_lib.categories import Categories, Category, Tags, Tag

METADATA_JSON = '''
{"count": 2,
"name": "test1",
"datasets": [
{"cell_type": "hindlimb bud", "assay": "H3K27ac", "file_name": "MS046901", "assay_category": "Histone Modifications", "md5sum": "f0fd84b5c0c7b0c56e165c8e0963e8c2", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "8"},
{"cell_type": "forelimb bud", "assay": "H3K27ac", "file_name": "MS046801", "assay_category": "Histone Modifications", "md5sum": "5600791b332ab4a88fade77ba50be26a", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "9"}
]}
'''
FILE_NAMES = ['MS046901', 'MS046801']
CATEGORIES = ['cell_type', 'assay', 'assay_category', 'publishing_group', 'cell_type_category']

class TestCategories(unittest.TestCase):
    def setUp(self):
        self.metadata = Metadata.load_from_file(StringIO(METADATA_JSON))
        self.categories = Categories.make_categories(self.metadata, FILE_NAMES, CATEGORIES)

    def tearDown(self):
        self.metadata = None
        self.categories = None

    def test_obtain_file_names_with_tag_name(self):
        one_md5 = self.categories.obtain_file_names_with_tag_name('hindlimb bud')
        self.assertEquals(len(one_md5), 1)

        two_md5 = self.categories.obtain_file_names_with_tag_name('H3K27ac')
        self.assertEquals(len(two_md5), 2)

        no_md5 = self.categories.obtain_file_names_with_tag_name('potato')
        self.assertFalse(no_md5)

    def test_obtain_size_of_tags_in_category(self):
        two_cell_type = self.categories.obtain_size_of_tags_in_category('cell_type')
        self.assertEquals(len(two_cell_type), 2)
        for _, x in two_cell_type:
            self.assertEquals(x, 1)

        one_assay = self.categories.obtain_size_of_tags_in_category('assay')
        self.assertEquals(len(one_assay), 1)
        for _, x in one_assay:
            self.assertEquals(x, 2)

        with self.assertRaises(KeyError):
            self.categories.obtain_size_of_tags_in_category('potato')

    def test_obtain_size_of_tags_from_tag_names(self):
        tag_names = ['H3K27ac']
        good = self.categories.obtain_size_of_tags_from_tag_names('assay', tag_names, FILE_NAMES)
        self.assertEquals(good, 2)

        empty_md5 = self.categories.obtain_size_of_tags_from_tag_names('assay', tag_names, [])
        self.assertEquals(empty_md5, 0)

        bad_md5 = self.categories.obtain_size_of_tags_from_tag_names('assay', tag_names, ['potato'])
        self.assertEquals(bad_md5, 0)

        empty_tags = self.categories.obtain_size_of_tags_from_tag_names('assay', [], FILE_NAMES)
        self.assertEquals(empty_tags, 0)

        bad_tags = self.categories.obtain_size_of_tags_from_tag_names('assay', ['potato'], FILE_NAMES)
        self.assertEquals(bad_tags, 0)

        with self.assertRaises(KeyError):
            self.categories.obtain_size_of_tags_from_tag_names('potato', tag_names, FILE_NAMES)

    def test_obtain_file_names_tag_names(self):
        good_assay = self.categories.obtain_file_names_tag_names('assay')
        md5s = set()
        for md5, tag_name in good_assay.iteritems():
            md5s.add(md5)
            self.assertEquals(tag_name, 'H3K27ac')

        self.assertEquals(md5s, set(FILE_NAMES))

    def test_obtain_sorted_tags(self):
        cell_type_sort = self.categories.obtain_sorted_tags('cell_type', key=lambda t: t.get_name())
        for cts, name in zip(cell_type_sort, ['forelimb bud', 'hindlimb bud']):
            self.assertEquals(cts.get_name(), name)

        with self.assertRaises(KeyError):
            self.categories.obtain_sorted_tags('potato', key=lambda t: t.get_name())

    def test_make_categories(self):
        # good 
        good_categories = Categories.make_categories(self.metadata, FILE_NAMES, CATEGORIES)
        self.cmp_categories_with_metadata(good_categories, self.metadata, FILE_NAMES, CATEGORIES)

        # empties
        empty_md5 = Categories.make_categories(self.metadata, [], CATEGORIES)
        self.cmp_categories_with_metadata(empty_md5, self.metadata, [], CATEGORIES)

        empty_cat = Categories.make_categories(self.metadata, FILE_NAMES, [])
        self.cmp_categories_with_metadata(empty_cat, self.metadata, [], [])

        # bad inputs
        bad_md5 = Categories.make_categories(self.metadata, ['potato'], CATEGORIES)
        self.cmp_categories_with_metadata(bad_md5, self.metadata, ['potato'], CATEGORIES)

        bad_cat = Categories.make_categories(self.metadata, FILE_NAMES, ['potato'])
        self.cmp_categories_with_metadata(bad_cat, self.metadata, FILE_NAMES, ['potato'])

    def cmp_categories_with_metadata(self, categories, metadata, file_names, categories_names):
        used_file_names = set()
        used_categories_names = set()

        for cat_name, cat in categories.iteritems():
            used_categories_names.add(cat_name)
            for tag_name, tag in cat.get_tags().iteritems():
                for md5 in tag.get_file_names():
                    used_file_names.add(md5)
                    self.assertEquals(metadata.obtain_dataset_item(md5, cat_name), tag_name)

        self.assertEquals(used_file_names, set(file_names))
        self.assertEquals(used_categories_names, set(categories_names))

class TestCategory(unittest.TestCase):
    def setUp(self):
        self.metadata = Metadata.load_from_file(StringIO(METADATA_JSON))
        self.categories = Categories.make_categories(self.metadata, FILE_NAMES, CATEGORIES)

    def tearDown(self):
        self.metadata = None
        self.categories = None

    def test_make_flat_clusters(self):
        # Two clusters
        cell_type_category = self.categories['cell_type']
        cell_type_fc = cell_type_category.make_flat_clusters(FILE_NAMES)
        self.assertEquals(cell_type_fc, [0, 1])

        # One cluster
        assay_category = self.categories['assay']
        assay_fc = assay_category.make_flat_clusters(FILE_NAMES)
        self.assertEquals(assay_fc, [0, 0])

        # empty md5
        empty_md5 = cell_type_category.make_flat_clusters([])
        self.assertFalse(empty_md5)

        # bad md5
        with self.assertRaises(KeyError):
            cell_type_category.make_flat_clusters(['potato'])
