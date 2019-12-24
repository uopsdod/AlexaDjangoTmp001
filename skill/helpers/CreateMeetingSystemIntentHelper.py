import json
from ..utils.common_util import UserStates

# CreateMeetingSystemIntent
TAG = 'CreateMeetingSystemIntent'
INTENT_NAME = 'CreateMeetingSystemIntent'
def execute(handler_input):
    # type: (HandlerInput) -> Response
    # store session data
    session_attr = handler_input.attributes_manager.session_attributes
    user_states = json.loads(session_attr["user_states"])
    user_states.append(UserStates.USING_MEETING_SYSTEM.name)
    session_attr["user_states"] = json.dumps(user_states)
    print(TAG + ' - user_states:' + session_attr["user_states"])
    # build response
    speech_text = "OK, I have created a new meeting system for you. "
    speech_text += "Do you want to book a meeting by day?"
    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

