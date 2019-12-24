import json
from ..utils.common_util import UserStates

# BookMeetingIntent
TAG = 'BookMeetingIntent'
INTENT_NAME = 'BookMeetingIntent'
def execute(self, handler_input):
    # type: (HandlerInput) -> Response
    # retrive slot values
    slots = handler_input.request_envelope.request.intent.slots
    slot_day_of_week = slots['DayOfWeek'].value
    slot_task = slots['Task'].value
    print(TAG + ' - slot_day_of_week: ' + slot_day_of_week)
    print(TAG + ' - slot_task: ' + slot_task)

    speech_text = "OK, I have booked " + slot_day_of_week + " for " + slot_task + ". "
    speech_text += "Thank you for using the meeting system. Bye."
    handler_input.response_builder.speak(speech_text).set_should_end_session(True)
    return handler_input.response_builder.response

