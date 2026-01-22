from modi_agent.agent import ModiAgent
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue


class ModiAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = ModiAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        # Get user input and thread ID from A2A context
        query = context.get_user_input()
        thread_id = context.get_thread_id()

        # Call ModiAgent (async)
        response = await self.agent.get_response(query, thread_id)
        return response

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        # Optional: handle cancellation if needed
        return
