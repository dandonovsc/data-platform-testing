import logging
import os

from pyspark.sql import SparkSession

script_dir = os.path.dirname(__file__)

INBOUND_BUCKET = os.path.join(script_dir, "data")
DICTIONARY_BUCKET = os.path.join(script_dir, "dictionary")
ARCHIVE_BUCKET = "s3a://sc-data-platform/test/archive"

FUNCTIONAL_AREAS = {
    'healthprofile': [
        "biometrics"
    ]
}


def suppress_py4j_logging():
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.WARN)


def create_testing_pyspark_session():
    return (SparkSession.builder
            .appName("spark-regression-testing")
            .config("javax.jdo.option.ConnectionURL", "jdbc:derby:;databaseName=/tmp/metastore_db;create=true")
            .enableHiveSupport()
            .getOrCreate())
