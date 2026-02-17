import streamlit as st
from gradio_client import Client, handle_file
import os

st.title("🔥 iPhone 17 Pro Max Ultra-Enhancer")
st.write("Bhai, agar pehle change nahi ho raha tha, toh ab pakka hoga!")

# Sidebar for Pro-Control
st.sidebar.header("🔧 Force Settings")
# Denoise ko 0.5 se upar rakhna hai tabhi farak dikhega
denoise = st.sidebar.slider("Denoise Strength (Force)", 0.0, 1.0, 0.65)
# Condition scale AI ko prompt follow karne pe majboor karta hai
c_scale = st.sidebar.slider("AI Creativity (Condition)", 1, 20, 12)

uploaded_file = st.file_uploader("Oppo Photo Upload Karo", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("✨ Force iPhone Magic"):
        with st.spinner("AI pixels generate kar raha hai..."):
            try:
                client = Client("finegrain/finegrain-image-enhancer")
                
                # 💡 THE SECRET SAUCE: Prompt mein 'raw photo' aur 'detailed' dalkar 
                # AI ko pixels change karne ke liye push kiya hai.
                result = client.predict(
                    input_image=handle_file("temp.jpg"),
                    prompt="ultra-realistic 8k photo, extremely detailed skin pores, sharp eyes, iphone 17 pro max cinematic style, high dynamic range, 48mp raw sensor quality",
                    negative_prompt="blurry, low quality, smooth skin, plastic, cartoon, painting, noise, out of focus",
                    seed=42,
                    upscale_factor=2,
                    controlnet_scale=0.7, # Structure ko tight rakhega
                    controlnet_decay=1.0,
                    condition_scale=c_scale, # Isse AI 'iPhone' wali baat maanega
                    tile_width=112,
                    tile_height=144,
                    denoise_strength=denoise, # Isse Oppo ki noise khatam hogi
                    num_inference_steps=20,
                    solver="DDIM",
                    api_name="/process"
                )

                output = result[0] if isinstance(result, list) else result
                st.image(output, caption="Finally! iPhone Quality")
                
                with open(output, "rb") as f:
                    st.download_button("📥 Download", f, file_name="iphone_shot.jpg")

            except Exception as e:
                st.error(f"Bhai Error aa gaya: {e}")
