#!/bin/bash
mysql -uSingularityHA -p'SingularityHA' -e 'create database base_test'
mv ../config.ini ../config.testbackup.ini
cp ../extras/dev/config/config.tests.ini ../config.ini
nosetests ../
mysql -uSingularityHA -p'SingularityHA' -e 'drop database base_test'
mv ../config.testbackup.ini ../config.ini
