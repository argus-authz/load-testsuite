FROM docker.io/centos:latest

COPY files/manifest.pp /
COPY files/setup.sh /
COPY files/dev_local_io.cert.pem /
COPY files/dev_local_io.key.pem /

RUN /setup.sh

WORKDIR /home/tester
COPY files/run.sh /
RUN cp /run.sh /home/tester/run.sh

USER tester
CMD /home/tester/run.sh