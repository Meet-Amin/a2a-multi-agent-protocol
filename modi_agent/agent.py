"""
Full async CrewAI agent runner for Modi availability.

✅ Works with:
- crewai Agent / Crew / Task / Process
- a custom tool class ModiAvailabilityTool (imported from tool.py)
- asyncio.run(...)

Fixes:
- correct indentation
- no missing args
- uses self.modi_agent everywhere
- async via asyncio.to_thread for blocking crew.kickoff()
"""

import os
import asyncio
from dotenv import load_dotenv

from crewai import Agent, LLM, Crew, Task, Process
try:
    from .tool import ModiAvailabilityTool  # package import
except ImportError:  # pragma: no cover - allows running as a script
    from tool import ModiAvailabilityTool  # type: ignore


load_dotenv()


class ModiAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Put it in your .env file like:\n"
                "OPENAI_API_KEY=your_key_here"
            )

        self.llm = LLM(
            model="gpt-4o-mini",
            api_key=api_key,
        )

        self.modi_agent = Agent(
            role="scheduling assistant",
            goal="Answer questions about Modi's availability on specific dates using the provided tool.",
            backstory=(
                "You are a professional scheduling assistant. "
                "You help users check availability for specific dates/times and respond politely. "
                "Always use the availability tool when a date/time is mentioned."
            ),
            tools=[ModiAvailabilityTool()],
            llm=self.llm,
        )

    async def invoke(self, user_question: str) -> str:
        """
        Async wrapper around Crew.kickoff() (which is sync/blocking),
        executed in a background thread.
        """
        task = Task(
            description=(
                f"User question: '{user_question}'. "
                "Use the provided tool to check availability if a date/time is asked."
            ),
            expected_output=(
                "A clear, polite answer about Modi's availability. "
                "If the tool returns no data, ask for the missing date/time details."
            ),
            agent=self.modi_agent,
        )

        crew = Crew(
            agents=[self.modi_agent],
            tasks=[task],
            process=Process.sequential,
        )

        # kickoff() is synchronous -> run it in a thread so invoke() stays async
        result = await asyncio.to_thread(crew.kickoff)
        return str(result)

    async def get_response(self, user_input: str, thread_id: str):
        # thread_id is unused by CrewAI, but kept for A2A interface parity
        response = await self.invoke(user_input)
        return {"content": response}
