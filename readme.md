# Remote Broker
This page contains a small technical challenge for Python (Django) developers. We ask you to read the instructions available below and find an answer to the questions listed.

Simple REST API with Django REST Framework to synchronize remote mobile devices executing Tasks.

Let's have a look to the [specifications](docs/specs.md) file or the [documentation](docs/docs.md) for the proposed solution.

### Install
Install postgresql and create the database:

```bash
psql -h localhost -U admin postgres
CREATE DATABASE rbroker;
```

Make virtualenv and install requirements

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Migrate:
```bash
python manage.py migrate
```

Load some data:
```bash
python manage.py loaddata fixtures/data.json
```

Launch the backend and the queue manager:
```bash
python manage.py runserver
python manage.py qcluster
```

Then go [here](http://localhost:8000/tasks/begin/1) and begin a task by selecting a device and performing a put.
Before 20 seconds go [here](http://localhost:8000/tasks/success/1) and put a success! or [here](http://localhost:8000/tasks/failure/1) for a fail!
You can always check in the admin panel the state of the database [here](http://localhost:8000/admin/) (username:admin/password:adminadmin).
Remember you can access to the list of available tasks [here](http://localhost:8000/tasks/).