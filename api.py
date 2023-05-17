import requests

URL = 'https://ece5725.herokuapp.com'

# Attempts to create a new user with the specified user name and password
# Returns whether the creation of the account was successful


def create_account(username, password):
    body = {'username': username, 'password': password}
    resp = requests.post(f'{URL}/register', json=body)
    return resp.status_code == requests.codes.ok

# An error raised when invalid credentials are entered


class InvalidCredentialsError(Exception):
    pass

# Represents a user of 2048


class User:

    # Attempt to login with the provided credentials.
    # Raises `InvalidCredentialsError` if they are invalid
    def __init__(self, username, password):
        body = {'username': username, 'password': password}
        resp = requests.post(f'{URL}/login', json=body)
        if resp.status_code != requests.codes.ok:
            raise InvalidCredentialsError
        self.token = resp.json()['token']

    # Get the high score of this user
    def high_score(self):
        headers = {'x-access-token': self.token}
        resp = requests.get(f'{URL}/high-score', headers=headers)
        if resp.status_code != requests.codes.ok:
            raise InvalidCredentialsError
        return resp.json()['score']

    # Sets the high score of this user. Does nothing if the provided score
    # is less than or equal to their current high score.
    def set_high_score(self, score):
        headers = headers = {'x-access-token': self.token}
        body = {'score': score}
        resp = requests.post(f'{URL}/high-score', json=body, headers=headers)
        if resp.status_code != requests.codes.ok:
            raise InvalidCredentialsError

# All high scores, associated with the corresponding user, listed in descending order
# Returns at most limit results, if provided
# Example result: [{ 'username': 'zak', 'score': 3}, { 'username': 'nadia', 'score': 2}]


def all_high_scores(limit=None):
   route_url = f'{URL}/high-score/rankings'
   if limit is None:
      resp = requests.get(route_url)
   else:
      params = { 'limit': str(limit) }
      resp = requests.get(route_url, params=params)
   return resp.json()['scores'] if resp.status_code == requests.codes.ok else []
