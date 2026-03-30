class ConversationMemory:
    def __init__(self,system_prompt, max_turns=10):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history = []
    
    def add_user_message(self, message):
        self.history.append({"role":"user","content":message})
        

    def add_assistant_message(self, message):
        self.history.append({"role":"assistant","content":message})
        self._trim()

    def _trim(self):
        self.history = self.history[-self.max_turns * 2:]

    def get_history_text(self):
        lines = []
        for msg in self.history:
            role = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines)
    
    def build_chat_prompt(self, current_user_message):
        history_text=self.get_history_text()
        return f"""{self.system_prompt}

Conversation History:
{history_text if history_text else "(empty)"}

Current User Message:
{current_user_message}

Assistant:"""