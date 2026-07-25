from main import (
    WorkflowContext,
    WorkflowStep,
    StepStatus,
    WorkflowStatus,
    WorkflowEvent,
    WorkflowEventType,
    Args,
)

from datetime import datetime
from uuid import UUID


stored_states: list[WorkflowContext] = [

    # Workflow paused after verify_order completed
    WorkflowContext(
        id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f527",
        workflow_name="useCase",
        status=WorkflowStatus.RUNNING,
        
        input_arguments=Args(),

        steps=[
            WorkflowStep(
                id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f521",
                step_name="verify_order",
                step_counter=1,
                status=StepStatus.COMPLETED,

                input_arguments=Args(),

                return_data=UUID(
                    "dd7e2e94-bd9c-4f4c-939e-a7f6d477f100"
                ),

                start_date=datetime(2026, 7, 24, 5, 0, 0),
                end_date=datetime(2026, 7, 24, 5, 0, 1),
            )
        ],

        _cursor=1,

        events=[
            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_STARTED,
                message="Workflow useCase started"
            ),

            WorkflowEvent(
                event_type=WorkflowEventType.STEP_CREATED,
                step_id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f521",
                step_name="verify_order",
                message="Created step verify_order"
            ),

            WorkflowEvent(
                event_type=WorkflowEventType.STEP_STARTED,
                step_id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f521",
                step_name="verify_order",
            ),

            WorkflowEvent(
                event_type=WorkflowEventType.STEP_COMPLETED,
                step_id="dd7e2e94-bd9c-4f4c-939e-a7f6d477f521",
                step_name="verify_order",
                data=UUID(
                    "dd7e2e94-bd9c-4f4c-939e-a7f6d477f100"
                ),
                message="verify_order completed"
            ),
        ]
    ),



    # Workflow crashed while send_email was running
    WorkflowContext(
        id="e0f1251a-36ee-4118-9806-2ee547300151",
        workflow_name="useCase",
        status=WorkflowStatus.RUNNING,
        
        input_arguments=Args(),

        steps=[

            WorkflowStep(
                id="f7f712f3-0567-4ca5-816e-1076787224ea",
                step_name="verify_order",
                step_counter=1,
                status=StepStatus.COMPLETED,
                
                input_arguments=Args(),

                return_data=UUID(
                    "ba55ab72-c083-4153-87a1-7d98af23c5df"
                ),

                start_date=datetime(2026,7,24,5,6,32),
                end_date=datetime(2026,7,24,5,6,33),
            ),


            WorkflowStep(
                id="c4001a4e-8ae4-49e7-9060-abca2ba7ba9c",
                step_name="withdraw_money",
                step_counter=2,
                status=StepStatus.COMPLETED,

                input_arguments=Args(
                    args=(
                        UUID("ba55ab72-c083-4153-87a1-7d98af23c5df"),
                    )
                ),

                return_data="withdraw_money_return",

                start_date=datetime(2026,7,24,5,6,33),
                end_date=datetime(2026,7,24,5,6,34),
            ),


            WorkflowStep(
                id="458f4470-dc0f-4167-a3de-40d059d23343",
                step_name="verify_order",
                step_counter=3,
                status=StepStatus.COMPLETED,
                
                input_arguments=Args(),

                return_data=UUID(
                    "7ef33c56-b736-439c-b27c-d6791884fec7"
                ),

                start_date=datetime(2026,7,24,5,6,34),
                end_date=datetime(2026,7,24,5,6,35),
            ),


            WorkflowStep(
                id="e7aeccbc-3dbf-4eff-abb0-0f92c7d7dbc8",
                step_name="send_email",
                step_counter=4,
                status=StepStatus.RUNNING,

                input_arguments=Args(
                    args=(
                        UUID("7ef33c56-b736-439c-b27c-d6791884fec7"),
                    )
                ),

                return_data=None,

                start_date=datetime(2026,7,24,5,6,35),
                end_date=None,
            ),
        ],

        _cursor=4,

        events=[

            WorkflowEvent(
                event_type=WorkflowEventType.WORKFLOW_STARTED,
            ),


            WorkflowEvent(
                event_type=WorkflowEventType.STEP_COMPLETED,
                step_name="verify_order",
                data=UUID(
                    "ba55ab72-c083-4153-87a1-7d98af23c5df"
                )
            ),


            WorkflowEvent(
                event_type=WorkflowEventType.STEP_COMPLETED,
                step_name="withdraw_money",
                data="withdraw_money_return"
            ),


            WorkflowEvent(
                event_type=WorkflowEventType.STEP_COMPLETED,
                step_name="verify_order",
                data=UUID(
                    "7ef33c56-b736-439c-b27c-d6791884fec7"
                )
            ),

            WorkflowEvent(
                event_type=WorkflowEventType.STEP_STARTED,
                step_name="send_email",
                step_id="e7aeccbc-3dbf-4eff-abb0-0f92c7d7dbc8"
            ),
       ]
    )
]