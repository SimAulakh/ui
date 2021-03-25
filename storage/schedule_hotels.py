from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class ScheduledReservation(Base):
    """ Blood Pressure """

    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    check_in = Column(String(100), nullable=False)
    check_out = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, city, country, check_in, check_out):
        """ Initializes an immediate hotel reservation """
        self.customer_id = customer_id
        self.city = city
        self.country = country
        self.check_in = check_in
        self.check_out = check_out
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of an immediate hotel reservation request """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['city'] = self.city
        dict['country'] = self.country
        dict['check_in'] = self.check_in
        dict['check_out'] = self.check_out
        dict['date_created'] = self.date_created

        return dict
