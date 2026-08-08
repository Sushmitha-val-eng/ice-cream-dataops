from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
import os
from cognite.client.data_classes.data_modeling.cdm.v1 import CogniteAsset, CogniteTimeSeries

creds = OAuthClientCredentials(
    token_url=os.environ.get("ICAPI_EXTRACTORS_TOKEN_URL", "https://login.microsoftonline.com/16e3985b-ebe8-4e24-9da4-933e21a9fc81/oauth2/v2.0/token"),
    client_id=os.environ["ICAPI_EXTRACTORS_CLIENT_ID"],
    client_secret=os.environ["ICAPI_EXTRACTORS_CLIENT_SECRET"],
    scopes=["https://westeurope-1.cognitedata.com/.default"],
)

cnf = ClientConfig(
    client_name="check-dm-client",
    project="cdf-bootcamp-02-test",
    credentials=creds,
    base_url="https://westeurope-1.cognitedata.com"
)

client = CogniteClient(cnf)

# Count DM assets
assets = client.data_modeling.instances.list(
    sources=[CogniteAsset.get_source()],
    limit=-1
)
print(f"Total DM assets: {len(assets)}")

# Count DM time series
ts = client.data_modeling.instances.list(
    sources=[CogniteTimeSeries.get_source()],
    limit=-1
)
print(f"Total DM time series: {len(ts)}")
