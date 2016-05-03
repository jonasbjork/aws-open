#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This script will add your current IP address to your security group in AWS VPC (port 22, ssh)
# In VPCs you can't use the security group name as reference, you must use the security group id
# like: "sg-01234567". Also, this script uses the ~/.aws/credentials file for AWS credentials.
#
# Setup:
#   You need "boto" and "urllib2" packages in Python to run this. "pip install boto" will probably do.
#
#   secgroup = "" set the security group ID
#   aws_profile = "" set the aws profile name you want to use (from your ~/.aws/credentials)
#   aws_region = "eu-west-1" set the AWS region you want to use
#
# Author:
#   Jonas Björk <jonas.bjork@gmail.com>
#   Written on the 3rd of may 2016 in room number 1023 at Radisson Blu Waterfront Hotel, Stockholm, Sweden
#
from boto import ec2
from urllib2 import urlopen

secgroup = ""   # We need the VPC id here, as groupname is not supported for VPC SGs
aws_profile = ""  # The profile name in ~/.aws/credentials file
aws_region = "eu-west-1"  # The AWS region

addIP = True  # Default, add IP (if found in Security Group we won't add IP)
currentIp = urlopen("https://api.ipify.org").read().strip() + "/32"  # Our current IP
ec2conn = ec2.connect_to_region(aws_region, profile_name=aws_profile)

sg = ec2conn.get_all_security_groups(group_ids=secgroup)

print "Current IP: %s" % currentIp
print "==================================="
for rule in sg[0].rules:
    if str(rule.from_port) == '22':
        for r in rule.grants:
            if str(r) == currentIp:
                print "IP: %s (Current IP)" % str(r).rjust(18, ' ')
                addIP = False
            else:
                print "IP: " + str(r).rjust(18, ' ')
print "==================================="
if addIP is True:
    ec2conn.authorize_security_group(group_id=secgroup,
                                            ip_protocol='tcp',
                                            from_port=22,
                                            to_port=22,
                                            cidr_ip=currentIp)
    print "Added IP: %s" % currentIp
else:
    print "IP %s already allowed." % currentIp
