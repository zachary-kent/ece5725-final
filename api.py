import requests

URL = 'https://ece5725.herokuapp.com/'

# Attempts to create a new user with the specified user name and password
# Returns whether the creation of the account was successful
def create_account(username, password):
    data = { 'username': username, 'password': password }
    resp = requests.get(f'{URL}/register', data=data)
    return resp.status_code == requests.codes.ok

# An error raised when invalid credentials are entered
class InvalidCredentialsError(Exception):
   pass

# Represents a user of 2048
class User:

  # Attempt to login with the provided credentials.
  # Raises `InvalidCredentialsError` if they are invalid
  def __init__(self, username, password):
    data = { 'username': username, 'password': password }
    resp = requests.post(f'{URL}/login', data=data)
    if resp.status_code != requests.codes.ok:
       raise InvalidCredentialsError
    self.token = resp.json()['token']

  # Get the high score of this user
  def high_score(self):
     headers = { 'x-access-token': self.token }
     resp = requests.get(f'{URL}/high-score', headers=headers)
     if resp.status_code != requests.codes.ok:
       raise InvalidCredentialsError
     return resp.json()['score']

  # Sets the high score of this user. Does nothing if the provided score
  # is less than or equal to their current high score.
  def set_high_score(self, score):
     headers = headers = { 'x-access-token': self.token }
     data = { 'score': score }
     resp = requests.post(f'{URL}/high-score', data=data, headers=headers)
     if resp.status_code != requests.codes.ok:
       raise InvalidCredentialsError
