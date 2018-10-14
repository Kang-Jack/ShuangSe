from fetch_new_lottery_info import saveNewData2DB
import os
from datetime import datetime
from urllib.request import Request, urlopen

NUM = os.environ['num']  # URL of the site to check, stored in the site environment variable

def lambda_handler(event, context):
    print('Fetching lottery at {}...'.format(event['time']))
    try:
        rs = saveNewData2DB(50)
        if (rs < 1):
            raise Exception('Validation failed')
    except:
        print('Fetching failed!')
        raise
    else:
        print('Fetching done!')
        return event['time']
    finally:
        print('Fetching complete at {}'.format(str(datetime.now())))
