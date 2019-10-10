# Twitter-Text-Mining
A text mining project. In this project, I call Twiiter Development API and get 1w5 Democracy Accounts and 1w5 Republic Accounts.

## Columns
- id: Twitter Identify ID
- party_type:
    - d: Demorcracy
    - r: Republic
- name: User name
- screen_name: Another user name for menion and search
- location: The user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable. This field will occasionally be fuzzily interpreted by the Search service
- description: The user defined string describing their account
- protected: 
    - True: This user decides to protect his/her tweets
    - False: Everyone can view this user's tweets
- Verified:
    - True: This is a verified user, usually famous person or big orgnization
    - False: Normal user
- Entities:
    - True: Including other links, like facebook and personal website
    - False: No other information besides description
- status_count: The number of Tweets (including retweets) issued by the user
- follower_count: The number of followers this account currently has
- friends_count: The number of users this account is following currently
- favorites_count: The number of Tweets this user has liked in the account’s lifetime
- geo_enabled (deprecated): New account in Twitter must set this attribute True
    - True: This user's location infomation is shared with Twitter
    - False: Not allow to get user location
- has_extended_profile (deprecated): New account in Twitter must set this attribute NULL

## Data Collecting Strategy

All the users are collected from 6 famous twitter account: SenateDems, HouseDemocrats, TheDemocrats, SenateGOP, HouseGOP and GOP, 3 for Democracy and 3 for Republic. The strategy to get users only following one party is quite tricky. Twiiter free developer account is only allowed to send request to check following list 1 time/min, so check all the users are unrealistic. 

Steps:
1. Get user lists from Democracy first, then insert them into ElasticSearch (database), mark them Demo set id unique. Right now, in the database, users may follow both D and R.

2. Then I get user lists from Republic, then insert them into ElasticSearch. Because I set id unique, if an account from Republic also follows Democarcy, it can’t insert since it has already in the database and marked Democracy. According to this, I get a pure Republic party user list. 

3.	We can get pure democracy list by the same way.

## Accounts Sampling Strategy

We want to make sure every account in our dataset is an **active** user. **Active** means this user likes to share his/her opinion on Twitter frequently. The strategy to filter them out is quite intuitive:

For each account I got from Twitter, I measure them by 2 threshhold:

1. The ```follower_count``` and ```friends_count``` should both above 200
2. Since I can get the tweets this account posted in 7 days, I will drop users didn't post anything in recent 7 days 