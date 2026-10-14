# Sequence diagrams

Use `shape: sequence_diagram` for time-ordered interactions. D2 has specialized
sequence layout and scoping; do not simulate it with an ordinary graph.

References: [D2 sequences](https://d2lang.com/tour/sequence-diagrams/),
[D2 arrowheads](https://d2lang.com/tour/connections/),
[UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF).

## Ordering and scope

Predeclare participants in the intended left-to-right order, especially before
using them inside groups. Within a sequence diagram, groups share the diagram's
participant scope. Messages, notes, and groups appear in source order; preserve
that order when revising the diagram.

Use groups to label meaningful phases, nested participant objects for activation
spans, and unconnected nested objects for notes. These are optional tools, not a
requirement to add more detail to every sequence.

## Message meaning

For UML-style messages, use a solid line and filled triangle for a synchronous
call, a solid line and open arrow for an asynchronous message, and a dashed line
and open arrow for a reply. Dashed lines alone do not mean asynchronous. For
informal architecture sequences, a different stated convention is acceptable.

D2 v0.9.0 does not provide the UML open stick arrow as a native arrowhead.
Its `arrow` is a filled pointed polygon; `style.filled: false` does not change
that shape. The example therefore uses `arrow` as an explicitly approximate
notation for replies and events, with labels and line styles preserving meaning.
If exact UML asynchronous/reply notation is required, use a tool supporting it
or disclose the need for a separately validated export adjustment.

The complete example below demonstrates participants, a group, spans, a note,
a synchronous call, its reply, and an asynchronous event:

```d2
shape: sequence_diagram
client: Client
api: API
payments: Payments
worker: Worker

client -> api.request: checkout {
  target-arrowhead: {shape: triangle; style.filled: true}
}
authorization: Authorize payment {
  api.request -> payments.auth: authorize {
    target-arrowhead: {shape: triangle; style.filled: true}
  }
  payments.auth -> api.request: approved {
    style.stroke-dash: 5
    target-arrowhead.shape: arrow
  }
}
api."Reuse the idempotency key when retrying the same checkout."
api.request -> worker: payment authorized event {
  target-arrowhead.shape: arrow
}
api.request -> client: accepted {
  style.stroke-dash: 5
  target-arrowhead.shape: arrow
}
```

D2 groups do not enforce the full semantics of UML combined fragments. Label an
alternative or loop explicitly when it is needed and state any notation limits.
Include failure or compensation paths when they matter to the requested flow;
do not invent an exception solely to satisfy a checklist.

## Review

- Are participants, message order, and ownership supported by the source?
- Are calls, replies, and events distinguishable and correctly labeled?
- Do spans and notes communicate relevant work and assumptions?
- If failure handling is in scope, does the diagram show the actual behavior?
- Is the final export readable, including long labels and group boundaries?
