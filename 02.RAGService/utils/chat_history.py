''''
    This block manages chat history
        - Creating and saving history
        - Loading history if already_exist

'''


import chat_store

class ChatHistoryManager:
    def __init__(self, session_id):
        self.session_id = session_id
        self.chat_history = []

    def load_history(self):
        self.chat_history = chat_store.get_messages(self.session_id)

    def save_message(self, role, content, metadata=None):
        # Save new Messages in history
        self.chat_history.append(
            session_id=self.session_id,
            message={
                
                "role": role,
                "content": content,
                "metadata": metadata or {},
            },
        )

    def archive_history(self):
        database.save_chat_history(self.chat_history)
