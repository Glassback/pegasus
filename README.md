# pegasus
API Pegasus
===========

You have a server with a public IP and want to host some friends? 

Pegasus allow you to create and manage hosting with a CLI.

## Install

You  need to have a fresh installation of Ubuntu 14.04 before running the script

Download the script ""install.py"" and launched it! It will install and configure your environement to use Pegasus API.

## Pegasus

The script is still on developpement. The alpha version is soon availbale. Be patient ;)

###Creating Vhosts

I chose to use **Apache2 for managing Vhosts** because it's the most popular server (populer = best performance...).
The API will add a new line at the end of the configuration file located on : /etc/apache/apache.conf
``IncludeOptional /destination/folder/of/your/website/configuration/file``

The Apache2 configuration file will create 2 subdomains:

- ``phpmyadmin.domain.foo``
- ``www.domain.foo``

The ``domain.foo`` will be redirected to ``www.domain.foo``
The ``phpmyadmin.domain.foo`` will redirect to the phpMyAdmin interface for managing MySQL databases
## Author

My name is Noé Ferrari, and I'm passionate by IT Security! I want to host some friends in my VPS. Let's do some Python :D
