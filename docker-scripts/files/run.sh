#!/bin/bash

REPO_BRANCH="${REPO_BRANCH:-master}"
PROXY_VO=${PROXY_VO:-test.vo}

echo pass|voms-proxy-init -pwstdin --voms $PROXY_VO --cert /home/tester/.globus/usercert.pem --key /home/tester/.globus/userkey.pem

echo "Clone grinder-load-testsuite repository ..."
git clone https://github.com/argus-authz/load-testsuite.git

echo "Switch branch ..."
pushd /home/tester/load-testsuite
git checkout $REPO_BRANCH

echo "Run ..."
./run.sh

echo "Done."
