# Zoe Bot Functions

- Install - `pip install -r requirements.txt`

  1. [dynamo layer](src/layers/dynamo)
  2. [league layer](src/layers/league)
  3. [main function](src/main)
  4. [register function](src/register)
  5. [task function](src/task)

- Vars - set os env variables

  1. AWS_REGION
  2. DISCORD_PUBLIC_KEY
  3. RIOT_KEY
  4. TOKEN
  5. STAGE

- Test - run unit tests

  1. `coverage run -m unittest -v`
  2. `coverage report`

- Run function in desired function directory - `python3 main.py --local True`

# Backlog

- Testing - test refinement
- Userlist - timeout caused by discord limitation
- Region - explore option to use a drop down &? implementation
- Dynamo - query by puuid key in delete_user
- Dynamo - explore strategies to lower number of dynamo calls &? implementation
