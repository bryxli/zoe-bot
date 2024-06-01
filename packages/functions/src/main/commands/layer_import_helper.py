import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--local", type=bool, default=False)

args = parser.parse_args()

if args.local: # pragma: no cover
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/dynamo/python')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/league/python')))

from dynamo import ZoeBotTable
from league import RiotAPI
    
def get_ZBT():
    return ZoeBotTable

def get_RAPI():
    return RiotAPI