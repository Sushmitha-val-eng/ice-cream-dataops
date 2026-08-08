from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
import os
from cognite.client.data_classes.data_modeling import filters

creds = OAuthClientCredentials(
    token_url=os.environ.get("ICAPI_EXTRACTORS_TOKEN_URL", "https://login.microsoftonline.com/16e3985b-ebe8-4e24-9da4-933e21a9fc81/oauth2/v2.0/token"),
    client_id=os.environ["ICAPI_EXTRACTORS_CLIENT_ID"],
    client_secret=os.environ["ICAPI_EXTRACTORS_CLIENT_SECRET"],
    scopes=["https://westeurope-1.cognitedata.com/.default"],
)

cnf = ClientConfig(
    client_name="check-my-data-client",
    project="cdf-bootcamp-02-test",
    credentials=creds,
    base_url="https://westeurope-1.cognitedata.com"
)

client = CogniteClient(cnf)

# List nodes only in YOUR space
nodes = client.data_modeling.instances.list(
    instance_type="node",
    space="icapi_dm_space",
    limit=-1
)
print(f"Total nodes in icapi_dm_space: {len(nodes)}")
