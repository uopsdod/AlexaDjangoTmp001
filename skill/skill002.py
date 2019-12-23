from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

import json
#TODO: BookMeetingIntentHandler - create slot to get Monday - Sunday
#TODO: BookMeetingIntentHandler - use slot to get Monday - Sunday

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # check request type
        print('LaunchRequestHandler - request type:' + handler_input.request_envelope.request.object_type)
        if not is_request_type("LaunchRequest")(handler_input):
            return False

        print('LaunchRequestHandler matched')
        return True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Version one, do you want to create a new meeting system or use an existing one?"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class CreateMeetingSystemIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # check request type
        print('CreateMeetingSystemIntentHandler - request type: ' + handler_input.request_envelope.request.object_type)
        if not is_request_type("IntentRequest")(handler_input):
            return False
        # check intent name
        print('CreateMeetingSystemIntentHandler - intent name: ' + handler_input.request_envelope.request.intent.name)
        if not is_intent_name("CreateMeetingSystemIntent")(handler_input):
            return False

        print('CreateMeetingSystemIntent matched')
        return True

    def handle(self, handler_input):
        speech_text = "OK, I have created a new meeting system for you. "
        speech_text += "Do you want to book a meeting by day?"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class BookMeetingIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # check request type
        print('BookMeetingIntentHandler - request type: ' + handler_input.request_envelope.request.object_type)
        if not is_request_type("IntentRequest")(handler_input):
            return False
        # check intent name
        print('BookMeetingIntentHandler - intent name: ' + handler_input.request_envelope.request.intent.name)
        if not is_intent_name("BookMeetingIntent")(handler_input):
            return False

        print('BookMeetingIntentHandler matched')
        return True

    def handle(self, handler_input):
        dayOfWeek = "Monday"
        speech_text = "OK, I have booked " + dayOfWeek + " for you. "
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


# register request handlers
sb.add_request_handler(LaunchRequestHandler())
# sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register intent handlers
sb.add_request_handler(CreateMeetingSystemIntentHandler())
sb.add_request_handler(BookMeetingIntentHandler())

# register exception handlers
sb.add_exception_handler(AllExceptionHandler())

myskill002 = sb.create()