# UML 2.5.1 Notation Reference

Use this file when the user asks for UML specifically, or when relationship correctness matters more than freeform architecture styling.

Primary references:
- OMG UML 2.5.1 specification: https://www.omg.org/spec/UML/2.5.1/PDF
- D2 UML classes: https://d2lang.com/tour/uml-classes/
- D2 connections and arrowheads: https://d2lang.com/tour/connections

## Scope

Most relevant for: class diagrams, object diagrams, package diagrams, component diagrams, deployment diagrams when UML notation is explicitly requested.

## Core Relationship Semantics

### Association

- Meaning: structural relationship between classifiers.
- Notation: solid line. Navigability: optional arrowhead.

```d2
Order -> Customer
```

### Aggregation

- Meaning: shared whole-part relationship.
- Notation: hollow diamond at the aggregate end.

```d2
Team -> Player: has members {
  source-arrowhead.shape: diamond
  source-arrowhead.style.filled: false
}
```

### Composition

- Meaning: strong whole-part relationship with owned lifecycle.
- Notation: filled diamond at the composite end.

```d2
Order -> OrderLine: contains {
  source-arrowhead.shape: diamond
  source-arrowhead.style.filled: true
}
```

### Generalization

- Meaning: inheritance / "is-a" specialization.
- Notation: solid line with hollow triangle pointing to the general classifier.

```d2
AdminUser -> User {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
```

### Realization

- Meaning: implementation of an interface or contract.
- Notation: dashed line with hollow triangle.

```d2
PaymentService -> PaymentProvider {
  style.stroke-dash: 5
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
```

### Dependency

- Meaning: usage or reliance without structural ownership.
- Notation: dashed line with open arrow.

```d2
ReportController -> PdfRenderer {
  style.stroke-dash: 5
}
```

## Practical Guidance

- If unsure between aggregation and association → prefer **association**.
- If unsure between dependency and association:
  - **association** for stable structural links or held references
  - **dependency** for temporary use, method-call reliance, or imports
- If unsure between aggregation and composition → **composition** only when lifecycle ownership is clearly strong.

## D2 UML Class Shape

```d2
User: {
  shape: class
  +id: UUID
  -passwordHash: string
  +login(email: string, password: string): boolean
}
```

## Relationship Checklist

- [ ] Is each relationship type semantically justified?
- [ ] Are diamonds on the correct whole side?
- [ ] Are hollow vs filled diamonds correct?
- [ ] Is inheritance using a hollow triangle, not a plain arrow?
- [ ] Is realization dashed while generalization is solid?
- [ ] Are multiplicities and role names attached to the ends they describe?
