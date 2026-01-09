import boto3

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"Instance Type: {instance['InstanceType']}")

            # Get Name tag
            name = None
            if "Tags" in instance:
                for tag in instance["Tags"]:
                    if tag["Key"] == "Name":
                        name = tag["Value"]

            print(f"Instance Name: {name}")
            print("-------------------------------------")

if __name__ == "__main__":
    list_ec2_instances()
