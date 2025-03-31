import streamlit as st
from openai import OpenAI
from PIL import Image
import base64

#st.sidebar.image("tume_logo.png",width=300)

if "page" not in st.session_state:
    st.session_state.page = None

# Load and encode your image
with open("tume_logo.png", "rb") as img_file:
    encoded = base64.b64encode(img_file.read()).decode()

# Create the clickable image with rounded corners
sidebar_html = f"""
<a href="https://tume.ai" target="_blank">
    <img src="data:image/png;base64,{encoded}" 
         width="280" 
         style="border-radius: 10px; display: block; margin: auto;">
</a>
"""

# Show in the sidebar
st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)

with st.sidebar:
    st.write("")

    st.title("Use cases")

    st.write("")

    button_col1, text_col1 = st.sidebar.columns([1, 4])

    with text_col1:
        st.write("Explore US electricity markets data")
    with button_col1:
        if st.button("➔ ", key='markets'):
            st.session_state.page = "markets"

    button_col2, text_col2  = st.sidebar.columns([1, 4])

    with text_col2:
        st.write("Perform battery energy storage revenue analysis")
    with button_col2:
        if st.button("➔ ", key='batteries'):
            st.session_state.page = "batteries"

    button_col3, text_col3  = st.sidebar.columns([1, 4])
    with text_col3:
        st.write("Get your customized briefs on energy market trends")
    with button_col3:
        if st.button("➔ ", key='briefs'):
            st.session_state.page = "briefs"

    button_col4, text_col4  = st.sidebar.columns([1, 4])
    with text_col4:
        st.write("Back to home")
    with button_col4:
        if st.button("🏠", key='home'):
            st.session_state.page = None
        
    st.write("")
    "[Tume AI blog - learn more about the exciting things we are building for you and other great energy markets insights!](https://www.tume.ai)"


if st.session_state.page is None:
    # Show the default "chat-style" welcome screen
    st.title("What can I help with?")
    st.write("Hi there! Your AI Energy Analyst here 🙂. Here are a couple of things I can do at the moment.")
    
    st.write("1. I know a whole lot about market protocols, pricing data, supply and demand patterns for ERCOT, PJM, CAISO and NYISO markets")
    st.write("2. I also know a lot batteries in ERCOT and can even run optimal battery dispatch models")
    st.write("3. I can help you evaluate potential returns for battery projects in ERCOT based on whatever assumptions you'd like to make")
    st.write("4. I'm really good at creating custom briefs to help you stay on top of energy market trends that are most important to you")
    "[Check out this blog to see new things I'll be able to do](https://www.tume.ai)."
    st.write("I'm learning everyday so I'll be able to do even more cooler things very soon. If there are specific things you'd like me to know so that I can help you with related tasks, you can reach out to my tutors at tume@tume.ai. Thanks!")

    
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.write(f"🤖 You said: {user_input}")

else:
    # Show content based on what was clicked
    if st.session_state.page == "markets":
        st.title("Energy Markets Data Explorer")
        st.write("I know a whole lot about market protocols, pricing data, supply and demand patterns for ERCOT, PJM, CAISO and NYISO markets. "
        "Feel free to ask me anything about those markets.")
        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.write(f"🤖 You said: {user_input}")

    elif st.session_state.page == "batteries":
        st.title("BESS Benchmarks and Returns Analyzer")
        st.write("I know a whole lot about revenues for actual FTM grid-scale batteries in ERCOT. I can also run optimal revenue analysis and dispatch with only energy"
        " arbitrage in ERCOT, PJM, NYISO and CAISO. I'll be able to do optimal revenue stacking for both FTM and BTM batteries across regulated and competitive markets very soon. "
        "Let me know what you need.")
        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.write(f"🤖 You said: {user_input}")

    elif st.session_state.page == "briefs":
        st.title("Market Trends and Briefs Generator")
        st.write("Let me know what energy market topics or trends you'd like to keep an eye on and when and how frequently you'd like to get your briefs. "
        "You'd need a subscription to be able to do this.")
        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.write(f"🤖 You said: {user_input}")
