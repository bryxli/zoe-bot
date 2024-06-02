# Zoe Bot Functions

- Install - `pip install -r requirements.txt`

  1. [dynamo layer](src/layers/dynamo)
  2. [league layer](src/layers/league)
  3. [main function](src/main)
  4. [register function](src/register)
  5. [task function](src/task)

To run tests, `pip install` in this directory

- Unit tests - run unittest

  1. `coverage run -m unittest`
  2. `coverage report --show-missing`

- Acceptance tests - run behave

  1. `behave`

- Run function in desired function directory - `python3 main.py --local True`

# Backlog

- Acceptance test refinement - adduser, deluser
- Acceptance test implementation - userlist
- Userlist - timeout caused by discord limitation
- Region - explore option to use a drop down &? implementation
- Dynamo - query by puuid key in delete_user
- Dynamo - explore strategies to lower number of dynamo calls &? implementation
