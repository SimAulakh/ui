from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class ImmediateReservation(Base):
    """ Blood Pressure """

    __tablename__ = "immediate"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    no_of_days = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, city, country, no_of_days):
        """ Initializes an immediate hotel reservation """
        self.customer_id = customer_id
        self.city = city
        self.country = country
        self.no_of_days = no_of_days
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of an immediate hotel reservation request """
        dict = {}
        dict['id'] = self.id
        dict['city'] = self.city
        dict['country'] = self.country
        dict['customer_id'] = self.customer_id
        dict['no_of_days'] = self.no_of_days
        dict['date_created'] = self.date_created

        return dict
