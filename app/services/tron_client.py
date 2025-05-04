from tronpy import Tron
from tronpy.providers import HTTPProvider
from typing import Optional


class TronCustomClient:
    def __init__(self, api_key: str) -> None:
        self.client = Tron(HTTPProvider(
            "https://api.shasta.trongrid.io",
            api_key=api_key))

    def get_tron_info(self, address: str) -> Optional[dict]:
        try:
            account = self.client.get_account(address)
            resources = self.client.get_account_resource(address)

            return {
                "bandwidth": resources.get("freeNetUsed", 0),
                "energy": resources.get("EnergyUsed", 0),
                "trx_balance": account.get("balance", 0),
            }

        except Exception as e:
            print(f'Tron API error: {e}')
            return None
