# Script to test NLP
import pandas as pd
import logging
import time
from transformers import pipeline
import os

# Check if CSV exists
print("CSV exists:", os.path.exists("output_for_sentiment_delimited.csv"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Logging is working!")

# Initialize the emotion model pipeline
nlp = pipeline(
    "text-classification",
    model="Panda0116/emotion-classification-model",
    top_k=None  # replaces deprecated return_all_scores=True
)

# Define emotion labels corresponding to the model
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

def process_sentiment_csv(input_csv, output_csv, column_name):
    # Read CSV
    df = pd.read_csv(input_csv)

    if column_name not in df.columns:
        logger.error(f"Error: Column '{column_name}' not found in CSV.")
        raise ValueError(f"Column '{column_name}' not found in CSV.")
    
    # Prepare dictionary for storing scores
    scores_dict = {emotion: [] for emotion in emotion_labels}

    # Process each row
    for idx, text in enumerate(df[column_name]):
        if pd.notna(text):
            results = nlp(text)  # returns list of dicts
            for r in results[0]:
                # Convert LABEL_X to index
                label_index = int(r['label'].replace("LABEL_", ""))
                emotion = emotion_labels[label_index]
                score = r['score']
                scores_dict[emotion].append(score)
        else:
            for emotion in emotion_labels:
                scores_dict[emotion].append(None)

        logger.info(f"Processed row {idx + 1}/{len(df)}")
        time.sleep(0.1)

    # Add emotion columns to the DataFrame
    for emotion in emotion_labels:
        df[emotion] = scores_dict[emotion]

    # Save the updated CSV
    df.to_csv(output_csv, index=False, encoding="utf-8")
    logger.info(f"Processed CSV saved as '{output_csv}'.")

def main():
    input_csv = "output_for_sentiment_delimited.csv"
    output_csv = "analysis_file_all_functions_applied.csv"
    column_name = "processed_text"

    process_sentiment_csv(input_csv, output_csv, column_name)

if __name__ == "__main__":
    main()
