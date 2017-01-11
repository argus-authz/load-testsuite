
$packages = ['voms', 'voms-clients-cpp', 'voms-test-ca', 'argus-pep-api-java', 'argus-pep-common']

$voms_str = '/C=IT/O=INFN/OU=Host/L=CNAF/CN=vgrid02.cnaf.infn.it
             /C=IT/O=INFN/CN=INFN Certification Authority'

class { 'mwdevel_infn_ca': } ->
class { 'mwdevel_test_ca': } ->
file { 'argus-repo':
  ensure => file,
  path   => '/etc/yum.repos.d/argus_el7.repo',
  owner  => root,
  group  => root,
  mode   => '0644',
  source => '/argus_el7.repo';
} ->
package { $packages: ensure => latest, } ->
user { 'tester':
  ensure     => present,
  name       => 'tester',
  managehome => true
} ->
file {
  '/etc/grid-security/hostcert.pem':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    require => Package['voms'],
    source  => '/dev_local_io.cert.pem';

  '/etc/grid-security/hostkey.pem':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0400',
    require => Package['voms'],
    source  => '/dev_local_io.key.pem';

  '/etc/vomses':
    ensure => directory;

  '/etc/grid-security/vomsdir':
    ensure  => directory,
    require => Package['voms'];

  '/etc/grid-security/vomsdir/test.vo':
    ensure  => directory,
    require => File['/etc/grid-security/vomsdir'];

  '/etc/vomses/test.vo-vgrid02.cnaf.infn.it':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => '"test.vo" "vgrid02.cnaf.infn.it" "15000" "/C=IT/O=INFN/OU=Host/L=CNAF/CN=vgrid02.cnaf.infn.it" "test.vo" "24"',
    require => File['/etc/vomses'];

  '/etc/grid-security/vomsdir/test.vo/vgrid02.cnaf.infn.it.lsc':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => $voms_str,
    require => File['/etc/grid-security/vomsdir/test.vo'];
}
