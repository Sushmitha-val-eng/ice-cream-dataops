from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
import os

creds = OAuthClientCredentials(
    token_url=os.environ.get("ICAPI_EXTRACTORS_TOKEN_URL", "https://login.microsoftonline.com/16e3985b-ebe8-4e24-9da4-933e21a9fc81/oauth2/v2.0/token"),
    client_id=os.environ["ICAPI_EXTRACTORS_CLIENT_ID"],
    client_secret=os.environ["ICAPI_EXTRACTORS_CLIENT_SECRET"],
    scopes=["https://westeurope-1.cognitedata.com/.default"],
)

cnf = ClientConfig(
    client_name="check-raw-client",
    project="cdf-bootcamp-02-test",
    credentials=creds,
    base_url="https://westeurope-1.cognitedata.com"
)

client = CogniteClient(cnf)

# Count all rows in assets table
rows = client.raw.rows.list("ice-cream-factory-db", "assets", limit=-1)
print(f"Total rows in assets table: {len(rows)}")

# Count assets in CDF
assets = client.assets.list(limit=-1)
print(f"Total assets in CDF: {len(assets)}")

# Count time series in CDF
ts = client.time_series.list(limit=-1)
print(f"Total time series in CDF: {len(ts)}")
