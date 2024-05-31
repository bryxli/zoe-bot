from behave import *

@then('bot sends {output}')
def step_bot_return(context, output):
    pass

@when('setup')
def step_setup(context):
    pass

@when('reset')
def step_reset(context):
    pass

@when('region {region}')
def step_region(context, region):
    pass

@when('acknowledge')
def step_acknowledge(context):
    pass

@when('adduser {gameName}:{tag}')
def step_adduser(context, gameName, tag):
    pass

@when('deluser {gameName}:{tag}')
def step_deluser(context, gameName, tag):
    pass

@when('userlist')
def step_userlist(context):
    pass

@given('help')
def step_help(context):
    pass

@given('speak')
def step_speak(context):
    raise Exception
