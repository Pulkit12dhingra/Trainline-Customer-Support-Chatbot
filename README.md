# Trainline-Customer-Support-Chatbot

(**Note**:- I was not able to deploy this project to any open source free platforms thus I request you to view this video explaining about the structure and approach that I took to develop this project.
<a href="https://youtu.be/Sm01LUBx0rg" target="_blank" rel="noopener noreferrer">Watch the video description of this project on YouTube</a>)


This projct is built on the FAQ data of a TrainLine Application that allows the users to book affordable train tickets.

In case the user face any issue, they have to go thorugh the FAQ documents that can sometimes be tricky. This chatbot helps the user to clarify thier issue without stuck in google searches and going through extensive documentations.

## Project Data
The data has been extracted using selenium Python from official Trainline FAQ pages.
1. The code goes though the the main FAQ page and extracts all the useful links (100+)
2. Once the useful URLs are acquired, the console goes through all these urls and performs the below operations
   - Click Accept Cookies to remove the initial cookie pop-up
   - Removes javascript to expand all the dropdown "+", thus making sure all the content is visible
   - Goes into the div class "tab-content-layer.current" and extracts all the text information
   - Saves the content in a Txt file

Data Files
Content.txt :- Contains the extracted content
intents.json :- Contain intents for normal conversations that were not present in the extracted content
train_Data.json :- Contains a refined version of Content.txt.

## RAG Pipeline
Following the data Extraction, we are using Ollama, Langchains to build a RAG pipeline over the extracted data
- I used `tinyllama` model from ollama, It is a liteweight model and would be enough for our personal project usecase.
- Used FAISS vectorstore using Langchain

## Frontend
-  The front end is build on Streamlit

Thank You !!
