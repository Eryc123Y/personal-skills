# D2 Style Guide -- Complete Reference

## Table of Contents

- [All Style Properties](#all-style-properties)
- [Palette Options](#palette-options)
- [Default Class Library](#default-class-library)
- [Abstraction Hierarchy (L1-L4)](#abstraction-hierarchy-l1-l4)
- [Connector Reference](#connector-reference)
- [Security Boundary Notation](#security-boundary-notation)
- [Required Diagram Elements](#required-diagram-elements)
- [Anti-Patterns](#anti-patterns)
- [ELK-Specific Configuration](#elk-specific-configuration)
- [Animation Patterns](#animation-patterns)
- [Grid Layouts](#grid-layouts)
- [Composition and Multi-Board](#composition-and-multi-board)
- [Advanced Connection Styling](#advanced-connection-styling)
- [Container Styling](#container-styling)
- [Layout Techniques](#layout-techniques)
- [Glob Patterns for Bulk Styling](#glob-patterns-for-bulk-styling)
- [Shape-Icon Compatibility](#shape-icon-compatibility)
- [Icon Quick Reference](#icon-quick-reference)
- [AWS Cloud Architecture Patterns](#aws-cloud-architecture-patterns)
- [Kubernetes Topology Patterns](#kubernetes-topology-patterns)

---

## All Style Properties

### Node Style Properties

```d2
my-node: {
  style: {
    fill: "#1C2F4A"          # Background color
    stroke: "#385FAF"        # Border color
    font-color: "#D6D6DA"    # Text color
    stroke-width: 2          # Border width
    border-radius: 12        # Corner rounding (0-20 typical)
    opacity: 0.9             # 0.0 to 1.0
    shadow: true             # Drop shadow
    3d: true                 # 3D extrusion effect
    multiple: true           # Stacked/multiple instances look
    bold: true
    italic: false
    font-size: 16
    font: "mono"
    fill-pattern: dots       # dots | lines | grain | paper
  }
}
```

### Connection Style Properties

```d2
A -> B: {
  style: {
    stroke: "#385FAF"
    stroke-width: 2
    stroke-dash: 5
    opacity: 0.8
    animated: true
    bold: true
    font-size: 14
    font-color: "#D6D6DA"
    font: "mono"
  }
}
```

---

## Palette Options

All palettes use the same variable names so classes are portable across them.

### Dark (engineering / technical audiences)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg:         "#1C2F4A"
  surface:    "#162646"
  text:       "#D6D6DA"
  text-light: "#FFFFFF"
  primary:    "#385FAF"
  accent:     "#9CADD7"
  muted:      "#739BCF"
  highlight:  "#F5871F"
  success:    "#4CAF80"
  danger:     "#E24B4A"
}
```

### Light (presentations / mixed audiences)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 0; layout-engine: elk }
  bg:         "#FFFFFF"
  surface:    "#F3F4F6"
  text:       "#111827"
  text-light: "#FFFFFF"
  primary:    "#2563EB"
  accent:     "#7C3AED"
  muted:      "#6B7280"
  highlight:  "#F59E0B"
  success:    "#16A34A"
  danger:     "#DC2626"
}
```

### Minimal (formal docs / print)

```d2
vars: {
  d2-config: { sketch: false; theme-id: 0; layout-engine: elk }
  bg:         "#FFFFFF"
  surface:    "#F9FAFB"
  text:       "#1F2937"
  text-light: "#FFFFFF"
  primary:    "#374151"
  accent:     "#6B7280"
  muted:      "#9CA3AF"
  highlight:  "#EF4444"
  success:    "#059669"
  danger:     "#DC2626"
}
```

### Nord (Arctic blue-grey)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg: "#3B4252"; surface: "#2E3440"; text: "#ECEFF4"; text-light: "#ECEFF4"
  primary: "#5E81AC"; accent: "#88C0D0"; muted: "#81A1C1"
  highlight: "#EBCB8B"; success: "#A3BE8C"; danger: "#BF616A"
}
```

### Dracula (purple-dark)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg: "#282A36"; surface: "#21222C"; text: "#F8F8F2"; text-light: "#F8F8F2"
  primary: "#6272A4"; accent: "#8BE9FD"; muted: "#44475A"
  highlight: "#FFB86C"; success: "#50FA7B"; danger: "#FF5555"
}
```

### Obsidian (near-black, security)

```d2
vars: {
  d2-config: { sketch: true; theme-id: 200; layout-engine: elk }
  bg: "#141414"; surface: "#0A0A0A"; text: "#E8E8E8"; text-light: "#FFFFFF"
  primary: "#6366F1"; accent: "#A78BFA"; muted: "#4B5563"
  highlight: "#F59E0B"; success: "#10B981"; danger: "#EF4444"
}
```

### High Contrast (accessibility-first, WCAG AAA)

```d2
vars: {
  d2-config: { sketch: false; theme-id: 0; layout-engine: elk }
  bg: "#FFFFFF"; surface: "#F0F0F0"; text: "#000000"; text-light: "#FFFFFF"
  primary: "#0057B8"; accent: "#5B2D8E"; muted: "#767676"
  highlight: "#B05C00"; success: "#0B6623"; danger: "#A4000F"
}
```

### Palette Quick-Pick by Context

| Context | Recommended Palette |
| ------- | ------------------- |
| Engineering / backend | Dark, Nord, Dracula |
| Security / infrastructure | Obsidian, Dark |
| Product / roadmap | Slate & Coral, Sakura |
| Presentations / slides | Light, Slate & Coral |
| Formal docs / print | Minimal, High Contrast |
| Accessibility required | High Contrast |

### Color Semantics (all palettes)

| Variable | Role |
| -------- | ---- |
| `${bg}` | Node / card fill |
| `${surface}` | Container / wrapper fill |
| `${text}` | All body labels |
| `${text-light}` | Labels on dark-filled containers |
| `${primary}` | Internal borders, sync connectors |
| `${accent}` | Data-flow connectors, animated edges |
| `${muted}` | Passive links, metadata, group borders |
| `${highlight}` | External entry points, critical paths — stroke only, never fill |
| `${success}` | Healthy / complete states |
| `${danger}` | Error / rejected states |

---

## Default Class Library

### Connection Classes (3)

```d2
classes: {
  sync-connection: { style: { stroke: ${primary}; stroke-width: 2 } }
  async-connection: { style: { stroke: ${accent}; stroke-dash: 5; animated: true; stroke-width: 2 } }
  critical-path: { style: { stroke: ${highlight}; stroke-width: 3; bold: true } }
}
```

### Node Classes (7)

```d2
classes: {
  internal-service: { style: { fill: ${bg}; stroke: ${primary}; stroke-width: 2; font-color: ${text}; border-radius: 6; shadow: true } }
  external-node: { style: { fill: ${bg}; stroke: ${highlight}; stroke-width: 2; font-color: ${text}; border-radius: 6 } }
  microservice: { shape: hexagon; style: { fill: ${bg}; stroke: ${primary}; stroke-width: 2; font-color: ${text} } }
  datastore: { shape: cylinder; width: 160; height: 130; label.near: outside-bottom-center; style: { fill: ${bg}; stroke: ${primary}; font-color: ${text}; shadow: true } }
  queue: { shape: queue; width: 120; height: 70; style: { fill: ${bg}; stroke: ${muted}; font-color: ${text} } }
  actor: { shape: person; width: 100; height: 80; style: { fill: ${bg}; stroke: ${muted}; font-color: ${text} } }
  aws-service: { shape: cloud; width: 130; height: 85; style: { fill: ${bg}; stroke: ${accent}; font-color: ${text} } }
}
```

### Container Classes (4)

```d2
classes: {
  account-boundary: { style: { fill: ${surface}; stroke: ${primary}; stroke-width: 2; font-color: ${text-light}; border-radius: 16; opacity: 0.95; bold: true } }
  vpc-container: { style: { fill: "#0E1829"; stroke: ${muted}; stroke-dash: 4; font-color: ${muted}; border-radius: 12; opacity: 0.9; bold: true } }
  service-group: { style: { fill: ${bg}; stroke: ${primary}; stroke-dash: 3; font-color: ${text}; border-radius: 8; opacity: 0.85; bold: true } }
  security-boundary: { style: { fill: "transparent"; stroke: ${highlight}; stroke-dash: 6; stroke-width: 2; font-color: ${highlight}; border-radius: 4; bold: true } }
}
```

### Connector Classes (4)

```d2
classes: {
  data-flow: { style: { stroke: ${accent}; stroke-width: 2; animated: true } }
  monitoring-link: { style: { stroke: "#494C4D"; stroke-dash: 3; stroke-width: 1 } }
  replication: { style: { stroke: ${muted}; stroke-dash: 4; stroke-width: 2; animated: true } }
  boundary-crossing: { style: { stroke: ${highlight}; stroke-width: 2; stroke-dash: 2 } }
}
```

---

## Abstraction Hierarchy (L1-L4)

| Level | Name | Audience | Scope | Connector Labels |
| ----- | ---- | -------- | ----- | ---------------- |
| **L1** | Landscape | Exec, customer | All products + major external deps | Short noun phrases |
| **L2** | Architecture | Engineering leads | One product/system + its integrations | Verb phrases |
| **L3** | Deployment | DevOps, cloud architects | Infrastructure: VPCs, AZs, GovCloud, IAM | Protocol + port |
| **L4** | Component | Developers | Internals of one container: classes, APIs | Method/event names |

- Default to **L2** when scope is ambiguous.
- **Never combine levels** in a single diagram.

---

## Connector Reference

| Class | Stroke | Dash | Animated | Use |
| ----- | ------ | ---- | -------- | --- |
| `sync-connection` | Blue | solid | no | Request/response, REST, gRPC |
| `async-connection` | Blue | dashed | yes | Events, pub/sub, SQS, SNS |
| `data-flow` | Blue | solid | yes | Active data movement |
| `monitoring-link` | Grey | dashed | no | Metrics, logs, passive links |
| `replication` | Blue | dashed | yes | DB replication, S3 sync |
| `critical-path` | Highlight | solid | no | Errors, alerts |
| `boundary-crossing` | Highlight | dash-2 | no | Traffic crossing a trust boundary |

---

## Security Boundary Notation

1. Use the `security-boundary` class as a wrapping container.
2. Name the container with the compliance scope: `FedRAMP High boundary`, `IL4 boundary`.
3. Add `# COMPLIANCE: <scope>` comment at the top of the file.
4. Never write classification markings in diagram node labels.
5. Trust zone crossings must use `boundary-crossing` class.

---

## Required Diagram Elements

Every diagram must include:
1. Header comment block (`# DIAGRAM TYPE:`, `# AUDIENCE:`, `# Shows:`)
2. `vars` block with chosen palette
3. `classes` block with default class library
4. Render command after the code block

---

## Anti-Patterns

- **Never mix abstraction levels** -- split into separate diagrams
- **Never use `${highlight}` as a fill** -- stroke/border only
- **Never mix sync and async on the same edge**
- **Never produce a single mega-diagram** -- prefer drill-down hierarchy
- **Avoid bidirectional arrows** -- use two separate edges
- **Connections after containers**: define structure first, then draw connections
- **Decimal stroke-width**: D2 v0.7.x rejects decimals -- use integers only (1, 2, 3)

---

## ELK-Specific Configuration

ELK is the default layout engine for all diagrams except `sequence_diagram` (uses dagre internally).

```d2
# Container width/height (ELK-exclusive)
web-tier: Web Tier {
  width: 350
  height: 200
  app-a: Frontend A
  app-b: Frontend B
}
```

ELK limitations:
- `near` keyword: only constant values (`top-left`, `bottom-center`, etc.) -- no node references
- Strictly hierarchical: no overlapping containers
- Direction inheritance: children inherit parent's `direction` unless overridden

---

## Animation Patterns

```d2
# Animated connection
producer -> queue: events {
  style.animated: true
  style.stroke-dash: 5
}
```

```bash
# Multi-board animation
d2 --animate-interval 1200 deploy.d2 deploy.svg
```

---

## Grid Layouts

```d2
dashboard: {
  grid-rows: 2
  grid-columns: 3
  grid-gap: 16
}
```

- `grid-rows`: Number of rows
- `grid-columns`: Number of columns
- `grid-gap`: Uniform gap between cells
- `vertical-gap` / `horizontal-gap`: Override per direction

---

## Composition and Multi-Board

| Mechanism | Inheritance | Best For |
| --------- | ----------- | -------- |
| `layers` | None | Independent views of same system |
| `scenarios` | From base board | Deployment variants, failure modes |
| `steps` | From previous step | Animated walkthroughs, request flows |

---

## Advanced Connection Styling

### Arrowhead Types

```d2
A -> B: {
  target-arrowhead: {
    shape: diamond        # diamond, arrow, triangle, cf-one, cf-one-required, cf-many
    style.filled: true
  }
  source-arrowhead: {
    shape: diamond
    style.filled: false
  }
}
```

### ER Notation

```d2
users -> orders: {
  source-arrowhead.shape: cf-one-required
  target-arrowhead.shape: cf-many
}
```

---

## Container Styling

```d2
critical-zone: "Critical Infrastructure" {
  style: {
    double-border: true
    stroke: ${danger}
    fill: ${surface}
    font-color: ${danger}
    bold: true
  }
}
```

---

## Layout Techniques

### Port Simulation for Clean Ingress/Egress

```d2
cloud: Cloud Environment {
  ingress: "" {
    shape: circle; width: 8; height: 8
    style.fill: ${primary}; style.stroke: ${primary}
  }
  ingress -> web-tier
}
user -> cloud.ingress: HTTPS
```

### Horizontal Child Layout

```d2
topic: "Orders (3 partitions)" {
  direction: right
  label.near: outside-top-center
  p0: "P0" { shape: queue; width: 80; height: 70 }
  p1: "P1" { shape: queue; width: 80; height: 70 }
  p2: "P2" { shape: queue; width: 80; height: 70 }
}
```

---

## Glob Patterns for Bulk Styling

```d2
# Style all nodes
*.style.border-radius: 8

# Style all connections
(* -> *)[*].style.stroke-width: 2

# Style all nodes in a container
my-container.*.style.fill: ${surface}

# Style all descendants (recursive)
vpc.**.style.font-color: ${text}
```

---

## Shape-Icon Compatibility

### Safe for Icons (with dimension constraints)

| Shape | Constraints | Notes |
| ----- | ----------- | ----- |
| Rectangle (default) | None needed | Built-in text padding |
| Cloud | `width: 130, height: 85` | Prevents icon-text overlap |
| Cylinder | `width: 160, height: 130` + `label.near: outside-bottom-center` | Text below |
| Queue | `width: 120, height: 70` | Prevents overlap |

### Avoid Icons (use text-only labels)

| Shape | Reason |
| ----- | ------ |
| Circle | Too small, icon dominates text |
| Hexagon | Non-rectangular, stretches and distorts |
| Diamond | Stretches to fit text, overlap |
| Person | Polygon distorts with long labels |

---

## Icon Quick Reference

Base URL: `https://icons.terrastruct.com/`

### AWS

| Service | Path |
| ------- | ---- |
| EC2 | `aws%2FCompute%2FAmazon-EC2.svg` |
| Lambda | `aws%2FCompute%2FAWS-Lambda.svg` |
| S3 | `aws%2FStorage%2FAmazon-Simple-Storage-Service-S3.svg` |
| RDS | `aws%2FDatabase%2FAmazon-RDS.svg` |
| DynamoDB | `aws%2FDatabase%2FAmazon-DynamoDB.svg` |
| SQS | `aws%2FApplication%20Integration%2FAmazon-Simple-Queue-Service-SQS.svg` |
| SNS | `aws%2FApplication%20Integration%2FAmazon-Simple-Notification-Service-SNS.svg` |
| CloudFront | `aws%2FNetworking%20%26%20Content%20Delivery%2FAmazon-CloudFront.svg` |
| API Gateway | `aws%2FNetworking%20%26%20Content%20Delivery%2FAmazon-API-Gateway.svg` |
| ELB | `aws%2FNetworking%20%26%20Content%20Delivery%2FElastic-Load-Balancing.svg` |
| Kinesis | `aws%2FAnalytics%2FAmazon-Kinesis.svg` |
| OpenSearch | `aws%2FAnalytics%2FAmazon-OpenSearch-Service.svg` |

### Dev Tools and Infra

| Tool | Path |
| ---- | ---- |
| Docker | `dev%2Fdocker.svg` |
| Kubernetes | `azure%2F_Companies%2FKubernetes.svg` |
| Redis | `dev%2Fredis.svg` |
| PostgreSQL | `dev%2Fpostgresql.svg` |
| MySQL | `dev%2Fmysql.svg` |
| MongoDB | `dev%2Fmongodb.svg` |
| Nginx | `dev%2Fnginx.svg` |
| GitHub | `dev%2Fgithub.svg` |
| Python | `dev%2Fpython.svg` |
| Go | `dev%2Fgo.svg` |
| Node.js | `dev%2Fnodejs.svg` |
| General User | `general%2Fuser.svg` |
| General Desktop | `general%2Fdesktop.svg` |

---

## AWS Cloud Architecture Patterns

### 5-Level Nesting Pattern

```
Region -> VPC -> Subnet -> Security Group -> Resources
```

```d2
govcloud: AWS GovCloud (us-gov-west-1) {
  class: account-boundary
  vpc: Production VPC {
    class: vpc-container
    public-subnet: Public Subnet (10.0.1.0/24) {
      class: service-group
      alb: ALB { class: internal-service }
    }
    private-subnet: Private Subnet (10.0.2.0/24) {
      class: service-group
      ecs: ECS Cluster { class: internal-service; style.multiple: true }
    }
    data-subnet: Data Subnet (10.0.3.0/24) {
      class: service-group
      rds: RDS Primary { class: datastore }
    }
  }
}
```

---

## Kubernetes Topology Patterns

### Cluster Hierarchy

```
Cluster -> Namespace -> Deployment/StatefulSet -> Pod -> Container
```

### Replica Sets with `multiple: true`

```d2
deployment: API Deployment {
  class: service-group
  pods: Pods (3 replicas) {
    class: internal-service
    style.multiple: true
  }
}
```

### Ingress-to-Service-to-Deployment Pattern

```d2
cluster: K8s Cluster {
  class: account-boundary
  ingress: Ingress Controller { class: internal-service }
  ns-app: app namespace {
    class: service-group
    svc-api: api-svc (ClusterIP) { class: internal-service }
    deploy-api: API Deployment { class: internal-service; style.multiple: true }
    svc-api -> deploy-api { class: sync-connection }
  }
  ingress -> ns-app.svc-api: /api/* { class: sync-connection }
}
```
