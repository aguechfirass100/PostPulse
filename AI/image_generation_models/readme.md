# Image Generation Models for PostPulse

This directory contains the implementation of image generation models for the PostPulse marketing platform. These models enable the generation of high-quality marketing images from text prompts, as well as image-to-image transformations for product customization.

## Overview

PostPulse's image generation capabilities include:
- Text-to-image generation for creating marketing visuals from text descriptions
- Image-to-image transformation for enhancing or modifying existing product images
- Support for various industry verticals and marketing styles

## Models

We evaluated multiple state-of-the-art image generation models and selected the following:

### Primary Model: Flux1-dev
- **Model Type**: Text-to-image diffusion model
- **Average User Rating**: 4.3/5
- **Key Strengths**: Superior prompt fidelity, higher creativity, better handling of sparse prompts
- **Fine-tuning**: Custom LoRA adapters trained on industry-specific content

### Secondary Model: Stable Diffusion XL
- **Model Type**: Image-to-image diffusion model
- **Usage**: Product image transformations and enhancements
- **Key Strengths**: Excellent face detail preservation (4.0/5 rating), suitable for human subjects in marketing

## Fine-Tuning Details

The Flux1-dev model was fine-tuned using the ostris/ai-toolkit with LoRA:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Image resolution | 512×512 px | Input image size |
| Batch size | 1 | Images processed per step |
| Learning rate | 1 × 10<sup>-4</sup> | Fine-tuning step size |
| Optimizer | AdamW 8bit | Memory-efficient variant of AdamW |
| Adapter Alpha | 16 | Scaling factor for LoRA adapters |
| Total steps | 2,000 | Number of training steps |
| Checkpoint interval | Every 250 steps | Save model every 250 steps |

## Dataset

Our fine-tuning dataset consists of:
- 2,000 prompt-image pairs across 10 industry sectors (200 per sector)
- Custom prompts with varying levels of detail
- Images standardized to 512×512 resolution

## API Endpoint

```
POST /generate-image
```

### Request Parameters

```json
{
  "prompt": "Professional product photo of a smartphone against a dark gradient background",
  "base_image_url": "[optional URL to base image for image-to-image transformation]",
  "industry": "technology",
  "style": "professional"
}
```

### Response

```json
{
  "generated_image_url": "https://postpulse-storage.com/images/generated/image123.png",
  "generation_time": "3.2s"
}
```

## Deployment

Currently deployed via Google Colab Pro with A100 40GB GPU instances and exposed through ngrok tunnels for API access.

## Future Improvements

- Implement containerization for more robust deployment
- Add image generation history and favorites for users
- Incorporate user feedback to improve model performance
- Add more industry-specific fine-tuning