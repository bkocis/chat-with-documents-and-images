---
# CLI chat with documents / images `ollama`'s models

## Chat with private documents using llamaindex and ollama on local computer 

-> `chat-with-documents.py`

#### Description 
This is a small application utilizing ollama, that enables a Q-A chat with private documents on local computer. The code is 
modified from the original post by [llamaindex](https://blog.llamaindex.ai/running-mixtral-8x7-locally-with-llamaindex-e6cebeabe0ab) 
The main difference is to chat loop, for simplicity of the application.

```python
    # main CLI interaction loop
    while True:
        query_message = input("Q: ")
        response = query_engine.query(query_message)
        response.print_response_stream()
        sys.stdout.flush()
        sys.stdout.write("\n")
```

#### Getting started

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


## Vision Models - Image understanding

-> `image-understanding-llava.py`

Ollama supports LLaVA (Large Language-and-Vision Assistant) model version 1.6! 

#### Download model

By running: 

`ollama run llava:34b` or `llava:13b` or `llava:7b`

References on llava: 
- [ollama vision models](https://ollama.ai/blog/vision-models)
- [llava version 1.6 release notes](https://llava-vl.github.io/blog/2024-01-30-llava-1-6/)

#### Chat / ask more about the image

Conversational chat loop allows to load new images and ask new questions about it:

```python 
    while True:
        query_message = input(f"Type a command, or a question to image {image_list}:")
        if query_message.lower() == 'quit':
            break
        if query_message.startswith("/load"):
            new_image = query_message.split("/load")[1].strip()
            image_list = [new_image]
            query_message = input("Ask anything about the image: ")
            print_out_the_response(query_message, image_list)
        if image_list == []:
            print("Give an image path after writing /load :\n")
        if query_message == '':
            print("Ask another question:")
        if query_message != '' and image_list != []:
            print_out_the_response(query_message, image_list)
```

For example: 
![](https://ollama.ai/public/blog/jmb.jpg)

```
$ python image-understanding-llava.py

Type /load <image_path> to load an image, and 'quit' to exit.
Type a command, or a question to image []:**/load** /home/snow/Downloads/llava1p6_test.jpg
Ask anything about the image: what do you see in the image?
 The image shows a graffiti artwork featuring a stylized black dinosaur with a crown on its head. Below the dinosaur, there is text that reads "JEAN-MICHEL BASQUIAT" and "ASYCON." The artwork has a vibrant and colorful style, typical of street art or graffiti. It appears to be done in chalk or paint on what seems to be a wall or a board. 

 The image shows a piece of wall art featuring a black silhouette of an animal, likely a wolf or a similar canid, with a crown on its head. Above the animal, there is text that reads "Jean-Michel Basquiat" and below it, another line of text says "Any Icon." The artwork has a stylized appearance with bold outlines and minimal detailing, suggesting it could be a reference to Jean-Michel Basquiat's work or an homage to him as an icon. The background is plain, which emphasizes the artwork itself. 

Type a command, or a question to image ['/home/snow/Downloads/llava1p6_test.jpg']:**Who is the author of this artwork?**
 Jean-Michel Basquiat 

Type a command, or a question to image ['/home/snow/Downloads/llava1p6_test.jpg']:**Can you give a short bio of the artist?**
 The image shows a piece of street art featuring a colorful character with the text "Jean-Michel Basquiat" and "Ayon." This suggests that the artwork is likely inspired by Jean-Michel Basquiat, a prolific Haitian-American artist who was active during the late 20th century. He is considered one of the most important figures in modern art and is known for his bold, colorful, and often symbolic paintings that explore themes of race, identity, and social commentary. The text "Ayon" may refer to a pseudonym or an artistic project associated with Basquiat's work. 

Type a command, or a question to image ['/home/snow/Downloads/llava1p6_test.jpg']:


```

The `/load` phrase allows to loop to parse a new filename on your local computer, pointing to the image. This will be then 
added to the `images` list, that `ollama.chat` needs to apply the model.

