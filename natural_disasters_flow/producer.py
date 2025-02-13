import json
import os
import logging
from confluent_kafka import Producer
from dotenv import load_dotenv
from api_requests import get_data

load_dotenv()

logging.basicConfig(filename=os.getenv('LOGFILE_PATH'), level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
try:
    events = get_data()

    producer_config = {
        'bootstrap.servers': os.getenv('SERVER_FOR_KAFKA'),
        'client.id': 'disaster-producer'
    }
    producer = Producer(producer_config)

    # pass all found events to the natural_disasters topic
    for event in events:
        producer.produce(topic='natural_disasters',
                         value=json.dumps(event))

    producer.flush()

except Exception as e:
    logging.error(f'Producer Error {e}')
