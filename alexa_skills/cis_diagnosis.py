# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import os
from alexa_skills import aws_utils

CIS_SERVICE_URL = os.environ['CIS_SERVICE_URL']
CIS_AWS_ACCESS_KEY_ID = os.environ['CIS_AWS_ACCESS_KEY_ID']
CIS_AWS_SECRET_ACCESS_KEY = os.environ.get('CIS_AWS_SECRET_ACCESS_KEY')


skill_name = "CISDiagnosis"
help_text = ("Please tell me your medical condition. You can say "
             "I have cold headache.")

report_slot = "report"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech = "Welcome."

    handler_input.response_builder.speak(
        speech + " " + help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response

from io import StringIO

def getMedicalAnalysis(medical_report):
    client = aws_utils.get_boto3_client(CIS_AWS_ACCESS_KEY_ID, CIS_AWS_SECRET_ACCESS_KEY, 'comprehendmedical')
    response = client.detect_entities_v2(
        Text=medical_report
    )
    # you will see the response from amazon comprehend in cloudwatch logs
    print(response)
    mc_dict = {}
    for entity in response['Entities']:
        if entity["Category"] == "MEDICAL_CONDITION" and len(entity["Traits"]) > 0:
            #print(f'| {entity["Text"]} |{entity["Category"]} |')
            mc_dict[entity["Text"]] = entity["Category"]

    #print(mc_dict)
    string_buffer = StringIO()
    for item in mc_dict:
        string_buffer.write( item + ' is ' + mc_dict[item] + ' ')

    return string_buffer.getvalue()



@sb.request_handler(can_handle_func=is_intent_name("MedicalIntent"))
def my_medical_diagnosis_handler(handler_input):
    """Check if color is provided in slot values. If provided, then
    set your favorite color from slot value into session attributes.
    If not, then it asks user to provide the color.
    """
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    if report_slot in slots:
        medical_report = slots[report_slot].value
        speakOutput =  getMedicalAnalysis(medical_report)
        # handler_input.attributes_manager.session_attributes[color_slot_key] = fav_color

        # we have figure out how to build json object of Medical Conditions as per the CISApi
        speech = "Identified diseases are " + speakOutput
        reprompt = ("That's " + speakOutput)
    else:
        speech = "I'm not sure, please try again"
        reprompt = ("I'm not sure, please try again")

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The {} skill can't help you with that.  " + help_text ).format(skill_name)
    reprompt = (help_text)
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=skill_name,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

from six import PY2
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()
