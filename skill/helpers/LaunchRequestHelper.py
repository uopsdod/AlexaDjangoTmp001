import json
from ..utils.common_util import UserStates

class LaunchRequestHelper():
    # LanchRequest
    TAG = 'LaunchRequest'
    def execute(self, handler_input):
        # type: (HandlerInput) -> Response
        # initialize session state
        session_attr = handler_input.attributes_manager.session_attributes
        user_states = []
        user_states.append(UserStates.INIT.name)
        session_attr["user_states"] = json.dumps(user_states)
        print(LaunchRequestHelper.TAG + ' - user_states:' + session_attr["user_states"])
        # build response
        speech_text = "Version one, do you want to create a new meeting system or use an existing one?"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response
