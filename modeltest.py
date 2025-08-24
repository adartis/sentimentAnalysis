from transformers import pipeline

# Initialize the emotion classification pipeline
nlp = pipeline(
    "text-classification",
    model="Panda0116/emotion-classification-model",
    top_k=None  # replaces deprecated return_all_scores=True
)

# Sample text for analysis
text = "I love using Hugging Face models!"

# Perform emotion classification
result = nlp(text)

# Define emotion labels corresponding to the model's output
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

# Extract the highest scoring emotion
max_emotion = max(result[0], key=lambda x: x['score'])

# Convert the label from "LABEL_X" to an index
label_index = int(max_emotion['label'].replace("LABEL_", ""))
predicted_emotion = emotion_labels[label_index]

print(f"Predicted Emotion: {predicted_emotion} with score {max_emotion['score']:.4f}")

# Optional: print all emotions and scores
print("All emotion scores:")
for r in result[0]:
    idx = int(r['label'].replace("LABEL_", ""))
    print(f"{emotion_labels[idx]}: {r['score']:.4f}")
