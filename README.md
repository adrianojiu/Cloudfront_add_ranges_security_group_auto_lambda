# Cloudfront_add_ranges_security_group_auto_lambda
Add Cloudfront IP ranges in a specific group using a Lambda function called by a SNS subscription as soon as AWS change ranges.

This script creates rules in a security group which contains subnet/ips for CloudFront Global and Edge locations.
Change variables as you need.
If a rule exist the creation of that will be skipped.
By default you can create up to 60 rules in a security group, if you need more than 60 rules in a security group request to AWS to increase a number of rules tha you can create in a security groups, I recomend 200 rules per security group.
To invoke this function manualy use aws cli:

    aws lambda invoke --function-name PUT_YOUR_LAMBDA_FUNCTION_NAME_HERE output.json

Lambda function definitions:
    Runtime: Python 3.9.
    Handler: lambda_function.lambda_handler.
    Architecture: x86_64.
    Timeout: 5 minutes (at least).
    Permission: Role wich have permission lo list and write in EC2, S3 and Cloudwatch services.

You can use the Cloud Formation template to create the function or create it manualy.
Cloud Formation uses a bucket to create a Lambda function, change teh template as you need.
The function requeres a python file named as lambda_function.py, this file have to be in the zip file in teh bucket.
File "sg_lambda.zip" it´s an example how you have to put in your bucket.

To automate add new IPs/ranges in security group, you must create a SNS subscription to AWS notification service AmazonIpSpaceChanged, use AWS cli:

    aws sns subscribe --topic-arn arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged --protocol lambda --notification-endpoint "put your lambda arn here"

When ip changes happened in AWS services it will be updated in security group "security_group_id".

Files description:

"cloudformation_create_lambda_function.json"
It is a Cloud formatio template wich creates a lambda function, you can create lambda function manualy instead.

"iam_policy_role_sample.json"
It is a example of policy to allow lambda function create rules.

"sg-cloudfront-global-edge-ips-rule-lambda.py"
It is a code called by lambda function wich createssecurity group rules.

"sg_lambda.zip"
It is an example of file used by Cloud formation to create alambda function, you must save the python script as "lambda_function.py" and put into a zip file, and refer this zip file in the Cloud formation template.

The flow to put it on work is:

Create IAM role --> Create Lambda function --> Create SNS subscription.

Caution: Use a dedicated security group for that, all rules are removed and recreated when lambda funtion is called.
