# Text Generation Models for PostPulse

This directory contains the implementation of text generation models for the PostPulse marketing platform. These models enable the creation of engaging social media copy, captions, and advertising text in various tones and styles.

## Overview

PostPulse's text generation capabilities include:
- Creating social media post captions and body text
- Generating advertising copy in multiple tones (professional, casual, persuasive, etc.)
- Crafting content tailored to different platforms and audience demographics

## Model Selection

We evaluated multiple language models and selected the following:

### Primary Model: LLaMA 3.2 3B (Fine-tuned)
- **Model Family**: Meta's open-source Large Language Model Meta AI
- **Size**: 3 billion parameters
- **Key Strengths**: Superior instruction-following, reasoning, and language coherence
- **Deployment Compatibility**: Runs on consumer-grade GPUs with quantization and LoRA
- **Training**: Fine-tuned using Unsloth library for optimization

### Alternative Considered: Mistral 7B
- **Design**: Lightweight, low-latency model optimized for inference on small GPUs
- **Strengths**: Fast response, low memory footprint, energy efficient
- **Limitations**: Less versatile across diverse marketing contexts compared to LLaMA 3.2

## Fine-Tuning Details

LLaMA 3.2 3B was fine-tuned using Unsloth with the following optimizations:
- **LoRA (Low-Rank Adaptation)**: Updates only a subset of parameters
- **Flash Attention 2**: Speeds up the attention mechanism
- **4-bit Quantization**: Reduces memory footprint

### Training Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Batch Size | 4 per device | Fits within 16 GB VRAM |
| Gradient Accumulation | 4 steps | Stabilizes updates without extra VRAM use |
| Warmup Steps | 1 | Smoothly ramps up learning rate |
| Learning Rate | 2 × 10<sup>-4</sup> | Balances convergence speed and stability |
| Optimizer | AdamW 8-bit | Reduces optimizer memory overhead |
| Weight Decay | 0.01 | Regularizes to prevent overfitting |
| Precision | FP16 / BF16 | Lowers memory use, speeds training |
| LR Scheduler | Linear decay | Gradually reduces learning rate |
| Logging | Every step | Enables close monitoring in Colab |

## Dataset

Our text generation model was fine-tuned on:
- Marketing copy across multiple industries and platforms
- Content with various tones and styles (professional, casual, persuasive, inspirational/motivational, FOMO, etc.)
- Platform-specific content formats (Instagram, Twitter/X, Facebook, LinkedIn)

## Tone Variations

The model can generate text in the following tones:
- Professional
- Casual
- Persuasive
- Inspirational/Motivational
- Fear of Missing Out (FOMO)
- And more...

## API Endpoint

```
POST /generate-text
```

### Request Parameters

```json
{
  "prompt": "Create a social media post about our new smartphone release",
  "platform": "instagram",
  "tone": "professional",
  "max_length": 150,
  "industry": "technology"
}
```

### Response

```json
{
  "generated_text": "Introducing our revolutionary new XYZ smartphone. Engineered with cutting-edge technology and sleek design, it's ready to transform how you connect, create, and communicate. Available now. #TechInnovation #NewRelease",
  "generation_time": "1.2s",
  "word_count": 28
}
```

## Deployment

Currently deployed via Google Colab Pro with L4 GPU instances and exposed through ngrok tunnels for API access.

## Future Improvements

- Expand tone variations to include more styles
- Add A/B testing integration to learn from successful content
- Implement more platform-specific formatting options
- Develop industry-specific terminology databases