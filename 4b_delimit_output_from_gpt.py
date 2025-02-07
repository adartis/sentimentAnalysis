import csv
import re

# Regular expression to capture the text between the first "[" and "]" 
# and all text following the closing bracket.
pattern = re.compile(r'^[^\[]*\[([^]]+)\](.*)', re.DOTALL)

input_filename = 'output_for_sentiment.csv'
output_filename = 'output_for_sentiment_delimited.csv'

with open(input_filename, mode='r', encoding='utf-8', newline='') as infile, \
     open(output_filename, mode='w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read the header row.
    header = next(reader)
    
    # Identify the index of the column headed "message".
    try:
        message_index = header.index("message")
    except ValueError:
        raise ValueError("The input CSV does not contain a column headed 'message'.")
    
    # Retain all columns preceding "message" and add two new headers.
    new_header = header[:message_index] + ["message_title", "message"]
    writer.writerow(new_header)
    
    # Process each row.
    for row in reader:
        message_text = row[message_index]
        match = pattern.match(message_text)
        if match:
            title_text = match.group(1).strip()
            remaining_text = match.group(2).strip()
        else:
            title_text = ""
            remaining_text = message_text.strip()
        
        # Construct the new row: preceding columns plus the two new columns.
        new_row = row[:message_index] + [title_text, remaining_text]
        writer.writerow(new_row)
