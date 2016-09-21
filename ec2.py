#!/usr/bin/python3
import argparse
import boto3
import os.path
import sqlite3
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--internal', action='store_true', default=False, dest='intip', help='use internal ip')
parser.add_argument('-l', '--list', action='store_true', default=False, dest='listtable', help='list local db')
parser.add_argument('-u', '--update', action='store_true', default=False, dest='tableupdate', help='update local db')
parser.add_argument('-su', '--user', default="ec2-user", dest="user", help="ec2 system user account")
parser.add_argument('-s', '--ssh', dest='sshid', help='ssh to provided id', default=0, type=int)
args = parser.parse_args()

#config
databasefile = os.path.expanduser('~')+'/aws.sqlite'
mykeys = os.path.expanduser('~')+'/Keys'
uw1 = boto3.resource('ec2', region_name='us-east-1')
ew1 = boto3.resource('ec2', region_name='eu-west-1')

#CREATE TABLE
createtable = """
CREATE TABLE "ec2" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ,
"instance_id" CHAR NOT NULL UNIQUE , "instance_type" CHAR, "key_name" VARCHAR,
"private_ip_address" CHAR, "public_ip_address" CHAR, "name" VARCHAR,
"customer" VARCHAR, "project" VARCHAR, "env" VARCHAR, "vpc_id" CHAR, "region" CHAR)
"""

def updatetable(dbconnect):
    global uw1, ew1
    cursor = dbconnect.cursor()
    cursor.execute("DELETE FROM ec2")
    dbconnect.commit()
    addinstances = []
    for region in uw1, ew1:
        instances = region.instances.all()
        for i in instances:
            tagname, tagcustomer, tagproject, tagenv = '', '', '', ''
            for tag in i.tags:
                if tag['Key']=='Name':
                    tagname = tag['Value']
                if tag['Key']=='customer':
                    tagcustomer = tag['Value']
                if tag['Key']=='project':
                    tagproject = tag['Value']
                if tag['Key']=='env':
                    tagenv = tag['Value']
            addinstances.append((i.instance_id, i.instance_type, i.key_name, i.private_ip_address, i.public_ip_address, tagname, tagcustomer, tagproject, tagenv, i.vpc_id, i.placement['AvailabilityZone']))
    cursor.executemany("INSERT INTO ec2 (instance_id, instance_type, key_name, private_ip_address, public_ip_address, name, customer, project, env, vpc_id, region) VALUES (?,?,?,?,?,?,?,?,?,?,?)", addinstances)
    dbconnect.commit()
    print('db table updated')

def tablelist(dbconnect):
    cursor = dbconnect.cursor()
    cursor.execute("SELECT * FROM ec2 ORDER BY customer, project, env, name")
    tablelist = cursor.fetchall()
    for singleinstance in tablelist:
        if singleinstance[5] is None:
            extip = '                 '
        else:
            extip = singleinstance[5].ljust(17)
        print('{0:03d}'.format(singleinstance[0]), extip, singleinstance[4].ljust(17), singleinstance[7].ljust(10), singleinstance[8].ljust(21), singleinstance[9].ljust(11), singleinstance[6])

dbconnect = sqlite3.connect(databasefile)

try:
    cursor = dbconnect.cursor()
    cursor.execute(createtable)
    dbconnect.commit()
except:
    print('')
else:
    args.tableupdate = True

if args.tableupdate == True:
    print('updating db table')
    updatetable(dbconnect)

if args.sshid > 0:
    sshsql = "SELECT * from ec2 WHERE id=?"
    cursor.execute(sshsql, [(args.sshid)])
    sshcmdq = cursor.fetchone()
    if sshcmdq is None:
        print('no server found')
    else:
        if args.intip ==True:
            sship = sshcmdq[4]
        elif sshcmdq[5] is None:
            sship = sshcmdq[4]
        else:
            sship = sshcmdq[5]
        cmd = ['/usr/bin/ssh', '-i', mykeys+'/'+sshcmdq[3]+'.pem', args.user+'@'+sship]
        print('running:', ' '.join(cmd))
        subprocess.call(cmd)

if args.tableupdate != True and not args.sshid > 0:
    args.listtable = True

if args.listtable == True:
    tablelist(dbconnect)

