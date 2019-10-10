# -*- encoding: utf-8 -*-
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterPager
import time
from elasticsearch import Elasticsearch

my_consumer_key=''
my_consumer_secret=''
my_access_token_key=''
my_access_token_secret=''

es = Elasticsearch()
api = TwitterAPI(consumer_key=my_consumer_key, consumer_secret=my_consumer_secret, access_token_key=my_access_token_key, \
                    access_token_secret=my_access_token_secret)


partis_screen_name = ['SenateDems', 'HouseDemocrats', 'TheDemocrats', 'SenateGOP', 'HouseGOP', 'GOP']
parties_id = [73238146, 43963249, 14377605, 14344823, 15207668, 11134252]

cur_num = 73238146

def check_num():
    current_num = es.count(index='twitter_accounts', body={'query': {'match': {'party_id': cur_num}}})['count']
    print('In twitter accounts, followers for {} is {}'.format(cur_num, current_num))
    if current_num > 5000:
        return False
    return True

def save_to_es(ready_to_store):
    for u in ready_to_store:
        if u['followers_count'] > 200 and u['friends_count'] > 200 and 'status' in u.keys():
            u['party_id'] = cur_num
            u['party_type'] = 'd'
            try:
                es.create(index='twitter_accounts', id=u['id'], body=u)
                print('Save account {}'.format(u['name']))
            except:
                print('This account already exists')

next_cursor = 1640142615147708008
fail_num = 0
while check_num() and fail_num < 50:
    followers = []
    try:
        r = api.request('followers/list', {'user_id': cur_num, 'count': 200, 'cursor': next_cursor})
        if r.status_code==200:
            for fans in r.json()['users']:
                followers.append(fans)
            next_cursor = r.json()['next_cursor']
            print(next_cursor)
            save_to_es(followers)
            fail_num = 0
        else:
            print('Api error')
            fail_num += 1
    except:
        print("Time out")
        fail_num += 1
        continue
    time.sleep(62)

print('Exit')