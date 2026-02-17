import streamlit as st
from gradio_client import Client, handle_file

client = Client("finegrain/finegrain-image-enhancer")

# --- Sabse Aggressive Settings ---
def force_iphone_magic(img_path):
    print("🔥 AI ko dhakka maar raha hoon pixels change karne ke liye...")
    
    result = client.predict(
        input_image=handle_file(img_path),
        # Prompt ko 'Hyper-Realistic' kiya hai
        prompt="ultra-detailed, 8k, sharp focus, cinematic, iphone 17 pro max, realistic skin, pores, highly defined hair", 
        negative_prompt="blurry, low quality, same as input, no change, cartoon",
        seed=42,
        upscale_factor=2,
        controlnet_scale=0.9,   # Isse image ka structure tight hoga
        controlnet_decay=1.0,
        condition_scale=15.0,   # AI ko majboor karne ke liye (Max value ke paas)
        tile_width=112,
        tile_height=144,
        denoise_strength=0.9,   # AGAR YE 0.9 HAI TOH CHANGE HONA HI HOGA!
        num_inference_steps=25,
        solver="DDIM",
        api_name="/process"
    )
    return result[0] if isinstance(result, list) else result
