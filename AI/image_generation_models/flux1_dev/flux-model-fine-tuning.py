# FLUX.1-dev Fine-Tuning with LoRA
# This notebook provides a comprehensive implementation for fine-tuning the FLUX.1-dev model using LoRA

# Required installations
!pip install -q torch transformers safetensors accelerate diffusers bitsandbytes pyyaml tqdm joblib

# Import necessary libraries
import os
import yaml
import torch
import joblib
import shutil
import numpy as np
from pathlib import Path
from tqdm.auto import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from diffusers import AutoencoderKL, DDPMScheduler, FlowMatchScheduler
from diffusers.models.attention_processor import LoRAAttnProcessor
from diffusers.optimization import get_scheduler
from diffusers import FluxModelPipeline

print("📚 Libraries imported successfully!")

# Set up device and paths
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️ Using device: {device}")

# Configuration loading function
def load_config(config_path):
    """Load configuration from YAML file"""
    print(f"🔍 Loading configuration from {config_path}...")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    print("✅ Configuration loaded successfully!")
    return config

# Function to download and cache the model
def get_or_load_model(model_id, auth_token=None, cache_dir="./model_cache"):
    """Download model if not cached, or load from cache"""
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, model_id.split("/")[-1])
    
    if os.path.exists(cache_path):
        print(f"🔄 Loading model from cache: {cache_path}")
        pipeline = FluxModelPipeline.from_pretrained(cache_path, local_files_only=True)
    else:
        print(f"⬇️ Downloading model from Hugging Face: {model_id}")
        pipeline = FluxModelPipeline.from_pretrained(
            model_id,
            use_auth_token=auth_token,
            torch_dtype=torch.float16
        )
        print(f"💾 Saving model to cache: {cache_path}")
        pipeline.save_pretrained(cache_path)
    
    return pipeline

# Dataset class for image-caption pairs
class FluxDataset(Dataset):
    def __init__(self, img_folder, caption_folder, tokenizer, image_size=1024, caption_ext="txt"):
        """
        Dataset for FLUX model fine-tuning
        
        Args:
            img_folder: Path to folder containing images
            caption_folder: Path to folder containing captions
            tokenizer: Tokenizer for processing captions
            image_size: Size for resizing images
            caption_ext: File extension for caption files
        """
        super().__init__()
        self.img_folder = Path(img_folder)
        self.caption_folder = Path(caption_folder)
        self.tokenizer = tokenizer
        self.image_size = image_size
        self.caption_ext = caption_ext
        
        # Get all image files
        self.image_files = [f for f in self.img_folder.glob("*") if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        print(f"📁 Found {len(self.image_files)} images in dataset")
    
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        img_name = img_path.stem
        
        # Load image
        image = Image.open(img_path).convert("RGB")
        
        # Resize image if needed
        if image.width != self.image_size or image.height != self.image_size:
            image = image.resize((self.image_size, self.image_size), Image.LANCZOS)
        
        # Convert to tensor and normalize
        image = np.array(image) / 255.0
        image = torch.from_numpy(image).permute(2, 0, 1).float()
        
        # Load caption
        caption_path = self.caption_folder / f"{img_name}.{self.caption_ext}"
        if caption_path.exists():
            with open(caption_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
        else:
            print(f"⚠️ No caption found for {img_name}, using empty string")
            caption = ""
        
        # Tokenize caption
        tokens = self.tokenizer(
            caption,
            padding="max_length",
            truncation=True,
            max_length=77,
            return_tensors="pt"
        )
        
        return {
            "image": image,
            "input_ids": tokens.input_ids[0],
            "attention_mask": tokens.attention_mask[0],
            "caption": caption
        }

# Helper function to prepare LoRA for model
def add_lora_to_model(pipeline, lora_rank=32, lora_alpha=32):
    """Add LoRA adapters to the model's attention layers"""
    print(f"🔧 Adding LoRA layers with rank={lora_rank}, alpha={lora_alpha}")
    
    # Add LoRA to UNet
    for name, module in pipeline.unet.named_modules():
        if "attn" in name:
            if hasattr(module, "to_q") and hasattr(module, "to_k") and hasattr(module, "to_v"):
                module.to_q = LoRAAttnProcessor(
                    hidden_size=module.to_q.in_features,
                    cross_attention_dim=None,
                    rank=lora_rank,
                    alpha=lora_alpha
                )
                module.to_k = LoRAAttnProcessor(
                    hidden_size=module.to_k.in_features,
                    cross_attention_dim=None,
                    rank=lora_rank,
                    alpha=lora_alpha
                )
                module.to_v = LoRAAttnProcessor(
                    hidden_size=module.to_v.in_features,
                    cross_attention_dim=None,
                    rank=lora_rank,
                    alpha=lora_alpha
                )
                module.to_out = LoRAAttnProcessor(
                    hidden_size=module.to_out[0].in_features,
                    cross_attention_dim=None,
                    rank=lora_rank,
                    alpha=lora_alpha
                )
    
    # Optional: Add LoRA to text encoder if specified in config
    # Implementation would be similar to above
    
    print("✅ LoRA layers added successfully!")
    return pipeline

# Training function
def train_model(pipeline, dataset, config):
    """Main training function for FLUX model fine-tuning"""
    # Create data loader
    dataloader = DataLoader(
        dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=True,
        num_workers=2
    )
    
    # Set up optimizer
    trainable_params = []
    for name, param in pipeline.unet.named_parameters():
        if "lora" in name:
            param.requires_grad = True
            trainable_params.append(param)
        else:
            param.requires_grad = False
    
    if config["train"].get("train_text_encoder", False):
        for name, param in pipeline.text_encoder.named_parameters():
            if "lora" in name:
                param.requires_grad = True
                trainable_params.append(param)
            else:
                param.requires_grad = False
    
    # Set up optimizer based on config
    optimizer_name = config["train"].get("optimizer", "adamw8bit")
    if optimizer_name == "adamw8bit":
        import bitsandbytes as bnb
        optimizer = bnb.optim.AdamW8bit(
            trainable_params,
            lr=float(config["train"]["lr"]),
            betas=(0.9, 0.999),
            weight_decay=0.01
        )
    else:
        optimizer = torch.optim.AdamW(
            trainable_params,
            lr=float(config["train"]["lr"]),
            betas=(0.9, 0.999),
            weight_decay=0.01
        )
    
    # Set up scheduler
    scheduler_name = config["train"].get("noise_scheduler", "flowmatch")
    if scheduler_name == "flowmatch":
        noise_scheduler = FlowMatchScheduler(
            num_train_timesteps=1000,
            sigma_min=0.002,
            sigma_max=80.0
        )
    else:
        noise_scheduler = DDPMScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            num_train_timesteps=1000
        )
    
    # Set up learning rate scheduler
    lr_scheduler = get_scheduler(
        name="cosine",
        optimizer=optimizer,
        num_warmup_steps=int(0.05 * config["train"]["steps"]),
        num_training_steps=config["train"]["steps"]
    )
    
    # EMA setup if enabled
    if config.get("ema_config", {}).get("use_ema", False):
        from torch_ema import ExponentialMovingAverage
        ema_decay = config["ema_config"].get("ema_decay", 0.99)
        ema = ExponentialMovingAverage(trainable_params, decay=ema_decay)
        print(f"📉 Using EMA with decay {ema_decay}")
    else:
        ema = None
    
    # Initialize progress bar
    progress_bar = tqdm(range(config["train"]["steps"]), desc="Training progress")
    
    # Create output directories
    output_dir = Path(config["config"]["training_folder"])
    output_dir.mkdir(exist_ok=True, parents=True)
    samples_dir = output_dir / "samples"
    samples_dir.mkdir(exist_ok=True)
    checkpoints_dir = output_dir / "checkpoints"
    checkpoints_dir.mkdir(exist_ok=True)
    
    # Track global step
    global_step = 0
    
    # Training loop
    print("🚀 Starting training loop...")
    while global_step < config["train"]["steps"]:
        for batch in dataloader:
            # Skip if we've reached the maximum steps
            if global_step >= config["train"]["steps"]:
                break
            
            # Move batch to device
            pixel_values = batch["image"].to(device)
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            
            # Forward pass through text encoder
            with torch.no_grad():
                text_embeds = pipeline.text_encoder(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )[0]
            
            # Prepare latents
            with torch.no_grad():
                latents = pipeline.vae.encode(pixel_values).latent_dist.sample()
                latents = latents * pipeline.vae.config.scaling_factor
            
            # Add noise to latents
            noise = torch.randn_like(latents)
            timesteps = torch.randint(
                0, noise_scheduler.config.num_train_timesteps, 
                (latents.shape[0],), device=device
            )
            noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)
            
            # Forward pass through UNet
            model_pred = pipeline.unet(
                noisy_latents,
                timesteps,
                encoder_hidden_states=text_embeds
            ).sample
            
            # Calculate loss based on scheduler
            if isinstance(noise_scheduler, FlowMatchScheduler):
                target = noise_scheduler.get_velocity(latents, noise, timesteps)
                loss = torch.nn.functional.mse_loss(model_pred, target, reduction="mean")
            else:
                if config["train"].get("prediction_type", "epsilon") == "v_prediction":
                    target = noise_scheduler.get_velocity(latents, noise, timesteps)
                else:
                    target = noise
                loss = torch.nn.functional.mse_loss(model_pred, target, reduction="mean")
            
            # Backward pass
            loss.backward()
            
            # Optimizer step
            if ((global_step + 1) % config["train"].get("gradient_accumulation_steps", 1) == 0):
                torch.nn.utils.clip_grad_norm_(trainable_params, 1.0)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()
                
                # Update EMA if enabled
                if ema is not None:
                    ema.update()
            
            # Log progress
            if global_step % config["config"].get("performance_log_every", 100) == 0:
                print(f"Step {global_step}: loss = {loss.item():.4f}, lr = {lr_scheduler.get_last_lr()[0]:.6f}")
            
            # Generate samples
            if global_step % config["sample"].get("sample_every", 250) == 0:
                print(f"🖼️ Generating samples at step {global_step}...")
                pipeline.unet.eval()
                
                # Use EMA weights if available
                if ema is not None:
                    with ema.average_parameters():
                        generate_samples(pipeline, config, global_step, samples_dir)
                else:
                    generate_samples(pipeline, config, global_step, samples_dir)
                
                pipeline.unet.train()
            
            # Save checkpoint
            if global_step % config["save"].get("save_every", 250) == 0:
                print(f"💾 Saving checkpoint at step {global_step}...")
                save_checkpoint(pipeline, global_step, config, checkpoints_dir, ema)
            
            # Update progress bar
            progress_bar.update(1)
            global_step += 1
    
    # Save final model
    print("🏁 Training complete! Saving final model...")
    save_final_model(pipeline, config, output_dir, ema)
    
    return pipeline

# Function to generate samples during training
def generate_samples(pipeline, config, global_step, samples_dir):
    """Generate and save sample images during training"""
    prompts = config["sample"]["prompts"]
    negative_prompt = config["sample"].get("neg", "")
    guidance_scale = config["sample"].get("guidance_scale", 4.0)
    num_steps = config["sample"].get("sample_steps", 20)
    
    # Generate images
    with torch.no_grad():
        for i, prompt in enumerate(prompts):
            # Set seed
            seed = config["sample"].get("seed", 42)
            if config["sample"].get("walk_seed", True):
                seed += global_step // config["sample"].get("sample_every", 250) + i
            
            generator = torch.Generator(device=device).manual_seed(seed)
            
            # Generate image
            image = pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_steps,
                generator=generator,
                width=config["sample"].get("width", 1024),
                height=config["sample"].get("height", 1024)
            ).images[0]
            
            # Save image
            sample_path = samples_dir / f"step_{global_step:06d}_prompt_{i:02d}.png"
            image.save(sample_path)
            print(f"  Saved sample to {sample_path}")

# Function to save checkpoint during training
def save_checkpoint(pipeline, global_step, config, checkpoints_dir, ema=None):
    """Save training checkpoint"""
    checkpoint_dir = checkpoints_dir / f"checkpoint-{global_step}"
    checkpoint_dir.mkdir(exist_ok=True)
    
    # Save LoRA weights
    lora_state_dict = {}
    for name, param in pipeline.unet.named_parameters():
        if "lora" in name:
            lora_state_dict[name] = param.data.cpu().clone()
    
    if config["train"].get("train_text_encoder", False):
        for name, param in pipeline.text_encoder.named_parameters():
            if "lora" in name:
                lora_state_dict[f"text_encoder.{name}"] = param.data.cpu().clone()
    
    # Save EMA state if used
    if ema is not None:
        ema_state_dict = {}
        for i, (name, _) in enumerate(ema.averaged_params):
            ema_state_dict[f"ema_{i}"] = ema.shadow_params[i].data.cpu().clone()
        torch.save(ema_state_dict, checkpoint_dir / "ema_state.bin")
    
    # Save model weights using joblib
    joblib.dump(lora_state_dict, checkpoint_dir / "lora_weights.joblib")
    
    # Save optimizer and scheduler state
    # (implementation would depend on specific requirements)
    
    print(f"  Checkpoint saved to {checkpoint_dir}")
    
    # Cleanup old checkpoints if needed
    max_saves = config["save"].get("max_step_saves_to_keep", 5)
    if max_saves > 0:
        checkpoints = sorted(
            [d for d in checkpoints_dir.glob("checkpoint-*") if d.is_dir()],
            key=lambda d: int(d.name.split("-")[1])
        )
        for old_checkpoint in checkpoints[:-max_saves]:
            shutil.rmtree(old_checkpoint)
            print(f"  Removed old checkpoint: {old_checkpoint}")

# Function to save the final fine-tuned model
def save_final_model(pipeline, config, output_dir, ema=None):
    """Save the final fine-tuned model"""
    final_dir = output_dir / f"{config['config']['name']}_final"
    final_dir.mkdir(exist_ok=True)
    
    # Save LoRA weights
    lora_state_dict = {}
    for name, param in pipeline.unet.named_parameters():
        if "lora" in name:
            lora_state_dict[name] = param.data.cpu().clone()
    
    if config["train"].get("train_text_encoder", False):
        for name, param in pipeline.text_encoder.named_parameters():
            if "lora" in name:
                lora_state_dict[f"text_encoder.{name}"] = param.data.cpu().clone()
    
    # Convert to specified dtype
    dtype = config["save"].get("dtype", "float16")
    if dtype == "float16":
        for k, v in lora_state_dict.items():
            lora_state_dict[k] = v.half()
    
    # Save full model if needed
    # (This would be a larger implementation that merges LoRA weights with base model)
    
    # Save LoRA adapter with joblib
    joblib.dump(lora_state_dict, final_dir / "lora_weights.joblib")
    
    # Save configuration
    with open(final_dir / "config.yaml", "w") as f:
        yaml.dump(config, f)
    
    # Save EMA state if used
    if ema is not None:
        ema_state_dict = {}
        for i, (name, _) in enumerate(ema.averaged_params):
            ema_state_dict[f"ema_{i}"] = ema.shadow_params[i].data.cpu().clone()
        torch.save(ema_state_dict, final_dir / "ema_state.bin")
    
    print(f"✅ Final model saved to {final_dir}")
    return final_dir

# Main execution
if __name__ == "__main__":
    print("🌟 Starting FLUX.1-dev fine-tuning with LoRA")
    
    # Load configuration from YAML file
    config = load_config("flux_fine_tuning_config.yaml")
    
    # Get access token either from config or environment variable
    access_token = os.environ.get("HF_ACCESS_TOKEN", None)
    
    # Download or load model
    pipeline = get_or_load_model(
        "black-forest-labs/FLUX.1-dev",
        auth_token=access_token
    )
    
    # Move model to device
    pipeline = pipeline.to(device)
    
    # Add LoRA to model
    lora_rank = config["config"]["network"]["linear"]
    lora_alpha = config["config"]["network"]["linear_alpha"]
    pipeline = add_lora_to_model(pipeline, lora_rank, lora_alpha)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
    
    # Create dataset
    dataset = FluxDataset(
        img_folder=config["datasets"][0]["folder_path"],
        caption_folder=config["datasets"][0].get("caption_folder", config["datasets"][0]["folder_path"]),
        tokenizer=tokenizer,
        image_size=1024,
        caption_ext=config["datasets"][0].get("caption_ext", "txt")
    )
    
    # Train model
    pipeline = train_model(pipeline, dataset, config)
    
    print("🎉 Fine-tuning complete!")

# Note: This code requires additional imports that would be added at runtime
# from PIL import Image
# import torch_ema (if EMA is enabled)
