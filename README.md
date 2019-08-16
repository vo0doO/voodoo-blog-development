# Python + Heroku + Gunicorn

##### Django App.

## Get need you pipe's
 Just job. If you use [Pipe lines](https://devcenter.heroku.com/articles/pipelines).
```shell script
$ git clone https://github.com/vo0doo/voodoo-blog-development.git
```
```shell script
$ git clone https://github.com/vo0doo/voodoo-blog-staging.git
```

```shell script
$ git clone https://github.com/vo0doo/voodoo-blog-prodaction.git
```
## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ cd voodoo-blog-development

$ python3 -m venv voodoo-blog-development
$ pip install -r requirements.txt

$ createdb voodoo-blog-development

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku apps:create voodoo-blog-development
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
