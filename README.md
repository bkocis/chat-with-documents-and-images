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
        query_message = input("Q: ")
        if query_message.startswith("/load"):
            new_image = query_message.split("/load")[1].strip()
            image_list = [new_image]
            query_message = input("Ask anything about the image: ")
            print_out_the_response(query_message, image_list)
        if image_list == [] or query_message == '':
            print("Give an image path after writing /load :\n")
        if query_message != '' and image_list != []:
            print_out_the_response(query_message, image_list)
```

For example: 
![](https://ollama.ai/public/blog/jmb.jpg)
```markdown
**Q: /load /home/snow/Downloads/llava1p6_test.jpg**
Ask anything about the image: What is this image?
 The image appears to be a street art piece. It features a stylized drawing or painting of what looks like a cartoon dinosaur wearing a crown, with text above it that reads "Jean-Michel Basquiat" and below it that says "Ayicon." The artwork has an urban, graffiti vibe and seems to be paying tribute to the artist Jean-Michel Basquiat, who was famously known for his unique style. The name "Basquiat" is a reference to one of the most prominent figures in modern art history, known for his distinctive paintings that often combined elements of street culture with high art themes and motifs. 

 The image shows a street art piece featuring a stylized black cartoon figure with horns and what appears to be an animal-like head, wearing a crown. There is text on the artwork that reads "Jean-Michel Basquiat" and "anyon," which seems to be part of the artwork's title or message. The art style has a graffiti-like quality with bold lines and vivid colors, which is characteristic of street art. 

**Q: Who is the author of the image?**
 Jean-Michel Basquiat 

**Q: Can you give me a short bio of the author?**
 This image features a graffiti mural with various elements. The most prominent figure in the foreground is Jean-Michel Basquiat, a famous American artist known for his unique and often controversial art style that incorporated elements of both African American culture and the Haitian flag motif. He was born in Brooklyn, New York, to parents who were immigrants from Haiti.

Basquiat is considered one of the founders of the neo-expressionist movement in contemporary art, and his work often addressed social and political issues of the time, including identity, race, and class. His art was highly influential, with many considering him a pioneer of street art and a significant figure in the development of urban contemporary art.

The mural appears to be a tribute or homage to Basquiat and may include additional text that is not fully visible in the image provided. The overall message seems to relate to Basquiat's legacy and influence on modern art. 


```

The `/load` phrase allows to loop to parse a new filename on your local computer, pointing to the image. This will be then 
added to the `images` list, that `ollama.chat` needs to apply the model.

