import streamlit as st
from gradio_client import Client, handle_file
import os

# --- APP UI ---
st.set_page_config(page_title="iPhone 17 Pro Max AI", page_icon="🔥")
st.title("🔥 Oppo to iPhone: Real Pixel Generator")
st.write("Bhai, agar pehle enhance nahi ho raha tha, toh ab hoga! (Fixed Logic)")

# --- SIDEBAR SETTINGS (Exact as per your Screenshot) ---
st.sidebar.header("🔧 Pro Settings")
u_factor = st.sidebar.slider("Upscale Factor", 1, 4, 2)
c_scale = st.sidebar.slider("ControlNet Scale", 0.0, 1.5, 0.8) # Badha diya 0.6 se 0.8 taaki details aayein
d_strength = st.sidebar.slider("Denoise Strength", 0.0, 1.0, 0.5) # Isse 'Zero Enhance' problem fix hogi
steps = st.sidebar.slider("Inference Steps", 1, 30, 20)

# --- FILE UPLOAD ---
img_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Save file locally for processing
    with open("input.jpg", "wb") as f:
        f.write(img_file.getbuffer())
    
    if st.button("🚀 Enhance Now"):
        with st.spinner("AI is hallucinating new pixels..."):
            try:
                client = Client("finegrain/finegrain-image-enhancer")
                
                # 💡 THE FIX: Prompt ko aur deep banaya hai taaki AI 'soye' na
                result = client.predict(
                    input_image=handle_file("input.jpg"),
                    prompt="ultra high definition, extremely detailed skin pores, 8k resolution, sharp focus, cinematic, shot on iphone 17 pro max, realistic textures",
                    negative_prompt="blurry, low quality, noise, grain, cartoon, painting, digital art, smooth skin, plastic look",
                    seed=42,
                    upscale_factor=u_factor,
                    controlnet_scale=c_scale,
                    controlnet_decay=1.0,
                    condition_scale=10.0, # 6 se badha kar 10 kiya taaki prompt ka asar dikhe
                    tile_width=112,
                    tile_height=144,
                    denoise_strength=d_strength,
                    num_inference_steps=steps,
                    solver="DDIM",
                    api_name="/process"
                )
                
                # Handling the output list
                output_path = result[0] if isinstance(result, list) else result
                
                if output_path:
                    st.image(output_path, caption="iPhone Level Quality")
                    with open(output_path, "rb") as file:
                        st.download_button("📥 Download Photo", file, file_name="enhanced.jpg")
                else:
                    st.error("Bhai, server ne blank image di hai. Parameters check kar!")
                    
            except Exception as e:
                st.error(f"Galti ho gayi: {e}")

