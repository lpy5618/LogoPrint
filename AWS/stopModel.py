#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import time


def stop_model(model_arn):

    client=boto3.client('rekognition',region_name='ap-southeast-2',aws_access_key_id='AKIATDU2AHYM6DIAV4WF',
                        aws_secret_access_key='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')

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Done...')
    
def main():
    
    model_arn='arn:aws:rekognition:ap-southeast-2:213997600281:project/logoPrint/version/logoPrint.2023-06-09T14.43.15/1686285796098'
    stop_model(model_arn)

if __name__ == "__main__":
    main() 