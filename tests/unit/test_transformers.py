import unittest

from pyspark import Row

from tests import config
import utilities.transformers as transformers


class TransformersTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.suppress_py4j_logging()
        cls.spark = config.create_testing_pyspark_session()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_should_drop_column(self):
        test_data = Row(_id = "123", topic = "test")
        test_df = self.spark.createDataFrame([test_data])

        test_df = transformers.col_drop(test_df, "_id")
        self.assertNotIn("_id", test_df.columns)

    def test_should_rename_column(self):
        test_data = Row(_id = "123", topic = "test")
        test_df = self.spark.createDataFrame([test_data])
        test_df = transformers.col_rename(test_df, ["topic", "topic_renamed"])
        self.assertListEqual(test_df.columns, ["_id", "topic_renamed"])