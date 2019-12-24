from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import enum
import json

#TODO: BookMeetingIntentHandler - create slot to get Monday - Sunday
#TODO: BookMeetingIntentHandler - use slot to get Monday - Sunday

class UserStates(enum.Enum):
   INIT = 0
   USING_MEETING_SYSTEM = 1

class EntryHandler(AbstractRequestHandler):
    TAG = 'EntryHandler'
    def can_handle(self, handler_input):
        print(EntryHandler.TAG + ' matched')
        return True

    def handle(self, handler_input):
        response_result = handler_input.response_builder.speak("no handler found").set_should_end_session(True)
        # retrieve common attributes
        request_type = handler_input.request_envelope.request.object_type
        print(EntryHandler.TAG + ' - request type: ' + request_type)
        # check request type
        if is_request_type("LaunchRequest")(handler_input):
            response_result = doLaunchRequestAction(self, handler_input)
        if is_request_type("IntentRequest")(handler_input):
            intent_name = handler_input.request_envelope.request.intent.name
            print(EntryHandler.TAG + ' - intent name: ' + intent_name)
            if is_intent_name(CreateMeetingSystemIntent_INTENT_NAME)(handler_input):
                if is_sesssion_correct(self, handler_input):
                    response_result = doCreateMeetingSystemIntentAction(self, handler_input)
        return response_result

# General
def is_sesssion_correct(self, handler_input):
    # check session state
    session_attr = handler_input.attributes_manager.session_attributes
    user_states = json.loads(session_attr["user_states"])
    print('is_sesssion_correct' + ' - session_attr["user_states"]: ' + session_attr[
        "user_states"])
    if is_intent_name(CreateMeetingSystemIntent_INTENT_NAME)(handler_input) \
            and UserStates.USING_MEETING_SYSTEM.name in user_states:
        print(CreateMeetingSystemIntent_TAG + ' - meeting system exists already')
        return False
    return True

# LanchRequest
LaunchRequest_TAG = 'LaunchRequest'
def doLaunchRequestAction(self, handler_input):
    # type: (HandlerInput) -> Response
    # initialize session state
    session_attr = handler_input.attributes_manager.session_attributes
    user_states = []
    user_states.append(UserStates.INIT.name)
    session_attr["user_states"] = json.dumps(user_states)
    print(LaunchRequest_TAG + ' - user_states:' + session_attr["user_states"])
    # build response
    speech_text = "Version one, do you want to create a new meeting system or use an existing one?"
    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

# CreateMeetingSystemIntent
CreateMeetingSystemIntent_TAG = 'CreateMeetingSystemIntent'
CreateMeetingSystemIntent_INTENT_NAME = 'CreateMeetingSystemIntent'
def doCreateMeetingSystemIntentAction(self, handler_input):
    # type: (HandlerInput) -> Response
    # store session data
    session_attr = handler_input.attributes_manager.session_attributes
    user_states = json.loads(session_attr["user_states"])
    user_states.append(UserStates.USING_MEETING_SYSTEM.name)
    session_attr["user_states"] = json.dumps(user_states)
    print(CreateMeetingSystemIntent_TAG + ' - user_states:' + session_attr["user_states"])
    # build response
    speech_text = "OK, I have created a new meeting system for you. "
    speech_text += "Do you want to book a meeting by day?"
    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response


# class LaunchRequestHandler(AbstractRequestHandler):
#     TAG = 'LaunchRequestHandler'
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         # check request type
#         print(LaunchRequestHandler.TAG + ' - request type:' + handler_input.request_envelope.request.object_type)
#         if not is_request_type("LaunchRequest")(handler_input):
#             return False
#
#         print(LaunchRequestHandler.TAG + ' matched')
#         return True
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         # initialize session state
#         session_attr = handler_input.attributes_manager.session_attributes
#         user_states = []
#         user_states.append(UserStates.INIT.name)
#         session_attr["user_states"] = json.dumps(user_states)
#         print(LaunchRequestHandler.TAG + ' - user_states:' + session_attr["user_states"])
#
#         speech_text = "Version one, do you want to create a new meeting system or use an existing one?"
#         handler_input.response_builder.speak(speech_text).set_should_end_session(False)
#         return handler_input.response_builder.response

# class CreateMeetingSystemIntentHandler(AbstractRequestHandler):
#     TAG = 'CreateMeetingSystemIntentHandler'
#     INTENT_NAME = 'CreateMeetingSystemIntent'
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         # check request type
#         print(CreateMeetingSystemIntentHandler.TAG + ' - request type: ' + handler_input.request_envelope.request.object_type)
#         if not is_request_type("IntentRequest")(handler_input):
#             return False
#         # check intent name
#         print(CreateMeetingSystemIntentHandler.TAG + ' - intent name: ' + handler_input.request_envelope.request.intent.name)
#         if not is_intent_name(CreateMeetingSystemIntentHandler.INTENT_NAME)(handler_input):
#             return False
#         # check session state
#         session_attr = handler_input.attributes_manager.session_attributes
#         user_states = json.loads(session_attr["user_states"])
#         print(CreateMeetingSystemIntentHandler.TAG + ' - session_attr["user_states"]: ' + session_attr["user_states"])
#         if UserStates.USING_MEETING_SYSTEM.name in user_states:
#             print(CreateMeetingSystemIntentHandler.TAG + ' - meeting system exists already')
#             return False
#         # store session data
#         user_states.append(UserStates.USING_MEETING_SYSTEM.name)
#         session_attr["user_states"] = json.dumps(user_states)
#
#         print(CreateMeetingSystemIntentHandler.TAG + ' matched')
#         return True
#
#     def handle(self, handler_input):
#         speech_text = "OK, I have created a new meeting system for you. "
#         speech_text += "Do you want to book a meeting by day?"
#         handler_input.response_builder.speak(speech_text).set_should_end_session(False)
#         return handler_input.response_builder.response


class BookMeetingIntentHandler(AbstractRequestHandler):
    TAG = 'BookMeetingIntentHandler'
    def can_handle(self, handler_input):
        # check request type
        print(BookMeetingIntentHandler.TAG + ' - request type: ' + handler_input.request_envelope.request.object_type)
        if not is_request_type("IntentRequest")(handler_input):
            return False
        # check intent name
        print(BookMeetingIntentHandler.TAG + ' - intent name: ' + handler_input.request_envelope.request.intent.name)
        if not is_intent_name("BookMeetingIntent")(handler_input):
            return False


        print(BookMeetingIntentHandler.TAG + ' matched')
        return True

    def handle(self, handler_input):
        # retrive slot values
        slots = handler_input.request_envelope.request.intent.slots
        slot_day_of_week = slots['DayOfWeek'].value
        slot_task = slots['Task'].value
        print(BookMeetingIntentHandler.TAG + ' - slot_day_of_week: ' + slot_day_of_week)
        print(BookMeetingIntentHandler.TAG + ' - slot_task: ' + slot_task)

        speech_text = "OK, I have booked " + slot_day_of_week + " for " + slot_task + ". "
        speech_text += "Thank you for using the meeting system. Bye."
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# class HelloWorldIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         print('hey005')
#         return is_intent_name("HelloWorldIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         speech_text = "Hello World"
#
#         handler_input.response_builder.speak(speech_text).set_card(
#             SimpleCard("Hello World", speech_text)).set_should_end_session(
#             True)
#         return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print('hey005')
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print('hey005')
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print('hey005')
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response

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