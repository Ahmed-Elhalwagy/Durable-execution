from typing_extensions import Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from time import sleep
from pprint import pprint

import asyncio
import uuid
import inspect

def _generate_random_number():
    return uuid.uuid4()

class WorkflowStatus(str, Enum):
    RUNNING = "running"
    PENDING = "pending"
    ERROR = "error"
    COMPLETED = "completed"


class StepStatus(str, Enum):
    RUNNING = "running"
    PENDING = "pending"
    FAILED = "failed"
    COMPLETED = "completed"

class WorkflowEventType(str, Enum):
    WORKFLOW_CREATED = "workflow_created"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_RESUMED = "workflow_resumed"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_CANCELLED = "workflow_cancelled"

    STEP_CREATED = "step_created"
    STEP_SCHEDULED = "step_scheduled" # !TODO
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    STEP_FAILED = "step_failed"
    STEP_SKIPPED = "step_skipped"

@dataclass
class WorkflowEvent:
    event_type: WorkflowEventType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # step information
    step_id: str | None = None
    step_name: str | None = None
    
    timestamp: datetime = field(default_factory=datetime.now)

    # payload
    message: str | None = None
    data: Any = None

    error: str | None = None

@dataclass
class Args:
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)

@dataclass
class WorkflowStep:
    # 2 identifiers
    step_name: str
    step_counter: int

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime | None = field(default=None)
    status: StepStatus = field(default=StepStatus.RUNNING)

    input_arguments: Args = Args
    return_data : Any = field(default=None)

    def update_step_status(self, new_status: StepStatus):
        self.status = new_status
        if new_status == StepStatus.COMPLETED:
            self.end_date = datetime.now()

    def update_step_return_data(self, data: Any):
        self.return_data = data

    def save_input_arguments(self, args):
        self.input_arguments = args

@dataclass
class WorkflowContext:
    workflow_name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    status: WorkflowStatus = field(default=WorkflowStatus.RUNNING)
    steps: list[WorkflowStep] = field(default_factory=list)
    _cursor: int = field(default=0, compare=False) # this cursor is incremented when step is executed

    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime | None = field(default=None)

    input_arguments: Args = Args
    return_data : Any = field(default=None)

    events: list[WorkflowEvent] = field(default_factory=list)

    def add_step(self, step: WorkflowStep) -> WorkflowStep:

        self.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.STEP_CREATED,
                step_id=step.id,
                step_name=step.step_name,
                message=f"Created step {step.step_name}"
            )
        )

        self.steps.append(step)
        return step

    def save_input_arguments(self, args: Args):
        self.input_arguments = args

    def update_status(self, new_status: WorkflowStatus):
        self.status = new_status
        if new_status == WorkflowStatus.COMPLETED:
            self.end_date = datetime.now()

    def next_counter(self) -> int:
        self._cursor += 1
        return self._cursor

    def update_return_date(self, data:Any):
        self.return_data = data

    def add_event(self, event_data: WorkflowEvent):
        self.events.append(event_data)  


### Wrappers
async def workflow(func: Callable, *args, **kwargs):
    ctx = WorkflowContext(workflow_name=func.__name__)

    try:
        ctx.save_input_arguments(Args(
            args=args,
            kwargs=kwargs
        ))
        
        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_STARTED,
                message=f"Workflow {ctx.workflow_name} started"
            )
        )

        ### execution
        if inspect.iscoroutinefunction(func):
            result = await func(ctx, *args, **kwargs) 
        else:
            result = await asyncio.to_thread(func,*args) # sync functions

        ctx.update_status(WorkflowStatus.COMPLETED)
        ctx.update_return_date(result)

        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_COMPLETED,
                data=result,
                message="Workflow completed successfully"
            )
        )

        return result

    except Exception as error:
        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_FAILED,
                error=str(error),
                message="Workflow Eexecution Error"
            )
        )
   
        ctx.update_status(WorkflowStatus.ERROR)
        raise

async def workflow_step(ctx: WorkflowContext, func: Callable[[], None], *args, **kwargs):
    step_counter = ctx.next_counter()
    step_exist = next(
        (s for s in ctx.steps
        if s.step_name == func.__name__ and s.step_counter == step_counter),
        None,
    )
    try:
        # resume skipping logic
        if step_exist:
            if step_exist.status == StepStatus.COMPLETED:
                ctx.add_event(
                    WorkflowEvent(
                        event_type=WorkflowEventType.STEP_SKIPPED,
                        step_id=step_exist.id,
                        step_name=step_exist.step_name,
                        message="Step already completed, replay skipped"
                    )
                )
                return step_exist.return_data
            elif step_exist.status == StepStatus.RUNNING:
                step = step_exist
        else:
            step = WorkflowStep(status=StepStatus.RUNNING, step_name=func.__name__, step_counter=step_counter)
            step.save_input_arguments(
                Args(
                    args=args,
                    kwargs=kwargs
                ))

            step = ctx.add_step(step)

        ### execution
        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.STEP_STARTED,
                step_name=step.step_name,
                step_id=step.id
            )
        )
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = await asyncio.to_thread(func,*args) # sync functions

        step.update_step_status(StepStatus.COMPLETED)
        step.update_step_return_data(result)
        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.STEP_COMPLETED,
                step_id=step.id,
                step_name=step.step_name,
                data=result,
                message=f"{step.step_name} completed"
            )
        )
        return result

    except Exception as error:
        ctx.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.STEP_FAILED,
                error=str(error),
                message="step failed"
            )
        )
        raise

async def resume(workflow_id: str):
    from store import stored_states

    workflow_state: WorkflowContext | None = next((w for w in stored_states if w.id == workflow_id), None)

    if workflow_state is None:
        return

    if workflow_state.status == WorkflowStatus.COMPLETED:
        return workflow_state.return_data
    else:

        ### Resume Execution
        workflow_state.add_event(
            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_RESUMED,
                message="Workflow resumed"
            )
        )

        workflow_state._cursor = 0
        func = globals()[workflow_state.workflow_name]
        result = await func(workflow_state, *workflow_state.input_arguments.args, **workflow_state.input_arguments.kwargs)

        workflow_state.update_status(WorkflowStatus.COMPLETED)
        workflow_state.update_return_date(result)

        return result

### Client
def verify_order() -> str:
    random_number = _generate_random_number()
    print("Verifying Order id ", random_number)
    sleep(1)
    return random_number

async def withdraw_money(order_id: str):
    print(f"Withdrawing for order id {order_id}")
    await asyncio.sleep(1)
    return "withdraw_money_return"

def send_email(order_id: str):
    print(f"Sending Email to order id owner {order_id}")
    sleep(1)
    return "send_email_return"

async def useCase(ctx: WorkflowContext):
    order_id = await workflow_step(ctx, verify_order)
    withdraw = await workflow_step(ctx, withdraw_money, order_id)
    email = await workflow_step(ctx, send_email, order_id)

    # pprint(ctx)

    return {
        "order_id": order_id,
        "withdraw": withdraw,
        "email": email,
    }

async def main():
    # await resume("dd7e2e94-bd9c-4f4c-939e-a7f6d477f527")
    # await resume("e0f1251a-36ee-4118-9806-2ee547300151")
    await workflow(useCase)


if __name__ == "__main__":
    asyncio.run(main())