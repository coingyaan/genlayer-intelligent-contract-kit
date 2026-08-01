# Test Plan

This repository contains reusable Intelligent Contract primitives for GenLayer.

Each contract should be tested in GenLayer Studio before production use.

---

## AI Escrow

### Test Cases

- Deploy contract
- Verify constructor values
- Read escrow status
- Read beneficiary
- Read amount
- Execute release
- Execute refund

Expected Result

All state transitions complete successfully.

---

## AI Guardian

### Test Cases

- Deploy contract
- Read protected value
- Request update
- Approve update
- Reject update
- Reactivate guardian

Expected Result

Status changes correctly for every workflow.

---

## AI Timelock

### Test Cases

- Deploy contract
- Read unlock timestamp
- Read locked value
- Extend lock
- Unlock contract

Expected Result

Timelock state updates successfully.

---

## Validation

Every contract should:

- Compile successfully
- Deploy successfully
- Reach consensus
- Execute public methods
- Return expected values