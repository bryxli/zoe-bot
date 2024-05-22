import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--local", type=bool, default=False)

args = parser.parse_args()

def get_local_status():
    return args.local