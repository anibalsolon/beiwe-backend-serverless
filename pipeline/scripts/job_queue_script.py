import json
from time import sleep

import boto3


def run(comp_env_role, instance_profile, comp_env_name, queue_name, job_defn_name, repo_uri):
    # Create a new IAM role for the compute environment
    with open('assume-batch-role.json') as fn:
        assume_batch_role_policy_json = json.dumps(json.load(fn))
    with open('batch-service-role.json') as fn:
        batch_service_role_policy_json = json.dumps(json.load(fn))
    with open('assume-ec2-role.json') as fn:
        assume_ec2_role_policy_json = json.dumps(json.load(fn))
    with open('batch-instance-role.json') as fn:
        batch_instance_role_policy_json = json.dumps(json.load(fn))
    with open('compute-environment.json') as fn:
        compute_environment_dict = json.load(fn)
    with open('container-props.json') as fn:
        container_props_dict = json.load(fn)
    print('JSON loaded')
    
    iam_client = boto3.client('iam')
    resp = iam_client.create_role(
        RoleName=comp_env_role,
        AssumeRolePolicyDocument=assume_batch_role_policy_json,
    )
    comp_env_role_arn = resp['Role']['Arn']
    iam_client.put_role_policy(
        RoleName=comp_env_role,
        PolicyName='aws-batch-service-policy',  # This name isn't used anywhere else
        PolicyDocument=batch_service_role_policy_json,
    )
    print('Batch role created')
    
    iam_client.create_role(
        RoleName=instance_profile,
        AssumeRolePolicyDocument=assume_ec2_role_policy_json,
    )
    iam_client.put_role_policy(
        RoleName=instance_profile,
        PolicyName='aws-batch-instance-policy',  # This name isn't used anywhere else
        PolicyDocument=batch_instance_role_policy_json,
    )
    resp = iam_client.create_instance_profile(
        InstanceProfileName=instance_profile,
    )
    instance_profile_arn = resp['InstanceProfile']['Arn']
    compute_environment_dict['instanceRole'] = instance_profile_arn
    iam_client.add_role_to_instance_profile(
        InstanceProfileName=instance_profile,
        RoleName=instance_profile,
    )
    print('Instance profile created')
    
    # Create the batch compute environment
    batch_client = boto3.client('batch')
    batch_client.create_compute_environment(
        computeEnvironmentName=comp_env_name,
        type='MANAGED',
        computeResources=compute_environment_dict,
        serviceRole=comp_env_role_arn,
    )
    
    # Wait for the compute environment to be valid. If it is deemed invalid, exit
    print('Waiting for compute environment...')
    while True:
        resp = batch_client.describe_compute_environments(
            computeEnvironments=[comp_env_name],
        )
        status = resp['computeEnvironments'][0]['status']
        if status == 'VALID':
            break
        elif status == 'CREATING' or status == 'UPDATING':
            sleep(1)
            continue
        else:
            raise RuntimeError('Compute Environment is Invalid')
    print('Compute environment created')
    
    # Create the batch job queue
    batch_client.create_job_queue(
        jobQueueName=queue_name,
        priority=1,
        computeEnvironmentOrder=[{'order': 0, 'computeEnvironment': comp_env_name}],
    )
    print('Job queue created')
    
    # Define a job definition
    container_props_dict['image'] = repo_uri
    batch_client.register_job_definition(
        jobDefinitionName=job_defn_name,
        type='container',
        containerProperties=container_props_dict,
    )
    print('Job definition created')
