# x4-context

**Context compression and persistent session memory for AI agents.**

Sandboxed tool output, aggressive context reduction patterns, multi-platform routing via MCP. Designed to keep agents aware across long sessions without burning tokens.

Part of the X4 / ARIEX4Ops ecosystem.

## Goals

- Reduce context window pressure by 90%+ on tool-heavy workflows
- Persist session memory across runs
- Route compressed context via MCP to any compatible agent
- Evidence-backed: every compression decision is logged

<!-- X4-APEX-DIAGRAM-START:x4-context -->

```mermaid
flowchart TD
    INPUT[Tool Output and Session Context] --> POLICY[Retention and Compression Policies]
    POLICY --> PROTECT[Preserve Required Instructions and Evidence]
    PROTECT --> COMPRESS[Compression Strategy]
    COMPRESS --> MEMORY[Session and Episodic Memory]
    MEMORY --> STORE[Context Store]
    STORE --> MCP[MCP Context Exposure]
    MCP --> AGENT[Compatible Agent]
    COMPRESS --> AUDIT[Log Compression Decision]
    INJECTION[Untrusted Retrieved Text] -. classify and flag .-> POLICY
    LIMIT[Configured Token Budget] -. constrains .-> COMPRESS
```

<!-- X4-APEX-DIAGRAM-END:x4-context -->

## Quick Start

```bash
pip install -e ".[dev]"
python -m x4_context.demo
```

## Structure

```
x4-context/
├── src/x4_context/
│   ├── compress.py      # core compression strategies
│   ├── memory.py        # session + episodic store
│   ├── mcp_server.py    # MCP exposure
│   └── policies.py      # what can be dropped vs kept
├── tests/
└── .github/workflows/ci.yml
```

## License

Apache-2.0

## APEX Architecture Map

> Status: architecture documentation; implementation and deployment claims require independent verification.

```mermaid
flowchart LR
  Input[Prompt + retrieved context] --> Size[Enforce input byte/token budget]
  Size --> SecretScan[Detect and redact sensitive values]
  SecretScan --> TrustLabel[Label source and trust level]
  TrustLabel --> InjectionScan[Detect instruction-like untrusted content]
  InjectionScan --> Segment[Segment by source and priority]
  Segment --> Compress[Compress with preserved provenance]
  Compress --> Fidelity{Required facts and constraints retained?}
  Fidelity -->|no| Rebuild[Rebuild with less compression]
  Rebuild --> Fidelity
  Fidelity -->|yes| Budget{Within output token budget?}
  Budget -->|no| Truncate[Truncate lowest-priority segments]
  Truncate --> Recheck[Revalidate required constraints]
  Recheck -->|fail| Reject[Return explicit context-budget error]
  Recheck -->|pass| Output[Emit bounded context + source labels]
  Budget -->|yes| Output
```
**Evidence note:** Token counting, redaction, provenance, and injection handling must be tested against adversarial fixtures; compression must not silently discard mandatory constraints.

