# ec2connect
script for easy ssh connection to aws ec2 instances

Managing ec2 instances with a populated ssh config can be a chore if you have lots of instances without elastic IP's or if your instances come and go with scaling policies.

This python script aims to help that.

First install aws cli & boto and populate your aws cli credentials file.

    usage: ec2.py [-h] [-i] [-l] [-u] [-su USER] [-s SSHID]

    optional arguments:
      -h, --help            show this help message and exit
      -i, --internal        use internal ip
      -l, --list            list local db
      -u, --update          update local db
      -su USER, --user USER ec2 system user account
      -s SSHID, --ssh SSHID ssh to provided id
