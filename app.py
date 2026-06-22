import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import io

def generate_dp(user_image_path, frame_image_path):
    frame = Image.open(frame_image_path).convert("RGBA")
    size = frame.size

    user_img = Image.open(user_image_path).convert("RGBA")
    user_img = ImageOps.fit(user_img, size, centering=(0.5, 0.5))

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    circular_user_img = Image.new("RGBA", size)
    circular_user_img.paste(user_img, (0, 0), mask=mask)

    final_output = Image.alpha_composite(circular_user_img, frame)
    return final_output

st.set_page_config(page_title="Delhivery DP Generator", page_icon="🚚", layout="centered")
st.title("🚚 Delhivery 15-Year Milestone DP Generator")
st.write("Upload your picture to generate your custom 'On the Move' profile frame.")

uploaded_file = st.file_uploader("Choose a profile photo...", type=["jpg", "jpeg", "png"])
FRAME_PATH = "DP Frame for 15 years.png"

if uploaded_file is not None:
    with st.spinner("Generating your DP..."):
        try:
            result_img = generate_dp(uploaded_file, FRAME_PATH)
            st.image(result_img, caption="Your Generated DP", use_container_width=True)

            buffer = io.BytesIO()
            result_img.save(buffer, format="PNG")
            st.download_button(
                label="📥 Download Profile Picture",
                data=buffer.getvalue(),
                file_name="Delhivery_15_Years_DP.png",
                mime="image/png"
            )
        except Exception as e:
            st.error("Error generating image. Please ensure your frame file is named correctly.")
