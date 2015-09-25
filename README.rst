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

To get usage instructions run in a terminal::

    emailprocessor --help


Examples
=====


Print email summary
-------------------

Start a SMTP server on port 1025 of your local host that prints a summary
of every incoming email::

    emailprocessor --address 127.0.0.1 --port 1025 print_summary


Move Bing Ads reports to S3
---------------------------

See this blog_ entry for more information. To start a server that does
exactly what is described in our blog you just need to run::

    emailprocessor \
        -a $ADDRESS \
        -p 25 \
        --username $USERNAME \
        bing_to_s3 \
        --bucket $S3_BUCKET
        --prefix $S3_PREFIX

where:

* ``$ADDRESS`` is the public IP or DNS name of your server
* ``$USERNAME`` is the email recipient that will be associated with the processing
  of incoming Bing Ads emails
* ``$S3_BUCKET`` is the name of the target S3 bucket
* ``$S3_PREFIX`` is the target S3 prefix (the destination path in S3)

Once the SMTP server is running you should direct your Bing reports to 
``$USERNAME@$ADDRESS``.

.. _blog: http://blog.innovativetravel.eu/2015/09/automate-bing-ads-reporting-the-lazy-way/


Development environment on AWS
====

You can easily set up a development environment in the AWS cloud with
vagrant_. Install vagrant and then install the required plug-ins::

    vagrant plugin install vagrant-aws
    vagrant plugin install inifile

Then install the dummy AWS box that you will find in the ``vagrant`` directory
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
