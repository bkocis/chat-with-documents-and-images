import ollama
import sys


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    res = ollama.chat(
        model=selected_model,
        messages=[
            {
            'role': 'user',
            'content': query,
            'images': image_list,
            }
        ]
    )
    return res['message']['content']


def print_out_the_response(query_message: str, image_list: list[str]) -> None:
    response = query_the_image(query_message, image_list)
    print(response)
    sys.stdout.flush()
    sys.stdout.write("\n")


if __name__ == "__main__":
    selected_model = "llava"
    image_list = []
    # main CLI interaction loop
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
