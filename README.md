# ec2connect
script for easy ssh connection to aws ec2 instances

Managing ec2 instances with a populated ssh config can be a chore if you have lots of instances without elastic IP's or if your instances come and go with scaling policies.

This python script aims to help that.

First install aws cli & boto and populate your aws cli credentials file.
Then, store your ec2 pem keys in a folder called Keys under your home dir... or change the source to suit

    usage: ec2.py [-h] [-i] [-l] [-u] [-su USER] [-s SSHID]

    optional arguments:
      -h, --help            show this help message and exit
      -i, --internal        use internal ip
      -l, --list            list local db
      -u, --update          update local db
      -su USER, --user USER ec2 system user account
      -s SSHID, --ssh SSHID ssh to provided id

## First Run
    python3 ec2.py

This will create a sqlite file in your home directory populated with the ec2 instances in eu west 1 & us east 1.

## Second Run
    python3 ec2.py
or

    python3 ec2.py -l

Will list all the instances stored in the local sqlite file. It also stores tags, currently: customer, project, env. Change to suit

    001 8.8.8.8     192.168.1.1       customer    project  env  name

## Update
    python3 ec2.py -u

Will empty and repopulate your local sqlite file.

## Connect
    python3 ec2.py -s 1

Will SSH to the machine with an ID of 1, example output above.

## Different User
    python3 ec2.py -s 1 -su ubuntu

The script defaults to using ec2-user as the ec2 user account to use.

## Internal IP
    python3 ec2.py -s 1 -i

Uses the internal IP even if the external IP exists. Script uses internal IP if no external IP exists.

## TOO MUCH TYPING
    alias ec2="/home/user/ec2.py"

Stick an alias in your .bashrc file and mark the script as executable. Then it's as simple as:

    ec2

