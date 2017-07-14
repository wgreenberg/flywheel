#!/bin/bash -e

# Startup the gremlin server
pushd /opt/gremlin-server
/opt/gremlin-server/bin/gremlin-server.sh /opt/flywheel/conf/gremlin-server.yml &
popd

echo "Waiting for gremlin to start..."
sleep 3

echo "Running server..."
python3 /opt/flywheel/main.py
