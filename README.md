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
 * a action id
 * which test you want run 
 

## Run
Before run the test, create a proxy certificate. For example:
```bash
$ voms-proxy-init --voms test.vo --cert user_cert/test0.cert.pem --key user_cert/test0.key.pem
```
Then execute the load test, running the shell script:
```bash
$ ./run.sh
```
