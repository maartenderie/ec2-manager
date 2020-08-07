import boto3
region = 'eu-central-1'
instances = ['i-0429dce048b91b898']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    description = ec2.describe_instances(InstanceIds=instances)
    instance = description['Reservations'][0]['Instances'][0]
    
    if 80 is instance['State']['Code'] :
        print( "Starting EC2 instance..")
        rsp = ec2.start_instances(InstanceIds=instances)
        description = ec2.describe_instances(InstanceIds=instances)
        instance = description['Reservations'][0]['Instances'][0]
    else:
        print( "Already running!", instance)
        
    return {
        "Lekker spelen!" : "true",
        "ip" : instance['PublicIpAddress'],
        "InstanceType" : instance['InstanceType'],
        "state" : instance['State']
    }
