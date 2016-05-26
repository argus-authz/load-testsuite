# load-testsuite
A load testsuite for Argus based on Grinder

## Synopsis
This load test suite provides two tests:

1. Authorize test

   Each run execute three authorize request: the first expects _Permit_ as response value, the second one expects _Deny_, the last expects _Not Applicable_.
2. Concurrent test

   Every thread of each process, execute the same request in every run. Before send the request, threads wait on a barrier, with the purpose of verify the correct user mapping.

## Configuration
For configuring load test, edit the file _test.properties_. Basically you need to specify:
 
 * user certificate path (public and private key);
 * one or more PEPD endpoints;
 * a resource id
 * a permit range, a deny range and a not applicable range
 * an action id
 * which test you want run 
 
Values specified in the properties file must be coherent with the policies loaded in the Argus deployment. An example for load some policy is provided within this testsuite in _bin/setup\_argus.sh_ shell script.

## Run manually
For run the load testsuite, on the client host must be installed:

 * Java Virtual Machine
 * [The Grinder](http://grinder.sourceforge.net/g3/getting-started.html)
 * Argus Java API
 
First, install dependencies:
```bash
# yum install java-1.8.0-openjdk argus-pep-api-java argus-pep-common
```
 
Before run the test, create a proxy certificate. For example:
```bash
$ voms-proxy-init --voms test.vo --cert user_cert/test0.cert.pem --key user_cert/test0.key.pem
```
Export an environment variable with the proxy location:
```bash
$ export X509_USER_PROXY=/tmp/x509up_u`id -u`
```
Then execute the load test, running the shell script:
```bash
$ ./run.sh
```

## Run with Docker
This testsuite provides a Docker image for run the load tests. All the needed files are located in _docker_ folder.
First, build the new image:
```bash
$ ./build-image.sh
```
This shell script creates a new docker image, named _italiangrid/argus-load-testsuite_ in the local image repository.
Then run the container:
```bash
$ docker run italiangrid/argus-load-testsuite:latest
```
The last command launch a container that run load-testsuite with default setup. For customize the execution, provide to Docker the _properties_ file with the _-v_ option and the proper environment variables with _-e_ option.
For example:
```bash
$ docker run -v ~/test.properties:/tmp/test.properties -e REPO_BRANCH="feature/ISSUE-1" -e PROCESS=1 -e THREADS=1 -e RUNS=1 -e TEST_PROP_FILE=/tmp/test.properties italiangrid/argus-load-testsuite:latest
```
When customize the _properties_ file, pay attention to _grinder.script_ option. Remember that load-testsuite is located in _/home/tester/load-testsuite_, so the use of absolute path is recommended.

##### Available environment variables
 
| Variable         | Default                           | Meaning |
| ---------------- | --------------------------------- | ------- |
| REPO_BRANCH      | master                            | Git branch to checkout |
| PROCESS          | 10                                | Number of process to run |
| THREADS          | 10                                | Number of thread for each process |
| RUNS             | 100                               | How many times iterate the test |
| TEST\_PROP\_FILE | argus/pepd/test.properties        | Test properties file |
| USE\_CONSOLE     | false                             | Use Grinder console for manage load test |
| CONSOLE\_HOST    | localhost                         | Hostname where Grinder console is running |
| PROXY\_VO        | test.vo                           | VO used for generate proxy certificate |
| USER\_CERT       | /home/tester/.globus/usercert.pem | User public key path | 
| USER\_KEY        | /home/tester/.globus/userkey.pem  | User private key path |

