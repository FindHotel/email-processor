=========================
Simple email processor
=========================

This repo contains a set of SMTP servers that do various things with the 
incoming emails.


Installation
=====

::
    pip install git+https://github.com/InnovativeTravel/emailprocessor


Usage
=====

Start a SMTP server on port 1025 of your local host that prints a summary of 
every incoming email::

    emailprocessor --address 127.0.0.1 --port 1025 print_summary

