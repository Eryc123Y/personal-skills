# D2 Diagram Examples -- Complete Renderable Examples

## Table of Contents

- [L1 System Landscape](#l1-system-landscape)
- [L2 Architecture Overview](#l2-architecture-overview)
- [L2 Sequence Diagram](#l2-sequence-diagram)
- [L2 ER Diagram](#l2-er-diagram)
- [State Machine](#state-machine)
- [Roadmap / Timeline](#roadmap--timeline)
- [UML class diagram](#uml-class-diagram)

Architecture examples below use dashed animated event edges as an informal
convention. For UML-style sequence messages, use the dedicated
[sequence reference](sequence-diagram-checklist.md).

---

## L1 System Landscape

Executive-level overview of a product ecosystem.

```d2
# LEVEL: L1 -- System Landscape
direction: right

vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  primary: "#162646"; secondary: "#385FAF"; accent: "#9CADD7"
  surface: "#1C2F4A"; text: "#D6D6DA"; text-light: "#FFFFFF"
  muted: "#739BCF"; orange: "#F5871F"
}

classes: {
  sync-connection: { style: { stroke: ${secondary}; stroke-width: 2 } }
  async-connection: { style: { stroke: ${accent}; stroke-dash: 5; animated: true; stroke-width: 2 } }
  internal-service: { style: { fill: ${surface}; stroke: ${secondary}; stroke-width: 2; font-color: ${text}; border-radius: 6; shadow: true } }
  external-node: { style: { fill: ${surface}; stroke: ${orange}; stroke-width: 2; font-color: ${text}; border-radius: 6 } }
  actor: { shape: person; width: 100; height: 80; style: { fill: ${surface}; stroke: ${muted}; font-color: ${text} } }
  aws-service: { shape: cloud; width: 130; height: 85; style: { fill: ${surface}; stroke: ${accent}; font-color: ${text} } }
  account-boundary: { style: { fill: ${primary}; stroke: ${secondary}; stroke-width: 2; font-color: ${text-light}; border-radius: 16; opacity: 0.95; bold: true } }
  service-group: { style: { fill: ${surface}; stroke: ${secondary}; stroke-dash: 3; font-color: ${text}; border-radius: 8; opacity: 0.85; bold: true } }
  data-flow: { style: { stroke: ${accent}; stroke-width: 2; animated: true } }
  monitoring-link: { style: { stroke: "#494C4D"; stroke-dash: 3; stroke-width: 1 } }
}

gov_user: Government operator { class: actor }
partner: Mission partner { class: actor }

bluestaq: Bluestaq {
  class: account-boundary
  udl: Unified Data Library { class: service-group; style.fill: "#1C2F4A" }
  gdm: Global Data Marketplace { class: service-group; style.fill: "#1C2F4A" }
  platform: Platform Services { class: service-group; style.fill: "#1C2F4A" }
}

dod: DoD Data Sources { class: external-node; shape: cloud }
aws_gov: AWS GovCloud { class: aws-service }

gov_user -> bluestaq.udl: discovers & shares data { class: sync-connection }
partner -> bluestaq.gdm: accesses marketplace { class: sync-connection }
dod -> bluestaq.udl: ingests { class: data-flow }
bluestaq.udl -> bluestaq.gdm: published data { class: data-flow }
bluestaq.platform -> aws_gov: hosted on { class: monitoring-link }
```

```bash
d2 --sketch --theme 200 --layout elk landscape.d2 landscape.svg
```

---

## L2 Architecture Overview

Default diagram type. One system + its integrations.

```d2
# LEVEL: L2 -- Architecture Overview
direction: right

vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  primary: "#162646"; secondary: "#385FAF"; accent: "#9CADD7"
  surface: "#1C2F4A"; text: "#D6D6DA"; text-light: "#FFFFFF"
  muted: "#739BCF"; orange: "#F5871F"
}

classes: {
  sync-connection: { style: { stroke: ${secondary}; stroke-width: 2 } }
  async-connection: { style: { stroke: ${accent}; stroke-dash: 5; animated: true; stroke-width: 2 } }
  internal-service: { style: { fill: ${surface}; stroke: ${secondary}; stroke-width: 2; font-color: ${text}; border-radius: 6; shadow: true } }
  external-node: { style: { fill: ${surface}; stroke: ${orange}; stroke-width: 2; font-color: ${text}; border-radius: 6 } }
  microservice: { shape: hexagon; style: { fill: ${surface}; stroke: ${secondary}; stroke-width: 2; font-color: ${text} } }
  datastore: { shape: cylinder; width: 160; height: 130; label.near: outside-bottom-center; style: { fill: ${surface}; stroke: ${secondary}; font-color: ${text}; shadow: true } }
  queue: { shape: queue; width: 120; height: 70; style: { fill: ${surface}; stroke: ${muted}; font-color: ${text} } }
  aws-service: { shape: cloud; width: 130; height: 85; style: { fill: ${surface}; stroke: ${accent}; font-color: ${text} } }
  account-boundary: { style: { fill: ${primary}; stroke: ${secondary}; stroke-width: 2; font-color: ${text-light}; border-radius: 16; opacity: 0.95; bold: true } }
  service-group: { style: { fill: ${surface}; stroke: ${secondary}; stroke-dash: 3; font-color: ${text}; border-radius: 8; opacity: 0.85; bold: true } }
  data-flow: { style: { stroke: ${accent}; stroke-width: 2; animated: true } }
  monitoring-link: { style: { stroke: "#494C4D"; stroke-dash: 3; stroke-width: 1 } }
}

client: Client application { class: external-node }
data_source: External data source { class: external-node; shape: cloud }

udl: Unified Data Library {
  class: account-boundary
  api: API gateway { class: internal-service }
  auth: Auth service { class: microservice }
  ingest: Ingest pipeline { class: internal-service; style.multiple: true }
  core: UDL core API { class: microservice }
  discovery: Discovery service { class: microservice }
  object_store: Object store { class: datastore }
  metadata: Metadata store { class: datastore }
  events: Event bus { class: queue }
  obs: Observability { class: aws-service; style.stroke-dash: 3 }
}

client -> udl.api: HTTPS { class: sync-connection }
data_source -> udl.ingest: raw data { class: data-flow }
udl.api -> udl.auth: validates { class: sync-connection }
udl.api -> udl.core: routes { class: sync-connection }
udl.ingest -> udl.object_store: stores { class: data-flow }
udl.ingest -> udl.events: publishes { class: async-connection }
udl.core -> udl.object_store: reads { class: sync-connection }
udl.core -> udl.metadata: queries { class: sync-connection }
udl.discovery -> udl.metadata: indexes { class: sync-connection }
udl.events -> udl.discovery: triggers reindex { class: async-connection }
udl.core -> udl.obs: metrics { class: monitoring-link }
udl.ingest -> udl.obs: metrics { class: monitoring-link }
```

```bash
d2 --sketch --theme 200 --layout elk architecture.d2 architecture.svg
```

---

## L2 Sequence Diagram

Temporal order of interactions for an authenticated data request.

```d2
# LEVEL: L2 -- Sequence Diagram
vars: {
  d2-config: { sketch: true; theme-id: 200 }
  secondary: "#385FAF"; accent: "#9CADD7"; orange: "#F5871F"
  surface: "#1C2F4A"; text: "#D6D6DA"; muted: "#739BCF"
}

shape: sequence_diagram

client: Client app
gateway: API gateway
auth: Auth service
core: UDL core API
meta: Metadata store
store: Object store

client -> gateway: "GET /data/{id}\nAuthorization: Bearer token"
gateway -> auth: validate token
auth -> gateway: 200 OK -- claims
gateway -> core: forward request + claims
core -> meta: check ACL for resource
meta -> core: permitted -- object key
core -> store: "GET s3://udl-raw/{key}"
store -> core: 200 OK -- object bytes
core -> gateway: 200 OK -- payload
gateway -> client: 200 OK -- payload

client -> gateway: "GET /data/{bad-id}"
gateway -> auth: validate token
auth -> gateway: 401 Unauthorized { style.stroke: "#E24B4A" }
gateway -> client: 401 Unauthorized { style.stroke: "#E24B4A" }
```

```bash
d2 --sketch --theme 200 sequence.d2 sequence.svg
```

---

## L2 ER Diagram

Database schema with sql_table shapes and ER cardinality notation.

```d2
# LEVEL: L2 -- ER Diagram
direction: right

vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  primary: "#162646"; secondary: "#385FAF"; muted: "#739BCF"
}

users: users {
  shape: sql_table
  id: int {constraint: primary_key}
  email: varchar(255) {constraint: unique}
  username: varchar(100) {constraint: unique}
  password_hash: varchar(255)
  created_at: timestamp
}

posts: posts {
  shape: sql_table
  id: int {constraint: primary_key}
  author_id: int {constraint: foreign_key}
  title: varchar(300)
  status: enum(draft,published,archived)
  created_at: timestamp
}

comments: comments {
  shape: sql_table
  id: int {constraint: primary_key}
  post_id: int {constraint: foreign_key}
  author_id: int {constraint: foreign_key}
  parent_id: int {constraint: foreign_key}
  body: text
}

tags: tags {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar(100) {constraint: unique}
}

post_tags: post_tags {
  shape: sql_table
  post_id: int {constraint: foreign_key}
  tag_id: int {constraint: foreign_key}
}

users -> posts: { source-arrowhead.shape: cf-one-required; target-arrowhead.shape: cf-many; style.stroke: ${secondary} }
users -> comments: { source-arrowhead.shape: cf-one-required; target-arrowhead.shape: cf-many; style.stroke: ${secondary} }
posts -> comments: { source-arrowhead.shape: cf-one-required; target-arrowhead.shape: cf-many; style.stroke: ${secondary} }
comments -> comments: replies { source-arrowhead.shape: cf-one; target-arrowhead.shape: cf-many; style.stroke: ${muted}; style.stroke-dash: 3 }
posts -> post_tags: { source-arrowhead.shape: cf-one-required; target-arrowhead.shape: cf-many; style.stroke: ${secondary} }
tags -> post_tags: { source-arrowhead.shape: cf-one-required; target-arrowhead.shape: cf-many; style.stroke: ${secondary} }
```

```bash
d2 --sketch --theme 200 --layout elk er-diagram.d2 er-diagram.svg
```

---

## State Machine

Finite state machine showing an order lifecycle.

```d2
# DIAGRAM TYPE: State Machine
direction: right

vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg: "#1C2F4A"; surface: "#162646"; text: "#D6D6DA"; text-light: "#FFFFFF"
  primary: "#385FAF"; muted: "#739BCF"; success: "#4CAF80"; danger: "#E24B4A"
}

classes: {
  state: { style: { fill: ${bg}; stroke: ${primary}; stroke-width: 2; font-color: ${text}; border-radius: 8; shadow: true } }
  error-state: { style: { fill: ${bg}; stroke: ${danger}; stroke-width: 2; font-color: ${danger}; border-radius: 8 } }
  terminal-start: { shape: circle; width: 36; height: 36; style: { fill: ${text}; stroke: ${primary}; stroke-width: 2 } }
  terminal-end: { shape: circle; width: 36; height: 36; style: { fill: ${surface}; stroke: ${text}; stroke-width: 4 } }
  transition: { style: { stroke: ${primary}; stroke-width: 2 } }
  success-transition: { style: { stroke: ${success}; stroke-width: 2 } }
  error-transition: { style: { stroke: ${danger}; stroke-width: 2; stroke-dash: 3 } }
}

start: "" { class: terminal-start }
end: "" { class: terminal-end }
pending: Pending { class: state }
confirmed: Confirmed { class: state }
processing: Processing { class: state }
shipped: Shipped { class: state }
delivered: Delivered { class: state }
cancelled: Cancelled { class: error-state }
refunded: Refunded { class: error-state }

start -> pending: "" { class: transition }
pending -> confirmed: payment received { class: success-transition }
pending -> cancelled: timeout / user cancel { class: error-transition }
confirmed -> processing: warehouse picks { class: transition }
confirmed -> cancelled: admin cancel { class: error-transition }
processing -> shipped: dispatched { class: transition }
shipped -> delivered: courier confirms { class: success-transition }
shipped -> processing: returned to warehouse { class: error-transition }
delivered -> refunded: return request { class: error-transition }
cancelled -> end: "" { class: transition }
refunded -> end: "" { class: transition }
delivered -> end: "" { class: success-transition }
```

```bash
d2 --sketch --theme 200 --layout elk state-machine.d2 state-machine.svg
```

---

## Roadmap / Timeline

Product roadmap by quarter using grid layout. Cards show status, not dependency
edges or a date-proportional scale. Shipped items are green, current work is
outlined in blue, and planned items use dashed borders.

```d2
# DIAGRAM TYPE: Roadmap / Timeline
direction: right

vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg: "#1C2F4A"; surface: "#162646"; text: "#D6D6DA"; text-light: "#FFFFFF"
  primary: "#385FAF"; muted: "#739BCF"; highlight: "#F5871F"; accent: "#9CADD7"
  success: "#4CAF80"
}

classes: {
  quarter: { style: { fill: ${surface}; stroke: ${primary}; stroke-width: 2; font-color: ${text-light}; bold: true; border-radius: 6 } }
  shipped: { shape: step; style: { fill: "#1A3A2A"; stroke: ${success}; stroke-width: 1; font-color: ${success}; border-radius: 4 } }
  in-progress: { shape: step; style: { fill: ${bg}; stroke: ${accent}; stroke-width: 2; font-color: ${text}; border-radius: 4 } }
  planned: { shape: step; style: { fill: ${surface}; stroke: ${muted}; stroke-dash: 3; stroke-width: 1; font-color: ${muted}; border-radius: 4 } }
}

roadmap: Quarterly plan {
  grid-columns: 4
  grid-gap: 24
  q1: Q1 { class: quarter; grid-rows: 3; grid-gap: 8; auth: Auth v2 { class: shipped }; search: Search revamp { class: shipped }; api_v1: Public API v1 { class: shipped } }
  q2: Q2 { class: quarter; grid-rows: 3; grid-gap: 8; billing: Billing integration { class: in-progress }; collab: Real-time collaboration { class: in-progress }; mobile: Mobile app beta { class: planned } }
  q3: Q3 { class: quarter; grid-rows: 3; grid-gap: 8; ai: AI assistant { class: planned }; analytics: Analytics dashboard { class: planned }; sso: Enterprise SSO { class: planned } }
  q4: Q4 { class: quarter; grid-rows: 3; grid-gap: 8; marketplace: Marketplace launch { class: planned }; api_v2: Public API v2 { class: planned }; i18n: Internationalization { class: planned } }
}

```

```bash
d2 --sketch --theme 200 --layout elk roadmap.d2 roadmap.svg
```

## UML class diagram

Use native class shapes and relationship markers rather than SQL tables.

```d2
direction: right
User: {
  shape: class
  +id: UUID
  +login(email, password): boolean
}
AdminUser: {
  shape: class
  +grantRole(role): void
}
AdminUser -> User: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
```

```bash
d2 --layout elk classes.d2 classes.svg
```
