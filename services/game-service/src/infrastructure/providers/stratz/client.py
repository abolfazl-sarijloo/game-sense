import httpx


class StratzClient:

    BASE_URL = "https://api.stratz.com/graphql"

    def __init__(self, token: str):
        self.token = token

    def execute(
        self,
        query: str,
        variables: dict | None = None,
    ) -> dict:

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "graphql-require-preflight": "1",
            "User-Agent": "GameSense",
        }

        response = httpx.post(
            self.BASE_URL,
            json={
                "query": query,
                "variables": variables or {},
            },
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        if result.get("errors"):
            raise RuntimeError(
                result["errors"]
            )

        return result.get("data", {})