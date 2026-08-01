# AI Guardian Example

## Scenario

A protected configuration value should not be changed without an approval workflow.

## Flow

1. Deploy the AI Guardian contract.
2. Store the protected value.
3. Request an update.
4. Status changes to `PENDING_REVIEW`.
5. The update is either:
   - Approved
   - Rejected

## Result

Applications can reuse this primitive to protect sensitive onchain state.