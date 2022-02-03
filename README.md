# Cloudfront_add_ranges_security_group_auto_lambda
Add Cloudfront IP ranges in a specific group using a Lambdafunction called by a SNS subscription as soon as AWS change ranges.

This script creates rules in a security group which contains subnet/ips for CloudFront Global and Edge locations.
Change variables as you need.
If a rule exist the creation of that will be skipped.
By default you can create up to 60 rules in a security group, if you need more than 60 rules in a security group request to AWS to increase a number of rules tha you can create in a security groups, I recomend 200 rules per security group.
To invoke this function manualy use aws cli:

    aws lambda invoke --function-name  sg-add-manual-cloudfront-global-edge-ips-rule-lambda output.json

Lambda function definitions:
    Runtime: Python 3.9.
    Handler: lambda_function.lambda_handler.
    Architecture: x86_64.
    Timeout: 5 minutes (at least).
    Permission: Role wich have permission lo list and write in EC2, S3 and Cloudwatch services.

You can use the Cloud Formation template to create the function or create it manualy.
Cloud Formation uses a bucket to create a Lambda function, change teh template as you need.
The function requeres a python file named as lambda_function.py, this file have to be in the zip file in teh bucket.

To automate add new IPs/ranges in security group, you must create a SNS subscription to AWS notification service AmazonIpSpaceChanged, use AWS cli:

    aws sns subscribe --topic-arn arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged --protocol lambda --notification-endpoint "put your lambda arn here"

When ip changes happened in AWS services it will be updated in security group "security_group_id".
