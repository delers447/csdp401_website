import tweepy, psycopg2

bearer = 'CHANGE_ME'
client = tweepy.Client(bearer_token=bearer)

query = '#100DaysOfCode -is:retweet lang:en -has:media'

conn = psycopg2.connect(
                    host = "localhost",
                    database = "twotter_db",
                    user = "user",
                    password = "password")
cursor = conn.cursor()

tweets = client.search_recent_tweets(query=query,
                            tweet_fields=['created_at', 'lang', 'author_id'],
                            user_fields=['profile_image_url'],
                            expansions='author_id', max_results=100)
#source: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
print(tweets)

#users = {u["id"]: u for u in tweets.includes['users']}
counter = 0
for tweet, user in zip(tweets.data,tweets.includes['users']):
    print('-'*10 + 'NEW TWEET' + '-'*10)
    print(f"User: @{user}")
    print(f"Time: {tweet.created_at}")
    print(f"Tweet: \n{tweet.text}")

    text = tweet.text
    username = user
    time =  tweet.created_at

    check_user = f"""SELECT userid from users where name='{str(username).replace("'","")}'"""
    cursor.execute(check_user)
    results = cursor.fetchall()
    #print(f"===> Checking If User Exists ===> Results: {results}")
    if len(results) == 0:
        #print(f"/t---USER DOESN't EXIST---")
        user_insert = f"""INSERT INTO users (name, handle, following, followers)
                        VALUES ('{str(username).replace("'","")}', '{str(username).replace("'","")}', '{0}', '{0}')
                        RETURNING UserID"""
                        #(UserID, name, handle, follwing, follows)"
        cursor.execute(user_insert)
        user_id = cursor.fetchall()[0][0]
    else:
        #print(f" /t ---USER DOES EXIST---")
        user_id = results[0][0]
        #print(f"UserID: {user_id}")
    tweet_insert = f"""INSERT INTO tweets (UserID, DateOfTweet, Content)
                        VALUES ({user_id},'{str(time)}', '{str(text).replace("'", "")}')
                        RETURNING tweetid"""
    #print(user_insert)
    #print(tweet_insert)
    cursor.execute(tweet_insert)
    tweet_id = cursor.fetchall()[0][0]
    cursor.execute("commit")
    print('-'*10 + 'NEW TWEET' + '-'*10)
    print(f"date: {str(time)}")
    print(f"from:{username} [{user_id}, {tweet_id}] at {time}") #2022-08-18
    print(text)

print("Program Completed")
