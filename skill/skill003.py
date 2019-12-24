from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import json

from .utils.common_util import UserStates
from .helpers import LaunchRequestHelper
from .helpers import CreateMeetingSystemIntentHelper
from .helpers import BookMeetingIntentHelper
from .helpers import CancelIntentHelper
from .helpers import StopIntentHelper
from .helpers import SessionEndedRequestHelper

#TODO: BookMeetingIntentHandler - create slot to get Monday - Sunday
#TODO: BookMeetingIntentHandler - use slot to get Monday - Sunday

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
            if is_sesssion_correct(handler_input):
                # check intent name
                if is_intent_name(CreateMeetingSystemIntentHelper.INTENT_NAME)(handler_input):
                    response_result = CreateMeetingSystemIntentHelper.execute(handler_input)
                if is_intent_name(BookMeetingIntentHelper.INTENT_NAME)(handler_input):
                    response_result = BookMeetingIntentHelper.execute(handler_input)
                if is_intent_name("AMAZON.CancelIntent")(handler_input):
                    response_result = CancelIntentHelper.execute(handler_input)
                if is_intent_name("AMAZON.StopIntent")(handler_input):
                    response_result = StopIntentHelper.execute(handler_input)
        if is_request_type("SessionEndedRequest")(handler_input):
            response_result = SessionEndedRequestHelper.execute(handler_input)
        return response_result

# General
def is_sesssion_correct(handler_input):
    # check session state
    session_attr = handler_input.attributes_manager.session_attributes
    user_states = json.loads(session_attr["user_states"])
    print('is_sesssion_correct' + ' - session_attr["user_states"]: ' + session_attr[
        "user_states"])
    if is_intent_name(CreateMeetingSystemIntentHelper.INTENT_NAME)(handler_input) \
            and UserStates.USING_MEETING_SYSTEM.name in user_states:
        print(CreateMeetingSystemIntentHelper.TAG + ' - meeting system exists already')
        return False
    return True



# class CancelAndStopIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         print('hey005')
#         return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
#             handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         speech_text = "Goodbye!"
#
#         handler_input.response_builder.speak(speech_text).set_card(
#             SimpleCard("Hello World", speech_text)).set_should_end_session(True)
#         return handler_input.response_builder.response

# class SessionEndedRequestHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         print('hey005')
#         return is_request_type("SessionEndedRequest")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         # any cleanup logic goes here
#
#         return handler_input.response_builder.response

from ask_sdk_core.dispatch_components import AbstractExceptionHandler

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        print('hey005')
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

# register entry handler
sb.add_request_handler(EntryHandler())

# register request handlers
# sb.add_request_handler(LaunchRequestHandler())
# sb.add_request_handler(HelloWorldIntentHandler())
# sb.add_request_handler(HelpIntentHandler())
# sb.add_request_handler(CancelAndStopIntentHandler())
# sb.add_request_handler(SessionEndedRequestHandler())

# register intent handlers
# sb.add_request_handler(CreateMeetingSystemIntentHandler())
# sb.add_request_handler(BookMeetingIntentHandler())

# register exception handlers
# sb.add_exception_handler(AllExceptionHandler())

myskill003 = sb.create()