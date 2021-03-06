# movies-db

The app is hosted on http://movies-db-ng.herokuapp.com/

## Project setup

Requirements:
* Python 3.6 and above
* PostgreSQL 9.6

Clone project repo and navigate to directory.
```
git clone https://github.com/umatbro/movies-db.git
cd movies-db
```

Create virtualenv for this project and activate it (*optional*)
```
python -m venv movies-env
# On windows:
"movies-env/Scripts/activate.bat"
# on Linux/mac:
source movies-env/bin/activate
```

Install required Python packages:
```
pip install -r requirements.txt
```

Create Postgres database. By default, the app will use database with following settings:
```
{
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'movies_db',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '127.0.0.1',
    'PORT': '5432',
}
```

If you want to use your custom database you should set `DATABASE_URL` environmental variable. 

```
postgres://{user}:{password}@{hostname}:{port}/{database-name}
```

Synchronize database:
```
python manage.py migrate
```

To start development server run:
```
python manage.py runserver
```

If you want to run server in development mode set `PROD_ENV` environmental variable 
```
PROD_ENV=1
```

If you set `SECRET_KEY` envirionmental variable it will override default value stored in settings.py file.

## Endpoints

### `/movies/`

<table>
  <tr>
    <th colspan="2"><span style="font-weight:bold">GET</span> - get list of movies (filtering available)</th>
  </tr>
  <tr>
    <td>query param</td>
    <td>description</td>
  </tr>
  <tr>
    <td><br>title</td>
    <td>type: String<br>Filter by title. Lookup expression: 'icontains'<br></td>
  </tr>
  <tr>
    <td><br>duration__gt<br></td>
    <td>type: Integer<br><br>Filter movies with duration greater than the given number (unit: minutes)</td>
  </tr>
  <tr>
    <td><br>duration__lt</td>
    <td>type: Integer<br>Filter movies with duration less than the given number (unit: minutes)<br></td>
  </tr>
  <tr>
    <td>release_date</td>
    <td>type: String<br>Filter movies by exact date. Date should be provided in format: "YYYY-MM-DD".<br></td>
  </tr>
  <tr>
    <td>release_year</td>
    <td>type: Number<br>Filter movies from a given year.<br></td>
  </tr>
  <tr>
    <td>release_year__gt</td>
    <td>type: Number<br>Filter movies released after the given year.<br></td>
  </tr>
  <tr>
    <td>release_year__lt</td>
    <td>type: Number<br>Filter movies released before the given year.<br></td>
  </tr>
  <tr>
    <td>director</td>
    <td>type: String<br>Filter movies with given director.<br></td>
  </tr>
</table>
<table>
  <tr>
    <th colspan="2"><span style="font-weight:bold">POST</span> - add new movie to the database</td>
  </tr>
  <tr>
    <td>title</td>
    <td>Type: String, *required*<br>Title of the movie to be added.<br></td>
  </tr>
</table>

### `/comments/`

<table>
  <tr>
    <th colspan="2">GET - get list of comments</th>
  </tr>
  <tr>
    <td>movie_id</td>
    <td><br>type: Integer<br>Filter by movie id.<br><br></td>
  </tr>
</table>

<table>
  <tr>
    <th colspan="2">POST - create a new comment</th>
  </tr>
  <tr>
    <td>movie_id</td>
    <td><br>type: Integer, *required*<br>Comment will be assigned to this movie<br><br></td>
  </tr>
  <tr>
    <td>body</td>
    <td><br>type: String *required*<br>Comment's body<br></td>
  </tr>
  <tr>
    <td>publish_date</td>
    <td><br>type: String *optional*<br>If ommited, current date will be saved to database.
    <br>Valid inputs are formats accepted by Python's <a href="https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse">dateutil.parser.parse function.</a><br></td>
  </tr>
</table>


### `/top/`

<table>
  <tr>
    <th colspan="2">GET - get top movies from given date range</th>
  </tr>
  <tr>
    <td>date_from</td>
    <td>type: String, *required*<br>Comments with publish_date greater than or equal this date will be taken into account for ranking calculations.<br></td>
  </tr>
  <tr>
    <td>date_until<br></td>
    <td>type: String, *required*<br>Comments with publish_date less than or equal this date will be taken into account for ranking calculations.</td>
  </tr>
</table>


## Project structure

Libraries and database choices:

* `django-rest-framework` - used for API endpoints views and model serializers.
* `django-filter` - allows creating complex filters with little effort
* PostgreSQL - for a small project like this sqlite might be a good choice but in this case, PG was used due to 
following reasons: 
  * Heroku provides free Postgres database for django apps
  * some of the queries used in app were not running on sqlite

Django apps:
* `movies_api` - contanis `Movie` model and Movie views
* `comments` - contains `Comment` model and view associated with this model
* `business_logic` - this is not traditional django app but this module separates application's business logic (adding new movies, adding comments, generating the ranking)

## tests

Run unit tests with this command
```
python manage.py test
```

Test cases locations:
* `movies_api/tests`
* `comments/tests`
* `business_logic/tests`
