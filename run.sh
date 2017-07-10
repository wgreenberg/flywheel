#!/bin/bash -e

# Startup the gremlin server
GREMLIN=/opt/gremlin-server
pushd /opt/gremlin-server
$GREMLIN/bin/gremlin-server.sh $GREMLIN/conf/gremlin-server-rest-modern.yaml &
popd

echo "Waiting for gremlin to start..."
sleep 3

echo "Running server..."
python3 /opt/flywheel/main.py
