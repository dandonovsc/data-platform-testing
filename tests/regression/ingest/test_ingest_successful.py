import unittest
import logging
from pyspark.sql import SparkSession

from tests import config
from app.tasks.ingestor import DataIngestor


class PySparkTest(unittest.TestCase):

    @classmethod
    def suppress_py4j_logging(cls):
        logger = logging.getLogger("py4j")
        logger.setLevel(logging.WARN)

    @classmethod
    def create_testing_pyspark_session(cls):
        return (SparkSession.builder
                .master("local[2]")
                .appName("my - local - testing - pyspark - context")
                .config("derby.system.home", "/tmp/derby")
                .config("hive.metastore.warehouse.dir", "/tmp/hive")
                .enableHiveSupport()
                .getOrCreate())

    @classmethod
    def setUpClass(cls):
        cls.suppress_py4j_logging()
        cls.spark = cls.create_testing_pyspark_session()
        cls.ingestor = DataIngestor(spark=cls.spark, config=config)

    def test_process_biometrics(self):
        self.ingestor.process(area="healthprofile", collection="biometrics")
        pass

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
