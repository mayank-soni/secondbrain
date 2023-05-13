# Second Brain
or at least the first few neurons of one

## Description
This project implements semantic search over a vector database, consisting of embedded Telegram chats as well as any weblinks from the chats. It also implements a LLM contextual search over the semantic search results. 

## Visuals

## Installation
Run 'pip install .' from the base folder of the repo. 

Make sure you have an OPENAI_API_KEY set as an environment variable. 
This is used for summarising long websites when creating a new database with links. 
It is also used for embedding each query text. 

## Usage
See notebooks/langchain.ipynb for an example of creating a new vector database and adding information to it, as well as running an end-to-end query. 

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Authors and acknowledgment
Mayank Soni

--
Initial protoype done together as part of AI Singapore AIAP Mini-project
Tan Yan Liong
Marvin Ng
Benjamin Phang

## License
No license
