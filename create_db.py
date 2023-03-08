
import psycopg2

print("Connecting to Database.")
conn = psycopg2.connect(
                    host = "localhost",
                    database = "twotter_db",
                    user = "dan",
                    password = "Woodland7!")
print("SUCCESS! Connected to Database.")

cur = conn.cursor()
create_cur = cur

create_user_table = """
    CREATE Table Users (
        UserID serial,
        name varchar(255) NOT NULL,
        handle varchar(255),
        following int,
        followers int,
        PRIMARY KEY (UserID)
    );
"""
#pictures?!
create_tweet_table = """
    CREATE Table Tweets (
        TweetID serial,
        UserId int REFERENCES Users(UserID),
        DateOfTweet TIMESTAMPTZ,
        Content varchar(255),
        PRIMARY KEY (TweetID)
    );
"""
print("Dropping Tables.")
create_cur.execute("drop table Users, Tweets;")
create_cur.execute(create_user_table)
create_cur.execute(create_tweet_table)

try:
    results = create_cur.fetchall()
    for r in results:
        print(r)
except:
    print("No results to fetch!")

print(create_cur.execute("commit"))

print("Closing connection.")
conn.close()
