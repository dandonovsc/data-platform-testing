import json

from pyspark.sql.types import StructType

def init_schema(json_location) -> StructType:
    with open(json_location) as source:
        data = json.load(source)
        return StructType.fromJson(data)