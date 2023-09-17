import wrappers.league as lol
import wrappers.dynamo as db


def init(command, data):
    if command == 'adduser':
        output = add_user(data)
    elif command == 'deluser':
        output = delete_user(data)
    elif command == 'userlist':
        output = userlist()

    return output


def add_user(data):
    return 'adduser' + str(data)


def delete_user(data):
    return 'deluser' + str(data)


def userlist():
    return 'userlist'
    