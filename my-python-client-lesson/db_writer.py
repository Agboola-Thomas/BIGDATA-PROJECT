from kafka import KafkaConsumer
from cockroach_connect import getConnection
import logging
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Get mandatory connection
conn = getConnection(True)

def setup_database():
    """Create the table if it does not exist."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cryptocurrency_data (
                    id SERIAL PRIMARY KEY,
                    crypto_id STRING,
                    name STRING,
                    symbol STRING,
                    current_price FLOAT,
                    market_cap BIGINT,
                    market_cap_rank INT,
                    total_volume BIGINT,
                    high_24h FLOAT,
                    low_24h FLOAT,
                    price_change_24h FLOAT,
                    price_change_percentage_24h FLOAT,
                    market_cap_change_24h BIGINT,
                    market_cap_change_percentage_24h FLOAT,
                    circulating_supply FLOAT,
                    total_supply FLOAT,
                    max_supply FLOAT,
                    ath FLOAT,
                    ath_change_percentage FLOAT,
                    ath_date TIMESTAMP,
                    atl FLOAT,
                    atl_change_percentage FLOAT,
                    atl_date TIMESTAMP,
                    last_updated TIMESTAMP
                )
            """)
            conn.commit()
            logging.debug("Table created or already exists.")
    except Exception as e:
        logging.error(f"Problem setting up the database: {e}")

def cockroachWrite(event):
    """Write Kafka event to the database."""
    try:
        # Decode and parse the JSON data from the Kafka event
        eventValue = event.value.decode('utf-8', errors='replace')
        data = json.loads(eventValue)

        # Extract relevant fields
        crypto_id = data.get('id')
        name = data.get('name')
        symbol = data.get('symbol')
        current_price = data.get('current_price')
        market_cap = data.get('market_cap')
        market_cap_rank = data.get('market_cap_rank')
        total_volume = data.get('total_volume')
        high_24h = data.get('high_24h')
        low_24h = data.get('low_24h')
        price_change_24h = data.get('price_change_24h')
        price_change_percentage_24h = data.get('price_change_percentage_24h')
        market_cap_change_24h = data.get('market_cap_change_24h')
        market_cap_change_percentage_24h = data.get('market_cap_change_percentage_24h')
        circulating_supply = data.get('circulating_supply')
        total_supply = data.get('total_supply')
        max_supply = data.get('max_supply')
        ath = data.get('ath')
        ath_change_percentage = data.get('ath_change_percentage')
        ath_date = datetime.fromisoformat(data.get('ath_date').replace('Z', '+00:00'))
        atl = data.get('atl')
        atl_change_percentage = data.get('atl_change_percentage')
        atl_date = datetime.fromisoformat(data.get('atl_date').replace('Z', '+00:00'))
        last_updated = datetime.fromisoformat(data.get('last_updated').replace('Z', '+00:00'))

        # Insert into the database
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cryptocurrency_data (
                    crypto_id, name, symbol, current_price, market_cap, market_cap_rank,
                    total_volume, high_24h, low_24h, price_change_24h,
                    price_change_percentage_24h, market_cap_change_24h,
                    market_cap_change_percentage_24h, circulating_supply,
                    total_supply, max_supply, ath, ath_change_percentage, ath_date,
                    atl, atl_change_percentage, atl_date, last_updated
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                crypto_id, name, symbol, current_price, market_cap, market_cap_rank,
                total_volume, high_24h, low_24h, price_change_24h,
                price_change_percentage_24h, market_cap_change_24h,
                market_cap_change_percentage_24h, circulating_supply,
                total_supply, max_supply, ath, ath_change_percentage, ath_date,
                atl, atl_change_percentage, atl_date, last_updated
            ))
            conn.commit()
            logging.debug("Data inserted successfully.")
    except Exception as e:
        logging.error(f"Problem writing to database: {e}")

# Initialize Kafka consumer
consumer = KafkaConsumer(
    "coingecko-crypto-data",
    bootstrap_servers=['broker:29092'], 
    auto_offset_reset='earliest'  # Replace with your Kafka server details
)

# Setup the database once
setup_database()

# Process messages
for msg in consumer:
    cockroachWrite(msg)
    logging.debug("Msg processed.")
