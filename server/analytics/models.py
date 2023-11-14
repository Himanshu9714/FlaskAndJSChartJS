from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Column
from .extensions import db
from datetime import datetime as dt


class IdMixin:
    """ID Mixin for the id field"""

    id = Column(Integer, primary_key=True)


class TimeStampMixin:
    """Time stamp mixin for the record"""

    created_at = Column(DateTime, nullable=False, default=dt.utcnow())
    updated_at = Column(DateTime, nullable=True)


class CommonMixin(IdMixin, TimeStampMixin):
    """Common mixin for each model"""

    pass


class Sector(CommonMixin, db.Model):
    """Sector"""

    __tablename__ = "sectors"

    # sector name
    name = Column(String, nullable=False)


class Region(CommonMixin, db.Model):
    """Region"""

    __tablename__ = "regions"

    # Region name
    name = Column(String, nullable=False)


class Country(CommonMixin, db.Model):
    """Country"""

    __tablename__ = "countries"

    # country name
    name = Column(String, nullable=False)


class Topic(CommonMixin, db.Model):
    """Topic"""

    __tablename__ = "topics"

    # topic name
    name = Column(String, nullable=False)


class Source(CommonMixin, db.Model):
    """Source"""

    __tablename__ = "sources"

    # source name
    name = Column(String, nullable=False)


class Analytics(CommonMixin, db.Model):
    """Analytics"""

    __tablename__ = "analytics"

    # Title for which the insights are generated
    title = Column(Text, unique=True, nullable=False)

    # End year at when the forecast impact should end
    end_year = Column(Integer, nullable=True)

    # Start year at when the forecast impact should start
    start_year = Column(Integer, nullable=True)

    # Defines the intensity, relevance, and likelihood score
    intensity = Column(Integer, nullable=True)
    relevance = Column(Integer, nullable=True)
    likelihood = Column(Integer, nullable=True)

    # Insight for the pestle
    insight = Column(String, nullable=True)
    impact = Column(Integer, nullable=True)

    # url from where the information is gathered and has detailed version
    url = Column(String, nullable=True)

    # pestle category
    pestle = Column(String, nullable=True)
    added = Column(DateTime, nullable=True)
    published = Column(DateTime, nullable=True)

    # Source of information
    source_id = Column(
        Integer, ForeignKey("sources.id", ondelete="SET NULL"), nullable=True
    )
    source = relationship("Source", backref="analytics")

    # Related sector
    sector_id = Column(
        Integer, ForeignKey("sectors.id", ondelete="SET NULL"), nullable=True
    )
    sector = relationship("Sector", backref="analytics")

    # Related region
    region_id = Column(
        Integer, ForeignKey("regions.id", ondelete="SET NULL"), nullable=True
    )
    region = relationship("Region", backref="analytics")

    # Related country
    country_id = Column(
        Integer, ForeignKey("countries.id", ondelete="SET NULL"), nullable=True
    )
    country = relationship("Country", backref="analytics")

    # Related topic
    topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
    )
    topic = relationship("Topic", backref="analytics")
