=========================
Simple email processor
=========================

.. image:: https://circleci.com/gh/InnovativeTravel/email-processor.svg?style=svg
    :target: https://circleci.com/gh/InnovativeTravel/email-processor


This repo contains a set of SMTP servers that do various things with the 
incoming emails.


Installation
=====

::

    pip install git+https://github.com/InnovativeTravel/emailprocessor


Usage
=====

Start a SMTP server on port 1025 of your local host that prints a summary
of every incoming email::

    emailprocessor --address 127.0.0.1 --port 1025 print_summary


Development environment on AWS
====

You can easily set up a development environment in the AWS cloud with
vagrant_. Install vagrant and then install the required plug-ins::

    vagrant plugin install vagrant-aws
    vagrant plugin install inifile

Then install the dummy AWS box that you will find in the `vagrant` directory
of this repo::

    vagrant box add aws-dummy aws-dummy.box


Then edit the Vagrantfile_ so that it matches your AWS VPC configuration. You
should then be ready to fire up the AWS instance using::

    vagrant up

You should also be able to SSH into the instance::

    vagrant ssh

.. _Vagrantfile: https://github.com/InnovativeTravel/email-processor/blob/master/vagrant/Vagrantfile
.. _vagrant: https://www.vagrantup.com/


Deployment
=====

To be done.


Who do I talk to?
====

German <german@innovativetravel.eu>
