# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise gl.vm.UserError(message)


def parse_json_response(text: str) -> dict:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise gl.vm.UserError("INVALID_ADJUDICATION_RESPONSE")

    return json.loads(text[start:end + 1])


@gl.evm.contract_interface
class _NativeRecipient:
    class View:
        pass

    class Write:
        pass


def send_native(recipient: Address, amount: u256) -> None:
    _NativeRecipient(recipient).emit_transfer(
        value=amount
    )


class IntelligentEscrow(gl.Contract):
    depositor: Address
    beneficiary: Address

    amount: u256

    evidence_url: str
    release_condition: str

    status: str
    claimable: TreeMap[Address, u256]

    def __init__(
        self,
        beneficiary: Address,
        amount: u256,
        evidence_url: str,
        release_condition: str,
    ):
        require(
            amount > u256(0),
            "ESCROW_AMOUNT_MUST_BE_POSITIVE"
        )

        require(
            len(evidence_url.strip()) > 0,
            "EVIDENCE_URL_REQUIRED"
        )

        require(
            len(release_condition.strip()) > 0,
            "RELEASE_CONDITION_REQUIRED"
        )

        self.depositor = gl.message.sender_address
        self.beneficiary = beneficiary
        self.amount = amount

        self.evidence_url = evidence_url
        self.release_condition = release_condition

        self.status = "CREATED"

    @gl.public.write.payable
    def fund(self) -> None:
        require(
            self.status == "CREATED",
            "ESCROW_ALREADY_FUNDED"
        )

        require(
            gl.message.sender_address == self.depositor,
            "ONLY_DEPOSITOR_CAN_FUND"
        )

        require(
            gl.message.value == self.amount,
            "INCORRECT_ESCROW_AMOUNT"
        )

        self.status = "FUNDED"

    def _adjudicate(self) -> str:
        url = self.evidence_url
        condition = self.release_condition

        def evaluate() -> str:
            try:
                page = gl.nondet.web.render(
                    url,
                    mode="text"
                )

                content = page[:6000] if page else ""

            except Exception:
                content = "[FETCH_FAILED]"

            prompt = f"""
You are the adjudicator for an escrow contract.

RELEASE CONDITION:
{condition}

EVIDENCE SOURCE:
{url}

EVIDENCE:
---
{content}
---

Determine whether the evidence establishes that the release condition
has been satisfied.

Use exactly one outcome:

RELEASE
REFUND
UNRESOLVED

Rules:

RELEASE means the evidence clearly establishes the condition.

REFUND means the evidence clearly establishes that the condition has not
been satisfied.

UNRESOLVED means the evidence is missing, contradictory, insufficient or
cannot establish either conclusion.

A failed web fetch must be treated as UNRESOLVED.

Do not guess.

Return ONLY JSON:

{{
  "outcome": "RELEASE" | "REFUND" | "UNRESOLVED",
  "reason": "one short factual explanation"
}}
"""

            raw = gl.nondet.exec_prompt(prompt)

            result = parse_json_response(raw)

            outcome = str(
                result.get("outcome", "")
            ).upper()

            if outcome not in (
                "RELEASE",
                "REFUND",
                "UNRESOLVED",
            ):
                outcome = "UNRESOLVED"

            return json.dumps(
                {
                    "outcome": outcome
                },
                sort_keys=True
            )

        principle = """
Both validators independently evaluate the same escrow release
condition using the same evidence source.

The `outcome` field is the only action-driving field.

Results are equivalent only when their outcome is exactly the same:
RELEASE, REFUND or UNRESOLVED.

Reason text must be ignored.
"""

        agreed = gl.eq_principle.prompt_comparative(
            evaluate,
            principle
        )

        result = parse_json_response(agreed)

        outcome = str(
            result.get("outcome", "")
        ).upper()

        require(
            outcome in (
                "RELEASE",
                "REFUND",
                "UNRESOLVED",
            ),
            "INVALID_CONSENSUS_OUTCOME"
        )

        return outcome

    @gl.public.write
    def adjudicate(self) -> str:
        require(
            self.status == "FUNDED",
            "ESCROW_NOT_FUNDED"
        )

        require(
            self.balance == self.amount,
            "ESCROW_BALANCE_INVARIANT_FAILED"
        )

        outcome = self._adjudicate()

        if outcome == "RELEASE":
            self.status = "RELEASED"

            self.claimable[self.beneficiary] = u256(
                int(
                    self.claimable.get(
                        self.beneficiary,
                        u256(0)
                    )
                ) + int(self.amount)
            )

        elif outcome == "REFUND":
            self.status = "REFUNDED"

            self.claimable[self.depositor] = u256(
                int(
                    self.claimable.get(
                        self.depositor,
                        u256(0)
                    )
                ) + int(self.amount)
            )

        return outcome

    @gl.public.write
    def withdraw(self) -> u256:
        require(
            self.status in (
                "RELEASED",
                "REFUNDED",
            ),
            "ESCROW_NOT_SETTLED"
        )

        recipient = gl.message.sender_address

        amount = self.claimable.get(
            recipient,
            u256(0)
        )

        require(
            amount > u256(0),
            "NOTHING_TO_WITHDRAW"
        )

        self.claimable[recipient] = u256(0)

        send_native(
            recipient,
            amount
        )

        return amount

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

    @gl.public.view
    def get_claimable(
        self,
        account: Address
    ) -> u256:
        return self.claimable.get(
            account,
            u256(0)
        )