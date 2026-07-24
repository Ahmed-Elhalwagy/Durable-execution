# Changelog

All notable changes to this project are documented in this file.

This project follows an incremental learning approach where each version introduces one new workflow orchestration concept.

---

# v0.1.0 — Initial Workflow Engine

## Added

* Initial `WorkflowContext` model
* Initial `WorkflowStep` model
* `WorkflowStatus` enum
* `StepStatus` enum
* `workflow_wrapper()` execution wrapper
* `step_wrapper()` execution wrapper
* Sequential workflow execution
* Basic workflow status tracking
* Basic step status tracking

## Notes

This version focused on executing workflows while tracking execution state.

---

# v0.2.0 — Workflow Resume

## Added

* Workflow reconstruction from stored state
* `resume()` functionality
* Workflow lookup using stored function name
* Ability to continue unfinished workflows

## Improved

* Introduced durable workflow state
* Added support for resuming instead of restarting execution

---

# v0.3.0 — Step Output Persistence

## Added

* `return_data` to `WorkflowStep`
* Step result persistence
* Reuse of completed step outputs

## Improved

* Completed steps are skipped during recovery
* Previous execution results are reused instead of executing again

Example

```python
order_id = step_wrapper(ctx, verify_order)
```

During recovery, `verify_order()` is no longer executed if it has already completed successfully.

---

# v0.4.0 — Workflow Data Flow

## Added

* Passing outputs between workflow steps
* Argument forwarding through `step_wrapper()`

Example

```python
order_id = step_wrapper(ctx, verify_order)

step_wrapper(
    ctx,
    withdraw_money,
    {"order_id": order_id}
)
```

## Improved

* Workflows now support data dependencies between activities.
* Steps can consume outputs from previous steps.

---

# v0.5.0 — Workflow Input & Output Persistence

## Added

### Workflow

* Workflow input arguments
* Workflow return value

### Steps

* Step input arguments
* Step return value persistence

## Improved

* Workflow executions now preserve execution context.
* Step executions now store both inputs and outputs.

---

# v0.6.0 — Execution Metadata

## Added

### Workflow

* `start_date`
* `end_date`

### Steps

* `start_date`
* `end_date`

## Improved

* Execution lifecycle tracking
* Foundation for monitoring and execution metrics
* Execution duration can now be calculated

---

# v0.7.0 — Workflow Recovery

## Added

* Workflow recovery API (`reconsolidate()`)
* Recovery by workflow identifier
* Recovery of unfinished workflow executions

## Improved

* Workflows can now be resumed from persisted execution state.
* Completed workflows are ignored during recovery.

---

# v0.8.0 — Argument-Based Step Execution

## Added

* Dynamic argument passing into workflow activities
* Generic activity invocation using keyword arguments

## Improved

* Activities are no longer restricted to zero-argument functions.
* Workflow engine now supports parameterized step execution.

---

# v0.9.0 — Execution Model Refinements

## Improved

* Cleaner separation between workflow state and step state
* Better encapsulation of workflow metadata
* Better encapsulation of activity metadata
* Improved execution lifecycle
* Improved return value handling
* Improved workflow orchestration flow

---

# v0.9.1 — Repeated Step Disambiguation

## Added

* `step_counter` on `WorkflowStep`
* `_cursor` on `WorkflowContext`
* `next_counter()` — increments and returns the workflow's step cursor

## Improved

* `step_wrapper()` now matches existing steps by `func_name` **and** `func_counter`, not `func_name` alone.
* Same activity can now be called more than once within a single workflow without result collisions.

Example

```python
def useCase(ctx: WorkflowContext):
    order_id = step_wrapper(ctx, verify_order)
    withdraw = step_wrapper(ctx, withdraw_money, {"order_id": order_id})
    order_id = step_wrapper(ctx, verify_order)  # second call, distinct counter
    email = step_wrapper(ctx, send_email, {"order_id": order_id})
```

* `resume()` resets `_cursor` to `0` before replay so counters realign with the original execution order.

---

# Planned

## v0.10.0

* Workflow repository abstraction
* Persistent storage layer
* JSON/SQLite/PostgreSQL support

---

## v0.11.0

* Workflow event history
* Event sourcing
* State reconstruction from events

---

## v0.12.0

* Retry policies
* Retry counters
* Configurable retry strategies

---

## v0.13.0

* Activity timeouts
* Workflow timeouts
* Heartbeat support

---

## v0.14.0

* Worker architecture
* Task queue
* Background execution model

---

## v0.15.0

* Multiple workers
* Parallel workflow execution

---

## v1.0.0

* Durable workflow execution
* Event replay
* Deterministic workflow recovery
* Production-ready workflow engine architecture
