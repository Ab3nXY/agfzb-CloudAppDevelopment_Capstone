import requests
import json
from .models import CarDealer, DealerReview, CarModel, CarMake
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
 

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#

def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        # If any error occurs
        print("Network exception occurred:", str(e))
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = response.json()  # Use .json() to parse JSON directly
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)

    if json_result:
        # Print the JSON data for debugging
        print("JSON Data:", json_result)

        dealers = json_result

        for dealer in dealers:
            # Print the keys of a dealer object for debugging
            print("Dealer Keys:", dealer.keys())

            dealer_obj = CarDealer(
                address=dealer.get("address", ""),
                city=dealer.get("city", ""),
                id=dealer.get("id", ""),
                lat=dealer.get("lat", ""),
                long=dealer.get("long", ""),
                st=dealer.get("st", ""),
                zip=dealer.get("zip", ""),
                full_name=dealer.get("full_name", ""),
                short_name=dealer.get("short_name", ""),
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)

    if json_result:
        reviews = json_result

        for dealer_review_data in reviews:
            print("Dealer Review Data:", dealer_review_data)
            review_obj = DealerReview(
                dealership=dealer_review_data["dealership"],
                name=dealer_review_data["name"],
                purchase=dealer_review_data["purchase"],
                review=dealer_review_data["review"],
                purchase_date=dealer_review_data.get("purchase_date", None),
                car_make=dealer_review_data.get("car_make", ""),
                car_model=dealer_review_data.get("car_model", ""),
                car_year=dealer_review_data.get("car_year", None),
                sentiment=dealer_review_data.get("sentiment", "")
            )
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)

    if json_result:
        dealers = json_result
        
    
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/1abb3d6a-8aef-4f81-a4e2-6dfc56e4c755"
    api_key = "gAtNJWFCsBbCRijGTPe9aY0BKB-umH-q0lm1ntbCFDuF"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']


