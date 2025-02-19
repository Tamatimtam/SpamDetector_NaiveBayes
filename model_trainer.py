import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load and prepare data
df = pd.read_csv("enron_spam_data.csv")
df['spam'] = df['Spam/Ham'].apply(lambda x: 1 if x == 'spam' else 0)

# Split data
x_train, x_test, y_train, y_test = train_test_split(df.Message, df.spam)

# Clean and transform data
non_null_mask = x_train.notna()
x_train_clean = x_train[non_null_mask]
y_train_clean = y_train[non_null_mask]

# Initialize and fit vectorizer
cv = CountVectorizer()
x_train_count = cv.fit_transform(x_train_clean.values)

# Train model
model = MultinomialNB()
model.fit(x_train_count, y_train_clean)

# Save model and vectorizer
with open('spam_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(cv, f)
