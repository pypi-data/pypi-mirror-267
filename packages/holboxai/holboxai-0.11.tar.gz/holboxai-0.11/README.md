# HolboxAI Package
Welcome to HolboxAI, a comprehensive AI package designed to enhance your data processing and creative capabilities. HolboxAI offers a range of functionalities including text-to-image generation, running textual queries on documents stored in your S3 bucket, and generating insights from natural language queries. This README provides a detailed guide on how to install and use the various features of HolboxAI.

### **Installation**

To get started with HolboxAI, you need to install the package. Run the following command in your terminal:
```sh
pip install holboxai
```

After installation, you can import HolboxAI into your project using:
```sh
import holboxai as hb
```
## Features
### 1. RAG 
To run textual queries on your S3 bucket documents, follow these steps:
Load Documents from S3 Bucket:
First, import the S3DocReader class and initialize it. Then, call the get_bucket() method and provide the name of your S3 bucket as its argument.
```sh
## To Select the documents from entire s3 bucket
reader = hb.S3DocReader()
documents = reader.get_docs(bucket="<bucket_name>")

## To select a specific document
doc_file = reader.get_file(bucket="<bucket_name>",file_name="file_name")
```
- **Index Documents and Generate Response:**

    Next, import the DocsQuery class. Use createindexes() to index the documents and query() to generate the response for your prompted query.
    ```sh
    docsQuery = hb.DocsQuery()
    indexes = docsQuery.create_index(documents)
    query = " "  # Your query here
    response = docsQuery.query(indexes, query)
    ```
- **Validate Sources:**

    To validate the sources that generated the response of your query, import RelevantDocs and call get_docs(). This will show all the documents from which the response is created.
    ```sh
    rel_docs = hb.RelevantDocs()
    docs = rel_docs.get_docs(query=query, n_docs=4, retriever=indexes)
    ```

### 2. Generating Insights from CSV Files
This feature will help User to get insight from .csv file using natural language.

- For insight on single csv file
    ```sh
    import pandas as pd

    csv_insight = hb.CsvQuery()
    query = "your query"
    df = pd.read_csv("<csv_file_path>")
    response = csv_insight.single_csv_query(df , query)
    print(response)
    ```
- For insight on multiple csv files
    ```sh
    import pandas as pd

    csv_insight = hb.CsvQuery()
    query = "your query"
    df1 = pd.read_csv("<csv_file1_path>")
    df2 = pd.read_csv("<csv_file2_path>")
    dfs = [df1,df2]
    response = csv_insight.multi_csv_query(dfs , query)
    print(response)
    ```

### 3. Generating Images from Text Prompts
To generate images based on your text prompts, use the text2image module. The generate_image() method's arguments include your desired prompt, guidance scale, and inference steps.


```sh
txt2img = hb.text2image()
prompt = "a sports car, on a racing track,4K" # Change the prompt according to requirement
txt2img.generate_image(prompt=prompt,cfg_scale=5, infernce_steps=25) 
```

- **cfg_scale** = Guidance scale is a parameter that controls how much the image generation 
            process follows the text prompt. The higher the value, the more the image
            sticks to a given text input and vice-versa. It ranges from (1-20)
             
- **inference_steps** = Inference steps controls how many steps will be taken during this process. 
                  The higher the value, the more steps that are taken to produce the image.
                  It ranges from (5-100) 


### 4. Getting Summary of the documents from S3 bucket
This feature will summarize the selected document from the s3 bucket for user.
```sh
reader = hb.S3DocReader()
docs = reader.get_file(bucket_name="<Bucket Name>",file_name = "<File Name>")
doc_summary = hb.Summarizer()
summary = doc_summary.summarize(docs)
print(summary)
```

### 5. Getting Sentiment of a text/sentence
This feature will help user to get the sentiment of the text/sentence
(Positive/Negative).

Supported Foundation models
1. Anthropic  Claude
2. Amazon Titan
3. Cohere (Default)
```sh
sa = hb.SentimentAnalysis()
response = sa.get_sentiment(text="<text>")
print(response)
```

```sh

sa = hb.SentimentAnalysis()
response = sa.get_sentiment( text="<text>", model="Amazon Titan")
print(response)
```
### 6. Getting name and entity from a text/sentence
This feature will help user to extract important keywords (Name,place) from the given sentence.

Supported Foundation models
1. Anthropic  Claude
2. Amazon Titan
3. Cohere (Default)
```sh

ner = hb.NameEntityRecognition()
response = ner.get_entity(text="<text>")
print(response)
```

```sh

ner = hb.NameEntityRecognition()
response = ner.get_entity(text="<text>", model = "Anthropic Claude")
print(response)
```
### 7. Meeting Summarizer
This feature will allow user to get things like sentiment, sentiment score, Action Items, summary of each topic discussed and the total time, each individual had spoken in the meeting.
Supported File Format: vtt and txt.
The structure of the content inside the file must be mantained, refer demo meeting_summary.txt file in demoFiles folder. 
```sh
ms = MeetingSummarizer()
response = ms.get_meeting_summary("<bucket_name>", "<file_name>")
print(response)
```
## Conclusion
HolboxAI is designed to simplify complex AI functionalities and make them accessible for various applications. Whether you're querying documents, generating creative images, or seeking insights from data, HolboxAI provides the tools you need. Enjoy exploring the capabilities of HolboxAI in your projects!
