---
Run LLM-s on local with ollama and query private documents with llamaindex
==========================================================================

## Description 
This is a small application utilizing ollama, that enables a Q-A chat with private documents on local computer. The code is 
modified from the original post by [llamaindex](https://blog.llamaindex.ai/running-mixtral-8x7-locally-with-llamaindex-e6cebeabe0ab)  

## Getting started

Installation of the main application `ollama` (from [ollama download](https://ollama.ai/download)) via a curl command: 
`curl https://ollama.ai/install.sh | sh`

After the framework application is downloaded to your local, the LLM models can be set with:

`ollama run mixtral` 

This will initalize the language model, load the libraries and prepare it for chatting.  
The application will not free up resources (GPU) after closing any client that interacts with the LLM model. To stop or restart the 'ollama` application 
use systemctl commands:  

`sudo systemctl status ollama`

`sudo systemctl stop/start ollama`


A small write-up can be found in my [medium article](https://medium.com/@balazskocsis/chatting-with-your-documents-in-the-cli-with-ollama-and-llamaindex-13481903f7ef).


