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

All the users are collected from 6 famous twitter account: SenateDems, HouseDemocrats, TheDemocrats, SenateGOP, HouseGOP and GOP, 3 for Democracy and 3 for Republic. We call the API, then Twitter will give us a list of followers randomly. However, Twiiter free developer account is only allowed to send request to check following list 1 time/min, so check all the users are unrealistic. The strategy to get users only following one party is quite tricky.

Steps:
1. Get user lists from Democracy first, then insert them into ElasticSearch (database), mark them Demo set id unique. Right now, in the database, users may follow both D and R.

2. Then I get user lists from Republic, then insert them into ElasticSearch. Because I set id unique, if an account from Republic also follows Democarcy, it can’t insert since it has already in the database and marked Democracy. According to this, I get a pure Republic party user list. 

3.	We can get pure democracy list by the same way.

## Accounts Sampling Strategy

We want to make sure every account in our dataset is an **active** user. **Active** means this user likes to share his/her opinion on Twitter frequently. The strategy to filter them out is quite intuitive:

For each account I got from Twitter, I measure them by 2 threshhold:

1. The ```follower_count``` and ```friends_count``` should both above 200
2. Since I can get the tweets this account posted in 7 days, I will drop users didn't post anything in recent 7 days 

## Most Frequent Words
Get top 100 frequent words from Democracy and Republic following's description.

Steps:

1. Extract description from dataframe.
2. Remove rows without description.
3. Remove punctuation and stopwords.
4. Stemming, so my program is able to deal with words like 'apple' and 'apples', regard them are the same word 'apple'.
5. Remove words only show once and ```len(words) < 4```.
6. Form corpora.
7. Count. 

## Apply TFIDF to Get Top 100 Weighted Keywords
I apply TFIDF model on this dataset then extract top 100 weighted keywords. Here are the steps.

Steps:

1. Throw our corpra into Gensim's TFIDF Model.
2. Go through every description.
3. Pickup top 3 weighted words in each description.
4. Count words picked up.
5. Rank them.

## Apply LIWC on Tweets
We bought LIWC 30 days license and run test. Here are the data cleasing things and some preprocessing before the data going to LIWC. Codes are in the script **arrange_tweets.ipynb**.

Steps:

1. Get recent 50 tweets of every user, then extract the attribute "full_textt" (Tweets textual content) from each tweet, put it into a txt file named **{user_id}_{tweet_id}.txt**, for example: **4216101_1090396584704126977.txt**, 4216101 is the user_id, 1090396584704126977 is the tweet_id. I will put the id into result file later, so you can combine them with description quickly.
2. Since LIWC will help us do the text cleasing, we don't need to do anything, just feed the original texts into LIWC.
3. Run LIWC, assign the directory name to LIWC, LIWC will check each txt file and count words.


