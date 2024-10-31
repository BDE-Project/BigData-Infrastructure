# BigData-Infrastructure
Designing a scalable Big Data infrastructure using the Lambda architecture to handle data from sources such as Reddit APIs.

# Reddit Data Pipeline

## Overview

The **Reddit Data Pipeline** is a comprehensive solution for collecting, processing, and analyzing data from Reddit using AWS services. This project leverages multiple scripts to handle data ingestion, processing, and storage, ensuring that information is readily available for analysis.

### Key Components

1. **Data Collection**:
   - **`reddit_batch_processing.py`**: 
     - Fetches posts from the `learnpython` subreddit.
     - Collects relevant post data and stores it in a CSV file.
     - Uploads the CSV file to an AWS S3 bucket.
     - Streams selected post data to an AWS Kinesis stream for further processing.

2. **Kinesis Data Streaming**:
   - **`reddit_kinesis_1.py`**: 
     - Collects Reddit data and sends it to an AWS Kinesis stream for real-time processing.

3. **Data Processing**:
   - **`kinesis_processing_2.py`**: 
     - Processes data from the Kinesis stream.
     - Executes SQL queries using AWS Athena to clean and aggregate data, storing results back in S3.

4. **Data Querying with AWS Lambda**:
   - **`reddit_lambda.py`**: 
     - Executes Athena queries to process and retrieve data from the `tbl_reddit_processed` table.
     - Stores the results in a designated S3 bucket for later use.

5. **DynamoDB Processing**:
   - **`dynamodb_processing.py`**: 
     - Loads and processes data from a DynamoDB table, applying transformations as needed.

6. **Secrets Management**:
   - **Secrets Manager**: Retrieves Reddit and AWS credentials securely, preventing hardcoding sensitive information in the scripts.

### Requirements

- Python 3.x
- AWS account with Kinesis, S3, and DynamoDB setup
- Reddit API credentials
- Required Python packages:
  - `praw`
  - `boto3`
  - `pandas`
  - `numpy`
  - `textblob`
  - `pyspark`
  - `python-dotenv`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BDE-Project/BigData-Infrastructure.git
   cd reddit-data-pipeline

### Usage


Data Processing
Important: Both reddit_kinesis_1.py and kinesis_processing_2.py must always run together. If you update either script, ensure you run them together to maintain the integrity of data processing.
