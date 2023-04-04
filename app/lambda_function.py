import json
import time
import Constants
import boto3
    
def write_records(current_time,messageBatch,table):
        print("Writing records")

        """guidToUriMapping = {
            "fdd58c5f-199a-47b5-9281-ceb48c1b1a37": "acme:site1:tower2:cell3:HWT:SensorGroup1",
	        "e6d9b7cb-e5f2-4353-9cff-5876638234c9": "acme:site1:tower2:cell3:CWT:SensorGroup1",
            "6a2b2e01-4469-4bc8-a09a-58a6db27d1b9": "acme:site1:tower2:cell3:DBT:SensorGroup1",
	        "ef81b409-9164-410a-bb70-59b1ed70cf8a": "acme:site1:tower2:cell3:RH:SensorGroup1",
	        "484ba2cc-3bff-4ad4-8c96-e0722cb69fee": "acme:site1:tower2:cell3:WBT:SensorGroup1",
	        "b177c4f8-f298-4fc2-bb55-0db478d77150": "acme:site1:tower2:cell3:AmbP:SensorGroup1",
	        "a0c686ad-9242-4398-9574-15751cb666e9": "acme:site1:tower2:cell3:WF:SensorGroup1",
	        "ef81b409-9164-410a-bb70-59b1ed70cf8a": "acme:site1:tower2:cell3:FS:SensorGroup1"
        }"""

        dimensions = [
            {'Name': 'type', 'Value': 'measure','DimensionValueType': 'VARCHAR'}
        ]

        recordsToWrite = []
        for singlePacket in messageBatch:
            print("Message data "+" "+str(singlePacket));
            measuresInThisMessage = list(singlePacket.keys())
            for measure, measureValue in singlePacket.items():
                print(measure, '->', measureValue)
                if (measure=='ts'):
                    sensor_ts=measureValue
                    print('ts ->' + str(sensor_ts))
                else:
                    #uri=guidToUriMapping[measure]
                    #print('uri ->' + uri)
                    sensor_measure = {
                        'Dimensions': dimensions,
                        'MeasureName': measure,
                        'MeasureValue': str(measureValue),
                        'MeasureValueType': 'DOUBLE',
                        'Time': str(sensor_ts),
                        'TimeUnit': 'MILLISECONDS',
                        'Version': 1,
                    }
                    recordsToWrite.append(sensor_measure)
                
        try:
            client = boto3.client('timestream-write')
            response = client.write_records(DatabaseName=Constants.DATABASE,TableName=table,CommonAttributes={},Records=recordsToWrite)
            #print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
        except client.exceptions.RejectedRecordsException as err:
            print("Error:", err)
            for rr in err.response["RejectedRecords"]:
                print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
        except Exception as err:
            print("Error:", err)    
            
        

                
def lambda_handler(event, context):
    # TODO implement
    
    #topicPrint = 'Topic is  {}!'.format(event['topic'])  
    #customerPrint = 'Customer is  {}!'.format(event['customer'])  
    tableNameToWriteTo=event['customer']+"_events"
    print("Topic, customer and table name to write to is  "+" "+str(event['topic']) +"  "+str(event['customer'])+"  "+str(tableNameToWriteTo));
    messagePrint = 'Message is  {}!'.format(event['data'])  
    print (messagePrint)
    for singlePacket in event['data']:
        print("Message data "+" "+str(singlePacket));
        
        
    obj = time.gmtime(0)
    curr_time = round(time.time()*1000)
    print("Milliseconds since epoch:",curr_time)
    write_records(curr_time,event['data'],tableNameToWriteTo)
        
    #print("Message data "+str(idx)+" "+str(singlePacket));
    
    return {
        'statusCode': 200,
        'body': json.dumps('Completed processing message batch!')
    }
