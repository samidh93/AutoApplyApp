import requests
import json
import os, sys
from dotenv import load_dotenv, find_dotenv

# Step 1: Send a GET request to LinkedIn's authorization endpoint
def getCode():
    response = requests.get('https://www.linkedin.com/oauth/v2/authorization',
        params={
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': callback_url,
            'state': 'foobar',
            'scope': 'r_liteprofile r_emailaddress w_member_social'
        }
    )
    print(response.json())
    # Step 2: Parse the authorization code from the redirect URL
    authorization_code = callback_url.split('=')[1]

def getToken(authorization_code: str, client_id: str, client_secret: str, callback_url: str)-> str:
# Step 3: Send a POST request to LinkedIn's access token endpoint
    response = requests.post('https://www.linkedin.com/oauth/v2/accessToken',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': callback_url
        }
    )
    print(response.json())
    return response.json()['access_token']

def testToken(token: str):
    # Step 4: Send a GET request to LinkedIn's API with the access token
    response = requests.get('https://api.linkedin.com/v2/me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    print(response.json())

def testTokenJobSearch(token: str):
    # Set the access token
    access_token = token
    # Set the API endpoint
    endpoint = 'https://api.linkedin.com/v2/job-search'
    # Set the parameters for the API call
    params = {
        'q': 'data scientist',  # The search query
        'companyName': 'Google',  # The company name filter
        'location': 'United States',  # The location filter
        'jobTitle': 'Engineer',  # The job title filter
        'sort': 'DD',  # The sort order ('DD' for date posted descending)
        'count': 10,  # The number of results to return
        'start': 0,  # The index of the first result to return
    }
    # Set the headers for the API call
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    # Make the API call
    response = requests.get(endpoint, headers=headers, params=params)
    # Print the response
    print(response.json())

if __name__ == '__main__':
    load_dotenv(find_dotenv())

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    callback_url= os.getenv("OAUTH2_REDIRECT_URL")
    access_token = os.getenv("ACCESS_TOKEN")
    authorization_code = os.getenv("authorization_code")
    print(client_id)
    #access_token = os.getenv("ACCESS_TOKEN")
    #token = getToken(authorization_code, client_id, client_secret, callback_url)
    #testToken(access_token)
    testTokenJobSearch(access_token)