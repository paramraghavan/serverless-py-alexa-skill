import random
from aws_helper.LambdaBase import LambdaBase, call_no_matching_intent, get_response_for_intent_not_defined, \
    default_upper_limit, parse_int

# this is can be read from S3 or database,
# right now defined/hard-coded here.
hacks = [
    'To make a room smell better, tape a dryer sheet over your AC unit and turn it on.',
    'To keep clothes from wrinkling when you travel, roll them instead of fold them in your suitcase.',
    'On a hot day, use a coozie to cover your car\'s gear shift to keep it cool.',
    'During a trip to the beach, store your keys and money in an old (cleaned) sunscreen bottle.',
    'To serve condiments at a BBQ, use a muffin tin pan rather than bowls.',
    'Too many keys?  Use fingernail polish to paint them different colors.',
    'To clean a blender, add water and soap, and turn it on.',
    'To keep pizza hot on the drive home, turn on your seat warmer.',
    'At a hotel and forgot your charger?  The TV usually has a USB plug-in.',
    'On your phone, use an accented letter in your passcode.  It\'ll be harder to guess.',
]

"""
    This is an implementation of a Lambda handler as a class for a specific     
    Lambda function, LuckNumberSkill
"""


class LuckNumberSkill(LambdaBase):

    def __init__(self):  # implementation-specific args and/or kwargs
        pass

    def handle(self, event, context):
        # following to be commented out or add debug flag
        print(f'event: {event}')
        print(f'context: {context}')
        print(f" User id : {event['session']['user']['userId']}")
        print(f" Request id : {event['request']['requestId']}")
        ##################################################

        # if intent not defined, return response
        if 'intent' not in event['request']:
            no_intent_message = 'Welcome to good ducky, what would you like to do, ' \
                                'my lucky number or hack for today'
            return get_response_for_intent_not_defined(event, no_intent_message)

        if event['request']['intent']['name'] == 'LuckyNumberIntent':
            return call_lucky_number_intent(event)
        elif event['request']['intent']['name'] == 'HackIntent':
            return call_hack_intent()
        else:
            no_intent_message = 'Welcome to good ducky, what would you like to do, ' \
                                'my lucky number or hack for today'
            return call_no_matching_intent(event, no_intent_message)


def call_hack_intent():
    # as array index is from 0(and not from 1) to n-1
    number_of_hacks = len(hacks) - 1
    hack_array_index = random.randint(0, number_of_hacks)

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': "Your today's hack is, " + hacks[hack_array_index] + ", enjoy!",
            },
            "shouldEndSession": True
        }
    }
    return response


def call_lucky_number_intent(event):
    upperLimitDict = event['request']['intent']['slots']['UpperLimit']
    upperLimit = None
    if 'value' in upperLimitDict:
        upperLimit = parse_int(upperLimitDict['value'])
    else:
        upperLimit = default_upper_limit

    number = random.randint(0, upperLimit)
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Your lucky number is ' + str(number),
            },
            'reprompt': {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": 'Ask for a hack, say - good ducky share a hack ',
                }
            },
            "shouldEndSession": False
        }
    }
    return response
