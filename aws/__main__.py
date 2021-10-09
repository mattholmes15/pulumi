"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('m1r5h-pulumi-bucket',
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
    )
)

bucketObject = aws.s3.BucketObject(
    'index.html',
    acl='public-read',
    content_type='text/html',
    bucket=bucket,
    source=pulumi.FileAsset('index.html')
)

size = 't2.micro'
ami = aws.get_ami(most_recent="true",
                  owners=["amazon"],
                  filters=[{"name":"name","values":["amzn-ami-hvm-*"]}]
                  )

group = aws.ec2.SecurityGroup('webserver.secgrp',
    description='Enable HTTP access',
    ingress=[
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']}
    ])

server = aws.ec2.Instance('webserver-m1r5h',
    instance_type=size,
    vpc_security_group_ids=[group.id],
    ami=ami.id)


# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))
pulumi.export('publicIp', server.public_ip)
pulumi.export('publicHostName', server.public_dns)