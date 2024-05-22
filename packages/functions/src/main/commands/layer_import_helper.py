import os
import sys

from argument_parser import get_local_status

if get_local_status():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/dynamo/python')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../layers/league/python')))

from dynamo import ZoeBotTable
from league import RiotAPI
    
def get_ZBT():
    return ZoeBotTable

def get_RAPI():
    return RiotAPI