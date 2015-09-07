# Ansible-Tasker

## What?
Poorly executed proof of concept for web based Ansible task manager.
In theory it will allow execution on any playbook that can be accessed via Git. Right now it has hardcoded path to `/tmp/main.yml`.
For current administration of tasks it uses Django admin panel.
Proper web interface will be added eventually.

## Why?
Because Ansible is awesome and I want to use it everywhere.
I hope that Tasker will eventually grown up to simple CI solution and I'll be free from Groovy in Jenkins.

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

You can drop PostgreSQL and use SQLite if you must. ;)
Also you can use other message broker compatible with Celery.

## Can I use it?
It's on GitHub - you can download it but highly doubt that you will be able to use it.
