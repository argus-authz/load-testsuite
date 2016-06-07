FROM docker.io/centos:latest

## Layer: base
RUN rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
RUN yum update -y && yum  install -y puppet git curl unzip tar git redhat-lsb wget java-1.8.0-openjdk epel-release
RUN puppet module install --force puppetlabs-stdlib && \
	puppet module install --force puppetlabs-java && \
	puppet module install --force maestrodev-wget

## Layer: setup
COPY files/manifest.pp /
COPY files/setup.sh /
COPY files/argus_el7.repo /
COPY files/dev_local_io.cert.pem /
COPY files/dev_local_io.key.pem /

RUN /setup.sh

## Layer: testing
WORKDIR /home/tester
COPY files/run.sh /
RUN cp /run.sh /home/tester/run.sh

USER tester
CMD /home/tester/run.sh