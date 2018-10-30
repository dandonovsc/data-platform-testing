import logging


class DataExporter:
    logger = logging.getLogger(__name__)

    def __init__(self, spark, area, collection):
        self.area = area
        self.collection = collection
        self.spark = spark

    def process(self):
        pass
