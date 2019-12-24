from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import json

from .helpers import LaunchRequestHelper
from .helpers import CreateMeetingSystemIntentHelper
from .helpers import BookMeetingIntentHelper
from .helpers import CancelIntentHelper
from .helpers import StopIntentHelper
from .helpers import SessionEndedRequestHelper
from .utils.common_util import UserStates

class EntryHandler(AbstractRequestHandler):
    TAG = 'EntryHandler'
    def can_handle(self, handler_input):
        print(EntryHandler.TAG + ' matched')
        return True

    def handle(self, handler_input):
        # build default response
        response_result = handler_input.response_builder.speak("I don't understand that. ").set_should_end_session(False).response
        # retrieve common attributes
        session_attr = handler_input.attributes_manager.session_attributes
        request_type = handler_input.request_envelope.request.object_type
        print(EntryHandler.TAG + ' - request type: ' + request_type)
        # check request type
        if request_type == "LaunchRequest":
            response_result = LaunchRequestHelper.execute(handler_input)
        if request_type == "IntentRequest":
            intent_name = handler_input.request_envelope.request.intent.name
            print(EntryHandler.TAG + ' - intent name: ' + intent_name)
            # check session
            if is_user_state_correct(session_attr["user_states"], intent_name):
                # check intent name
                if intent_name == CreateMeetingSystemIntentHelper.INTENT_NAME:
                    response_result = CreateMeetingSystemIntentHelper.execute(handler_input)
                if intent_name == BookMeetingIntentHelper.INTENT_NAME:
                    response_result = BookMeetingIntentHelper.execute(handler_input)
                if intent_name == "AMAZON.CancelIntent":
                    response_result = CancelIntentHelper.execute(handler_input)
                if intent_name == "AMAZON.StopIntent":
                    response_result = StopIntentHelper.execute(handler_input)
        if request_type == "SessionEndedRequest":
            response_result = SessionEndedRequestHelper.execute(handler_input)
        return response_result

# to check user state
def is_user_state_correct(user_states_json, intent_name):
   print('is_user_state_correct' + ' - user_states: ' + user_states_json)
   user_states = json.loads(user_states_json)

   if intent_name == CreateMeetingSystemIntentHelper.INTENT_NAME:
        if UserStates.USING_MEETING_SYSTEM.name in user_states:
            print('is_user_state_correct' + ' - meeting system exists already')
            return False
   return True

# build Skill with handlers
sb = SkillBuilder()
sb.add_request_handler(EntryHandler())
myskill003 = sb.create()