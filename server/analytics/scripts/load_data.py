import json
import click
from flask.cli import AppGroup
from ..extensions import db
from ..models import (
    Analytics,
    Source,
    Sector,
    Region,
    Country,
    Topic,
)
from ..schemas.base import (
    AnalyticsSchema,
)
from datetime import datetime as dt

cli = AppGroup("app")


def replace_empty_strings_with_none(record: dict):
    """The method replaces the blank values with the None."""

    for key, value in record.items():
        # if value is not none and it contains the blank string, update its value to none
        if (value is not None and isinstance(value, str) and value.strip() == "") or (
            not isinstance(value, bool) and not value
        ):
            record[key] = None


def process_dates(data, **kwargs):
    """Process the json `added` and `published` date keys in the proper datetime format."""

    # If added key is passed then format the value
    if "added" in data and data["added"]:
        data["added"] = dt.strptime(data["added"], "%B, %d %Y %H:%M:%S").strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    # If published key is passed then format the value
    if "published" in data and data["published"]:
        data["published"] = dt.strptime(
            data["published"], "%B, %d %Y %H:%M:%S"
        ).strftime("%Y-%m-%dT%H:%M:%S")

    return data


def update_or_create(
    db,
    model,
    filter_column,
    filter_value,
    column_attr_value_mapping: dict,
    get_if_found=False,
):
    """
    The method either updates or create the object for the passed model.

    It filter by the `filter_column` and `filter_value`, if obj exist, then it will perform the update operation else create operation.

    Additionally, if object exist, and `get_if_found` flag is set to True, then there will be updation on the object and it will simply return the object.
    """

    # Check if the object exist for the provided model by filtering
    obj = db.session.query(model).filter(filter_column == filter_value).first()

    # If flag is true and object exist, return the object
    if get_if_found and obj:
        return obj

    # If object exist, perform the update operation and update the column values with the passed one
    if obj:
        for col_attr, value in column_attr_value_mapping.items():
            setattr(obj, col_attr, value)

    # Else create a new object
    else:
        obj = model(**column_attr_value_mapping)
        db.session.add(obj)

    # Add the object to DB and return the refreshed object
    db.session.commit()
    db.session.refresh(obj)

    return obj


def get_relationships_for_obj(record: dict):
    """The method creates the reletionship objects for the `Analytics` if doesn't exist."""

    relationships = {
        "source": {
            "model": Source,
            "value": record.pop("source", None),
            "column": Source.name,
            "column_attr": "name",
            "result": None,
        },
        "topic": {
            "model": Topic,
            "value": record.pop("topic", None),
            "column": Source.name,
            "column_attr": "name",
            "result": None,
        },
        "region": {
            "model": Region,
            "value": record.pop("region", None),
            "column": Source.name,
            "column_attr": "name",
            "result": None,
        },
        "country": {
            "model": Country,
            "value": record.pop("country", None),
            "column": Source.name,
            "column_attr": "name",
            "result": None,
        },
        "sector": {
            "model": Sector,
            "value": record.pop("sector", None),
            "column": Source.name,
            "column_attr": "name",
            "result": None,
        },
    }
    for key, value in relationships.items():
        if value["value"]:
            relationships[key]["result"] = update_or_create(
                db,
                value["model"],
                value["column"],
                value["value"],
                {value["column_attr"]: value["value"]},
                get_if_found=True,
            )

    return relationships


@cli.command("import_json_data")
@click.option("-p", "--path", "path", required=True)
def import_json_data(path):
    """
    The method loads the data from the json file and save it to the DB.
    """

    # Read the json file
    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    # Analytics model schema for the data validation
    analytics_schema = AnalyticsSchema()

    # Loop through each record
    for idx, record in enumerate(data):
        print(idx)

        # Replace empty string with none
        replace_empty_strings_with_none(record)

        # Reformat the added and published key date formats
        record = process_dates(record)

        # Get relationship objects for the analytic record
        relationships = get_relationships_for_obj(record)

        # Validate the data using Marshmallow schema
        record = analytics_schema.load(record)

        # Create or update the analytics record
        analytics_obj = update_or_create(
            db, Analytics, Analytics.title, record["title"], record
        )

        # Assign the relationship objects to the parent object
        for key, value in relationships.items():
            setattr(analytics_obj, key, value["result"])

    # Commit changes to the database
    db.session.commit()
    print("Data import completed successfully.")
