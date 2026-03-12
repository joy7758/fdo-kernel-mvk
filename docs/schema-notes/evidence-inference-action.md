# Evidence → Inference → Action

This note captures a schema extension idea for agent execution traces.

The current MVK direction focuses on deterministic execution traces:

- append-only trace
- explicit tool calls
- deterministic state transitions
- replay verification

That already answers an important question:

**what happened?**

A useful next layer is to make the decision path more explicit:

**what was observed → what was inferred → what action was taken**

This does not replace the current execution-integrity model.
It extends it.

## Why this matters

A plain event log is useful for replay, but often not enough for audit.

For real agent systems, reviewers usually want to understand:

- what evidence the system saw
- what the system inferred from that evidence
- what action it decided to take
- what changed in the environment afterwards

This becomes especially important when agents interact with tools, APIs, databases, tickets, or workflows.

## Compatibility principle

This should be treated as a schema extension, not a replacement.

Current event structure can remain centered on:

- state_before
- action
- tool_call
- tool_result
- state_after

The new layer should add optional fields for decision-path semantics.

## Proposed optional fields

### observed_evidence

Raw observations available to the agent before action.

Examples:
- retrieved documents
- tool outputs
- user input
- environment state snapshot

### inference_step

What the system concluded from the observed evidence.

Examples:
- "incident appears verified"
- "query returned no matching record"
- "policy threshold exceeded"

### action_intent

Why the action is being proposed.

Examples:
- "create ticket"
- "retry query"
- "block unsafe action"

### side_effect_diff

What changed in the environment after execution.

Examples:
- ticket created
- database row updated
- file modified
- no external side effect

## Example event model

```json
{
  "event_id": "evt-0003",
  "timestamp": "2026-03-13T10:15:00Z",
  "state_before_hash": "sha256:...",
  "observed_evidence": {
    "source": "servicenow_lookup",
    "records_found": 0
  },
  "inference_step": {
    "summary": "no matching incident found"
  },
  "action_intent": {
    "type": "create_ticket",
    "reason": "verified incident missing from system"
  },
  "tool_call": {
    "tool_name": "jira.create_ticket",
    "input_hash": "sha256:..."
  },
  "tool_result": {
    "status": "success",
    "ticket_id": "INC-1042"
  },
  "side_effect_diff": {
    "external_change": "new ticket created"
  },
  "state_after_hash": "sha256:..."
}
```

## Design goal

The long-term goal is to make execution traces answer both:

- what happened
- why the system moved from one step to the next

This helps bridge raw replay logs and human-auditable runtime records.

## Recommended rollout path

### v1

Keep the current kernel trace model unchanged.

### v1.1

Add schema notes and example traces for:

- observed_evidence
- inference_step
- action_intent
- side_effect_diff

### v2

Evaluate whether these fields should become first-class runtime events.
