import asyncio
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages.ai import AIMessage
from ambani_agent.tools import get_ambani_availability



load_dotenv()
memory = MemorySaver()

class AmbaniAgent:
    
    SUPPORTS_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
       
        self.model = ChatOpenAI(model="gpt-4o-mini")

        self.tools = [get_ambani_availability]
        self.systemprompt = (
                 "You are a scheduling assistant for Ambani.\n"
                 "Your task is to help users check Ambani's availability on specific dates.\n"
                 "Use the provided get_ambani_availability tool to fetch availability information when needed.\n"
                  "If the query is not related to ambani's availability, respond with 'I am here to help you with Ambani's availability only.'"
                " respond with unique answers."
                "respond like human and make sure to be polite and professional in your responses."
                )

        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.systemprompt,
            checkpointer=memory
        )

    async def get_response(self, user_input: str, thread_id: str):
        payload = {"messages": [("user", user_input)]}
        config = {"configurable": {"thread_id": thread_id}}

        result = self.agent.invoke(payload, config)
        assistant_reply = result["messages"][-1].content
        return {"content": assistant_reply}

#agent = AmbaniAgent()
#assistant = asyncio.run(
#    agent.get_response(
#       user_input="is ambani available on 20th August 2026 at 11:00 PM?",
#       thread_id="thread_123",
#   )
#)
#print(assistant)
