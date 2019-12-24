import json
from ..utils.common_util import UserStates

# utterance: "cancel"
TAG = 'AMAZON.CancelIntent'
INTENT_NAME = 'AMAZON.CancelIntent'
def execute(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"
    return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response
