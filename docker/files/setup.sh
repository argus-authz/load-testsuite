#!/usr/bin/env bash

set -ex

CERT_DIR="/usr/share/igi-test-ca"
PROXY_USER=${PROXY_USER:-test0}
PROXY_VO=${PROXY_VO:-test.vo}

git clone git://github.com/cnaf/ci-puppet-modules.git /opt/ci-puppet-modules

puppet apply --modulepath=/opt/ci-puppet-modules/modules:/etc/puppet/modules /manifest.pp

wget https://www.dropbox.com/s/2s974oqhyttgdjh/grinder-cnaf-3.11-binary.tar.gz
tar -C /opt -xvzf grinder-cnaf-3.11-binary.tar.gz
rm -f grinder-cnaf-3.11-binary.tar.gz

echo 'export X509_USER_PROXY="/tmp/x509up_u$(id -u)"'>/etc/profile.d/x509_user_proxy.sh
cat /etc/profile.d/x509_user_proxy.sh

echo 'export GRINDER_HOME="/opt/grinder-3.11"'>/etc/profile.d/grinder.sh
cat /etc/profile.d/grinder.sh

echo "Create tester user ..."
useradd tester

echo "Create proxy certificate ..."
mkdir /home/tester/.globus
cp $CERT_DIR/$PROXY_USER.cert.pem /home/tester/.globus/usercert.pem
chmod 644 /home/tester/.globus/usercert.pem
cp $CERT_DIR/$PROXY_USER.key.pem /home/tester/.globus/userkey.pem
chmod 400 /home/tester/.globus/userkey.pem
chown -R tester:tester /home/tester/.globus



