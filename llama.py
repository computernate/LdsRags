from transformers import pipeline
import torch

#Token: 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
pipe = pipeline("text-generation", model="meta-llama/Llama-2-7b-hf", device_map="auto")

def generate_text(prompt):
    output = pipe(prompt, max_length=100, do_sample=True)
    return output[0]['generated_text']
# prompt = "I have here a chapter of scripture. For this chapter, I would like a list of doctrines taught. Please list as many as you can in a json list, and respond in nothing other than that json. Here is the text: \n"
#
# with open('book_of_mormon.txt', 'r') as file:
#     prompt += file.read()
prompt = "I am trying to set up Llama on my computer. Please let me know that you work."
print(generate_text(prompt))