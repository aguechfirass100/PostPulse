# Video Generation Models for PostPulse

This directory contains the implementation of the video generation component for the PostPulse marketing platform. This functionality allows users to create animated marketing videos from static images.

## Overview

PostPulse's video generation system enables:
- Transformation of product/brand images into short animated videos
- Creation of engaging social media video content with minimal user input
- Dynamic motion effects while preserving the visual identity of source images

## Model Selection

We evaluated two leading image-to-video diffusion models:

### Selected Model: Stable-Video-Diffusion-Img2Vid-XT
- **Architecture**: Stable Diffusion variant optimized for sequential frame decoding
- **Input**: Single image
- **Output**: 25-frame video sequence (typically at 7 fps)
- **Key Strengths**: 
  - High fidelity to original image appearance (4.5/5)
  - Smooth transitions between frames (4.0/5)
  - Strong frame-to-frame coherence (4.2/5)

### Alternative Considered: AnimateDiff-Lightning
- **Architecture**: Diffusion-based with UNet backbone
- **Limitations**: Failed to maintain consistency across frames (1.5/5), producing disjointed sequences

## Evaluation Metrics

| Model | Frame Coherence (1-5) | Motion Smoothness (1-5) | Style Fidelity (1-5) | Remarks |
|-------|------------------------|-------------------------|----------------------|---------|
| AnimateDiff-Lightning | 1.5 | 2.0 | 3.0 | Disjointed frames; failed to progress coherently |
| Stable-Video-Diffusion-Img2Vid-XT | 4.2 | 4.0 | 4.5 | Smooth motion, faithful to input style |

## Implementation

The video generation process follows these steps:

1. **Input Processing**: Standardize the source image to required dimensions
2. **Frame Generation**: Process the image through Stable-Video-Diffusion-Img2Vid-XT with fixed seed for reproducibility
3. **Memory Management**: Chunk frame decoding (groups of 5-10 frames) to fit GPU constraints
4. **Output Standardization**: Post-process generated frames to uniform resolution 
5. **Video Assembly**: Combine frames into a cohesive video clip

## API Endpoint

```
POST /generate-video
```

### Request Parameters

```json
{
  "image_url": "https://example.com/path/to/source_image.jpg",
  "motion_strength": 0.6,
  "duration_seconds": 3.5
}
```

### Response

```json
{
  "video_url": "https://postpulse-storage.com/videos/generated/video123.mp4",
  "thumbnail_url": "https://postpulse-storage.com/videos/thumbnails/thumb123.jpg",
  "generation_time": "8.2s"
}
```

## Deployment

Currently deployed on Google Colab Pro using A100 40GB GPU instances. The model is served via a Flask application and exposed through an ngrok tunnel for API access.

## Resource Requirements

- **GPU**: NVIDIA A100 40GB (or equivalent)
- **RAM**: Minimum 16GB
- **Storage**: ~10GB for model weights

## Limitations

- Maximum input image resolution: 1024×1024
- Maximum output video length: ~5 seconds (25 frames at 7fps)
- No audio generation capabilities

## Future Improvements

- Add text prompt conditioning for more controlled motion
- Implement longer video generation (60+ frames)
- Add style transfer options for more creative control
- Integrate audio generation or template-based audio tracks