# Project Setup

### Clone the project

```
git clone https://github.com/Himanshu9714/FlaskAndJSChartJS.git
```

## Backend

### Change directory

```
cd server
```

### Create the python virtual environment

Create

```
python -m venv venv
```

Activate

```
Windows: venv/Scripts/activate
Mac: source venv/bin/activate
```

### Install the dependencies

```
pip install -r requirements.txt
```

### Set the flask app

```
Windows: set FLASK_APP=app.py
Mac: export FLASK_APP=app.py
```

### Run the flask app

```
flask run
```

### DB Migrations

Run the migrations

```
flask db upgrade
```

To create a new migration

```
flask db migrate -m "<message>"
```

#### Data import

Load the data to the database from json file

```
flask app import_json_data -p <path/to/json_file>
```

### API Endpoints

- `/get-rows`: Get all the analytics data
- `/get-stats`: Get the stats for the intensity, relevance, and likelihood year wise
- `/get-counts`: Get number of records belongs to passed group by key (country, region, sector, source, or topic)

## Frontend

- Run the index.html file on live server and see the visualization.
