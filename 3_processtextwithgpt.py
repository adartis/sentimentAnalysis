# import os to secure env variable - using .gitignore to prevent upload
import os
# openAI package for API
from openai import OpenAI
# Pandas for dataframe manipulation
import pandas as pd
# load environmental variables for API key
from dotenv import load_dotenv
# load for managing timing of requests
import time
# load for logging 
import logging

# Load environment variables (for API key storage)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_text_with_chatgpt(text, prompt_template, model="gpt-4o-mini"):
    """
    Sends text to ChatGPT with a custom prompt and returns the transformed output.
    
    :param text: The text from the CSV cell.
    :param prompt_template: The prompt template to guide transformation.
    :param model: OpenAI model to use (default is "gpt-4-mini").
    :return: The transformed text.
    """
    try:
        # Format the prompt with the text input
        prompt = prompt_template.format(text=text)

        # Send request to OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": ("You are an AI that processes text in order to draw out the main messages "
                                "relating to Serbia and its relations with the UK and the rest of the world. Aim to be "
                                "parsimonious in your summaries but accurate insofar as the main messages are retained. "
                                "You are writing for a senior executive audience.")
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Extract and return the response text
        return response.choices[0].message.content.strip()


    # exception if error
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return "Error"

def process_csv(input_csv, output_csv, column_name, new_column_name, prompt_template):
    """
    Reads a CSV file, processes text using ChatGPT, and writes the results to a new column.

    :param input_csv: The input CSV file.
    :param output_csv: The output CSV file.
    :param column_name: The name of the column to process.
    :param new_column_name: The name of the new column to store transformed text.
    :param prompt_template: The prompt template guiding transformation.
    """
    # Read CSV file
    df = pd.read_csv(input_csv)

    # Validate that the required column exists
    if column_name not in df.columns:
        logger.error(f"Error: Column '{column_name}' not found in CSV.")
        raise ValueError(f"Column '{column_name}' not found in CSV.")


    # Process each row using an explicit loop to allow rate limiting
    processed_texts = []
    for idx, text in enumerate(df[column_name]):
        if pd.notna(text):
            processed = process_text_with_chatgpt(text, prompt_template)
        else:
            processed = ""
        processed_texts.append(processed)
        logger.info(f"Processed row {idx + 1}/{len(df)}")
        time.sleep(1)  # Pause to avoid hitting API rate limits

     # Add new column with processed text
    df[new_column_name] = processed_texts

    # Save the updated CSV file
    df.to_csv(output_csv, index=False, encoding="utf-8")
    logger.info(f"Processed CSV saved as '{output_csv}'.")

def main():
    """
    Main function to execute the CSV processing.
    """
    input_csv = "news_results_with_text.csv"  # Input CSV file
    output_csv = "news_results_with_text_gpt_processed.csv"  # Output CSV file with new column
    column_name = "text"  # Column name to process
    new_column_name = "processed_text"  # New column name
    prompt_template = (
        "Please review the text and provide a summary. The summary should inform the reader of the at least 2 and at most 5 key messages in the text. "
        "Ensure that the sentiment relating to each legal or natural person is preserved in each key message. "
        "Please structure the output like this: (1) Put a keyword in [square braces] which describes who or what each key message is about. Keep the keywords as clear nouns, e.g. a country name or a concept like 'corruption' "
        "(2) Write a short paragraph, at least 1 and at most 4 sentences, summarising the key message. "
        "(3) After each key message, put a delimiter #. Only use a # as delimiter. "
        "(4) The maximum length of the output should be no more than 350 words"
        "The text for you to review is: {text}"
    )

    process_csv(input_csv, output_csv, column_name, new_column_name, prompt_template)

if __name__ == "__main__":
    main()
