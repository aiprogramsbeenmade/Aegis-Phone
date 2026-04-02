import httpx
from src.modules.base_module import BaseModule
from typing import Dict, Any, List

class IdentityFinder(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.platforms = {
            "GitHub": "https://github.com/",
            "Instagram": "https://www.instagram.com/",
            "Twitter": "https://twitter.com/",
            "Pinterest": "https://www.pinterest.com/"
        }

    async def check_username(self, username: str) -> Dict[str, Any]:
        found = []
        async with httpx.AsyncClient(timeout=5.0) as client:
            for platform, url in self.platforms.items():
                try:
                    target = f"{url}{username}"
                    resp = await client.get(target)
                    if resp.status_code == 200:
                        found.append(platform)
                except:
                    continue
        return {"username": username, "found_on": found}