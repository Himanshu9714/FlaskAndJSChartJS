from flask import request
from flask_restful import Resource

from sqlalchemy import func
from sqlalchemy import distinct

from ..extensions import db
from ..models import Analytics
from ..models import Country
from ..models import Region
from ..models import Sector
from ..models import Source
from ..models import Topic
from ..schemas.base import AnalyticsResponseSchema


class AnalyticsView(Resource):
    def get(self):
        """Get all the analytics record."""

        # Pagination
        page = request.args.get("page", type=int, default=1)
        per_page = request.args.get("per_page", type=int, default=10)
        offset = (page - 1) * per_page

        # Get the analytics records
        analytics = db.session.query(Analytics).limit(per_page).offset(offset).all()

        # Dump the DB objects with marshmallow schema
        analytics_records = AnalyticsResponseSchema().dump(analytics, many=True)

        # Return the json data
        return analytics_records


class IntensityRelevanceLikelihoodChartView(Resource):
    def post(self):
        """Get the stats for intensity, relevance, and likelihood.

        User can filter the years ranges.
        He can choose the start and end year and the API will return the records that falls in that range.
        """

        # Get the paylod body
        payload = request.json

        # Get the start and end year the user has selected
        start = payload.get("start_year", None)
        end = payload.get("end_year", None)

        # Check if start and end is none or not
        start = start if start != "--" else None
        end = end if end != "--" else None

        # Query the Analytics model
        analytics = db.session.query(
            Analytics.start_year,
            Analytics.end_year,
            Analytics.intensity,
            Analytics.relevance,
            Analytics.likelihood,
        ).filter(
            Analytics.start_year.is_not(None),
            Analytics.end_year.is_not(None),
        )

        # If start and end years are passed, filter the result
        if start and end:
            analytics = analytics.filter(
                Analytics.start_year.between(start, end),
                Analytics.end_year.between(start, end),
            )

        # Create the response
        year_wise_data = dict()
        for row in analytics:
            # Get the column values
            start_year = int(row[0])
            end_year = int(row[1])
            intensity = row[2] if row[2] else 0
            relevance = row[3] if row[3] else 0
            likelihood = row[4] if row[4] else 0

            # Add the year as key starting from start to end for this record
            while start_year <= end_year:
                # If there doesn't exist start_year in the mapping, add it
                if start_year not in year_wise_data:
                    year_wise_data[start_year] = {
                        "intensity": [intensity],
                        "relevance": [relevance],
                        "likelihood": [likelihood],
                    }

                # else updates the inner keys values
                else:
                    year_wise_data[start_year]["intensity"].append(intensity)
                    year_wise_data[start_year]["relevance"].append(relevance)
                    year_wise_data[start_year]["likelihood"].append(likelihood)

                # Increment the year
                start_year += 1

        # Calculate the average intensity, relevance, likelihood by year
        for key, value in year_wise_data.items():
            value["intensity"] = sum(value["intensity"]) / len(value["intensity"])
            value["relevance"] = sum(value["relevance"]) / len(value["relevance"])
            value["likelihood"] = sum(value["likelihood"]) / len(value["likelihood"])

        return year_wise_data


class NoOfRecordsByGroupView(Resource):
    def post(self):
        """Get the number of records by the provided group by key.

        User can visualize the number of records per country, region, source, topic, and sector.
        """

        # Get the paylod body
        payload = request.json

        # Get the start and end year the user has selected
        start = payload.get("start_year", None)
        start = start if start != "--" else None
        end = payload.get("end_year", None)
        end = end if end != "--" else None

        # Check if user has selected the group by key as well
        group_by = payload.get("group_by", "country")
        group_by = "country" if group_by == "--" else group_by

        # Possible group by values
        group_by_keys = {
            "country": {
                "col": Country.name,
                "model": Country,
                "joins": [Country.id == Analytics.country_id],
            },
            "region": {
                "col": Region.name,
                "model": Region,
                "joins": [Region.id == Analytics.region_id],
            },
            "sector": {
                "col": Sector.name,
                "model": Sector,
                "joins": [Sector.id == Analytics.sector_id],
            },
            "source": {
                "col": Source.name,
                "model": Source,
                "joins": [Source.id == Analytics.source_id],
            },
            "topic": {
                "col": Topic.name,
                "model": Topic,
                "joins": [Topic.id == Analytics.topic_id],
            },
        }

        # Get the records for the passed group by column
        records = (
            db.session.query(group_by_keys[group_by]["col"], func.count(Analytics.id))
            .join(group_by_keys[group_by]["model"], *group_by_keys[group_by]["joins"])
            .group_by(group_by_keys[group_by]["col"])
            .filter(group_by_keys[group_by]["col"].is_not(None))
        )

        # If start and end years are passed, filter the result
        if start and end:
            records = records.filter(
                Analytics.start_year.between(start, end),
                Analytics.end_year.between(start, end),
            )

        # Create the response by xaxis ad yaxis
        response = {"xaxis": [], "yaxis": []}
        for row in records:
            response["xaxis"].append(row[0])
            response["yaxis"].append(row[1])

        return response


class GetYearsView(Resource):
    def get(self):
        """Get the all possible years values for the FE dropdown."""

        # Get all the distinct start year list
        start_year_list = (
            db.session.query(distinct(Analytics.start_year))
            .filter(Analytics.start_year.is_not(None))
            .all()
        )
        # Restructured the list
        start_year_list = [year[0] for year in start_year_list]

        # Get all the distinct end year list
        end_year_list = (
            db.session.query(distinct(Analytics.end_year))
            .filter(Analytics.end_year.is_not(None))
            .all()
        )
        # Restructured the list
        end_year_list = [year[0] for year in end_year_list]

        # Union the start and end years list
        years_list = list(set(start_year_list).union(set(end_year_list)))

        # Return the sorted years list
        return {"years": sorted(years_list)}
