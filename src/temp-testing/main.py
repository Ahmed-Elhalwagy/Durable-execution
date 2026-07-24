from dataclasses import dataclass, field
from enum import Enum
from time import sleep
from datetime import datetime

from typing import Callable
import uuid
from typing_extensions import Any


class WorflowStatus(str, Enum):
    RUNNING = "running"
    PENDING = "pending"
    ERROR = "error"
    COMPLETED = "completed"


class StepStatus(str, Enum):
    RUNNING = "running"
    PENDING = "pending"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class WorkflowStep:
    # 2 identifiers
    func_name: str
    step_counter: int

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime | None = field(default=None)
    status: StepStatus = field(default=StepStatus.RUNNING)

    input_arguments: dict = field(default_factory=dict)
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
    func_name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    status: WorflowStatus = field(default=WorflowStatus.RUNNING)
    steps: list[WorkflowStep] = field(default_factory=list)
    _cursor: int = field(default=0, compare=False) # this cursor is incremented when step is executed

    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime | None = field(default=None)

    input_arguments: dict = field(default_factory=dict)
    return_data : Any = field(default=None)

    def add_step(self, step: WorkflowStep):
        self.steps.append(step)

    def save_input_arguments(self, args):
        self.input_arguments = args

    def update_status(self, new_status: WorflowStatus):
        self.status = new_status
        if new_status == WorflowStatus.COMPLETED:
            self.end_date = datetime.now()

    def next_counter(self) -> int:
        self._cursor += 1
        return self._cursor

    def update_return_date(self, data:Any):
        self.return_data = data

def _generate_random_number():
    return uuid.uuid4()

def verify_order() -> str:
    random_number = _generate_random_number()
    print("Verifying Order id ", random_number)
    sleep(1)
    return random_number

def withdraw_money(order_id: str):
    print(f"Withdrawing for order id {order_id}")
    # raise
    sleep(1)
    return "withdraw_money_return"

def send_email(order_id: str):
    print(f"Sending Email to order id owner {order_id}")
    sleep(1)
    return "send_email_return"


### Wrappers
def worflow_wrapper(func: Callable[[WorkflowContext], None], args: dict[str, Any] | None = None,):
    args = args or {}
    ctx = WorkflowContext(status=WorflowStatus.RUNNING, func_name=func.__name__)
    try:
        ctx.save_input_arguments(args)
        result = func(ctx, **args)
        ctx.update_status(WorflowStatus.COMPLETED)
        ctx.update_return_date(result)
    except Exception as error:
        ctx.update_status(WorflowStatus.ERROR)

def step_wrapper(ctx: WorkflowContext, func: Callable[[], None],  args: dict[str, Any] | None = None):
    args = args or {}
    step_counter = ctx.next_counter()

    step_exist = next(
        (s for s in ctx.steps
         if s.func_name == func.__name__ and s.step_counter == step_counter),
        None,
    )
    try:
        # resume skipping logic
        if step_exist:
            if step_exist.status == StepStatus.COMPLETED:
                return step_exist.return_data
            elif step_exist.status == StepStatus.RUNNING:
                step = step_exist
        else:
            step = WorkflowStep(status=StepStatus.RUNNING, func_name=func.__name__, step_counter=step_counter)
            step.save_input_arguments(args)
            ctx.add_step(step)
        result = func(**args) # execute step
        step.update_step_status(StepStatus.COMPLETED)
        step.update_step_return_data(result)

        return result
    except Exception as error:
        raise


def useCase(ctx: WorkflowContext):
    order_id = step_wrapper(ctx, verify_order)
    
    withdraw = step_wrapper(ctx, withdraw_money, {"order_id": order_id})

    order_id = step_wrapper(ctx, verify_order)

    email = step_wrapper(ctx, send_email, {"order_id": order_id})

def resume(workflow_id: str):
    from store import stored_states
    workflow_state: WorkflowContext | None = next((w for w in stored_states if w.id == workflow_id), None)
    if(workflow_state and workflow_state.status != WorflowStatus.COMPLETED):
        workflow_state._cursor = 0
        func = globals()[workflow_state.func_name]
        func(workflow_state)
    else:
        return

def main():
    # resume("dd7e2e94-bd9c-4f4c-939e-a7f6d477f527")
    resume("e0f1251a-36ee-4118-9806-2ee547300151")
    # worflow_wrapper(useCase)


if __name__ == "__main__":
    main()