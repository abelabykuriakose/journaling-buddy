from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from database import save_fact, get_all_facts

@tool
def remember_user_fact(key: str, value: str) -> str:
    """
    Call this tool whenever the user shares a personal fact about themselves 
    (e.g., name, hobbies, favorite things, current mood, or updates about their life).
    The key should be short (like 'user_name', 'hobby', 'current_mood') and the value should be the detail.
    """
    save_fact(key, value)
    return f"Successfully saved {key} to long-term memory."

class JournalAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.5)
        self.tools = [remember_user_fact]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def chat(self, user_message: str) -> str:
        # 1. Pull everything we know about the user from SQLite
        long_term_memory = get_all_facts()
        
        # 2. Build a system prompt telling the AI who it is and what it remembers
        system_instructions = (
            "You are a supportive, insightful Journaling Buddy. Your goal is to help the user reflect on their day.\n"
            f"Here are the facts you currently remember about the user from past sessions:\n{long_term_memory}\n\n"
            "If the user tells you a new fact about themselves, their mood, or their life, use the 'remember_user_fact' tool instantly.\n"
            "Always speak naturally, weave in things you already remember if relevant, and keep the conversation engaging."
        )
        
        # 3. Ask the AI how to respond
        ai_msg = self.llm_with_tools.invoke(f"{system_instructions}\n\nUser: {user_message}")
        
        # 4. If the AI decided it needs to memorize something, run the tool
        if ai_msg.tool_calls:
            tool_call = ai_msg.tool_calls[0]
            tool_args = tool_call["args"]
            
            # Execute the database saving function
            remember_user_fact.invoke(tool_args)
            
            # Formulate the final conversational reply after saving
            final_reply = self.llm.invoke(
                f"You just saved a new fact using the arguments {tool_args}. "
                f"Respond to the user's message: '{user_message}' warmly, acknowledging what you just remembered."
            )
            return final_reply.content
            
        # If no tool call was needed, just return the text response safely
        # Clean string extraction for conversational payloads
        content = ai_msg.content
        if isinstance(content, list) and len(content) > 0:
            if isinstance(content[0], dict) and "text" in content[0]:
                return content[0]["text"]
        elif isinstance(content, str):
            return content
        return str(content)