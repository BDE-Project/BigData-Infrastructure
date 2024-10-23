import praw
import boto3
import os
import json
from datetime import datetime
from botocore.exceptions import NoCredentialsError

def get_secret():
    secret_name = "redddit-user-secret" 
    region_name = "eu-north-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret
    except Exception as e:
        print(f"Error retrieving secret: {e}")
    return None


# Fetch the secrets
secrets = get_secret()
if not secrets:
    raise NoCredentialsError("Could not load secrets")

# Set up Reddit API using secrets
reddit = praw.Reddit(client_id=secrets['reddit_client_id'],
                     client_secret=secrets['reddit_client_secret'],
                     user_agent=secrets['reddit_user_agent'])

# Check Boto3 version
#print(boto3.__version__)


# Set up AWS environment variables
os.environ['AWS_ACCESS_KEY_ID'] = secrets['aws_access_key_id']
os.environ['AWS_SECRET_ACCESS_KEY'] = secrets['aws_secret_access_key']
os.environ['AWS_DEFAULT_REGION'] = secrets['aws_default_region']


# Fetch top 20000 posts from a subreddit
subreddit = reddit.subreddit('learnpython')
for post in subreddit.hot(limit=20000):
    print(post.title)

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

# Kinesis: Get stream description and print Shard IDs
response = kinesis.describe_stream(StreamName='reddit-stream')
shards = response['StreamDescription']['Shards']
for shard in shards:
    print(f"Shard ID: {shard['ShardId']}")

    
# Initialize S3 client and upload data
#s3 = boto3.client('s3')
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
#s3.upload_file(filename, bucket_name, filename)

print(f"Uploaded {filename} to S3 bucket {bucket_name}")
