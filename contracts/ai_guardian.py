# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class GuardianPrimitive(gl.Contract):
    owner: Address
    protected_value: str
    pending_value: str
    status: str
    validation_url: str
    validation_marker: str

    def __init__(
        self,
        initial_value: str,
        validation_url: str,
        validation_marker: str,
    ):
        if validation_marker == "":
            raise gl.vm.UserError("VALIDATION_MARKER_REQUIRED")

        self.owner = gl.message.sender_address
        self.protected_value = initial_value
        self.pending_value = ""
        self.status = "ACTIVE"
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
    def propose(self, new_value: str) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("ONLY_OWNER_CAN_PROPOSE")

        if self.status != "ACTIVE":
            raise gl.vm.UserError("GUARDIAN_NOT_ACTIVE")

        self.pending_value = new_value
        self.status = "PENDING"

    @gl.public.write
    def approve(self) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("ONLY_OWNER_CAN_APPROVE")

        if self.status != "PENDING":
            raise gl.vm.UserError("NO_PENDING_CHANGE")

        if not self._verify_external_condition():
            raise gl.vm.UserError("EXTERNAL_CONDITION_NOT_VERIFIED")

        self.protected_value = self.pending_value
        self.pending_value = ""
        self.status = "ACTIVE"

    @gl.public.write
    def cancel(self) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("ONLY_OWNER_CAN_CANCEL")

        if self.status != "PENDING":
            raise gl.vm.UserError("NO_PENDING_CHANGE")

        self.pending_value = ""
        self.status = "ACTIVE"

    @gl.public.view
    def get_value(self) -> str:
        return self.protected_value

    @gl.public.view
    def get_pending_value(self) -> str:
        return self.pending_value

    @gl.public.view
    def get_status(self) -> str:
        return self.status

    @gl.public.view
    def get_owner(self) -> Address:
        return self.owner