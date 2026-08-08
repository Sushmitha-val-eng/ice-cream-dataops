import re
import os
from cognite.client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials


def load_env(path=".env"):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def find_clients(env):
    # Look for common CLIENT_ID / CLIENT_SECRET pairs by prefix
    prefixes = set()
    for k in env:
        m = re.match(r"([A-Z0-9_]+)_CLIENT_ID$", k)
        if m:
            prefixes.add(m.group(1))
    # Also include IDP_CLIENT_ID if present
    if "IDP_CLIENT_ID" in env:
        prefixes.add("IDP")
    clients = []
    for p in prefixes:
        idk = f"{p}_CLIENT_ID"
        ssk = f"{p}_CLIENT_SECRET"
        if idk in env and ssk in env:
            clients.append((p, env[idk], env[ssk]))
    return clients


def inspect_client(token_url, scopes, project, base_url, client_id, client_secret):
    try:
        config = ClientConfig(
            client_name=f"inspect-{client_id[:8]}",
            project=project,
            base_url=base_url,
            credentials=OAuthClientCredentials(
                token_url=token_url,
                client_id=client_id,
                client_secret=client_secret,
                scopes=[scopes] if isinstance(scopes, str) else scopes,
            ),
        )
        client = CogniteClient(config)
        res = client.iam.token.inspect()
        return res
    except Exception as e:
        return {"error": str(e)}


def main():
    env = load_env()
    token_url = env.get("IDP_TOKEN_URL")
    scopes = env.get("IDP_SCOPES", "https://westeurope-1.cognitedata.com/.default")
    project = env.get("CDF_PROJECT", None)
    base_url = env.get("CDF_URL", "https://westeurope-1.cognitedata.com")

    clients = find_clients(env)
    if not clients:
        print("No client id/secret pairs found in .env")
        return

    for prefix, cid, csecret in clients:
        print(f"--- Inspecting {prefix} (client_id={cid}) ---")
        out = inspect_client(token_url, scopes, project, base_url, cid, csecret)
        print(out)


if __name__ == "__main__":
    main()
