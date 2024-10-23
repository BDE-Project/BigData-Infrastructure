import praw
import boto3
import os
import json
from datetime import datetime

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent = '')

# Fetch top 20000 posts from a subreddit
subreddit = reddit.subreddit('learnpython')
for post in subreddit.hot(limit=20000):
    print(post.title)

# Check Boto3 version
#print(boto3.__version__)


# Set your AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''
os.environ['AWS_DEFAULT_REGION'] = 'eu-north-1'  

# Reddit API setup
reddit = praw.Reddit( client_id='',
                     client_secret='',
                     user_agent = '')

# Kinesis setup
kinesis = boto3.client('kinesis', region_name='eu-north-1')

# Stream Reddit data to Kinesis
subreddit = reddit.subreddit('learnpython')
for post in subreddit.hot(limit=10):
    data = {
        'title': post.title,
        'score': post.score,
        'url': post.url,
        'comments': post.num_comments
    }
    kinesis.put_record(
        StreamName='reddit-stream',
        Data=json.dumps(data),
        PartitionKey='partition_key'
    )


# Kinesis setup
kinesis = boto3.client('kinesis', region_name='eu-north-1')

# Get the stream description
response = kinesis.describe_stream(StreamName='reddit-stream')

# Print the Shard ID
shards = response['StreamDescription']['Shards']
for shard in shards:
    print(f"Shard ID: {shard['ShardId']}")

    
# Initialize S3 client
s3 = boto3.client('s3')

# Define the S3 bucket and file name
bucket_name = 'reddit-batch-data'
filename = f"reddit_batch.csv"

# Gather data from Reddit (similar to what you did for streaming)
subreddit_data = []
for post in subreddit.hot(limit=100):
    data = {
        'title': post.title,
        'score': post.score,
        'url': post.url,
        'comments': post.num_comments
    }
    subreddit_data.append(data)

# Save the data to a local file
with open(filename, 'w') as f:
    json.dump(subreddit_data, f)

# Upload the file to S3
s3.upload_file(filename, bucket_name, filename)

print(f"Uploaded {filename} to S3 bucket {bucket_name}")
