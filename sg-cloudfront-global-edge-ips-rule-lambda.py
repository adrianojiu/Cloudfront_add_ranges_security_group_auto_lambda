from itertools import count
from urllib.request import urlopen
import json
import boto3

'''
This script creates rules in a security group which contains subnet/ips for CloudFront Global and Edge locations.
Change variables as you need, the most important to be changed are the variables in lines just below.
If a rule exist the creation of that will be skipped.
By default you can create up to 60 rules in a security group, if you need more than 60 rules in a security group request to AWS to increase a number of rules tha you can create in a security groups.
To invoke this function manualy use aws cli:

aws lambda invoke --function-name  sg-add-manual-cloudfront-global-edge-ips-rule-lambda output.json

Lambda function definitions:
    Runtime: Python 3.9.
    Handler: lambda_function.lambda_handler.
    Architecture: x86_64.
    Timeout: 5 minutes (at least).
    Permission: Role wich have permission lo list and write in EC2, S3 and Cloudwatch services.

To automate add new IPs/ranges in security group, you must create a SNS subscription to AWS notification service AmazonIpSpaceChanged, use AWS cli:

    aws sns subscribe --topic-arn arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged --protocol lambda --notification-endpoint "put your lambda arn here"

When ip changes happened in AWS services it will be updated in security group "security_group_id".

'''
security_group_id = "sg-01010101010101010"  # Set Security Group ID
port_range_start = 80                       # Set port range to be opened.
port_range_end = 80                         # Set port range to be opened.
protocol = "tcp"                            # Set rule protocol.
url_cf_ip = "https://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips"        # Cloudfront ips url api.
description_all = "CloudFrontRange"

response = urlopen(url_cf_ip)                                           # Getting IPs in AWS api.
data_json = json.loads(response.read())                                 # Storing the JSON response from url in data.

data_json_ip_edg = data_json['CLOUDFRONT_REGIONAL_EDGE_IP_LIST']        # Getting cloudfront edge ips.
data_json_ip_glo = data_json['CLOUDFRONT_GLOBAL_IP_LIST']               # Getting cloudfront global ips.
data_json_ip_append = data_json_ip_edg + data_json_ip_glo               # Put ips together.

client = boto3.Session().resource('ec2')
security_group = client.SecurityGroup(security_group_id)

#
def lambda_handler(event, context):
    
    # Remove all rules. 
    security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)

    # Add rules cloudfront global and edge ranges.
    for ip_i_all in data_json_ip_append: 

        try:
            # Creating rule for each IP in the list.
            security_group.authorize_ingress(
            DryRun=False,
            IpPermissions=[
                    {
                        'FromPort': port_range_start,
                        'ToPort': port_range_end,
                        'IpProtocol': protocol,
                        'IpRanges': [
                            {
                                'CidrIp': ip_i_all,
                                'Description': description_all
                            },
                        ]
                    }
                ]
            )
        except Exception as error:
            error_strig = str(error)
            print(error_strig)
