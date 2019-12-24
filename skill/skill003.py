from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import json

from .helpers import LaunchRequestHelper
from .helpers import CreateMeetingSystemIntentHelper
from .helpers.BookMeetingIntentHelper import BookMeetingIntentHelper
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
        request_type = handler_input.request_envelope.request.object_type
        print(EntryHandler.TAG + ' - request type: ' + request_type)
        # check request type
        if is_request_type("LaunchRequest")(handler_input):
            response_result = LaunchRequestHelper.execute(handler_input)
        if is_request_type("IntentRequest")(handler_input):
            intent_name = handler_input.request_envelope.request.intent.name
            print(EntryHandler.TAG + ' - intent name: ' + intent_name)
            # check session
            if is_user_state_correct(handler_input):
                # check intent name
                if is_intent_name(CreateMeetingSystemIntentHelper.INTENT_NAME)(handler_input):
                    response_result = CreateMeetingSystemIntentHelper.execute(handler_input)
                if is_intent_name(BookMeetingIntentHelper.INTENT_NAME)(handler_input):
                    response_result = BookMeetingIntentHelper().execute(handler_input)
                if is_intent_name("AMAZON.CancelIntent")(handler_input):
                    response_result = CancelIntentHelper.execute(handler_input)
                if is_intent_name("AMAZON.StopIntent")(handler_input):
                    response_result = StopIntentHelper.execute(handler_input)
        if is_request_type("SessionEndedRequest")(handler_input):
            response_result = SessionEndedRequestHelper.execute(handler_input)
        return response_result

# to check user state
def is_user_state_correct(handler_input):
   # check session state
   session_attr = handler_input.attributes_manager.session_attributes
   user_states = json.loads(session_attr["user_states"])
   print('is_user_state_correct' + ' - session_attr["user_states"]: ' + session_attr[
      "user_states"])
   if is_intent_name(CreateMeetingSystemIntentHelper.INTENT_NAME)(handler_input) \
           and UserStates.USING_MEETING_SYSTEM.name in user_states:
      print('is_user_state_correct' + ' - meeting system exists already')
      return False
   return True

# create Skill
sb = SkillBuilder()
# register entry handler
sb.add_request_handler(EntryHandler())
myskill003 = sb.create()