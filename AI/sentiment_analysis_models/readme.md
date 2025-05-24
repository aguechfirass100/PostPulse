# Sentiment Analysis Models for PostPulse

This directory contains the implementation of sentiment analysis models for the PostPulse marketing platform. These models analyze social media comments and user feedback to provide insights into audience reception and brand perception.

## Overview

PostPulse's sentiment analysis capabilities include:
- Classification of comments into positive, neutral, or negative sentiment
- Analysis of audience reception across multiple platforms
- Trend tracking of sentiment over time
- Identification of potential PR issues or customer service opportunities

## Model Selection

We evaluated multiple sentiment analysis models and selected BERT (Bidirectional Encoder Representations from Transformers) as our primary model:

### Primary Model: Fine-tuned BERT
- **Architecture**: Transformer-based language model developed by Google
- **Key Strengths**: 
  - Deep contextual understanding of language
  - Captures word meaning within full sentence context
  - Robust to sarcasm, negation, and linguistic nuances
  - Fine-tuning efficiency with moderate compute resources
- **Performance**: 76% accuracy on our test dataset (outperforming RoBERTa by 14%)

### Alternative Considered: RoBERTa
- **Performance**: 62% accuracy on our test dataset
- **Limitations**: Despite similar architecture, produced less accurate sentiment classifications for social media content

## Model Comparison

| Model | Accuracy (%) |
|-------|-------------|
| BERT  | 76          |
| RoBERTa | 62        |

## Hyperparameter Optimization

We used Optuna for automated hyperparameter search, resulting in these optimal settings:

| Parameter | Value |
|-----------|-------|
| Learning Rate | 4.36e-05 |
| Per Device Train Batch Size | 8 |
| Num Train Epochs | 3 |
| Weight Decay | 0.029 |

## Dataset

Our sentiment analysis model was trained on:
- Instagram comments scraped using Apify
- Manual and automated labeling for sentiment classification
- Data preparation process:
  1. Removing duplicate comments to eliminate spam
  2. Filtering out comments containing only mentions (@user)
  3. Using langdetect to identify and remove non-English comments
  4. Assigning sentiment labels (positive, negative, neutral)

## Data Labeling Approach

- Leveraged RoBERTa, a pre-trained model for initial automated labeling
- Used cardiffnlp/tweet-eval dataset for fine-tuning
- Combined automated labeling with manual annotation for accuracy

## Integration Workflow

1. **Data Ingestion**: Collect comments from Facebook, Instagram, Twitter/X, and product pages
2. **Preprocessing**: Tokenize text, truncate or pad to fixed sequence length
3. **Classification**: Process through fine-tuned BERT model
4. **Storage**: Store sentiment labels alongside original text
5. **Visualization**: Display sentiment trends and insights in user dashboard

## API Endpoint

```
POST /sentiment
```

### Request Parameters

```json
{
  "comments": [
    "This product is amazing, I love it!",
    "Meh, it's okay I guess.",
    "Terrible experience, would not recommend."
  ]
}
```

### Response

```json
{
  "results": [
    {"text": "This product is amazing, I love it!", "sentiment": "positive", "confidence": 0.94},
    {"text": "Meh, it's okay I guess.", "sentiment": "neutral", "confidence": 0.78},
    {"text": "Terrible experience, would not recommend.", "sentiment": "negative", "confidence": 0.91}
  ],
  "summary": {
    "positive": 1,
    "neutral": 1,
    "negative": 1,
    "overall_sentiment": "neutral"
  }
}
```

## Deployment

Currently deployed via Google Colab Pro with L4 GPU instances and exposed through ngrok tunnels for API access.

## Future Improvements

- Implement multilingual sentiment analysis
- Add emotion detection (beyond positive/negative/neutral)
- Develop specialized models for different industry contexts
- Add aspect-based sentiment analysis to identify specific product/service features mentioned in comments