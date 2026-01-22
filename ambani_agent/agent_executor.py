from ambani_agent.agent import AmbaniAgent
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue

class AmbaniAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = AmbaniAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        query = context.get_user_input()
        thread_id = context.get_thread_id()

      
        response = await self.agent.get_response(query, thread_id)
        return response

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
    
        return
