import requests
import json
import os, sys

# Step 1: Send a GET request to LinkedIn's authorization endpoint
def getCode(client_id, callback_url, scopes):
    # Construct the URL with the necessary parameters
    auth_url = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': callback_url,
        'state': 'foobar',
        'scope': ' '.join(scopes)  # Join multiple scopes with a space
    }

    try:
        response = requests.get(auth_url, params=params)
        print(response)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Step 2: Parse the authorization code from the redirect URL
            callback_params = response.url.split('?')[1]
            query_params = dict(param.split('=') for param in callback_params.split('&'))
            authorization_code = query_params.get('code')

            if authorization_code:
                print(f"Authorization code: {authorization_code}")
            else:
                print("Authorization code not found in the callback URL.")
        else:
            print(f"Request to LinkedIn's authorization endpoint failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the GET request: {e}")


def getToken(code: str, client_id: str, client_secret: str, callback_url: str)-> str:
# Step 3: Send a POST request to LinkedIn's access token endpoint
    response = requests.post('https://www.linkedin.com/oauth/v2/accessToken',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'authorization_code',
            'code': code,
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
    clientId = '78rfyafkruvy7p'
    redirectUri = 'https://samidhiabx.wixsite.com/easyapplyhub/_functions/linkedincallback' 
    scopes = {'openid', 'profile', 'email'}
    clientSecret = 'loNi9ZU7nofWv4sz'
    code = "AQRtPyGJ5F7dHPzvE5VH23jzyJkcFjy4kHwEm0UoDsI72B6cpgbN2zI2Spm0otzVAgT3ys6Obd1gKhx47Wop2HvXeMiXwh2pDjFtYX5YFEKosMS2gt6n6E1YhDIRdixLo1H-ZiqLWAnBSSOQtA2z2ShCvsXM5XqlkKnMXFNhcES0TThPtnoysq_4k0gCuOB-xt6ZZ5FXJCbiXh9UIyk"
    #token = getToken(code,clientId,clientSecret,redirectUri  )
    token = "AQXwXfVvjlAdkfxFXiT5LwvI7UvuFuhmxs9EQuyRT8KFA5FH_vdSNYVaNG0DRvvOE1O3sdELZW1fE88zwMW_6kooeHdFt-HLVOFyQbmTdrjlpmv4rXXl7X-yXZku-baEAWcx8d_56fF93MquZPtC77ZOcbYCVIlFUqdmvBzy1_EgLJ-vOh-7Tm4OUXF7R0QeyKkLBaCQ3GyIud7YuJ4-k42ewyioNYPU_c0ESGDLMLbtCD5AxpLVn2skXg-2b9dBbmbvmArDZ53pDzT1DERRCclH04gvVrJm-0dYdYmcSlAkJogddEsFxF8THRTHiayHAJi8LGretnBVoarBaXZbDhB00LRCeg"
    testTokenJobSearch(token)
    