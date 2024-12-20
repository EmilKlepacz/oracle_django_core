# oracle_django_core

#### setting up the credentials and OCI driver:

env variables:

- <b>ORADJA_USER</b>
- <b>ORADJA_NAME</b>
- <b>ORADJA_PASSWORD</b>
- <b>ORADJA_HOST</b>
- <b>ORADJA_PORT</b>
- <b>ORADJA_OCI</b>

need to be set for db connection. <br>

```bash
export ORADJA_USER="dummy_user"
export ORADJA_NAME="dummy_name"
export ORADJA_PASSWORD="dummy_password"
export ORADJA_HOST="dummy.host.com"
export ORADJA_PORT="1521"
export ORADJA_OCI="/dummy/path/to/instantclient_23_3"
export ORADJA_SECRET_KEY="to_retrieve_secure_key_contact_the_owner"
```

#### setting SECRET_KEY:

```bash
export ORADJA_SECRET_KEY="to_get_secure_key_contact_the_owner"
```

#### running tests:

1. concise output:

```bash
pytest
```

2. verbose output:

```bash
pytest -vv
```

3. verbose (if any print occurrences in test for debug)

```bash
pytest -vv -s
```

4. coverage report

```bash
pytest --cov=oradja --cov-report term-missing tests
```

#### generate requirements.txt:

```bash
pip freeze > requirements.txt 
```

#### running custom management command:

```bash
python manage.py env
```

#### importing models for existing table:

```bash
python manage.py inspectdb your_table_name > models.py
```

#### running enhanced django shell:

```bash
python manage.py shell_plus
```

#### to enable autoreload in ipython shell

```bash
%load_ext autoreload
%autoreload 2
```

or shorter

```bash
autoreload()
```

