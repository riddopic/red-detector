import subprocess
import argparse
import sys
import threading
import datetime
import boto3
begin_time = datetime.datetime.now()


class Scan(threading.Thread):
    def __init__(self, instance_region, instance_id, instance_keypair, instance_log_level):
        threading.Thread.__init__(self)
        self.region = instance_region
        self.id = instance_id
        self.keypair = instance_keypair
        self.log_level = instance_log_level

    def run(self):
        """
        running the main with "one instance at a time" (in threads of course)
        """
        command = "python3 main.py --region {region} --instance-id {id} --keypair {keypair} --log-level {loglevel}". \
            format(region=self.region, id=self.id, keypair=self.keypair, loglevel=self.log_level)
        command = command.split(" ")  # the command should be in this format in order to get live output
        with open('test.log', 'wb') as f:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE)
            for c in iter(lambda: process.stdout.readline(1), b''):
                # sys.stdout.write(" [ From: " + self.instance_id + " ]" + str(c))
                pass


"""
ec2 = boto3.resource('ec2')
lst_of_account_instances = []  # this lst will contain all of the running instances ids. for scanning later
for instance in ec2.instances.all():
    if str(instance.state["Code"]) == "16":  # getting just the running instances
        lst_of_account_instances.append(instance.id)
"""


parser = argparse.ArgumentParser()
parser.add_argument('--region', action='store', dest='region', type=str,
                    help='region name', required=False)
parser.add_argument('--instance-id', action='store', dest='instance_id', type=str,
                    help='EC2 instance id', required=False)
parser.add_argument('--keypair', action='store', dest='keypair', type=str,
                    help='existing key pair name', required=False)
parser.add_argument('--log-level', action='store', dest='log_level', type=str,
                    help='log level', required=False, default="INFO")
region = "us-east-2"
source_volume_id = "id"
keypair = "red_detector_key3"
log_level = "INFO"

cmd_args = parser.parse_args()
if cmd_args.region:
    region = cmd_args.region
if cmd_args.instance_id:
    source_volume_id = cmd_args.instance_id
if cmd_args.keypair:
    keypair = cmd_args.keypair
if cmd_args.log_level:
    log_level = cmd_args.log_level

lst_of_ids = source_volume_id.split("_")  # need to provide the ids with a _ between them.
print(lst_of_ids)
threads = []
for instance_id in lst_of_ids:
    instance_scan = Scan(region, instance_id, keypair, log_level)
    instance_scan.start()
    threads.append(instance_scan)

for x in threads:
    x.join() # wait for all of the threads to end.

print(datetime.datetime.now() - begin_time)