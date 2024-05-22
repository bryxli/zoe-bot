import argparse
import os
import sys

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=bool, default=False)
    args = parser.parse_args()
    local = True
except:
    local = False

if local:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/dynamo/python')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/league/python')))

from dynamo import ZoeBotTable
from league import RiotAPI
    
def get_ZBT():
    return ZoeBotTable

def get_RAPI():
    return RiotAPI