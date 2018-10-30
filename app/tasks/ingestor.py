import app.utilities.transformers as transformers
from app.utilities.dataframes import init_schema


class DataIngestor:

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
        self.logger = spark._jvm.org.apache.log4j.LogManager.getLogger("DP DataIngestor")

    def process(self, area, collection):
        self.logger.info(f"Starting ingest of area: {area}")
        raw_areas_input = self._read_raw_areas_data(area, collection)
        transformed_df = self._transform_raw_areas(raw_areas_input)
        self.persist_temp_data(transformed_df)

    def _read_raw_areas_data(self, area, collection):
        areas = []
        if area == "all":
            for a in self.config.FUNCTIONAL_AREAS:
                areas.append(self._process_raw_area(a, collection))
        else:
            areas.append(self._process_raw_area(area, collection))

        return areas

    def _process_raw_area(self, area, collection):

        collections = []
        if collection == "all":
            for collection in self.config.FUNCTIONAL_AREAS[area]:
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
            "name": collection,
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
            rules_set_location = f"{self.config.DICTIONARY_BUCKET}/{area_name}/{collection['name']}-mappings.json"
            self.logger.info(f"Reading rule set data: {rules_set_location}")
            with open(rules_set_location, newline='') as rules_file:
                for line in rules_file:
                    rule_pair = line.split("=>")
                    operation = rule_pair[0]
                    args = rule_pair[1].split("|")
                    collection['df'] = getattr(transformers, operation)(collection['df'], args)

        return collections

    def persist_temp_data(self, transformed_df):
        self.logger.info("Started persisting temp data...")
        for df_data in transformed_df:
            for collection in df_data['collections']:
                collection_name = collection['name']
                data_frame = collection['df']
                self.logger.info(f"Persisting temp table {collection_name}")
                self.spark.catalog.dropGlobalTempView(collection_name)
                data_frame.createGlobalTempView(collection_name)
