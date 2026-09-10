import httpx


class OpenDotaClient:

    BASE_URL = "https://api.opendota.com/api"

    def __init__(self):
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=10.0,
        )

    def get(self, path: str, params: dict | None = None):
        response = self._client.get(
            path,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    def close(self):
        self._client.close()