# Tiny Workflow Engine

> A learning project to understand how workflow orchestration engines like Temporal work internally by building one from scratch.

## Why I Started This Project

After spending a long time using high-level frameworks and AI coding assistants, I realized that I was becoming better at architecture discussions than implementing systems from first principles.

Instead of reading Temporal's source code or Restate Source Code, I decided to rebuild the core ideas myself.

The goal is **not** to clone Simple Durable Execution Engine feature-by-feature.
The goal is to understand the engineering problems that Temporal and Restate solve.

Note: Here I am more in Temporal Philosiphe Each Workflow (Use Case) is Guranteed to be Completed.
---

# Learning Objectives

- Build a durable workflow execution engine
- Understand workflow state management
- Learn workflow recovery after crashes
- Explore workflow orchestration concepts
- Build everything incrementally
- Avoid over-engineering

---

# Current Features

- Workflow execution
- Step execution
- Workflow context
- Step context
- Workflow state tracking
- Step state tracking
- Workflow resume
- Step resume
- Step input persistence
- Step output persistence
- Workflow input persistence
- Workflow output persistence
- Execution timestamps
- Step timestamps
