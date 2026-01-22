from __future__ import annotations

if __package__ is None:
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from a2a.server.apps.jsonrpc import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from ambani_agent.agent_executor import AmbaniAgentExecutor
import uvicorn


def main(host="localhost", port=10004):
         
    skill = AgentSkill(
        id="schedule_bedminton",
        name="Bedminton Scheduling Tool",
        description="Helps users check Ambani's availability and schedule appointments for Bedminton.",
        tags=["scheduling", "availability", "appointments", "bedminton"],
        examples=[
            "is ambani available on 10th August 2026? for bedminton match",
        ],
    )

    agent_card = AgentCard(
        name="Ambani's Agent",
        description="An agent to check Ambani's availability on specific dates. and help with scheduling appointments.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=AmbaniAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host=host, port=port)
if __name__ == "__main__":
    main()
