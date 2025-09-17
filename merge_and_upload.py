import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- Configuration ---
# The base model you used for fine-tuning
base_model_id = "microsoft/Phi-3-mini-4k-instruct"

# The path to your saved adapter weights
adapter_path = "./finetuned_model"

# The name for your new, merged model on the Hugging Face Hub
# IMPORTANT: Replace "YourUsername" with your actual Hugging Face username
new_repo_id = "Barghav777/phi3-lab-report-coder"

print("Loading base model...")
# Load the base model in a format suitable for merging (e.g., float16)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.float16,
    trust_remote_code=True
)

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)

print("Loading PEFT adapter...")
# Load the PEFT model with the adapter weights
peft_model = PeftModel.from_pretrained(base_model, adapter_path)

print("Merging adapter with base model...")
# Merge the adapter layers into the base model
merged_model = peft_model.merge_and_unload()
print("Merge complete!")

print(f"Uploading merged model to Hugging Face Hub at: {new_repo_id}")
# Push the merged model and tokenizer to the Hub
merged_model.push_to_hub(new_repo_id)
tokenizer.push_to_hub(new_repo_id)

print("✅ Successfully uploaded model and tokenizer to the Hub!")