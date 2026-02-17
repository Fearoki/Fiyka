import streamlit as st
from gradio_client import Client, handle_file
import os

# --- Page Config ---
st.set_page_config(page_title="iPhone 17 Pro Max AI", page_icon="📸")
st.title("📸 Oppo A15s to iPhone 17 Pro Max")
st.write("Bhai, agar ab change nahi hua toh bataiyo, pura system hila denge! 😤")

# --- UI Layout ---
col1, col2 = st.columns(2)

with st.sidebar:
    st.header("🔧 Magic Settings")
    # Maine ye values wahi rakhi hain jo tere screenshot mein thin, par thoda 'Force' badha diya hai
    u_factor = st.slider("Upscale (Size)", 1, 4, 2)
    d_strength = st.slider("Denoise (Isse Details Aayengi)", 0.0, 1.0, 0.70) # 0.70 is the sweet spot!
    c_scale = st.slider("AI Creativity", 1, 20, 15)
    steps = st.slider("Quality Steps", 1, 50, 20)

# --- Logic ---
uploaded_file = st.file_uploader("Apni Grainy Photo Yahan Daalo...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # 1. Temporary file save karo
    with open("input_img.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Bhai photo mil gayi, ab iPhone banate hain...")

    if st.button("✨ Convert to iPhone Quality"):
        with st.spinner("AI naye pixels generate kar raha hai... Thoda wait kar bhai!"):
            try:
                # 2. Connection to Finegrain API
                client = Client("finegrain/finegrain-image-enhancer")
                
                # 3. AI Prediction (The Magic Part)
                result = client.predict(
                    input_image=handle_file("input_img.jpg"),
                    # Ye prompt AI ko majboor karega ki woh iPhone ka sensor imitate kare
                    prompt="masterpiece, best quality, ultra-detailed, 8k uhd, iphone 17 pro max cinematic shot, highly defined skin texture, sharp eyes, professional photography",
                    negative_prompt="blurry, low quality, noise, grain, cartoon, plastic skin, painting, out of focus, no change",
                    seed=42,
                    upscale_factor=u_factor,
                    controlnet_scale=0.8, # Texture tight karne ke liye
                    controlnet_decay=1.0,
                    condition_scale=c_scale,
                    tile_width=112,
                    tile_height=144,
                    denoise_strength=d_strength, # AGAR YE 0.7 HAI TOH CHANGE PAKKA HOGA!
                    num_inference_steps=steps,
                    solver="DDIM",
                    api_name="/process"
                )

                # 4. Result Handling
                output_image = result[0] if isinstance(result, list) else result
                
                if output_image:
                    st.success("✅ Oteri! Dekh bhai, pixels chamak gaye!")
                    st.image(output_image, caption="iPhone 17 Pro Max Result")
                    
                    # Download button
                    with open(output_image, "rb") as file:
                        st.download_button(
                            label="📥 Download iPhone Shot",
                            data=file,
                            file_name=f"iPhone_Quality_{uploaded_file.name}",
                            mime="image/jpeg"
                        )
                else:
                    st.error("Bhai server ne blank file di. Ek baar settings kam karke try kar.")

            except Exception as e:
                st.error(f"Abe yaar, error aa gaya: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Finegrain ViT Technology | Made for the Oppo Gang 🤜🤛")
