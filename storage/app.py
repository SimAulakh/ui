import connexion
import yaml
import logging
import logging.config
import datetime
import json
import logger

from connexion import NoContent
from pykafka.common import OffsetType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from immediate_hotels import ImmediateReservation
from schedule_hotels import ScheduledReservation
from pykafka import KafkaClient
from threading import Thread

with open('app_conf.yml', 'r') as f:
    app_conf = yaml.safe_load(f.read())

user = app_conf['datastore']['user']
password = app_conf['datastore']['password']
host_name = app_conf['datastore']['hostname']
port = app_conf['datastore']['port']
db = app_conf['datastore']['db']

DB_ENGINE = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (user, password, host_name, port, db))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_immediate_requests(timestamp):
    """Gets new immediate hotel reservation requests after the timestamp"""
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(ImmediateReservation).filter(ImmediateReservation.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logging.info("Query for Immediate Hotel reservation requests after %s returns %d results" %
                (timestamp, len(results_list)))

    return results_list, 200


def get_scheduled_requests(timestamp):

    """Gets new scheduled hotel reservation requests after the timestamp"""

    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)

    readings = session.query(ScheduledReservation).filter(ScheduledReservation.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logging.info("Query for Scheduled Hotel reservation requests after %s returns %d results" %
                 (timestamp, len(results_list)))

    return results_list, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_conf["events"]["hostname"],
                          app_conf["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_conf["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logging.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "ImmediateHotelReservation":
            session = DB_SESSION()

            immediate = ImmediateReservation(payload['customer_id'],
                                             payload['city'],
                                             payload['country'],
                                             payload['no_of_days'])

            session.add(immediate)

            session.commit()
            session.close()

            logging.debug("Stored event find_hotels_immediately request with a unique id of %s" % payload['customer_id'])

        # Change this to your event type # Store the event1 (i.e., the payload) to the DB
        elif msg["type"] == "ScheduledHotelReservation":
            session = DB_SESSION()

            immediate = ScheduledReservation(payload['customer_id'],
                                             payload['city'],
                                             payload['country'],
                                             payload['check_in'],
                                             payload['check_out'])

            session.add(immediate)

            session.commit()
            session.close()

            logging.debug(
                "Stored event schedule hotels request with a unique id of %s" % payload['customer_id'])

    # Commit the new message as being read
    consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
