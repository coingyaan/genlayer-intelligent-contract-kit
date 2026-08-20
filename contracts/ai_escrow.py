# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class EscrowPrimitive(gl.Contract):
    depositor: Address
    beneficiary: Address
    amount: u256
    release_url: str
    release_marker: str
    status: str

    def __init__(
        self,
        beneficiary: Address,
        amount: u256,
        release_url: str,
        release_marker: str,
    ):
        if amount == u256(0):
            raise gl.vm.UserError("ESCROW_AMOUNT_MUST_BE_POSITIVE")

        if release_marker == "":
            raise gl.vm.UserError("RELEASE_MARKER_REQUIRED")

        self.depositor = gl.message.sender_address
        self.beneficiary = beneficiary
        self.amount = amount
        self.release_url = release_url
        self.release_marker = release_marker
        self.status = "CREATED"

    @gl.public.write.payable
    def fund(self) -> None:
        if gl.message.sender_address != self.depositor:
            raise gl.vm.UserError("ONLY_DEPOSITOR_CAN_FUND")

        if self.status != "CREATED":
            raise gl.vm.UserError("ESCROW_ALREADY_FUNDED_OR_SETTLED")

        if gl.message.value != self.amount:
            raise gl.vm.UserError("INCORRECT_ESCROW_AMOUNT")

        self.status = "FUNDED"

    def _verify_release_condition(self) -> bool:
        url = self.release_url
        marker = self.release_marker

        def check_evidence():
            page = gl.nondet.web.get(url)
            body = page.body.decode("utf-8")
            return marker.lower() in body.lower()

        return gl.eq_principle.strict_eq(check_evidence)

    @gl.public.write
    def release(self) -> None:
        if gl.message.sender_address != self.beneficiary:
            raise gl.vm.UserError("ONLY_BENEFICIARY_CAN_RELEASE")

        if self.status != "FUNDED":
            raise gl.vm.UserError("ESCROW_NOT_FUNDED")

        if self.balance != self.amount:
            raise gl.vm.UserError("ESCROW_BALANCE_INVARIANT_FAILED")

        if not self._verify_release_condition():
            raise gl.vm.UserError("RELEASE_CONDITION_NOT_VERIFIED")

        self.emit_transfer(
            to=self.beneficiary,
            value=self.amount,
        )

        self.status = "RELEASED"

    @gl.public.write
    def refund(self) -> None:
        if gl.message.sender_address != self.depositor:
            raise gl.vm.UserError("ONLY_DEPOSITOR_CAN_REFUND")

        if self.status != "FUNDED":
            raise gl.vm.UserError("ESCROW_NOT_REFUNDABLE")

        if self.balance != self.amount:
            raise gl.vm.UserError("ESCROW_BALANCE_INVARIANT_FAILED")

        if self._verify_release_condition():
            raise gl.vm.UserError("RELEASE_CONDITION_IS_VERIFIED")

        self.emit_transfer(
            to=self.depositor,
            value=self.amount,
        )

        self.status = "REFUNDED"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_amount(self) -> u256:
        return self.amount

    @gl.public.view
    def get_balance(self) -> u256:
        return self.balance

    @gl.public.view
    def get_depositor(self) -> Address:
        return self.depositor

    @gl.public.view
    def get_beneficiary(self) -> Address:
        return self.beneficiary