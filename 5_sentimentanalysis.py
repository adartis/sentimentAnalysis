#script to test nlp
#import dependencies
import pandas as pd
# import pipeline for handling use of NLP
from transformers import pipeline
# import BERT for NLP
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
# import logging for testing
import logging
#import time for flow management
import time


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#  load of load the pretrained tokeniser and model
tokeniser = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

def process_sentiment_csv(input_csv, output_csv, column_name, new_label_column, new_score_column, tokeniser, model):
    """
    Reads a CSV, processes the text using BERT for sentiment analysis,
    and writes the results to two new columns: one for the sentiment label and one for the score.
    
    :param input_csv: the input CSV file.
    :param output_csv: the output CSV file.
    :param column_name: the name of the column containing text to process.
    :param new_label_column: the name of the new column for the sentiment label.
    :param new_score_column: the name of the new column for the sentiment score.
    :param tokeniser: the tokenizer for the model.
    :param model: the sentiment analysis model.
    """
    #read csv with pandas
    df = pd.read_csv(input_csv)

    #define pipeline as nlp
    nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokeniser)

    # validate if requisite column exists
    if column_name not in df.columns:
        logger.error(f"Error: Column '{column_name}' not found in CSV.")
        raise ValueError(f"Column '{column_name}' not found in CSV.")
    
    # Prepare lists to store the sentiment labels and scores
    labels_list = []
    scores_list = []

    # Process each row using an explicit loop to allow rate limiting
    for idx, text in enumerate(df[column_name]):
        if pd.notna(text):
            result = nlp(text)
            # result is a list with one dictionary, e.g. [{'label': 'POSITIVE', 'score': 0.9886701107025146}]
            label = result[0]['label']
            score = result[0]['score']
        else:
            label = ""
            score = ""
        labels_list.append(label)
        scores_list.append(score)
        logger.info(f"Processed row {idx + 1}/{len(df)}")
        time.sleep(0.4)  # Pause to avoid hitting API rate limits
    
    # Create new columns for label and score
    df[new_label_column] = labels_list
    df[new_score_column] = scores_list

    # Save the updated CSV file
    df.to_csv(output_csv, index=False, encoding="utf-8")
    logger.info(f"Processed CSV saved as '{output_csv}'.")

def main():
    """
    Main function to execute the sentiment analysis.
    """
    input_csv = "output_for_sentiment_delimited.csv"
    output_csv = "analysis_file_all_functions_applied.csv"
    # Column in the CSV containing text to process
    column_name = "processed_text"
    # Define the names for the new columns for label and score
    new_label_column = "sentiment_label"
    new_score_column = "sentiment_score"

    # call function to process csv listing relevant params
    process_sentiment_csv(input_csv, output_csv, column_name, new_label_column, new_score_column, tokeniser, model)

if __name__ == "__main__":
    main()