#!/usr/bin/python3
import getopt, sys

argument_list = sys.argv[1:]
short_options = "cduw"
long_options = ["create", "delete", "update", "website"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    command = arguments[0][0]
except getopt.error as err:
    print (str(err))
    sys.exit(2)

###############################################################################
import boto3

PROJECT = "gm-website-1"
S3_BUCKET_NAME = f'{PROJECT}-111'
PARAMETERS = [{'ParameterKey': 'S3Bucket','ParameterValue': S3_BUCKET_NAME}]

cf = boto3.client('cloudformation')
s3 = boto3.client('s3')

with open('template.yaml', 'r') as file:
    template = file.read()

if command in ("--create", "-c"):

    create_stack_response = cf.create_stack(
        StackName=PROJECT,
        TemplateBody=template,
        Parameters=PARAMETERS
    )
    print(create_stack_response)

elif command in ("--website", "-w"):

    s3.upload_file('index.html', S3_BUCKET_NAME, 'index.html')

elif command in ("--update", "-u"):

    update_stack_response = cf.update_stack(
        StackName=PROJECT,
        TemplateBody=template,
        Parameters=PARAMETERS
    )
    print(update_stack_response)

elif command in ("--delete", "-d"):
    
    bucket = boto3.resource('s3').Bucket(S3_BUCKET_NAME)
    bucket.objects.all().delete()

    delete_stack_response = cf.delete_stack(
        StackName=PROJECT
    )
    print(delete_stack_response)
