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

print("✅ Data written to PostgreSQL successfully!")
