import sys
from transformers import pipeline

def generate_text(prompt, max_length=50):
    try:
        # Initialize the text generation pipeline with GPT-2
        generator = pipeline("text-generation", model="gpt2")
        # Generate text
        result = generator(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]["generated_text"]
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Default prompt or take from command line
    prompt = sys.argv[1] if len(sys.argv) > 1 else "The future of AI is"
    print("Generating text for prompt:", prompt)
    output = generate_text(prompt, max_length=100)
    print("Generated text:", output)

if __name__ == "__main__":
    main()