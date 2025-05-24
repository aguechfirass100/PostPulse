# PDF Summary Module for PostPulse

This directory contains the implementation of the PDF summary module for the PostPulse marketing platform. This component extracts valuable information from user-provided PDF documents to tailor marketing content and improve onboarding.

## Overview

PostPulse's PDF summary capabilities include:
- Extracting key business information from uploaded PDFs
- Identifying brand voice, target audience, and marketing goals
- Analyzing product/service offerings for better content generation
- Creating a structured profile for new users based on their documentation

## Implementation

The PDF summary module leverages Google's Gemini API for advanced document understanding and information extraction:

### Key Components

1. **PDF Parser**: Handles PDF document uploads and converts them to text
2. **Gemini API Integration**: Processes extracted text to identify key information
3. **Information Structuring**: Organizes extracted data into user profiles
4. **Database Integration**: Stores structured profiles in MongoDB for use across the platform

## Workflow

1. During user onboarding, the platform prompts new users to upload a business document (brochure, report, etc.)
2. The PDF parser extracts the text content from the document
3. The content is sent to the Gemini API with specific prompts to extract key information:
   - Company/brand description
   - Product/service details
   - Target audience demographics
   - Brand voice and tone
   - Marketing goals and KPIs
   - Industry-specific terminology
4. The extracted information is structured into a user profile
5. This profile is used to customize the platform experience and inform AI-generated content

## API Endpoint

```
POST /summarize-pdf
```

### Request Parameters

```json
{
  "file": "[PDF binary data]",
  "extraction_focus": ["brand_voice", "products", "target_audience"]
}
```

### Response

```json
{
  "summary": {
    "company_name": "TechNova Solutions",
    "brand_description": "A cutting-edge software development company focused on AI and machine learning solutions",
    "products": [
      {
        "name": "AI Analyzer Pro",
        "description": "Data analysis platform powered by machine learning"
      },
      {
        "name": "CloudSync Enterprise",
        "description": "Cloud storage and synchronization solution for businesses"
      }
    ],
    "target_audience": {
      "industries": ["Finance", "Healthcare", "Manufacturing"],
      "company_size": "Mid to large enterprises",
      "key_decision_makers": "CIOs, CTOs, IT Directors"
    },
    "brand_voice": {
      "tone": "Professional, authoritative, innovative",
      "key_terms": ["cutting-edge", "enterprise-grade", "scalable", "secure"]
    },
    "marketing_goals": ["Increase enterprise client acquisition", "Expand presence in healthcare sector"]
  },
  "confidence_score": 0.87,
  "extraction_time": "3.5s"
}
```

## Security Considerations

- All uploaded PDFs are processed securely and deleted after information extraction
- User data is stored in MongoDB with appropriate encryption
- API keys for Gemini are stored as environment variables, not in code

## Deployment

Currently deployed via Google Colab Pro and exposed through ngrok tunnels for API access. The PDF processing is handled within the Flask application.

## Dependencies

- PyPDF2: For PDF text extraction
- Google Gemini API: For advanced text analysis and information extraction
- Flask: For API endpoint implementation
- MongoDB: For storing structured user profiles

## Future Improvements

- Support for additional document formats (DOCX, PPT, etc.)
- Enhanced information extraction for industry-specific documents
- Visual element analysis (logos, color schemes, imagery)
- Competitive analysis based on uploaded materials
- Multilingual document support
- Integration with image generation to match brand visuals