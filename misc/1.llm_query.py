from transformers import pipeline
llm = pipeline('text-generation', model='distilgpt2')
prompt = "Explain Agentic AI in one sentence."
response = llm(prompt, max_length=50)
print(response[0]['generated_text'])
