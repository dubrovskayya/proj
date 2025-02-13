import logging
import os
import json
import pymysql
from confluent_kafka import Consumer
from dotenv import load_dotenv
from datetime import datetime
from api_requests import get_categories

load_dotenv()

# configure logging
logging.basicConfig(filename=os.getenv('LOGFILE_PATH'), level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# the function gets a dictionary of current categories and their IDs from the table
# to speed up the insertion of new events
def get_current_categories(connection, cursor):
    # get a list of current categories from the source
    # and insert them into the categories table if they are not there yet
    current_categories = [cat['title'] for cat in get_categories()]
    cursor.execute("SELECT name FROM categories")
    existing_categories = [row[0] for row in cursor.fetchall()]
    for category in current_categories:
        if category not in existing_categories:
            cursor.execute('INSERT INTO categories (name) VALUES (%s);', (category,))
    connection.commit()

    # get a dictionary of current categories
    cursor.execute("SELECT id, name FROM categories")
    result = {row[1]: row[0] for row in cursor.fetchall()}
    logging.error(f"consumer ran")
    return result


consumer_config = {
    'bootstrap.servers': os.getenv('SERVER_FOR_KAFKA'),
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# create the consumer and subscribe to the natural_disasters topic
consumer = Consumer(consumer_config)
consumer.subscribe(['natural_disasters'])

# track empty cycles to terminate the process when there is no more data
empty_cycles = 0

with pymysql.connect(host=os.getenv('HOST_x'), user=os.getenv('USER_x'), password=os.getenv('DB_PASSWORD_x'),
                     database=os.getenv('DB_x')) as conn:
    cursor = conn.cursor()
    try:
        categories = get_current_categories(conn, cursor)
        while True:
            try:
                message = consumer.poll(timeout=1.0)
                if not message:
                    empty_cycles += 1
                    # terminate the process after 10 empty cycles
                    if empty_cycles > 10:
                        cursor.close()
                        break
                    continue
                else:
                    empty_cycle = 0
                event = json.loads(message.value().decode('utf-8'))

                # get the category name  and assign the category_id according to the categories dictionary
                category_name = event['categories'][0]['title']
                category_id = categories[category_name]

                # insert the event data into the table, if it already exists we update it (information may change)
                event_insert_query = ('INSERT INTO events (id, title, description, category_id) VALUES (%s,%s,%s,%s) '
                                      'ON DUPLICATE KEY UPDATE title = VALUES(title), description = VALUES(description), '
                                      'category_id = VALUES(category_id);')
                event_values = (event['id'], event['title'], event['description'], category_id)
                cursor.execute(event_insert_query, event_values)

                # get all event locations and insert them into the location table
                locations = event['geometry']
                location_values_list = []

                # collect a list of locations
                for location in locations:
                    event_date = location['date']
                    formatted_date = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%SZ').strftime(
                        '%Y-%m-%d %H:%M:%S')  # transform date into the appropriate format
                    location_values = (
                        event['id'], location['coordinates'][1], location['coordinates'][0], formatted_date)
                    location_values_list.append(location_values)

                # insert locations into the table, skip if the  record already exists
                location_insert_query = 'INSERT IGNORE INTO event_locations (event_id,latitude,longitude,event_date) VALUES (%s,%s,%s,%s);'
                cursor.executemany(location_insert_query, location_values_list)

                # commit for db and kafka
                conn.commit()
                consumer.commit()

            except Exception as e:
                # on error, write to log and skip the message
                logging.error(f"Message {event['id']} skipped after failed attempt. Error {str(e)}.")
                conn.rollback()
                consumer.commit()
    except Exception as e:
        logging.error(f"Consumer Error {str(e)} {e}.")
        conn.rollback()
