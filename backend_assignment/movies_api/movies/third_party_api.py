from rest_framework import status
import requests

from movies_api.serializers import ThirdPartyApiSerializer


class ThirdPartyApi:
    """Used by ThirdPartyApiWrapper to create requests to Third Party API"""
    URL ='https://demo.credy.in/api/v1/maya/movies/'
    # Basic Auth
    AUTH_USERNAME = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
    AUTH_PASSWORD = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

    _get_params=''
    # Requested URL = url + get_params

    def __init__(self, get_params):
        self._get_params = get_params

    def fetch_json(self):
        response =  requests.get(
            '{}?{}'.format(self.URL, self._get_params), 
            auth=requests.auth.HTTPBasicAuth(
                self.AUTH_USERNAME, 
                self.AUTH_PASSWORD
            )
        )
        self.status_code = response.status_code
        return response.json()


class ThirdPartyApiWrapper:
    """
    Returns deserialized data from Third Party API.

    Ex:   home_url = 127.0.0.1:8000/?page=2
          requested_url = third_party_url + get_params(home_url)
          requested_url = www.thirdpartyurl.com/?page=2
          
    The JSON data returned by Third Party API has links which point to it,
    (Ex: Next page link), these links must be changed so that it points 
    to our API.
    
    Ex:  Next page link = www.thirdpartyurl.com/?page=3
         Changed link   = 127.0.0.1:8000/?page=3
    """
    def __init__(self, home_url):
        self._home_url = home_url
        self._get_params = self._extract_get_params_from_url(home_url)

    def get_serialized_data(self):
        """
        Fetch JSON from Third Party API, deserialize it and Change links.
        Return deserialized data.
        """
        tpa = ThirdPartyApi(self._get_params)
        json_response = tpa.fetch_json()
        if tpa.status_code != status.HTTP_200_OK:
            raise Exception('Third Party API fetch error')

        serializer = ThirdPartyApiSerializer(data=json_response)

        if not serializer.is_valid():
            raise Exception('Third Party API serialization error')

        serialized_data = serializer.validated_data.copy()
        self._change_page_links(serialized_data)
        return serialized_data

    def _change_page_links(self, serialized_data):
        next_page = self._build_home_url(serialized_data['next'])
        previous_page = self._build_home_url(serialized_data['previous'])

        serialized_data['next'] = next_page
        serialized_data['previous'] = previous_page

    def _extract_get_params_from_url(self, url):
        url_split = url.split('?')
        if len(url_split) == 2:
            return url_split[1]
        return ''

    def _build_home_url(self, third_party_url):
        # Replace Home URL's get params with Third Party URL's get params.
        # Return the new Home URL.
        if third_party_url is None:
            # Previous link is null on first page and Next link will be 
            # null on last page.
            return None
        
        return '{url}?{params}'.format(url=self._home_url.split('?')[0], 
                params=self._extract_get_params_from_url(third_party_url))
