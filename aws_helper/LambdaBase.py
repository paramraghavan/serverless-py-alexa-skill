"""
Base class for implementing Lambda handlers as classes.
Used across multiple Lambda functions (included in each zip file).
Add additional features here common to all your Lambdas, like logging.
"""

from abc import ABC, abstractmethod
import json


# https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/


def call_no_matching_intent(event, no_intent_message):
    if 'type' in event['request'] and event['request']['type'] == 'SessionEndedRequest':
        # SessionEndedRequest notifies that a session was ended. This handler
        # will be triggered when a currently open
        # session is closed for one of the following reasons: 1) The user says "exit" or "quit".
        # 2) The user does not
        # respond or says something that does not match an intent defined in your voice model.
        # 3) An error occurs
        print('Session Ended...')
        # send an empty response
        response = {}
        return response

    message = ''
    should_end_session = True
    if 'intent' not in event['request']:
        return get_response_for_intent_not_defined(event, no_intent_message)
    elif 'name' in event['request']['intent']:
        if event['request']['intent']['name'] == 'AMAZON.HelpIntent':
            message = 'You can say hello to me! How can I help?'
            # should_end_session = False
        elif event['request']['intent']['name'] == ('AMAZON.CancelIntent' or 'AMAZON.StopIntent'):
            message = 'Goodbye!'
        elif event['request']['intent']['name'] == 'AMAZON.FallbackIntent':
            message = 'Sorry, I don\'t know about that. Please try again.'
            should_end_session = False
        else:
            message = 'This ,' + event['request']['intent']['name'] + ', intent is not supported'
    else:
        message = 'Empty intent name'

    print(f'message: {message} and shouldEndSession status: {should_end_session}')

    # response_msg, a dictionary data type
    response_msg = {'version': '1.0', 'response': {}}
    response_msg['response']['outputSpeech'] = {}
    response_msg['response']['outputSpeech']['type'] = 'PlainText'
    response_msg['response']['outputSpeech']['text'] = message
    if not should_end_session:
        response_msg['response']['reprompt'] = {}
        response_msg['response']['reprompt']['outputSpeech'] = {}
        response_msg['response']['reprompt']['outputSpeech']['type'] = 'PlainText'
        response_msg['response']['reprompt']['outputSpeech']['text'] = message

    response_msg['response']['shouldEndSession'] = should_end_session
    # dictionary to json string
    response = json.dumps(response_msg)

    return response


def get_response_for_intent_not_defined(event, message):
    # response_msg, a dictionary data type
    response_msg = {'version': '1.0', 'response': {}}
    response_msg['response']['outputSpeech'] = {}
    response_msg['response']['outputSpeech']['type'] = 'PlainText'
    response_msg['response']['outputSpeech']['text'] = message
    response_msg['response']['reprompt'] = {}
    response_msg['response']['reprompt']['outputSpeech'] = {}
    response_msg['response']['reprompt']['outputSpeech']['type'] = 'PlainText'
    response_msg['response']['reprompt']['outputSpeech']['text'] = message

    response_msg['response']['shouldEndSession'] = False
    # dictionary to json string
    response = json.dumps(response_msg)

    return response


default_upper_limit = 108


def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return default_upper_limit


class LambdaBase(ABC):

    @abstractmethod
    def handle(self, event, context):
        pass
