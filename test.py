from ollama import Client

client = Client()

response = client.generate(
    model="llama3:latest",
    prompt="Say hello in a cute way!"
)

print(response["response"])
