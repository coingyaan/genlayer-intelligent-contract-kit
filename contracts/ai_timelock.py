# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class TimelockPrimitive(gl.Contract):
    owner: Address
    unlock_time: u256
    protected_value: str
    status: str
    validation_url: str
    validation_marker: str

    def __init__(
        self,
        unlock_time: u256,
        protected_value: str,
        validation_url: str,
        validation_marker: str,
    ):
        if unlock_time <= gl.block.timestamp:
            raise gl.vm.UserError("UNLOCK_TIME_MUST_BE_IN_FUTURE")

        if validation_marker == "":
            raise gl.vm.UserError("VALIDATION_MARKER_REQUIRED")

        self.owner = gl.message.sender_address
        self.unlock_time = unlock_time
        self.protected_value = protected_value
        self.status = "LOCKED"
        self.validation_url = validation_url
        self.validation_marker = validation_marker

    def _verify_external_condition(self) -> bool:
        url = self.validation_url
        marker = self.validation_marker

        def check_evidence():
            page = gl.nondet.web.get(url)
            body = page.body.decode("utf-8")
            return marker.lower() in body.lower()

        return gl.eq_principle.strict_eq(check_evidence)

    @gl.public.write
    def unlock(self) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("ONLY_OWNER_CAN_UNLOCK")

        if self.status != "LOCKED":
            raise gl.vm.UserError("TIMELOCK_ALREADY_UNLOCKED")

        if gl.block.timestamp < self.unlock_time:
            raise gl.vm.UserError("TIMELOCK_NOT_EXPIRED")

        if not self._verify_external_condition():
            raise gl.vm.UserError("EXTERNAL_CONDITION_NOT_VERIFIED")

        self.status = "UNLOCKED"

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_unlock_time(self) -> u256:
        return self.unlock_time

    @gl.public.view
    def get_value(self) -> str:
        return self.protected_value

    @gl.public.view
    def get_owner(self) -> Address:
        return self.owner