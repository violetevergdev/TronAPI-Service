from tronpy import Tron
from tronpy.providers import HTTPProvider
from typing import Optional, Dict, Any


class TronCustomClient:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.client = Tron(HTTPProvider("https://api.shasta.trongrid.io",
                                        api_key=self.config['tron-api']['api-key']),
                           network='shasta')

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
