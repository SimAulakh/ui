import connexion
import json
import os.path
import requests
import yaml
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

json_file = app_config['datastore']['filename']
url = app_config['eventstore']['url']


def populate_stats():
    """Periodically update stats"""
    logger.info("Start Periodic Processing")

    # Reading contents of the json file/ setting default values if doesn't exist
    if os.path.exists(json_file):
        with open(json_file, 'r') as j:
            json_stats = j.read()
            current_stats = json.loads(json_stats)
    else:
        default_values = {
            "num_imm_requests": 0,
            "num_sch_requests": 0,
            "current_date_time_n": "2021-03-07T11:20:02"
        }

        with open(json_file, 'w') as j:
            j.write(json.dumps(default_values))

    dt = datetime.now()
    current_dt = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    get_endpts = requests.get(url + "/requests/immediate?timestamp=" + current_dt)
    no_imm_events = len(get_endpts.json())
    if get_endpts.status_code == 200:
        logger.info("INFO: No. of immediate hotel reservation requests: %d" % no_imm_events)
    else:
        logger.error("ERROR: Received a %d response code instead of 200" % get_endpts.status_code)

    get_sch_endpts = requests.get(url + "/requests/scheduled?timestamp=" + current_dt)
    no_sch_events = len(get_sch_endpts.json())
    if get_endpts.status_code == 200:
        logger.info("INFO: No. of scheduled hotel reservation requests: %d" % no_sch_events)
    else:
        logger.error("ERROR: Received a %d response code instead of 200" % get_sch_endpts.status_code)

    current_stats["num_imm_requests"] += no_imm_events
    current_stats["num_sch_requests"] += no_sch_events
    current_stats["current_dt"] = current_dt

    with open(json_file, 'w') as j:
        j.write(json.dumps(current_stats))

    logger.debug("DEBUG: Updated statistics values are imm: %s, sch: %s, timestamp: %s" %
                 (get_endpts, get_sch_endpts, current_dt))
    logger.info("Periodic processing finished")


def get_stats():
    logger.info("Request has started")
    if os.path.exists(json_file):
        with open(json_file, 'r') as j:
            json_stats = j.read()
            current_stats = json.loads(json_stats)
    else:
        logger.error("ERROR: Statistics do not exist")
        return 404

    logger.debug("DEBUG: Current statistics are: %s" % current_stats)
    logger.info("Request has completed")
    return current_stats, 200


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
