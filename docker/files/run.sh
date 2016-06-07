#!/bin/bash

set -x

REPO_BRANCH="${REPO_BRANCH:-master}"
PROXY_VO=${PROXY_VO:-test.vo}
USER_CERT=${USER_CERT:-/home/tester/.globus/usercert.pem}
USER_KEY=${USER_KEY:-/home/tester/.globus/userkey.pem}

echo pass|voms-proxy-init -pwstdin --voms $PROXY_VO --cert $USER_CERT --key $USER_KEY

echo "Clone grinder-load-testsuite repository ..."
git clone https://github.com/argus-authz/load-testsuite.git

echo "Switch branch ..."
pushd /home/tester/load-testsuite
git checkout $REPO_BRANCH

echo "Run ..."
sh run.sh

echo "Done."
