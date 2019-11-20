# Table of contents
1. Get started on local
2. Get started on local (docker)
3. Deploy to heroku.

<hr>

## GET STARTED:
#### create database and user on your local: 
```
CREATE DATABASE village_scrape_prod;
CREATE DATABASE village_scrape_dev;
CREATE DATABASE village_scrape_test;

CREATE USER villagescrapeuser WITH password 'villagescrapepassword';
GRANT ALL PRIVILEGES ON database village_scrape_dev to villagescrapeuser;
ALTER USER villagescrapeuser SUPERUSER;
```


#### Setup:
```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### upgrade db for init data:
```
$ source ./scripts/dev_env.sh
$ python manage.py db upgrade
```


#### Running:
```
$ ./scripts/run.sh
```
**open localhost:5000/admin*
<hr><hr>


## GET STARTED (With Docker):
**Running:**
```sh
sudo ./scripts/docker_run_dev.sh
```
**open localhost:5001/admin*


<hr><hr>

## Deploy (Docker):
```
$ sudo ./scripts/docker_run_prod.sh
```


<hr><hr>

## Deploy (Heroku):

```sh
$ heroku login
$ heroku create app_name
$ git remote add heroku heroku_git_url
$ heroku addons:create heroku-postgresql:hobby-dev --app app_name
```

See database url with command:
```sh
$ heroku config --app app_name
```
Then Paste database URL to scripts/heroku_config.sh. Next commit your code changes and then:

```shell script
$ git push heroku master
$ ./scripts heroku_config.sh
$ heroku run python manage.py db upgrade
```
**Open app_name.herokuapp.com/admin on your browser*






<hr><hr>

## NOTES
**Drop database**
```shell script
DROP DATABASE village_scrape_prod;
DROP DATABASE village_scrape_dev;
DROP DATABASE village_scrape_test;
```


**How migration**:
```
$ python manage.py db migrate
$ python manage.py db upgrade
```

**Exec DB (docker)**
```sh
sudo ./scripts/engine-db.sh
psql -U postgres
```

**Migrate DB (docker)**
```sh
sudo ./scripts/engine.sh
python manage.py db migrate
python manage.py db upgrade
```

**Remote Server:**
```sh
$ sudo ./scripts/connect_server.sh
```