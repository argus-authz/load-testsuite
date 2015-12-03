#!/bin/bash

export GRINDER_PROCESSES=${PROCESS:-10}
export GRINDER_THREADS=${THREADS:-10}
export GRINDER_USE_CONSOLE=${USE_CONSOLE:-false}
export GRINDER_CONSOLE_HOST=${CONSOLE_HOST:-localhost}
export GRINDER_RUNS=${RUNS:-100}

TEST=${TEST_PROP_FILE:-./argus/pepd/test.properties}

echo "Test: $TEST"
echo "Processes: $GRINDER_PROCESSES"
echo "Threads: $GRINDER_THREADS"
echo "Runs: $GRINDER_RUNS"
echo "---"
echo "Removing logs"

rm -f log/*
./bin/runAgent.sh $TEST

tail -n15 log/*.log