import pandas as pd
from textblob import TextBlob
import re
import json

# Load Excel File
excel_file = "input_resources/Transcript_Input.xlsx"
# Replace with your file path
df = pd.read_excel(excel_file)

def redact_pii(transcript):
    # Replace names and address with placeholders
    redacted_transcript = re.sub(r'\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+?)\b','[REDACTED]',transcript)
    return redacted_transcript

def analyze_sentiment(transcript):
    analysis = TextBlob(transcript)
    return "positive" if analysis.sentiment.polarity > 0 else "negative"

def summarize_transcript(transcript):
    # simple summary extraction (This can be improved with more sophosticated NLP techniques)
    return transcript[:min(200,len(transcript))] # Example: first 200 characters

def extract_subject(transcript):
    if 'account access' in transcript.lower():
        return "Account Access Issue"
    elif "technical supprt" in transcript.lower():
        return "Technical Support Issue"
    else:
        return "General Inquiry"

def process_transcript(df):
    results = []
    for index, row in df.iterrows():
        transcript = row['Transcript']
        sentiment = analyze_sentiment(transcript)
        summary = summarize_transcript(transcript)
        subject = extract_subject(transcript)
        redacted_transcript = redact_pii(transcript)

        result = {
            "sentiment": sentiment,
            "summary": summary,
            "subject": subject,
            "transcript": redacted_transcript
        }

        results.append(result)

    return results

#Process the transcripts and output results
processed_results = process_transcript(df)

#Output JSON to a file or print
with open("transcripts_summary.json","w") as f:
    json.dump(processed_results,f,indent=4)

print(json.dumps(processed_results, indent=4))



