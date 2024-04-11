import threading
import time
from typing import List

from persona_ai.domain.conversations import Message
from persona_ai.transport.messagebus import (
    MessageBus,
    Participant,
    Event,
)


class LocalSubscription:
    """
    This class represents a local subscription.
    """

    participant: Participant
    """The participant."""

    def __init__(self, participant: Participant):
        self.participant = participant

    def handle_message(self, message: Message):
        self.participant.last_activity = time.time()
        self.participant.receive(message)

    def handle_event(self, event: Event):
        self.participant.last_activity = time.time()
        self.participant.handle_event(event)


class LocalMessageBus(MessageBus):
    """
    This class represents a local message bus.
    """

    subscriptions: List[LocalSubscription] = []
    running: bool = False

    def register(self, participants: Participant | List[Participant]):
        participants = (
            [participants] if isinstance(participants, Participant) else participants
        )

        for participant in participants:
            if not any(s.participant.id == participant.id for s in self.subscriptions):
                subscription = LocalSubscription(participant)
                self.subscriptions.append(subscription)

    def unregister(self, participants: List[Participant]):
        for participant in participants:
            subscription = next(
                filter(
                    lambda s: s.participant.id == participant.id,
                    self.subscriptions,
                ),
                None,
            )

            if subscription is not None:
                self.subscriptions.remove(subscription)

    def start(self) -> threading.Event:
        self.running = True
        event = threading.Event()
        event.set()
        return event

    def stop(self) -> threading.Event:
        self.running = False
        event = threading.Event()
        event.set()
        return event

    def publish_message(self, message: Message, recipient_id: str, **kwargs):
        subscription = next(
            filter(lambda s: s.participant.id == recipient_id, self.subscriptions),
            None,
        )
        subscription.handle_message(message)

    def publish_event(self, event: Event, recipient_id: str | None = None, **kwargs):
        subscription = next(
            filter(lambda s: s.participant.id == recipient_id, self.subscriptions),
            None,
        )
        subscription.handle_event(event)
