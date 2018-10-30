import csv
import json
import logging
import app.tests.utilities.transformers as transformers

from tests.utilities.dataframes import init_schema
import config


class DataIngestor:

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
        self.logger = spark._jvm.org.apache.log4j.LogManager.getLogger("DP DataIngestor")

    def process(self, area, collection=None):
        self.logger.info(f"Starting ingest of area: {area}")
        raw_areas_input = self._read_raw_areas_data(area, collection)
        transformed_df = self._transform_raw_areas(raw_areas_input)

    def _read_raw_areas_data(self, area, collection):
        areas = []
        if area == "all":
            for a in config.FUNCTIONAL_AREAS:
                areas.append(self._process_raw_area(a, collection))
        else:
            areas.append(self._process_raw_area(area, collection))

        return areas

    def _process_raw_area(self, area, collection):

        collections = []
        if collection == "all":
            for collection in config.FUNCTIONAL_AREAS[area]:
                collections.append(self._process_raw_collection(area, collection))
        else:
            collections.append(self._process_raw_collection(area, collection))

        return {
            "area": area,
            "collections": collections
        }

    def _process_raw_collection(self, area, collection):
        data_set = f"{self.config.INBOUND_BUCKET}/{area}/{collection}"
        schema_json = f"{self.config.DICTIONARY_BUCKET}/{area}/{collection}.json"
        self.logger.info(f"Reading inbound data: {data_set}. Schema {schema_json}")

        schema_df = init_schema(schema_json)
        raw_df = self.spark.read.schema(schema_df).json(data_set)
        raw_df.cache()

        self.logger.info(f"Cached staging data. Area {area}, collection {collection}, count {raw_df.count()}")

        return {
            "collection": collection,
            "df": raw_df
        }

    def _transform_raw_areas(self, raw_areas_input):
        transformed = []
        for area in raw_areas_input:
            area_name = area["area"]
            transformed.append({
                "area": area_name,
                "collections": self._transform_raw_collections(area_name, area["collections"])
            })

        return transformed

    def _transform_raw_collections(self, area_name, collections):
        for collection in collections:
            rules_set_location = f"{self.config.DICTIONARY_BUCKET}/{area_name}/{collection}-mappings.json"
            self.logger.info(f"Reading rule set data: {rules_set_location}")

            with open(rules_set_location, newline='') as rules_file:
                rule_set = csv.reader(rules_file, delimiter='=>')
                for line in rule_set:
                    operation = line[0]
                    column_pair = line[1].split("|")
                    transformer = getattr(transformers, operation)(column_pair[0], column_pair[1])
