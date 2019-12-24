import json
from ..utils.common_util import UserStates

# utterance: "exit", "quit"
TAG = 'SessionEndedRequest'
def execute(handler_input):
    print(TAG + ' - clean up resources')
    return handler_input.response_builder.response
