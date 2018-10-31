"""
  Tests for the ingest step
"""
import unittest
from app.tasks.ingestor import DataIngestor
from tests import config


class IngestSuccessfulTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.suppress_py4j_logging()
        cls.spark = config.create_testing_pyspark_session()
        cls.ingestor = DataIngestor(spark=cls.spark, config=config)

    def test_process_biometrics(self):
        self.ingestor.process(area="healthprofile", collection="biometrics")
        tmp_view = self.spark.newSession().sql("SELECT * FROM global_temp.biometrics")
        print(f"\n\n\n\ >>> {tmp_view.count()}")
        # TODO Add assertions here

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
