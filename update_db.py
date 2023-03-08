import psycopg2

print("Connecting to Database.")
conn = psycopg2.connect(
                    host = "localhost",
                    database = "twotter_db",
                    user = "user",
                    password = "password")
print("SUCCESS! Connected to Database.")

cur = conn.cursor()
update_cur = cur


update_tweet_table = """
        ALTER Table Tweets
        ALTER COLUMN DateOfTweet TYPE TIMESTAMPTZ;
        """

print("Trying to update table.")
update_cur.execute(update_tweet_table)
update_cur.execute("commit")
print("Update complete.")
