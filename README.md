# movies-db

The app is hosted on http://movies-db-ng.herokuapp.com/

## project setup

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
