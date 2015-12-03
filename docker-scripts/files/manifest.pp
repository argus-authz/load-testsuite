include puppet-infn-ca
include puppet-test-ca

class { 'puppet-java': java_version => 8 }

$packages = ['curl', 'unzip', 'tar', 'git', 'redhat-lsb', 'wget', 'voms', 'voms-clients', 'voms-test-ca']

package { $packages: ensure => installed, }

user { 'tester':
  name       => 'tester',
  ensure     => present,
  managehome => true
}

file {
  '/etc/grid-security/hostcert.pem':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    require => Package['voms'],
    source  => "/dev_local_io.cert.pem";

  '/etc/grid-security/hostkey.pem':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0400',
    require => Package['voms'],
    source  => "/dev_local_io.key.pem";

  '/etc/vomses':
    ensure => directory;

  '/etc/grid-security/vomsdir':
    ensure  => directory,
    require => Package['voms'];

  '/etc/grid-security/vomsdir/test.vo':
    ensure  => directory,
    require => File['/etc/grid-security/vomsdir'];
}