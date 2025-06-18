#  REST API to Trino Integration

This project demonstrates how to extract data from a live REST API, load it into PostgreSQL on an AWS EC2 instance, connect that database to Trino, and make the data queryable from both Trino and external metadata tools like Informatica MCC.

##  Architecture Overview

```
REST API → Python → PostgreSQL → Trino 
```

##  Stack

- Python (pandas, SQLAlchemy, psycopg2)
- PostgreSQL
- Trino
- AWS EC2 (Ubuntu)

## Steps

### 1. Clone this repo and SSH into your EC2 instance.

### 2. Install dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib -y
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv apienv
source apienv/bin/activate
pip install pandas requests sqlalchemy psycopg2-binary
```

##  `fetch_api_data.py`

```python
import requests
import pandas as pd
from sqlalchemy import create_engine

# Fetch data
url = "https://jsonplaceholder.typicode.com/posts"
data = requests.get(url).json()
df = pd.DataFrame(data)

# PostgreSQL connection
engine = create_engine("postgresql://trino:trino@localhost/apidata")

# Write to Postgres
df.to_sql("posts", engine, if_exists="replace", index=False)

print(" Data written to PostgreSQL successfully!")
```

##  `setup_postgres.sql`

```sql
-- Run these as the 'postgres' user
CREATE DATABASE apidata;
CREATE USER trino WITH PASSWORD 'trino';
GRANT ALL PRIVILEGES ON DATABASE apidata TO trino;

-- Optional: assign schema ownership
\c apidata
ALTER SCHEMA public OWNER TO trino;
GRANT ALL ON SCHEMA public TO trino;
```

##  Trino PostgreSQL Connector

Place the file in `trino_catalog_config/postgres.properties`:

```properties
connector.name=postgresql
connection-url=jdbc:postgresql://localhost:5432/apidata
connection-user=trino
connection-password=trino
```

Restart Trino:

```bash
cd /trino-server-351
bin/launcher restart
```

##  Query from Trino CLI

```bash
./trino --server localhost:8080 --catalog postgres --schema public
```

```sql
SHOW TABLES;
SELECT * FROM posts LIMIT 5;
```



## Outcome

Trino now surfaces live API data for analytics. Enjoy!
