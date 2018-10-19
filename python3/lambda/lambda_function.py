from fetch_new_lottery_info import saveNewData2DB
import os
from datetime import datetime
from urllib.request import Request, urlopen
import cuckoo

NUM = os.environ['num']  # URL of the site to check, stored in the site environment variable

def lambda_handler(event, context):
    print('Fetching lottery at {}...'.format(event['time']))
    try:
        rs = saveNewData2DB(50)
        if (rs == [] ):
            cuckoo.handler({'resources':['error_reminder']}, 'context')
            raise Exception('Validation failed')
        else:
            cuckoo.handler({'resources':['records_updated']},rs)
            print('Fetching done!')
            return event['time']
    except:
        print('Fetching failed!')
        raise
    finally:
        print('Fetching complete at {}'.format(str(datetime.now())))
