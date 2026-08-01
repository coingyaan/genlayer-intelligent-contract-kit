# Architecture

## Overview

The GenLayer Intelligent Contract Kit provides reusable contract primitives that demonstrate common application patterns for developers building on GenLayer.

Each primitive is independent and can be integrated into larger applications.

---

## Included Contracts

### AI Escrow

Purpose

Manage conditional agreements between two parties.

Core Components

- Depositor
- Beneficiary
- Amount
- Status
- Release
- Refund

---

### AI Guardian

Purpose

Protect sensitive state through an approval workflow.

Core Components

- Protected value
- Pending review
- Approval
- Rejection
- Reactivation

---

### AI Timelock

Purpose

Manage time based state transitions.

Core Components

- Locked value
- Unlock timestamp
- Lock extension
- Unlock state

---

## Design Principles

- Simple
- Reusable
- Modular
- Educational
- Extendable