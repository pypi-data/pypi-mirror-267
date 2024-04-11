from typing import Any, List, Optional

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.client import RestClient
from aptos_sdk.async_client import RestClient as AsyncRestClient
from aptos_sdk.transactions import EntryFunction, TransactionPayload


class EconiaClient:
    econia_address: AccountAddress
    aptos_client: RestClient
    aptos_client_async: AsyncRestClient
    user_account: Account

    def __init__(
            self,
            node_url: str,
            econia: AccountAddress,
            account: Account,
            rest_client: Optional[RestClient] = None,
            rest_client_async: Optional[AsyncRestClient] = None,
            node_api_key: Optional[str] = None
        ):
        self.econia_address = econia
        if rest_client == None and rest_client_async == None:
            self.aptos_client = RestClient(node_url)
            if node_api_key != None:
                self.aptos_client.client.headers["Authorization"] = f"Bearer {node_api_key}"
        elif rest_client != None:
            if node_api_key != None:
                rest_client.client.headers["Authorization"] = f"Bearer {node_api_key}"
            self.aptos_client = rest_client
        elif rest_client_async != None:
            if node_api_key != None:
                rest_client_async.client.headers["Authorization"] = f"Bearer {node_api_key}"
            self.aptos_client_async = rest_client_async
        self.user_account = account

    def submit_tx(self, entry: EntryFunction) -> str:
        payload = TransactionPayload(entry)
        signed_tx = self.aptos_client.create_bcs_signed_transaction(
            self.user_account, payload
        )
        return self.aptos_client.submit_bcs_transaction(signed_tx)
    
    async def gen_submit_tx(self, entry: EntryFunction) -> str:
        payload = TransactionPayload(entry)
        signed_tx = await self.aptos_client_async.create_bcs_signed_transaction(
            self.user_account, payload
        )
        return await self.aptos_client_async.submit_bcs_transaction(signed_tx)

    def submit_tx_wait(self, entry: EntryFunction) -> str:
        txn_hash = self.submit_tx(entry)
        self.aptos_client.wait_for_transaction(txn_hash)
        return txn_hash
    
    async def gen_submit_tx_wait(self, entry: EntryFunction) -> str:
        txn_hash = await self.gen_submit_tx(entry)
        await self.aptos_client_async.wait_for_transaction(txn_hash)
        return txn_hash


class EconiaViewer:
    econia_address: AccountAddress
    aptos_client: RestClient

    def __init__(self, node_url: str, econia: AccountAddress, node_api_key: Optional[str] = None):
        self.econia_address = econia
        self.aptos_client = RestClient(node_url)
        if node_api_key != None:
            self.aptos_client.client.headers["Authorization"] = f"Bearer {node_api_key}"

    def get_returns(
        self,
        module: str,
        function: str,
        type_arguments: List[str] = [],
        arguments: List = [],  # string encoded args i.e "12345" or "0xabcdef" or "abracadabra"
        ledger_version: int = -1,
    ) -> List:
        if ledger_version < 0:
            request = f"{self.aptos_client.base_url}/view"
        else:
            request = (
                f"{self.aptos_client.base_url}/view?ledger_version={ledger_version}"
            )

        response = self.aptos_client.client.post(
            request,
            json={
                "function": f"{self.econia_address}::{module}::{function}",
                "type_arguments": type_arguments,
                "arguments": arguments,
            },
        )

        if response.status_code >= 400:
            raise Exception(response.text, response.status_code)
        return response.json()

    def get_events_by_handle(
        self,
        struct_type: str,  # i.e 0x1::account::Account
        field_name: str,
        limit: Optional[int] = None,
    ) -> Any:
        request = f"{self.aptos_client.base_url}/accounts/{self.econia_address.hex()}/events/{struct_type}/{field_name}"
        if limit is not None:
            request = f"{request}?limit={limit}"

        response = self.aptos_client.client.get(request)
        if response.status_code >= 400:
            raise Exception(response.text, response.status_code)
        return response.json()

    def get_events_by_creation_number(
        self,
        emission_address: AccountAddress,
        creation_number: int,
        limit: Optional[int] = None,
        start: Optional[int] = None,  # sequence number to start from
    ) -> Any:
        request = f"{self.aptos_client.base_url}/accounts/{emission_address.hex()}/events/{creation_number}"
        if limit is not None and start is not None:
            request = f"{request}?limit={limit}&start={start}"
        elif limit is not None:
            request = f"{request}?limit={limit}"
        elif start is not None:
            request = f"{request}?start={start}"

        response = self.aptos_client.client.get(request)
        if response.status_code >= 400:
            raise Exception(response.text, response.status_code)
        return response.json()
