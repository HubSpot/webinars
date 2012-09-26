#!/bin/bash -x

function pause_setup {
    read -p "Press any key to continue..."
}

function reset_db {
    for i in $*
    do
        echo "\
          DROP DATABASE IF EXISTS $i; \
          DROP USER webinars@localhost; \
          CREATE DATABASE $i CHARACTER SET UTF8; \
          USE $i; \
          CREATE USER webinars@localhost IDENTIFIED BY 'SECRET'; \
          GRANT ALL ON webinars.* TO webinars@localhost; " | mysql -u root
    done
}

function setup_db {
    for i in $*
    do
        ./manage.py syncdb #--database $i
        ./manage.py migrate webinars #--database $i
        #django-admin.py loaddata --database $i content_app_starter_data.json
    done
}

reset_db webinars
setup_db webinars
