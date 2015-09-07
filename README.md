# Ansible-Tasker

## What?
Poorly executed proof of concept for web based Ansible task manager.
In theory it will allow execution on any playbook that can be accessed via Git. Right now it has hard coded path to `/tmp/main.yml`.

## Why?
Becouse Ansible is awesome and I want to use it everywhere.
I hope that Tasker will eventualy grown up to simple CI solution and I'll be free from Groovy in Jenkins.

## What is needed?
Python modules:
* Djnago
* psycopg2
* django-fsm
* django-fsm-admin
* django-fsm-log
* Celery
* Ansible < 2.0

Other software:
* PostgreSQL
* RabbitMQ
