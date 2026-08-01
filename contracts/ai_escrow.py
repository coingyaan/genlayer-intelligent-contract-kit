# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class EscrowPrimitive(gl.Contract):
    depositor: Address
    beneficiary: Address
    amount: u256
    status: str

    def __init__(self, beneficiary: Address, amount: u256):
        self.depositor = gl.message.sender_address
        self.beneficiary = beneficiary
        self.amount = amount
        self.status = "CREATED"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_amount(self) -> u256:
        return self.amount

    @gl.public.view
    def get_depositor(self) -> Address:
        return self.depositor

    @gl.public.view
    def get_beneficiary(self) -> Address:
        return self.beneficiary

    @gl.public.write
    def release(self) -> None:
        if self.status != "CREATED":
            raise Exception("Escrow is not releasable")

        self.status = "RELEASED"

    @gl.public.write
    def refund(self) -> None:
        if self.status != "CREATED":
            raise Exception("Escrow is not refundable")

        self.status = "REFUNDED"