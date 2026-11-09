# Kind


## audit https://medium.com/@dbsiavichay/como-crear-registros-de-auditoria-para-tu-proyecto-en-django-usando-el-admin-log-d3e1bf375ff4


Commands utility

```
docker compose -f local.yml build
docker compose -f local.yml up
docker compose -f local.yml ps
docker compose -f local.yml down
export COMPOSE_FILE=local.yml

docker stop $ (docker ps -a -q)
docker rm $ (docker ps -a -q)
```

# --rm cuando se termine de ejecutar el comando va a matar el contenedor

```
docker compose -f local.yml run --rm django python manage.py createsuperuser
docker compose -f local.yml run --rm django python manage.py makemigrations
docker compose -f local.yml run --rm django python manage.py migrate
docker compose -f local.yml run --rm django python manage.py runserver
docker compose -f local.yml run --rm django python manage.py showmigrations
docker compose -f local.yml run --rm django python manage.py startapp
docker compose -f local.yml run --rm django python manage.py test
```

# Ejecutar tests

```
docker compose -f local.yml run --rm django pytest -x
```

# Problemas con cors

```
google-chrome --user-data-dir="/tmp/chrome_dev_test" --disable-web-security
```

# Otros comandos

## eliminar migrations

´´´
find . -path "_/migrations/_.py" -not -name "**init**.py" -delete
find . -path "_/migrations/_.pyc" -delete

Get-ChildItem -Path . -Filter "*.py" -Recurse | Where-Object { $_.FullName -notmatch '\\migrations\\__init__.py$' -and $_.Directory.Name -eq 'migrations' } | Remove-Item
Get-ChildItem -Path . -Filter "*.py" -Recurse | Where-Object { $_.FullName -notmatch '\\migrations\\__init__.py$' -and $_.Directory.Name -eq 'migrations' }

´´´

## eliminar **pycache**

´´´
find . | grep -E "(/**pycache**$|\.pyc$|\.pyo$)" | xargs rm -rf
´´´

## Cargar datos

```
  docker compose -f local.yml run --rm django python manage.py loaddata asucom.json

  docker compose -f production.yml run --rm django python manage.py createsuperuser
```
