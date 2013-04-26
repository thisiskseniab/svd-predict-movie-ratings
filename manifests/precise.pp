exec { "apt-update":
  command => "/usr/bin/sudo /usr/bin/apt-get update"
}

# Ensure apt-get update has been run before installing any packages
Exec["apt-update"] -> Package <| |>

package {
  "build-essential":
    ensure => installed,
    provider => apt;
  "python":
    ensure => installed,
    provider => apt;
  "python-dev":
    ensure => installed,
    provider => apt;
  "python-setuptools":
    ensure => installed,
    provider => apt;
  "python-software-properties":
    ensure => installed,
    provider => apt;
  "redis-server":
    ensure => installed;
  "pypy": 
    ensure => installed,
    require => Package['python'];
  ["vim", "curl"]:
    ensure => installed;
  "git":
    ensure => installed;
}


package { "python-pip": 
  ensure => latest,
  require => Package['python']
}

package { "sqlite3": 
  ensure => latest,
}

package { ["Flask", "Flask-SQLAlchemy", "Flask-WTF", "Flask-Bootstrap", "Jinja2", "SQLAlchemy", "WTForms", "Werkzeug", "wsgiref", "redis"]: 
  ensure => latest,
  provider => pip,
  require => Package['python-pip']
}

