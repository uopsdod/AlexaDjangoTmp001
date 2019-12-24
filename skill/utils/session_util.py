import json
from ask_sdk_core.utils import is_intent_name
from .common_util import UserStates

def is_sesssion_correct(handler_input):
   # check session state
   session_attr = handler_input.attributes_manager.session_attributes
   user_states = json.loads(session_attr["user_states"])
   print('is_sesssion_correct' + ' - session_attr["user_states"]: ' + session_attr[
      "user_states"])
   if is_intent_name(CreateMeetingSystemIntentHelper.INTENT_NAME)(handler_input) \
           and UserStates.USING_MEETING_SYSTEM.name in user_states:
      print('is_sesssion_correct' + ' - meeting system exists already')
      return False
   return True