from chatgpt import openai, ChatGPT
import tensorflow as tf

# Set up chat gpt
#chatgpt = ChatGPT("jobApp/secrets/openai.json")
print(tf.test.is_built_with_cuda())
print(tf.config.experimental.list_physical_devices('GPU'))

