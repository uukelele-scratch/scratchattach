"""v2 ready: MessageEvents class"""

from . import user
from .commons import BaseEventHandler

class MessageEvents(BaseEventHandler):
    """
    Class that calls events when you receive messages on your Scratch account. Data fetched from Scratch's API.
    """
    def __init__(self, user):
        self.user = user
        self._thread = None
        self.running = False
        self._events = {}
        self.current_message_count = int(self.user.message_count())
    
    def _update(self):
        while True:
            if self.running is False:
                return
            message_count = int(self.user.message_count())
            if message_count != self.current_message_count:
                try:
                    self.events["on_count_change"](int(self.current_message_count), int(message_count))
                except Exception as e:
                    print(f"Caught exception in event on_message: "+str(e))
                if message_count != 0:
                    if message_count < self.current_message_count:
                        self.current_message_count = 0
                    if self.user._session is not None: # authentication check
                        if self.user._session.username == self.user.username: # authorization check
                            new_messages = self.user._session.messages(limit=message_count-self.current_message_count)
                            for message in new_messages[::-1]:
                                try:
                                    self.events["on_message"](message)
                                except Exception as e:
                                    print(f"Caught exception in event on_message: "+str(e))
                self.current_message_count = int(message_count)
            