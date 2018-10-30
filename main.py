#!/usr/bin/env python3

import argparse

from pyspark.sql import SparkSession

import app.config as config
from app.tasks.exporter import DataExporter
from app.tasks.ingestor import DataIngestor

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Data Warehouse CLI.')

    parser.add_argument('--operation', '-o',
                        type=str,
                        dest="operation",
                        choices=('all', 'ingest', 'export'),
                        default='all',
                        help='Data warehouse task')

    parser.add_argument('--area', '-a',
                        type=str,
                        dest="area",
                        choices=('all', 'health-profile', 'membership', 'RealAgeDB', 'ChallengesDB',
                                 'digital', 'incentives', 'messaging', 'consent'),
                        default='all',
                        help='Functional area to process')

    parser.add_argument('--collection', '-c',
                        type=str,
                        dest="collection",
                        default='all',
                        help='Collection of functional area to process')

    args = parser.parse_args()
    operation = args.operation

    spark = SparkSession.builder.appName("Data Platform").getOrCreate()

    if operation == "ingest":
        ingestor = DataIngestor(spark=spark, config=config)
        ingestor.process(args.area, args.collection)

    elif operation == "export":
        exporter = DataExporter(spark, args.area, args.collection)
        exporter.process()

    spark.stop()
