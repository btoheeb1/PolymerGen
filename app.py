import streamlit as st
import subprocess

st.title("Polymer Generator GUI")

st.write("Configure the number of each polymer type you'd like to generate:")

ring = st.number_input("Number of ring polymers", min_value=0, value=5, step=1)
star = st.number_input("Number of star polymers", min_value=0, value=3, step=1)
block = st.number_input("Number of block polymers", min_value=0, value=4, step=1)
graft = st.number_input("Number of graft polymers", min_value=0, value=2, step=1)
bottlebrush = st.number_input("Number of bottlebrush polymers", min_value=0, value=1, step=1)

output_file = st.text_input("Output filename", value="user_responses.txt")

if st.button("Generate & Build Polymers"):
    try:
        with st.spinner("Generating user_responses.txt..."):
            subprocess.run([
                "python", "generate_user_responses_custom.py",
                "--ring", str(ring),
                "--star", str(star),
                "--block", str(block),
                "--graft", str(graft),
                "--bottlebrush", str(bottlebrush),
                "--output", output_file
            ], check=True)

        with st.spinner("Running polymer generator..."):
            subprocess.run(["python", "polymer_generator.py"], check=True)

        st.success(f" Finished! Polymers saved in `outputs/` using {output_file}")

    except subprocess.CalledProcessError as e:
        st.error(f"Error: {e}")


