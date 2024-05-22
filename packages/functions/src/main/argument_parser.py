import argparse

def get_local_status():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--local", type=bool, default=False)
        parser.parse_args()
        return True
    except:
        return False