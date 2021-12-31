import json

from utils import APIHelper

# Constants
REGISTERING_ENDPOINT = "register"

MODELS_ENDPOINT = "api/models"

PREDICTION_ENDPOINT_SENTIMENT = "api/predict/sentiment"

PREDICTION_ENDPOINT_STROKE = "api/predict/stroke"


#######################
#  Authentication     #
######################


def should_be_authenticated(helper, credentials):
    result = helper.makeRequest(endpoint=MODELS_ENDPOINT, credentials=credentials)
    assert result['status'] == 200, 'Authentication should succeed'


def should_not_be_authenticated(helper, credentials):
    expected = {"status": "401", "message": "Unauthorized"}
    result = helper.makeRequest(endpoint=MODELS_ENDPOINT, credentials=credentials, expected=expected)
    assert result['status'] == 401, 'Authentication should failed'


def test_authentication(helper: APIHelper, credentials):
    # Should be authenticated
    credentials_ = (credentials["access_key"], credentials["secret_access_key"])
    should_be_authenticated(helper, credentials_)

    # Should not be authenticated
    credentials_ = (credentials["access_key_unauthorized"], credentials["secret_access_key_unauthorized"])
    should_not_be_authenticated(helper, credentials_)


#######################
#  Registering       #
######################

def should_be_able_to_register(helper):
    expected = {"status": "201", "message": "Created"}
    body = {
        "username": "azerty",
        "password": "Azerty09",
    }
    # Convert into json
    body = json.dumps(body)
    result = helper.makeRequest(endpoint=REGISTERING_ENDPOINT, method="POST", body=body, expected=expected)
    assert result['status'] == 201, 'Should be able to register'


def should_not_be_able_to_register(helper, existing_username):
    # Weak password
    expected = {"status": "400", "message": "Password must be ?"}
    body = {
        "username": "qsdrtyuy",
        "password": "pass",  # Weak password
    }
    # Convert into json
    body = json.dumps(body)
    result = helper.makeRequest(endpoint=REGISTERING_ENDPOINT, method="POST", body=body, expected=expected)
    assert result['status'] == 400, 'Weak password'

    # Weak username
    expected = {"status": "400", "message": "Username/Login must be at least ? characters"}
    body = {
        "username": "pass",  # Weak username
        "password": "Azertyu09Wq",
    }
    body = json.dumps(body)
    result = helper.makeRequest(endpoint=REGISTERING_ENDPOINT, method="POST", body=body, expected=expected)
    assert result['status'] == 400, 'Weak username'

    # Use a login that already exist
    expected = {"status": "400", "message": "Username not available!"}
    body = {
        "username": existing_username,
        "password": "Azertyu09Wq",
    }
    body = json.dumps(body)
    result = helper.makeRequest(endpoint=REGISTERING_ENDPOINT, method="POST", body=body, expected=expected)
    assert result['status'] == 400, 'Should not register with existing username'


def test_registering(helper: APIHelper, credentials):
    # Should be register
    should_be_able_to_register(helper)

    # Should not be register
    credentials_ = (credentials["access_key"], credentials["secret_access_key"])
    should_not_be_able_to_register(helper, credentials_[0])


#######################
#  Models             #
######################

def should_list_models(helper, credentials):
    result = helper.makeRequest(endpoint=MODELS_ENDPOINT, credentials=credentials)
    assert result['status'] == 200, 'Models should be retrieved'


def should_get_model(helper, version, credentials):
    endpoint = MODELS_ENDPOINT + "/" + version
    result = helper.makeRequest(endpoint=endpoint, credentials=credentials)
    assert result['status'] == 200, f'Model {version} should be retrieved'


def test_models(helper: APIHelper, credentials):
    credentials_ = (credentials["access_key"], credentials["secret_access_key"])

    # Should list models
    should_list_models(helper, credentials_)

    # Should get model(s)  by version
    should_get_model(helper, "V1", credentials_)
    should_get_model(helper, "V2", credentials_)
    should_get_model(helper, "V3", credentials_)


################################
#  Prediction Sentiment        #
###############################

def should_predict_rating(helper: APIHelper, model_version, credentials, text, expected_rating):
    data = {
        "version": model_version,
        "text": text
    }

    data = json.dumps(data)
    result = helper.makeRequest(endpoint=PREDICTION_ENDPOINT_SENTIMENT, method="PUT", credentials=credentials,
                                body=data)
    assert result['status'] == 200, 'Should predicate'
    content = json.loads(result['content'])
    rating = content['rating']
    assert rating == expected_rating, f'Expect rating {expected_rating}, but found {rating}'


def test_sentiment_prediction(helper: APIHelper, credentials):
    credentials_ = (credentials["access_key"], credentials["secret_access_key"])

    text = "It was amazing place with many things to do"
    should_predict_rating(helper, "V1", credentials_, text, 5)
    should_predict_rating(helper, "V2", credentials_, text, 5)
    should_predict_rating(helper, "V3", credentials_, text, 5)

    text = "I didn't like it and I don't recommended it at all, it was horrible"
    should_predict_rating(helper, "V1", credentials_, text, 1)
    should_predict_rating(helper, "V2", credentials_, text, 1)
    should_predict_rating(helper, "V3", credentials_, text, 1)


################################
#  Prediction Stroke          #
###############################
def should_predict_stroke(helper: APIHelper, data, credentials, model_id, expected_stroke):
    data = json.dumps(data)
    result = helper.makeRequest(endpoint=PREDICTION_ENDPOINT_STROKE, method="PUT", credentials=credentials,
                                body=data)
    assert result['status'] == 200, 'Should predicate'
    content = json.loads(result['content'])
    prediction = content['prediction']
    assert prediction == expected_stroke, f'Expect Stroke {expected_stroke}, but found {prediction}. For Model {model_id}'


def test_stroke_prediction(helper: APIHelper, credentials):
    credentials_ = (credentials["access_key"], credentials["secret_access_key"])
    prediction_request = {
        "observation": {
            "gender": "Male",
            "age": 67.0,
            "hypertension": "0",
            "heart_disease": "0",
            "Residence_type": "Urban",
            "avg_glucose_level": 228.69,
            "bmi": 36.6,
            "smoking_status": "smokes"
        },
        "id": -1
    }
    # FIXME To improve by doing stuff dynamically from type: Stroke and Version
    for model_id in [4, 5, 6]:
        prediction_request["id"] = model_id
        should_predict_stroke(helper, data=prediction_request, credentials=credentials_, model_id=model_id,
                              expected_stroke="Stroke Attack: YES")
