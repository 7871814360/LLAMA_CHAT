import openai

def generate_image(prompt):
    openai.api_key = ''  # Replace with your OpenAI API key

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response['data'][0]['url']
    return image_url

topic = input("Enter a class 6 topic: ")
image_url = generate_image(topic)
print(image_url)