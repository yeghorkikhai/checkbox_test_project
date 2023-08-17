### Checkbox Тестове завдання
ТЗ: https://docs.google.com/document/d/1BXHc1_tzpsqpE1fMqkcWwVFmxDJ9kQNP40dmdYuYTqg/edit

#### Clone from GitHub

```
git clone https://github.com/yeghorkikhai/checkbox_test_project
cd checkbox_test_project
```

#### Setup ENV
```
cp .env.example .env
```

#### Example of .env for test
```
DATABASE_HOST=psql
DATABASE_PORT=5432
DATABASE_USER=user
DATABASE_PASSWORD=admin
DATABASE_NAME=postgres

JWT_SECRET=12345

VERSION=0.0.1
```

#### Run app
```
sudo docker-compose up -d --build
```

#### Open docs
```
http://localhost:8080/docs
```

### Pytest Tests

#### Create venv
```
python3.11 -m venv venv
source venv/bin/activate
venv/bin/pip install -U pip setuptools
venv/bin/pip install poetry
```

#### Install requirements
```
poetry install
```

#### Run tests
```
python -m pytest tests/
```