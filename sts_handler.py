import boto3
import logging
## lib needed to interact with the aws console

sts = boto3.client('sts')
## configure aws in cli by running cmd <aws configure>

## create a s3 bucket to upload file into - sample code can be found in aws documentation
def create_bucket(bucket_name, region=None):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except Exception as e:
        # logging.error(e)
        print('Error while creating bucket', e)
        return False
    return True

def delete_bucket(bucket_name, region=None):
    #Delete bucket
    try:
        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
        print(bucket_name + ' deleted from s3')
    except Exception as e:
        # logging.error(e)
        print('Error while deleting s3 bucket', e)

## upload a text file to s3 using current aws key
## './abc.txt'
def upload_s3_default(bucket_name, file_name):
    print('uploading file from s3 bucket, bucketname: ' + bucket_name + '| filename: ' + file_name)
    try:
        s3 = boto3.client('s3')
        response = s3.upload_file(Bucket=bucket_name,Filename='./'+file_name,Key=file_name)
        print(response)
    except Exception as e:
        # logging.error(e)
        print('Error while uploading object to bucket', e)

def download_s3(bucket_name ,file_name, keys=None):
    print('downloading file from s3 bucket, bucketname: ' + bucket_name + '| filename: ' + file_name)
    try:
        if(keys):
            print('using temp credentials')
            s3 = boto3.resource('s3',aws_access_key_id=keys.get('AccessKeyId'),aws_secret_access_key=keys.get('SecretAccessKey'),aws_session_token=keys.get('SessionToken'))
        else:
            print('using environment keys')
            s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            file_body = obj.get()['Body'].read()
            print("File says : ", file_body)
    except Exception as e:
        # logging.error(e)
        print('Error while downloading object from s3 bucket', e)

def get_temp_access():
    try:
        sts = boto3.client('sts')
        response = sts.assume_role(
            RoleArn='arn:aws:iam::231295510145:role/User-S3-Role',
            RoleSessionName='limited_s3_20s',
            PolicyArns=[
                {
                    'arn': 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
                }
            ],
            DurationSeconds=900,
        )
        return response.get('Credentials')
    except Exception as e:
        # logging.error(e)
        print('Error while getting temp credentials', e)
        return None

def util():
    bucket = 'stsbucket123'
    filename = 'abc.txt'
    region = 'us-west-2'
    create_bucket(bucket, region) # name should be unique 
    upload_s3_default(bucket, filename)
    download_s3(bucket, filename)
    # delete_bucket(bucket, region)
    download_s3(bucket, filename, get_temp_access())

util()
