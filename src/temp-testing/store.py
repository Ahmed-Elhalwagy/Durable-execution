from main import WorkflowContext, WorkflowStep, StepStatus, WorflowStatus
from datetime import datetime
from uuid import  UUID

stored_states: list[WorkflowContext] = [
    WorkflowContext(
        id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f527",
        func_name="useCase",
        status=WorflowStatus.RUNNING,
        steps=[
            WorkflowStep(
                id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f521",
                status=StepStatus.COMPLETED,
                func_name="verify_order",
                return_data="dd7e2e94-bd9c-4f4c-939e-a7f6d477f100",
                end_date=None,
                step_counter=1,
            ),
        ],
        _cursor=1,
    ),
    WorkflowContext(
        func_name="useCase",
        id="e0f1251a-36ee-4118-9806-2ee547300151",
        status=WorflowStatus.RUNNING,
        steps=[
            WorkflowStep(
                func_name="verify_order",
                step_counter=1,
                id="f7f712f3-0567-4ca5-816e-1076787224ea",
                start_date=datetime(2026, 7, 24, 5, 6, 32, 401427),
                end_date=datetime(2026, 7, 24, 5, 6, 33, 401616),
                status=StepStatus.COMPLETED,
                input_arguments={},
                return_data=UUID("ba55ab72-c083-4153-87a1-7d98af23c5df"),
            ),
            WorkflowStep(
                func_name="withdraw_money",
                step_counter=2,
                id="c4001a4e-8ae4-49e7-9060-abca2ba7ba9c",
                start_date=datetime(2026, 7, 24, 5, 6, 33, 401736),
                end_date=datetime(2026, 7, 24, 5, 6, 34, 401913),
                status=StepStatus.COMPLETED,
                input_arguments={
                    "order_id": UUID("ba55ab72-c083-4153-87a1-7d98af23c5df")
                },
                return_data="withdraw_money_return",
            ),
            WorkflowStep(
                func_name="verify_order",
                step_counter=3,
                id="458f4470-dc0f-4167-a3de-40d059d23343",
                start_date=datetime(2026, 7, 24, 5, 6, 34, 402028),
                end_date=datetime(2026, 7, 24, 5, 6, 35, 402270),
                status=StepStatus.COMPLETED,
                input_arguments={},
                return_data=UUID("7ef33c56-b736-439c-b27c-d6791884fec7"),
            ),
            WorkflowStep(
                func_name="send_email",
                step_counter=4,
                id="e7aeccbc-3dbf-4eff-abb0-0f92c7d7dbc8",
                start_date=datetime(2026, 7, 24, 5, 6, 35, 402383),
                end_date=datetime(2026, 7, 24, 5, 6, 36, 402573),
                status=StepStatus.RUNNING,
                input_arguments={
                    "order_id": UUID("7ef33c56-b736-439c-b27c-d6791884fec7")
                },
                return_data=None,
            ),
        ],
        _cursor=4,
        start_date=datetime(2026, 7, 24, 5, 6, 32, 401356),
        end_date=None,
        input_arguments={},
        return_data=None,
    )
]