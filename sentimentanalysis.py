#script to test nlp
#import dependencies
import pandas as pd
from transformers import pipeline
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

#load the pretrained tokeniser and model
tokeniser = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

#define pipeline as nlp
nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokeniser)

#load dataframe as df
df = pd.read_csv("data.csv")

#name columns
df.columns = ['Website', 'Link', 'date published', 'title', 'content']

texts = list(df.content.values)

results = nlp(texts)

#for text, result, score in zip(texts, results, df.score.values):
for text, result in zip(texts, results):
    print("text: ", text)
    print("result: ", result)
    #print("Score: ", score)

df['sentiment'] = [r['label'] for r in results]