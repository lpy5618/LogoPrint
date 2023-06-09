#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def start_model(project_arn, model_arn, version_name, min_inference_units):

    client=boto3.client('rekognition',region_name='ap-southeast-2',aws_access_key_id='AKIATDU2AHYM6DIAV4WF',
    aws_secret_access_key='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')

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Done...')
    
def main():
    project_arn='arn:aws:rekognition:ap-southeast-2:213997600281:project/logoPrint/1686210245429'
    model_arn='arn:aws:rekognition:ap-southeast-2:213997600281:project/logoPrint/version/logoPrint.2023-06-09T14.43.15/1686285796098'
    min_inference_units=1 
    version_name='logoPrint.2023-06-09T14.43.15'
    start_model(project_arn, model_arn, version_name, min_inference_units)

if __name__ == "__main__":
    main()