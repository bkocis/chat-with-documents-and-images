import ollama

res = ollama.chat(
    model="llava",
    messages=[
        {
        'role': 'user',
        'content': "Which city landmark is in the image:",
        'images': ["/home/snow/Downloads/Santa_Maria_della_Salute_from_Hotel_Monaco.jpg"],
        }
    ]
)

print(res['message']['content'])
