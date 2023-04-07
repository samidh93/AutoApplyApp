from chatgpt import openai, ChatGPT
import tensorflow as tf

# Set up chat gpt
chatgpt = ChatGPT("jobApp/secrets/openai.json")

# Set up the TensorFlow-GPU environment
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Set the memory growth for the GPU
    tf.config.experimental.set_memory_growth(gpus[0], True)
  except RuntimeError as e:
    print(e)

# Generate a response to a user message using the OpenAI API
def generate_response(message):
  model_engine = "text-davinci-002"
  prompt = f"User: {message}\nAI:"
  response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
  )
  return response.choices[0].text.strip()

# Test the generation of a response using TensorFlow-GPU
response = generate_response("Hello, how are you?")
print(response)
