# PostPulse

![PostPulse Logo](https://via.placeholder.com/800x200?text=PostPulse)

## 📌 Overview

PostPulse is an AI-powered marketing platform designed for marketers, small businesses, startups, and influencers. It leverages cutting-edge AI models to automate social media content creation and provide deep insights into audience engagement and sentiment.

### 🎯 Key Features

- **AI Content Generation**
  - Text generation for captivating post copy
  - Social media ad poster creation
  - Image-to-image transformation for product marketing
  - Video generation from static images
  
- **Audience Insights**
  - Sentiment analysis for social media comments
  - Engagement trend prediction
  - Performance analytics

- **Platform Integration**
  - Seamless social media platform connectivity
  - Authentication via Facebook and Google
  - Business profile analysis from PDF uploads

## 🏗️ Architecture

PostPulse follows a microservice architecture with AI models deployed as separate services:

```
Client <-> Frontend (React) <-> Backend API (Flask) <-> AI Models (Colab+ngrok) <-> Database (MongoDB)
```

## 🧠 AI Models

### Image Generation

- **Models Evaluated**: Flux.1 [dev], SDXL, SD3.5
- **Selected Model**: Flux.1 [dev] (fine-tuned)
- **Fine-tuning Method**: LoRA via ostris/ai-toolkit
- **Features**: Both text-to-image and image-to-image generation

### Video Generation

- **Models Evaluated**: Stable Video Diffusion (SVD), AnimateDiff
- **Selected Model**: Stable Video Diffusion
- **Features**: Transforms static images into animated videos with prompt guidance

### Text Generation

- **Models Evaluated**: LLaMA 3.2, Mistral 7B
- **Selected Model**: LLaMA 3.2 (fine-tuned)
- **Fine-tuning Method**: Optimized with Unsloth
- **Features**: Generates engaging copy with various tones (professional, casual, persuasive, etc.)

### Sentiment Analysis

- **Model**: BERT (fine-tuned)
- **Features**: Classifies comments as positive, neutral, or negative
- **Accuracy**: 76% (outperforming RoBERTa at 62%)

### Trend Prediction

- **Model**: Prophet
- **Features**: Forecasts 5-day engagement metrics for posts
- **Metrics**: MAE: 92, RMSE: 124

### PDF Analysis

- **Approach**: Extracts key business information from uploaded PDFs
- **Use Case**: Personalizes content strategies based on business profiles

## 💻 Technical Stack

### Frontend

- Framework: React.js with Next.js
- State Management: React Context API
- Styling: Tailwind CSS

### Backend

- Framework: Flask microservices
- Database: MongoDB
- Authentication: OAuth 2.0 (Google, Facebook)

### Deployment

- AI Model Hosting: Google Colab Pro (A100 40GB and L4 GPU instances)
- API Exposure: ngrok tunnels
- Configuration: Dynamic endpoint discovery

### Data Collection

- Tools: Python libraries, Apify scrapers
- Sources: Pinterest, Instagram, and other social platforms

## 📥 Installation & Setup

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- MongoDB
- Google Colab Pro account (for AI model deployment)

### Frontend Setup

```bash
# Navigate to frontend directory
cd marketmind_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup

```bash
# Navigate to backend directory
cd marketmind_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

### AI Models Setup

See specific README files in each model directory under the `AI` folder:

- `image_generation_models/README.md`
- `video_generation_models/README.md`
- `text_generation_models/README.md`
- `sentiment_analysis_models/README.md`
- `trend_prediction_models/README.md`
- `pdf_summary/README.md`

## 🛠️ Development Workflow

1. **Data Collection & Processing**
   - Scraped Pinterest images using Apify
   - Generated textual prompts with Gemini API
   - Collected Instagram comments for sentiment analysis
   - Designed rule-based approach for trend data collection

2. **Model Training & Fine-tuning**
   - Fine-tuned Flux.1 [dev] for image generation
   - Optimized LLaMA 3.2 with Unsloth
   - Trained BERT for sentiment classification
   - Configured Prophet for trend prediction

3. **Deployment**
   - Each AI model runs in a separate Colab notebook
   - Flask APIs expose model functionality
   - ngrok tunnels make endpoints publicly accessible
   - Frontend dynamically discovers services

## 📊 Performance & Metrics

### Image Generation

- **Average User Rating**: 4.3/5 for Flux.1 [dev]
- **Generation Time**: ~8 seconds per image

### Video Generation

- **Frame Coherence**: 4.2/5
- **Motion Smoothness**: 4.0/5
- **Style Fidelity**: 4.5/5

### Text Generation

- **Response Time**: ~1.2 seconds
- **Tone Variations**: Professional, Casual, Persuasive, Inspirational, FOMO

### Sentiment Analysis

- **Accuracy**: 76%
- **Processing Time**: ~1.2 seconds per batch

### Trend Prediction

- **MAE**: 92
- **RMSE**: 124
- **Forecast Horizon**: 5 days

## 🚀 Future Enhancements

- Migrate from Colab+ngrok to containerized deployment
- Implement CI/CD pipeline
- Add comprehensive monitoring and logging
- Expand social media platform integrations
- Develop A/B testing capabilities
- Implement user feedback loops for model improvement

## 📜 License

[MIT License](LICENSE)

## 👥 Contributors

- Data Diggers Team

## 📞 Contact

For inquiries, please reach out to [contact@postpulse.ai](mailto:aguechfirass100@gmail.com)
