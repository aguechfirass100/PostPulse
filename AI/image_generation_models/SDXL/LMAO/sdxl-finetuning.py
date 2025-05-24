# SDXL LoRA Fine-tuning for MarketMind
# This notebook fine-tunes Stable Diffusion XL using LoRA for generating
# social media ad posters with the [marketmind] trigger word

# Cell 1: Install required dependencies
!pip install -q torch==2.0.1 torchvision==0.15.2 accelerate==0.23.0 transformers==4.34.0
!pip install -q diffusers==0.21.4 peft==0.5.0 bitsandbytes==0.41.1
!pip install -q pillow==10.0.1 ftfy==6.1.1 gradio==3.41.2
!pip install -q safetensors==0.3.2 wandb==0.15.12 pyyaml==6.0.1

# Cell 2: Import necessary libraries
import os
import yaml
import math
import random
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Union

import numpy as np
import torch
import torch.nn.functional as F
import torch.utils.checkpoint
from torch.utils.data import Dataset, DataLoader

from accelerate import Accelerator
from accelerate.logging import get_logger
from accelerate.utils import set_seed

import transformers
from transformers import AutoTokenizer, PretrainedConfig, CLIPTextModel

import diffusers
from diffusers import (
    AutoencoderKL,
    DDPMScheduler,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
)
from diffusers.loaders import LoraLoaderMixin
from diffusers.optimization import get_scheduler
from diffusers.utils import check_min_version
from diffusers.utils.import_utils import is_xformers_available

import PIL
from PIL import Image

logger = get_logger(__name__)

# Cell 3: Set up utility functions
def load_config(config_path):
    """Load the configuration from a YAML file"""
    print(f"🔍 Loading configuration from {config_path}...")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    print("✅ Configuration loaded successfully!")
    return config

def setup_logging(logging_dir):
    """Set up logging configuration"""
    os.makedirs(logging_dir, exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(logging_dir, "training.log"))
        ]
    )
    logger.info("Logging setup complete")

# Cell 4: Define the dataset class
class MarketMindDataset(Dataset):
    """Dataset for SDXL LoRA fine-tuning with MarketMind images and captions"""
    
    def __init__(
        self,
        img_folder,
        caption_folder,
        tokenizer,
        tokenizer_2=None,
        width=1024,
        height=1024,
        center_crop=False,
        caption_ext="txt",
        trigger_word="marketmind"
    ):
        self.img_folder = Path(img_folder)
        self.caption_folder = Path(caption_folder)
        self.tokenizer = tokenizer
        self.tokenizer_2 = tokenizer_2 if tokenizer_2 is not None else tokenizer
        self.width = width
        self.height = height
        self.center_crop = center_crop
        self.caption_ext = caption_ext
        self.trigger_word = trigger_word
        
        self.image_paths = list(self.img_folder.glob("*.jpg")) + list(self.img_folder.glob("*.png"))
        print(f"📊 Found {len(self.image_paths)} images in dataset")
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        img_name = img_path.stem
        
        # Load and process image
        image = Image.open(img_path).convert("RGB")
        
        # Resize and potentially crop the image
        if self.center_crop:
            image = self._center_crop_image(image)
        image = image.resize((self.width, self.height), resample=PIL.Image.LANCZOS)
        
        # Convert to numpy and normalize to [0, 1]
        image_array = np.array(image) / 255.0
        image_tensor = torch.from_numpy(image_array).permute(2, 0, 1).float()
        
        # Load caption
        caption_path = self.caption_folder / f"{img_name}.{self.caption_ext}"
        if caption_path.exists():
            with open(caption_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
        else:
            print(f"⚠️ No caption found for {img_name}, using default caption")
            caption = f"[{self.trigger_word}] an advertisement"
            
        # Make sure the caption has the trigger word
        if f"[{self.trigger_word}]" not in caption:
            caption = f"[{self.trigger_word}] {caption}"
            
        # Encode caption for UNet conditioning (SDXL uses two text encoders)
        # First text encoder (CLIP ViT-L)
        tokenizer_output = self.tokenizer(
            caption,
            padding="max_length",
            truncation=True,
            max_length=77,
            return_tensors="pt"
        )
        prompt_embeds_input_ids = tokenizer_output.input_ids[0]
        prompt_embeds_attention_mask = tokenizer_output.attention_mask[0]
        
        # Second text encoder (CLIP ViT-G)
        tokenizer_2_output = self.tokenizer_2(
            caption,
            padding="max_length",
            truncation=True,
            max_length=77,
            return_tensors="pt"
        )
        pooled_prompt_embeds_input_ids = tokenizer_2_output.input_ids[0]
        pooled_prompt_embeds_attention_mask = tokenizer_2_output.attention_mask[0]
        
        return {
            "pixel_values": image_tensor,
            "prompt_embeds_input_ids": prompt_embeds_input_ids,
            "prompt_embeds_attention_mask": prompt_embeds_attention_mask,
            "pooled_prompt_embeds_input_ids": pooled_prompt_embeds_input_ids,
            "pooled_prompt_embeds_attention_mask": pooled_prompt_embeds_attention_mask,
            "caption": caption
        }
        
    def _center_crop_image(self, image):
        """Center crop the image to achieve a square aspect ratio"""
        width, height = image.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        return image.crop((left, top, right, bottom))

# Cell 5: LoRA configuration and implementation
def create_lora_layers(unet, text_encoder=None, text_encoder_2=None, rank=4, alpha=8):
    """Apply LoRA adapters to the model components"""
    from peft import LoraConfig, get_peft_model
    
    # Configure LoRA for UNet
    unet_target_modules = [
        "to_q", "to_k", "to_v", "to_out.0", 
        "proj_in", "proj_out", 
        "ff.net.0.proj", "ff.net.2"
    ]
    
    unet_config = LoraConfig(
        r=rank,
        lora_alpha=alpha,
        target_modules=unet_target_modules,
        lora_dropout=0.0,
        bias="none"
    )
    
    # Apply LoRA to UNet
    unet = get_peft_model(unet, unet_config)
    
    # Apply LoRA to text encoders if requested
    if text_encoder is not None:
        text_encoder_target_modules = ["q_proj", "k_proj", "v_proj", "out_proj"]
        text_encoder_config = LoraConfig(
            r=rank,
            lora_alpha=alpha,
            target_modules=text_encoder_target_modules,
            lora_dropout=0.0,
            bias="none"
        )
        text_encoder = get_peft_model(text_encoder, text_encoder_config)
    
    if text_encoder_2 is not None:
        text_encoder_2_target_modules = ["q_proj", "k_proj", "v_proj", "out_proj"]
        text_encoder_2_config = LoraConfig(
            r=rank,
            lora_alpha=alpha,
            target_modules=text_encoder_2_target_modules,
            lora_dropout=0.0,
            bias="none"
        )
        text_encoder_2 = get_peft_model(text_encoder_2, text_encoder_2_config)
    
    return unet, text_encoder, text_encoder_2

# Cell 6: Training function
def train_model(config):
    """Main training function for SDXL LoRA fine-tuning"""
    
    # Set up accelerator
    accelerator = Accelerator(
        gradient_accumulation_steps=config["train"]["gradient_accumulation_steps"],
        mixed_precision="fp16" if config["dtype"] == "fp16" else "no"
    )
    
    # Make one log on every process with the configuration for debugging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    logger.info(accelerator.state, main_process_only=False)
    
    # Set random seed for reproducibility
    set_seed(config["train"].get("seed", 42))
    
    # Create output directories
    output_dir = Path(config["config"]["training_folder"])
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Load SDXL model components
    print(f"🔄 Loading model components from {config['model']['name_or_path']}...")
    
    # Load VAE
    vae = AutoencoderKL.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="vae",
        revision=config["model"].get("revision", None)
    )
    
    # Load text encoders
    text_encoder = CLIPTextModel.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="text_encoder",
        revision=config["model"].get("revision", None)
    )
    
    text_encoder_2 = CLIPTextModel.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="text_encoder_2",
        revision=config["model"].get("revision", None)
    )
    
    # Load tokenizers
    tokenizer = AutoTokenizer.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="tokenizer",
        use_fast=False,
        revision=config["model"].get("revision", None)
    )
    
    tokenizer_2 = AutoTokenizer.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="tokenizer_2",
        use_fast=False,
        revision=config["model"].get("revision", None)
    )
    
    # Load UNet
    unet = UNet2DConditionModel.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="unet",
        revision=config["model"].get("revision", None)
    )
    
    # Enable xFormers if available
    if is_xformers_available():
        import xformers
        unet.enable_xformers_memory_efficient_attention()
        text_encoder.enable_xformers_memory_efficient_attention()
        text_encoder_2.enable_xformers_memory_efficient_attention()
        print("✅ xFormers enabled for memory-efficient attention")
    
    # Freeze VAE and text encoders
    vae.requires_grad_(False)
    
    # Apply LoRA to UNet and optionally text encoders
    train_text_encoder = config["train"].get("train_text_encoder", False)
    train_text_encoder_2 = config["train"].get("train_text_encoder_2", False)
    
    if not train_text_encoder:
        text_encoder.requires_grad_(False)
    
    if not train_text_encoder_2:
        text_encoder_2.requires_grad_(False)
    
    # Create LoRA layers
    print("🔄 Applying LoRA adapters...")
    rank = config["config"]["network"]["linear"]
    alpha = config["config"]["network"]["linear_alpha"]
    
    unet, text_encoder_lora, text_encoder_2_lora = create_lora_layers(
        unet, 
        text_encoder if train_text_encoder else None,
        text_encoder_2 if train_text_encoder_2 else None,
        rank=rank,
        alpha=alpha
    )
    
    if train_text_encoder:
        text_encoder = text_encoder_lora
    
    if train_text_encoder_2:
        text_encoder_2 = text_encoder_2_lora
    
    # Create noise scheduler
    noise_scheduler = DDPMScheduler.from_pretrained(
        config["model"]["name_or_path"],
        subfolder="scheduler"
    )
    
    # Create dataset and dataloader
    print("🔄 Preparing dataset...")
    dataset = MarketMindDataset(
        img_folder=config["datasets"][0]["folder_path"],
        caption_folder=config["datasets"][0]["caption_folder"],
        tokenizer=tokenizer,
        tokenizer_2=tokenizer_2,
        width=config["datasets"][0].get("width", 1024),
        height=config["datasets"][0].get("height", 1024),
        caption_ext=config["datasets"][0].get("caption_ext", "txt"),
        trigger_word=config["config"]["trigger_word"]
    )
    
    dataloader = DataLoader(
        dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=True,
        num_workers=config["train"].get("num_workers", 2)
    )
    
    # Prepare optimizer
    print("🔄 Setting up optimizer and scheduler...")
    trainable_params = []
    trainable_names = []
    
    # Add UNet parameters
    for name, param in unet.named_parameters():
        if param.requires_grad:
            trainable_params.append(param)
            trainable_names.append(f"unet.{name}")
    
    # Add text encoder parameters if needed
    if train_text_encoder:
        for name, param in text_encoder.named_parameters():
            if param.requires_grad:
                trainable_params.append(param)
                trainable_names.append(f"text_encoder.{name}")
    
    if train_text_encoder_2:
        for name, param in text_encoder_2.named_parameters():
            if param.requires_grad:
                trainable_params.append(param)
                trainable_names.append(f"text_encoder_2.{name}")
    
    # Print number of trainable parameters
    trainable_params_count = sum(p.numel() for p in trainable_params)
    print(f"🔢 Number of trainable parameters: {trainable_params_count:,}")
    
    # Create optimizer
    optimizer_class = torch.optim.AdamW
    optimizer = optimizer_class(
        trainable_params,
        lr=float(config["train"]["lr"]),
        betas=(0.9, 0.999),
        weight_decay=config["train"].get("weight_decay", 1e-2),
        eps=config["train"].get("adam_epsilon", 1e-8)
    )
    
    # Prepare for training with accelerator
    unet, optimizer, dataloader = accelerator.prepare(unet, optimizer, dataloader)
    
    if train_text_encoder:
        text_encoder = accelerator.prepare(text_encoder)
    
    if train_text_encoder_2:
        text_encoder_2 = accelerator.prepare(text_encoder_2)
    
    # Move VAE and text encoders to device
    vae = vae.to(accelerator.device)
    if not train_text_encoder:
        text_encoder = text_encoder.to(accelerator.device)
    if not train_text_encoder_2:
        text_encoder_2 = text_encoder_2.to(accelerator.device)
    
    # Create learning rate scheduler
    lr_scheduler = get_scheduler(
        config["train"].get("lr_scheduler", "cosine"),
        optimizer=optimizer,
        num_warmup_steps=int(config["train"].get("warmup_steps", 0)),
        num_training_steps=config["train"]["steps"]
    )
    
    # Prepare lr_scheduler with accelerator
    lr_scheduler = accelerator.prepare(lr_scheduler)
    
    # Track global progress
    global_step = 0
    progress_bar = transformers.tqdm(
        range(config["train"]["steps"]),
        disable=not accelerator.is_local_main_process
    )
    progress_bar.set_description("Training steps")
    
    # Training loop
    print("🚀 Starting training loop...")
    unet.train()
    if train_text_encoder:
        text_encoder.train()
    if train_text_encoder_2:
        text_encoder_2.train()
    
    # Main training loop
    while global_step < config["train"]["steps"]:
        for batch in dataloader:
            # Skip if we've reached max steps
            if global_step >= config["train"]["steps"]:
                break
            
            with accelerator.accumulate(unet):
                # Get input tensors
                pixel_values = batch["pixel_values"].to(accelerator.device)
                
                # Get text embeddings for conditioning
                with torch.no_grad():
                    if train_text_encoder:
                        prompt_embeds = text_encoder(
                            input_ids=batch["prompt_embeds_input_ids"].to(accelerator.device),
                            attention_mask=batch["prompt_embeds_attention_mask"].to(accelerator.device)
                        )[0]
                    else:
                        prompt_embeds = text_encoder(
                            input_ids=batch["prompt_embeds_input_ids"].to(accelerator.device),
                            attention_mask=batch["prompt_embeds_attention_mask"].to(accelerator.device)
                        )[0]
                    
                    if train_text_encoder_2:
                        pooled_prompt_embeds = text_encoder_2(
                            input_ids=batch["pooled_prompt_embeds_input_ids"].to(accelerator.device),
                            attention_mask=batch["pooled_prompt_embeds_attention_mask"].to(accelerator.device)
                        )[0]
                    else:
                        pooled_prompt_embeds = text_encoder_2(
                            input_ids=batch["pooled_prompt_embeds_input_ids"].to(accelerator.device),
                            attention_mask=batch["pooled_prompt_embeds_attention_mask"].to(accelerator.device)
                        )[0]
                
                # Convert images to latent space
                with torch.no_grad():
                    latents = vae.encode(pixel_values).latent_dist.sample()
                    latents = latents * vae.config.scaling_factor
                
                # Add noise to latents
                noise = torch.randn_like(latents)
                bsz = latents.shape[0]
                timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device)
                latents = noise_scheduler.add_noise(latents, noise, timesteps)
                
                # Predict the noise residual
                added_cond_kwargs = {"text_embeds": pooled_prompt_embeds, "time_ids": torch.zeros(bsz, 2).to(accelerator.device)}
                
                model_pred = unet(
                    latents,
                    timesteps,
                    encoder_hidden_states=prompt_embeds,
                    added_cond_kwargs=added_cond_kwargs
                ).sample
                
                # Get the target for loss calculation
                target = noise
                
                # Calculate loss
                loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")
                
                # Backward pass and optimizer step
                accelerator.backward(loss)
                
                if accelerator.sync_gradients:
                    params_to_clip = trainable_params
                    accelerator.clip_grad_norm_(params_to_clip, config["train"].get("max_grad_norm", 1.0))
                
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad(set_to_none=True)
            
            # Log progress
            if global_step % config["config"].get("performance_log_every", 10) == 0:
                logs = {"loss": loss.detach().item(), "lr": lr_scheduler.get_last_lr()[0]}
                progress_bar.set_postfix(**logs)
                accelerator.log(logs, step=global_step)
            
            # Save checkpoint
            if global_step % config["save"].get("save_every", 500) == 0 and global_step > 0:
                save_checkpoint(
                    accelerator, unet, text_encoder if train_text_encoder else None,
                    text_encoder_2 if train_text_encoder_2 else None, 
                    tokenizer, tokenizer_2, global_step, output_dir, config
                )
            
            # Generate sample images
            if global_step % config["sample"].get("sample_every", 500) == 0:
                generate_samples(
                    accelerator, unet, vae, text_encoder, text_encoder_2,
                    tokenizer, tokenizer_2, global_step, output_dir, config
                )
            
            progress_bar.update(1)
            global_step += 1
    
    # Save the final model
    save_checkpoint(
        accelerator, unet, text_encoder if train_text_encoder else None,
        text_encoder_2 if train_text_encoder_2 else None, 
        tokenizer, tokenizer_2, global_step, output_dir, config, is_final=True
    )
    
    print("✅ Training complete!")

# Cell 7: Function to save checkpoints
def save_checkpoint(accelerator, unet, text_encoder, text_encoder_2, tokenizer, tokenizer_2, 
                   global_step, output_dir, config, is_final=False):
    """Save a training checkpoint or the final model"""
    
    # Wait for all processes to sync
    accelerator.wait_for_everyone()
    
    # Determine save directory
    if is_final:
        save_dir = output_dir / f"{config['config']['name']}_final"
    else:
        save_dir = output_dir / f"checkpoint-{global_step}"
    
    # Create directory
    os.makedirs(save_dir, exist_ok=True)
    
    # Get unwrapped models
    unet_lora = accelerator.unwrap_model(unet)
    
    # Save LoRA weights for UNet
    unet_lora_state_dict = get_peft_model_state_dict(unet_lora)
    
    # Save state dicts
    if accelerator.is_main_process:
        print(f"💾 Saving checkpoint to {save_dir}")
        
        # Save UNet LoRA weights
        torch.save(unet_lora_state_dict, save_dir / "unet_lora_state_dict.safetensors")
        
        # Save text encoder LoRA weights if trained
        if text_encoder is not None:
            text_encoder_lora = accelerator.unwrap_model(text_encoder)
            text_encoder_lora_state_dict = get_peft_model_state_dict(text_encoder_lora)
            torch.save(text_encoder_lora_state_dict, save_dir / "text_encoder_lora_state_dict.safetensors")
        
        if text_encoder_2 is not None:
            text_encoder_2_lora = accelerator.unwrap_model(text_encoder_2)
            text_encoder_2_lora_state_dict = get_peft_model_state_dict(text_encoder_2_lora)
            torch.save(text_encoder_2_lora_state_dict, save_dir / "text_encoder_2_lora_state_dict.safetensors")
            
        # Save tokenizers
        tokenizer.save_pretrained(save_dir / "tokenizer")
        tokenizer_2.save_pretrained(save_dir / "tokenizer_2")
        
        # Save configuration
        with open(save_dir / "config.yaml", "w") as f:
            yaml.dump(config, f)
    
    # Cleanup old checkpoints if needed and not final save
    if not is_final and accelerator.is_main_process:
        checkpoints = sorted(
            [d for d in output_dir.glob("checkpoint-*") if d.is_dir()],
            key=lambda d: int(d.name.split("-")[1])
        )
        
        # Keep only the specified number of checkpoints
        max_checkpoints = config["save"].get("max_step_saves_to_keep", 5)
        if len(checkpoints) > max_checkpoints:
            for old_checkpoint in checkpoints[:-max_checkpoints]:
                import shutil
                shutil.rmtree(old_checkpoint)
                print(f"🗑️ Removed old checkpoint: {old_checkpoint}")

# Cell 8: Helper function to get PEFT model state dict
def get_peft_model_state_dict(model):
    """Extract the LoRA state dictionary from a PEFT model"""
    state_dict = {}
    
    # Iterate through named parameters
    for name, param in model.named_parameters():
        if "lora" in name:
            state_dict[name] = param.data.cpu().clone()
            
    return state_dict

# Cell 9: Function to generate samples during training
def generate_samples(accelerator, unet, vae, text_encoder, text_encoder_2, 
                     tokenizer, tokenizer_2, global_step, output_dir, config):
    """Generate sample images during training"""
    
    if accelerator.is_main_process:
        print(f"🖼️ Generating samples at step {global_step}")
        
        # Create pipeline for inference
        pipeline = StableDiffusionXLPipeline.from_pretrained(
            config["model"]["name_or_path"],
            unet=accelerator.unwrap_model(unet),
            text_encoder=accelerator.unwrap_model(text_encoder),
            text_encoder_2=accelerator.unwrap_model(text_encoder_2),
            vae=vae,
            torch_dtype=torch.float16 if config["dtype"] == "fp16" else torch.float32,
            revision=config["model"].get("revision", None)
        )
        
        # Enable memory-efficient attention
        if is_xformers_available():
            pipeline.enable_xformers_memory_efficient_attention()
        
        # Move to accelerator device
        pipeline = pipeline.to(accelerator.device)
        
        # Set to eval mode for inference
        pipeline.unet.eval()
        pipeline.text_encoder.eval()
        pipeline.text_encoder_2.eval()
        
        # Create samples directory
        samples_dir = output_dir / "samples"
        os.makedirs(samples_dir, exist_ok=True)
        
        # Generate images for each prompt
        for i, prompt in enumerate(config["sample"]["prompts"]):
            # Set seed for reproducibility
            base_seed = config["sample"].get("seed", 42)
            
            if config["sample"].get("walk_seed", True):
                seed = base_seed + global_step // config["sample"].get("sample_every", 500) + i
            else:
                seed = base_seed + i
            
            generator = torch.Generator(device=accelerator.device).manual_seed(seed)
            
            # Generate image
            image = pipeline(
                prompt=prompt,
                negative_prompt=config["sample"].get("neg", ""),
                generator=generator,
                num_inference_steps=config["sample"].get("sample_steps", 30),
                guidance_scale=config["sample"].get("guidance_scale", 7.5)
            ).images[0]
            
            # Save image
            sample_path = samples_dir / f"step_{global_step:06d}_prompt_{i:02d}.png"
            image.save(sample_path)
            print(f"  📄 Saved sample to {sample_path}")
        
        # Clean up memory
        del pipeline
        torch.cuda.empty_cache()

# Cell 10: Main execution code
if __name__ == "__main__":
    print("🚀 Starting SDXL LoRA fine-tuning for MarketMind")
    
    # Load configuration
    config_path = "sdxl_lora_config.yaml"
    config = load_config(config_path)
    
    # Set up logging
    setup_logging(Path(config["config"]["training_folder"]) / "logs")
    
    # Start training
    train_model(config)
