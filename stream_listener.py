
import tweepy, psycopg2

#for account @delers447
consumer_key = 'ASK MR RICE FOR THIS STRING'
consumer_secret = 'ASK MR RICE FOR THIS STRING'
access_token = 'ASK MR RICE FOR THIS STRING'
access_token_secret = 'ASK MR RICE FOR THIS STRING'

filters = ["#100DaysOfCode", "#100daysofcode", "python", "Python",
            "SQL", "sql", "Java", "java", "coding", "Coding",
            "JavaScript", "Java Script", "JS", "React", "GitHub", "CSS"]

#filters = ["..."]

class My_listener(tweepy.Stream):
    def on_status(self, status):
        self.conn = psycopg2.connect(
                            host = "localhost",
                            database = "twotter_db",
                            user = "dan",
                            password = "Woodland7!")
        self.cursor = self.conn.cursor()

        if status.text.find("RT") == -1 and status.lang=='en':# and status.in_reply_to_status_id:

            check_user = f"""SELECT userid from users where name='{str(status.user.name).replace("'","")}'"""
            self.cursor.execute(check_user)
            results = self.cursor.fetchall()
            #print(f"===> Checking If User Exists ===> Results: {results}")
            if len(results) == 0:
                #print(f"/t---USER DOESN't EXIST---")
                user_insert = f"""INSERT INTO users (name, handle, following, followers)
                                VALUES ('{str(status.user.name).replace("'","")}', '{str(status.user.screen_name).replace("'","")}', '{status.user.friends_count}', '{status.user.followers_count}')
                                RETURNING UserID"""
                                #(UserID, name, handle, follwing, follows)"
                self.cursor.execute(user_insert)
                user_id = self.cursor.fetchall()[0][0]
            else:
                #print(f" /t ---USER DOES EXIST---")
                user_id = results[0][0]

            #print(f"UserID: {user_id}")
            tweet_insert = f"""INSERT INTO tweets (UserID, DateOfTweet, Content)
                                VALUES ({user_id},'{str(status.created_at)}', '{str(status.text).replace("'", "")}')
                                RETURNING tweetid"""
            #print(user_insert)
            #print(tweet_insert)

            self.cursor.execute(tweet_insert)
            tweet_id = self.cursor.fetchall()[0][0]
            self.cursor.execute("commit")

            print('-'*10 + 'NEW TWEET' + '-'*10)
            print(f"date: {str(status.created_at)}")
            print(f"from:{status.user.screen_name} [{user_id}, {tweet_id}] at {status.created_at}") #2022-08-18
            print(status.text)

            #print("----> What was stored?")
            #sql_get_query = f""" select content from tweets where tweetid={tweet_id}"""
            #self.cursor.execute(sql_get_query)
            #print(self.cursor.fetchall())

        else:
            print(".")

print("Trying to connect to Twitter API.")
listener =My_listener(consumer_key, consumer_secret, access_token, access_token_secret)

listener.filter(track=filters)
