# movies-db

The app is hosted on http://movies-db-ng.herokuapp.com/

## Project setup

Requirements:
* Python 3.6 and above

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

Synchronize database:
```
python manage.py migrate
```

To start development server run:
```
python manage.py runserver
```

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