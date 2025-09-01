import pandas as pd
from datasets import load_dataset, DatasetDict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai
from pinecone import Pinecone, ServerlessSpec
from google.colab import userdata # Import userdata to access secrets

# Load SNIPS dataset
dataset = load_dataset('snips_built_in_intents')
train_dataset = dataset['train']

# Get intent names from the dataset features
intent_names = train_dataset.features['label'].names

# Filter scheduling-related utterances (e.g., 'BookRestaurant')
tasks = []
target_intent_name = 'BookRestaurant' # Or any other intent name you want to filter by

for item in train_dataset:
    # Check if the label corresponds to the target intent name
    if intent_names[item['label']] == target_intent_name:
        tasks.append({
            'task': item['text'],
            'response': f"Create Google Calendar event for {item['text'].lower()}"
        })

# Create DataFrame and save to faqs.csv (limit to 50 for speed)
# Ensure tasks list is not empty before creating DataFrame
if tasks:
    df = pd.DataFrame(tasks[:50])
    df.to_csv('data/faqs.csv', index=False)

    # Generate embeddings with Sentence Transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['task'].tolist(), show_progress_bar=True)

    # Save embeddings
    pd.DataFrame(embeddings).to_json('embeddings.json')

    # Store in FAISS
    dimension = embeddings.shape[1]  # 384 for MiniLM
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype='float32'))
    faiss.write_index(index, 'data/faiss_index.bin')

    print("Data processed, embeddings and FAISS index created.")

else:
    print(f"No tasks found for intent '{target_intent_name}'. Please check the intent name or the dataset.")
