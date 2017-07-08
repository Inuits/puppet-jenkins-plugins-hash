# Puppet-Jenkins plugins hash

Takes a yaml as input, returns yaml ready to be used as
puppet::jenkins::plugins_hash parameter.

## Which problem does it solve?

puppet::jenkins::plugins_hash does not know about dependencies, so you need to
crawl them manually.

This script does the crawling for you.


# Contributing

## Linting

You can run the lint task by using:

  invoke lint
