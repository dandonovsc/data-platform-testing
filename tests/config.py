import os
script_dir = os.path.dirname(__file__)

INBOUND_BUCKET = os.path.join(script_dir, "data")
DICTIONARY_BUCKET = os.path.join(script_dir, "dictionary")
ARCHIVE_BUCKET = "s3a://sc-data-platform/test/archive"


FUNCTIONAL_AREAS = {
    'healthprofile' : [
         "biometrics"
    ]
}