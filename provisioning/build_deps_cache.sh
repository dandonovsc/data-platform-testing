#!/usr/bin/env bash
set -o nounset  # Throw error if uninitialized variable is used
set -o errexit  # Fail on any error

DIR=$(dirname "$0") # Get the directory this script is in
VERSION="1.0"

if [ "$DIR" == "" ]; then
    echo "DIR is empty. Can't continue."
    exit 1;
fi

function main {
    cp ~/.ivy2/.credentials .
    echo "Docker build"
    docker build -t data-processor-scala-deps-cache:latest -f $DIR/DepCacheDockerfile .

#    echo "Docker tag data-processor-scala-deps-cache:latest nexus.admin.sharecare.com/sso-scala-deps-cache:$VERSION"
#    docker tag data-processor-scala-deps-cache:latest nexus.admin.sharecare.com/data-processor-scala-deps-cache:$VERSION
#
#    echo "Docker push nexus.admin.sharecare.com/sso-scala-deps-cache:$VERSION"
#    docker push "nexus.admin.sharecare.com/sso-scala-deps-cache:$VERSION"

    echo "Remove .credentials file"
    rm -f .credentials
}

function finish {
    echo "Remove .credentials file"
    rm -f .credentials
}

trap finish EXIT
main

