# Sequence Diagram Checklist

Use this file before generating production-grade sequence diagrams.

Primary references:
- D2 official sequence diagram docs: https://d2lang.com/tour/sequence-diagrams/
- UML 2.5.1 spec: https://www.omg.org/spec/UML/2.5.1/PDF

## Required Checks

### 1. Use `shape: sequence_diagram`

Do not fake a sequence diagram with ordinary nodes and arrows.

```d2
Checkout flow: {
  shape: sequence_diagram
}
```

### 2. Predeclare actors in the intended left-to-right order

Ordering matters. Declare participants explicitly before groups.

### 3. Use groups for meaningful fragments

Use them for: happy path, authorization flow, webhook reconciliation, failure/compensation branch, retry path.

```d2
authorize_payment: Authorize payment {
  api -> payments: authorize
  payments -> api: approved
}
```

### 4. Use spans for activation-like behavior

When one actor is actively processing work over multiple messages, use nested objects:

```d2
api.request -> payments.auth: authorize
payments.auth -> threeds.challenge: create challenge
threeds.challenge -> payments.auth: challenge url
payments.auth -> api.request: action required
```

### 5. Use notes for operational context

Notes carry assumptions that do not belong in message labels:
- idempotency key reuse
- reservation TTL
- webhook ordering caveats
- timeout windows
- retry semantics

```d2
checkout."Idempotency key is reused across retries for the same checkout attempt."
```

### 6. Respect definition order

D2 sequence diagrams render in the order you define things.

### 7. Distinguish synchronous vs asynchronous messages

Style async messages distinctly:

```d2
payments.webhook -> api.reconcile: payment.authorized {
  style.stroke-dash: 5
}
```

Good candidates: webhooks, event bus publications, background notifications, delayed callbacks.

### 8. Prefer semantic clarity over message count

Make clear: who initiates the flow, what the authoritative services are, where decisions happen, which parts are async, where state is committed, how compensation/rollback works.

### 9. Keep failure handling explicit

Include at least one clearly labeled exception or compensation path:
- payment authorization failure
- persistence failure after successful authorization
- stock release on compensation
- void / refund after downstream failure

### 10. Final review checklist

- [ ] Is this truly a `sequence_diagram`, not a generic flow chart?
- [ ] Are participants explicitly declared in the intended order?
- [ ] Are major phases separated into groups?
- [ ] Are spans used where activation-like behavior matters?
- [ ] Are notes carrying operational assumptions?
- [ ] Are async callbacks styled distinctly?
- [ ] Is the failure / compensation path visible and readable?
