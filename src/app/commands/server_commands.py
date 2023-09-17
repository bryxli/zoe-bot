import dynamo as db


def init(command, data):
    if command == 'setup':
        output = init_guild()
    elif command == 'reset':
        output = delete_guild()
    elif command == 'region':
        output = change_region(data)

    return output


def init_guild():
    return 'setup'


def delete_guild():
    return 'reset'


def change_region(data):
    return 'region' + str(data)
    