# GenLayer Intelligent Contract Kit

A collection of reusable Intelligent Contract primitives built for the GenLayer ecosystem.

This repository demonstrates practical contract patterns that developers can reuse when building decentralized applications powered by GenLayer consensus.

---

## Included Contracts

### AI Escrow

A reusable escrow primitive that manages agreement lifecycle between two parties.

Features

- Create escrow
- Store beneficiary
- Store amount
- Track escrow status
- Release workflow
- Refund workflow

---

### AI Guardian

A reusable guardian contract for protecting sensitive onchain state.

Features

- Protected state
- Approval workflow
- Pending review state
- Validator approval
- Validator rejection
- Reactivation

---

### AI Timelock

A reusable time based locking primitive.

Features

- Lock values
- Extend lock period
- Unlock workflow
- Status tracking

---

## Repository Structure

```
contracts/
    ai_escrow.py
    ai_guardian.py
    ai_timelock.py

docs/
examples/
tests/
```

---

## Why this repository exists

Developers often rebuild the same contract patterns repeatedly.

This repository provides reusable Intelligent Contract primitives that can serve as a starting point for marketplaces, governance systems, AI applications, payment workflows and other GenLayer powered products.

---

## Built for

- GenLayer Studio
- py-genlayer
- Full Consensus Mode

---

## Future primitives

- AI Multisig
- AI Oracle
- AI Marketplace
- AI Reputation
- AI DAO Voting
- AI Subscription

---

## License

MIT