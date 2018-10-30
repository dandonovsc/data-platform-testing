import os

ENV = os.environ.get('env', "test")

INBOUND_BUCKET = "s3a://sc-data-platform/test/input"
DICTIONARY_BUCKET = "s3a://sc-data-dictionary"
ARCHIVE_BUCKET = "s3a://sc-data-platform/test/archive"


FUNCTIONAL_AREAS = {
    'health-profile' : [
        "biometrics"
    ]
}