import connexion
import yaml

import logging
import logging.config
from connexion import NoContent
import requests
import datetime
import json
from pykafka import KafkaClient


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

hostname = app_config['events']['hostname']
port = app_config['events']['port']
topic_event = app_config['events']['topic']


def find_hotels_immediately(body):
    """Receives requests for immediate reservations"""
    headers = {"Content-Type": "application/json"}
    logger.info("Received event immediate hotel reservation request with a unique id of %s" % body['customer_id'])
    client = KafkaClient(hosts="%s:%d" % (hostname, port))
    topic = client.topics[str.encode(topic_event)]
    producer = topic.get_sync_producer()
    msg = {"type": "ImmediateHotelReservation",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info("Returned event Immediate hotel reservation response (id: %s) with 201 status code" %
                (body['customer_id']))

    return NoContent, 201


def find_scheduled_hotels(body):
    """Receives requests for immediate reservations"""
    headers = {"Content-Type": "application/json"}
    logger.info("Received event scheduled hotel reservation request with a unique id of %s" % body['customer_id'])

    client = KafkaClient(hosts= "%s:%d"%(hostname,port))
    topic = client.topics[str.encode(topic_event)]
    producer = topic.get_sync_producer()
    msg = {"type": "ScheduledHotelReservation",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info("Returned event Scheduled hotel reservation response (id: %s) with 201 status code" %
                (body['customer_id']))

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
