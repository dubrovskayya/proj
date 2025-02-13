import os
import pymysql
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename=os.getenv('LOGFILE_PATH'), level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# create all the necessary tables
categories = """
CREATE TABLE  categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150));
"""

events = """
CREATE TABLE  events (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(150),
    description VARCHAR(350),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE cascade);
"""

locations = """CREATE TABLE event_locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    event_date DATETIME,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    UNIQUE (event_id, latitude, longitude)
);"""

with pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                     database=os.getenv('DB_BASE')) as conn:
    try:
        cursor = conn.cursor()
        cursor.execute(categories)
        conn.commit()

        cursor.execute(events)
        conn.commit()

        cursor.execute(locations)
        conn.commit()

    except Exception as e:
        logging.error(f'DB Error {str(e)}')

    finally:
        cursor.close()
