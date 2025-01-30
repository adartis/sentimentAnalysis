import os
import openai
import pandas as pd
from dotenv import load_dotenv
import time

# Load environment variables (for API key storage)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key

def process_text_with_chatgpt(text, prompt_template, model="gpt-4o-mini"):
    """
    Sends text to ChatGPT with a custom prompt and returns the transformed output.
    
    :param text: The text from the CSV cell.
    :param prompt_template: The prompt template to guide transformation.
    :param model: OpenAI model to use (default is "gpt-4-turbo").
    :return: The transformed text.
    """
    try:
        # Format the prompt with the text input
        prompt = prompt_template.format(text=text)

        # Send request to OpenAI API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are an AI that processes text."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Extract and return the response text
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"Error processing text: {e}")
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

    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in CSV.")
        return

    # Create new column with ChatGPT-processed text
    df[new_column_name] = df[column_name].apply(lambda x: process_text_with_chatgpt(x, prompt_template) if pd.notna(x) else "")

    # Save the updated CSV file
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Processed CSV saved as '{output_csv}'.")

def main():
    """
    Main function to execute the CSV processing.
    """
    input_csv = "news_results.csv"  # Input CSV file
    output_csv = "news_results_processed.csv"  # Output CSV file with new column
    column_name = "Title"  # Column name to process
    new_column_name = "Processed_Text"  # New column name
    prompt_template = "Transform this text so that it captures the key topic: {text}"  # Modify prompt as needed

    process_csv(input_csv, output_csv, column_name, new_column_name, prompt_template)

if __name__ == "__main__":
    main()
