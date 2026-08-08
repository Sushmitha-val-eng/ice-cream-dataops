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
    client_name="delete-job-client",
    project="cdf-bootcamp-02-test",
    credentials=creds,
    base_url="https://westeurope-1.cognitedata.com"
)

client = CogniteClient(cnf)

# First list all jobs to find the duplicate
jobs = client.hosted_extractors.jobs.list(limit=None)
print(f"Total jobs: {len(jobs)}")
for j in jobs:
    print(f"Job ID: '{j.external_id}'")
