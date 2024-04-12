import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

# Load the pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def generate_syn_data(prompt, data_type, max_length=200, num_samples=1, device='cpu'):
    """
    Generate synthetic data from a given prompt using the GPT-2 model.
    
    Args:
        prompt (str): The input prompt to start the data generation.
        data_type (str): The type of data to generate ('text' or 'research').
        max_length (int): The maximum length of the generated text.
        num_samples (int): The number of samples to generate.
        device (str): The device to use for the model (e.g., 'cpu' or 'cuda').
    
    Returns:
        List[str]: The generated synthetic data.
    """
    # Move the model to the specified device
    model.to(device)
    
    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
    
    # Generate the synthetic data
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_samples,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_beams=1,
        early_stopping=True
    )
    
    # Decode the generated text
    synthetic_data = [tokenizer.decode(seq, skip_special_tokens=True) for seq in output]
    
    return synthetic_data

def save_data(data, data_type, file_name):
    """
    Save the generated synthetic data in the specified format.
    
    Args:
        data (List[str]): The generated synthetic data.
        data_type (str): The type of data ('text' or 'research').
        file_name (str): The name of the output file.
    """
    if data_type == 'text':
        with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(data))
        print(f"Synthetic text data saved as {file_name}.txt")
    elif data_type == 'research':
        import csv
        with open(f"{file_name}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(data)
        print(f"Synthetic research data saved as {file_name}.csv")
    else:
        print("Invalid data type. Please choose 'text' or 'research'.")
