import boto3
import boto3
from jinja2 import Template
import json
import re
from datetime import datetime, timedelta

"""
prompt for generating the JSON formated output of Meeting Transcript.
"""

prompt_template = """
I need to summarize a conversation. The transcript of the 
conversation is between the <data> XML like tags.

<data>
{{ content }}
</data>

The summary must contain a one word sentiment analysis, sentiment score value ranging between 0 to 10,
a list of Action items, a list of issues, problems or causes of friction during the conversation.
JSON format shown in the following example. 

Example output:
{
    "sentiment": <sentiment>,
    "sentiment score": <score>,
    "Action item": [<action1>],
    "issues": [
        {
            "topic": <topic>,
            "summary": <issue_summary>,
        },
        {
            "topic": <topic>,
            "summary": <issue_summary>,
        },
        {
            "topic": <topic>,
            "summary": <issue_summary>,
        }
    ],
    

}
Write the JSON output and nothing more.

Here is the JSON output: """



class MeetingSummarizer():
    
    """
    Class for summarizing meeting content and calculating speaking time for each speaker based on file content.

    Attributes:
        bedrock_runtime (boto3.client): Boto3 client for interacting with the Bedrock runtime service.
        s3 (boto3.client): Boto3 client for interacting with Amazon S3.

    Methods:
        __init__(self): Constructor method for initializing the MeetingSummarizer class.
        get_meeting_summary(self, bucket_name: str, file_name: str) -> Json: Retrieves meeting summary and total speaking time.
        parse_file_to_json(self, content: bytes) -> dict: Parses content into JSON format.
        parse_time(self, time_str: str) -> datetime.datetime: Parses time string into datetime object.
        calculate_speaking_time(self, captions: list) -> dict: Calculates total speaking time for each speaker.
    """
    
    def __init__(self):
        
        """
        Constructor method for initializing the MeetingSummarizer class.

        Initializes a boto3 session to interact with AWS services, and sets up clients for Bedrock runtime and Amazon S3.
        """
        
        try:
            # Initialize a boto3 session to interact with AWS services
            session = boto3.Session()
            self.bedrock_runtime = boto3.client("bedrock-runtime")
            self.s3 = boto3.client('s3')
        except Exception as e:
            # Print the exception if the session initialization fails
            print(e)
            
    def get_meeting_summary(self, bucket_name: str, file_name: str):
        
        """
        Retrieves meeting summary and total speaking time.

        Args:
            bucket_name (str): Name of the Amazon S3 bucket containing the file.
            file_name (str): Name of the file stored in the Amazon S3 bucket.

        Returns:
            JSON: A JSON containing the sentiment, sentiment_score, Action items, issues and TimeStamp.
        """
        
        try:
            file = self.s3.get_object(Bucket=bucket_name, Key=file_name)
       
            file_content = file['Body'].read()

            template = Template(prompt_template)
            prompt = template.render(content=file_content)


            kwargs = {
                "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
                "contentType": "application/json",
                "accept": "application/json",
                "body": json.dumps(
                    {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10000, 
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                    }
                )    
            }
            response = self.bedrock_runtime.invoke_model(**kwargs)
            response_body = json.loads(response.get('body').read())
            result = response_body['content'][0]['text']
            
            output = json.loads(result)
            
            file_json = self.parse_file_to_json(file_content)
            total_speaking_time = self.calculate_speaking_time(file_json["captions"])
            
            output['TimeStamp'] = [total_speaking_time]
            
            return output
        
        except Exception as e:
            print(e)
            
       
   
       
    def parse_file_to_json(self, file_content:bytes):
        try:
            
            """
            Parses file content into JSON format.

            Args:
                file_content (bytes): Content of the file in bytes.

            Returns:
                dict: A dictionary representing the parsed file content in JSON format.
            """
            
            
            # Decode bytes content into a string
            file_content_str = file_content.decode('utf-8')

            # Splitting the content into lines for processing
            lines = file_content_str.split('\n')

            # Regex to match the time codes and speaker names
            time_code_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')
            speaker_pattern = re.compile(r'<v ([^>]+)>')

            # List to hold each caption block as a dict
            captions = []

            # Variables to hold the current block's details
            start_time, end_time, speaker, text = None, None, None, ""

            for line in lines[1:]: 
                time_match = time_code_pattern.match(line)
                if time_match:
                    # If there's a previous caption, append it to the list
                    if start_time is not None:
                        captions.append({
                            "start": start_time,
                            "end": end_time,
                            "speaker": speaker,
                            "text": text.strip()
                        })
                        # Resetting the text for the next block
                        text = ""

                    # Updating the time codes for the new block
                    start_time, end_time = time_match.groups()
                else:
                    speaker_match = speaker_pattern.search(line)
                    if speaker_match:
                        speaker = speaker_match.group(1)
                        # Adding the dialogue text, removing the speaker tag
                        text += line[speaker_match.end():].strip() + " "
                    elif line.strip():
                        # Continuation of dialogue without speaker tag
                        text += line.strip() + " "

            # Adding the last caption block if any
            if start_time is not None:
                captions.append({
                    "start": start_time,
                    "end": end_time,
                    "speaker": speaker,
                    "text": text.strip()
                })

            return {"captions": captions}

        except Exception as e:
            print(e)
            
            
            
    def parse_time(self, time_str:str):
        
        """
        Parses time string into datetime object.

        Args:
            time_str (str): Time string in the format 'HH:MM:SS.sss'.

        Returns:
            datetime.datetime: A datetime object representing the parsed time.
        """
        
        try:
            return datetime.strptime(time_str, "%H:%M:%S.%f")
        
        except Exception as e:
            print(e)
            
            

    # Correcting the parsing issue and calculating the total speaking time for each speaker
    def calculate_speaking_time(self, captions):
        try:
            """
            Calculates total speaking time for each speaker.

            Args:
                captions (list): List of caption blocks as dictionaries.

            Returns:
                dict: A dictionary containing total speaking time for each speaker.
            """
            
            speaking_time = {}

            for caption in captions:
                # Correcting the parsing issue with closing tags
                corrected_text = caption["text"].replace("</v>", "").strip()
                start_time = self.parse_time(caption["start"])
                end_time = self.parse_time(caption["end"])
                duration = end_time - start_time


                if caption["speaker"] in speaking_time:
                    speaking_time[caption["speaker"]] += duration
                else:
                    speaking_time[caption["speaker"]] = duration

            # Converting timedelta to a more readable format (e.g., seconds or minutes:seconds)
            for speaker, duration in speaking_time.items():
                speaking_time[speaker] = str(duration)


            return speaking_time

        except Exception as e:
            print(e)

    
            
            
            
            