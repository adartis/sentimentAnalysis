import pandas as pd

# Read the CSV file (adjust the filename as needed)
df = pd.read_csv('news_results_with_text_gpt_processed.csv')

# Assume the column with the multi-message text is named "messages"
# Split the column's text by '#' delimiter into lists
df['message_list'] = df['processed_text'].str.split('#')

# Clean each list: strip extra whitespace and remove any empty messages
df['message_list'] = df['message_list'].apply(
    lambda msgs: [msg.strip() for msg in msgs if msg.strip()] if isinstance(msgs, list) else msgs
)

# Explode the list so that each message gets its own row
df_exploded = df.explode('message_list')

# Optionally, you might want to rename the new column
df_exploded = df_exploded.rename(columns={'message_list': 'message'})

# If you no longer need the original "messages" column, you can drop it:
# df_exploded = df_exploded.drop(columns=['messages'])

# Save the result to a new CSV file
df_exploded.to_csv('output_for_sentiment.csv', index=False)

print("New CSV with one message per row saved as 'output_for_sentiment.csv'")
