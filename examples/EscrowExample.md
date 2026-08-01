# AI Escrow Example

## Scenario

Alice wants to pay Bob after work is completed.

## Flow

1. Alice deploys the AI Escrow contract.
2. Bob is set as the beneficiary.
3. Alice specifies the escrow amount.
4. The escrow remains in the `CREATED` state.
5. After the agreed conditions are met, the escrow is either:
   - Released
   - Refunded

## Result

The contract provides a reusable escrow workflow for future GenLayer applications.