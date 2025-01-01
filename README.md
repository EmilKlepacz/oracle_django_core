# oracle_django_core

### setting up db credentials and OCI driver:

```bash
export ORADJA_USER="dummy_user"
export ORADJA_NAME="dummy_name"
export ORADJA_PASSWORD="dummy_password"
export ORADJA_HOST="dummy.host.com"
export ORADJA_PORT="1521"
export ORADJA_OCI="/dummy/path/to/instantclient_23_3"
```

### setting up SECRET_KEY:

```bash
export ORADJA_SECRET_KEY="to_get_secure_key_contact_the_owner"
```

### activating virtual environment and install dependencies:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
# for Windows: venv\Scripts\activate 
```

```bash
pip install -r requirements.txt
```

### verify installation:

```bash
pip list
```

### running tests:

1. concise output:

```bash
pytest
```

2. verbose output:

```bash
pytest -vv
```

3. verbose [if any print() occurrences in test for debug]:

```bash
pytest -vv -s
```

4. coverage report:

```bash
pytest --cov=oradja --cov-report term-missing tests
```

### generating requirements.txt:

```bash
pip freeze > requirements.txt 
```

### running custom management commands examples:

```bash
python manage.py env
```

```bash
python manage.py download --created_dati_from 01-01-2024 --created_dati_to 31-12-2024 --file_types pdf png jpg --limit 10
```

### generating model for existing table:

```bash
python manage.py inspectdb your_table_name > models.py
```

### running Django shell with autoloading of the apps database models:

```bash
python manage.py shell_plus
```

### enabling autoreload in ipython shell:

```bash
%load_ext autoreload
%autoreload 2
```

or shorter:

```bash
autoreload()
```

### running development server:

```bash
python manage.py runserver
```

### testing rest api examples:

```bash
curl -X GET "http://127.0.0.1:8000/api/umvdocuments/" | json_pp
```

```bash
curl -X POST "http://127.0.0.1:8000/api/umvdocuments/search/" \
-H "Content-Type: application/json" \
-d '{
    "created_dati_from": "2023-01-01",
    "created_dati_to": "2024-12-01",
    "limit": 10,
    "file_types": ["pdf", "png", "jpg"]
}' | json_pp

```

or when params are passed with urls:
```bash
curl -X GET "http://127.0.0.1:8000/api/umvdocuments/search-url/?ids=10653,10654" | json_pp
```

```bash
curl -X GET "http://127.0.0.1:8000/api/umvdocuments/search-url/?limit=20&created_dati_from=01-01-2023&created_dati_to=01-12-2024&file_types=pdf,png,jpg" | json_pp
```
