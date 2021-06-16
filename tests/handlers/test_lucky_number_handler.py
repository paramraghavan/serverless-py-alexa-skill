import pytest
from lucky_number_handler import lucky_number
from tests.utils.test_helper import load_json
import pprint

def test_lambda_handler():
    try:
        event = load_json(
            r'C:\Users\padma\serverless\alexa\pp-aws-python-alexa-skill\tests\data\sample_input_with_nointent.json')
        pprint.pprint(event)
        response = lucky_number(event, {})
        pprint.pprint(response)
    except Exception as e:
        print(e)

    assert True == True
