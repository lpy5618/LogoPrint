import boto3

def start_model(project_arn, model_arn, version_name, min_inference_units):

    client=boto3.client('rekognition',region_name='ap-southeast-2',aws_access_key_id='AKIAZ7RYVZQ3NNQFXGC5',
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
    project_arn='arn:aws:rekognition:ap-southeast-2:181647024244:project/logoPrint/1686716167375'
    model_arn='arn:aws:rekognition:ap-southeast-2:181647024244:project/logoPrint/version/logoPrint.2023-06-14T16.31.18/1686724280558'
    min_inference_units=1 
    version_name='logoPrint.2023-06-14T16.31.18'
    start_model(project_arn, model_arn, version_name, min_inference_units)

if __name__ == "__main__":
    main()