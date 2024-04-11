from persona_ai.domain.conversations import Conversation, Message
from persona_ai.domain.tasks import Task
from persona_ai.infrastructure.repositories.mongo import MongoRepository


class ConversationsRepository(MongoRepository[Conversation]):
    def __init__(self):
        super().__init__("conversations", Conversation)


class MessagesRepository(MongoRepository[Message]):
    def __init__(self):
        super().__init__("messages", Message)

        self.collection.create_index("conversation_id", unique=False)


class TasksRepository(MongoRepository[Task]):
    def __init__(self):
        super().__init__("tasks", Task)

        self.collection.create_index("conversation_id", unique=False)
