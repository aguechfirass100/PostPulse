import numpy as np
import base64
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class ImageGenerator:
    """
    Mock image generator class that creates images based on user prompts.
    In a real application, this would integrate with an ML model like DALL-E or Stable Diffusion.
    """
    
    @staticmethod
    def generate_image(prompt, width=512, height=512):
        """
        Generate an image based on the text prompt.
        This is a mock implementation that creates a gradient image with the prompt text.
        
        Args:
            prompt (str): Text description of the image to generate
            width (int): Width of the output image
            height (int): Height of the output image
            
        Returns:
            str: Base64 encoded image data
        """
        try:
            # Create a gradient background
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Generate colors based on prompt hash for deterministic but varied results
            prompt_hash = sum(ord(c) for c in prompt)
            r_start = (prompt_hash * 123) % 256
            g_start = (prompt_hash * 456) % 256
            b_start = (prompt_hash * 789) % 256
            
            r_end = (r_start + 100) % 256
            g_end = (g_start + 100) % 256
            b_end = (b_start + 100) % 256
            
            # Draw gradient
            for y in range(height):
                r = int(r_start + (r_end - r_start) * y / height)
                g = int(g_start + (g_end - g_start) * y / height)
                b = int(b_start + (b_end - b_start) * y / height)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add some random shapes based on prompt
            for i in range(5):
                shape_type = (prompt_hash + i * i) % 3
                x1 = (prompt_hash * (i+1) * 13) % width
                y1 = (prompt_hash * (i+1) * 17) % height
                x2 = (x1 + 50 + (prompt_hash * (i+1) * 7) % 150) % width
                y2 = (y1 + 50 + (prompt_hash * (i+1) * 11) % 150) % height
                
                fill_color = (
                    (r_end + i * 30) % 256,
                    (g_end + i * 30) % 256,
                    (b_end + i * 30) % 256,
                    128  # Alpha for transparency
                )
                
                if shape_type == 0:
                    # Circle
                    draw.ellipse([x1, y1, x2, y2], fill=fill_color)
                elif shape_type == 1:
                    # Rectangle
                    draw.rectangle([x1, y1, x2, y2], fill=fill_color)
                else:
                    # Polygon
                    points = [
                        x1, y1,
                        x2, y1,
                        x2, y2,
                        x1 + (x2-x1)//2, y2 + (y2-y1)//2,
                        x1, y2
                    ]
                    draw.polygon(points, fill=fill_color)
            
            # Apply some filters
            image = image.filter(ImageFilter.GaussianBlur(radius=2))
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Add the prompt as text
            try:
                # Use a default font
                draw = ImageDraw.Draw(image)
                font_size = 20
                text_position = (width // 10, height // 10)
                
                # Wrap text to fit in the image
                max_width = width - 2 * text_position[0]
                words = prompt.split()
                lines = []
                current_line = []
                
                for word in words:
                    current_line.append(word)
                    text = ' '.join(current_line)
                    # Estimate text width (rough approximation)
                    estimated_width = len(text) * (font_size * 0.6)
                    
                    if estimated_width > max_width:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw each line of text
                y_text = text_position[1]
                for line in lines:
                    draw.text((text_position[0], y_text), line, fill="white")
                    y_text += font_size + 5  # Add spacing between lines
            except Exception as e:
                print(f"Error adding text to image: {e}")
                
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return a simple error image
            error_img = Image.new('RGB', (width, height), (255, 0, 0))
            buffered = io.BytesIO()
            error_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str