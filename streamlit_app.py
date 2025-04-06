import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import uuid
import webbrowser

#st.sidebar.image("tume_logo.png",width=300)

user_store = {"akintondeabbas@gmail.com": {
        "email": "akintondeabbas@gmail.com",
        "password": "Akin123",
        "first_name": "Akintonde",
        "last_name": "Abbas",
        "subscribed": True
    },
    "bob@example.com": {
        "email": "bob@example.com",
        "password": "mypassword",
        "first_name": "Bob",
        "last_name": "Jones",
        "subscribed": False
    }
    } #database placeholder

STRIPE_CHECKOUT_URL = "https://buy.stripe.com/test_9AQeWD8mw0va4PmaEE"

if "page" not in st.session_state:
    st.session_state.page = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

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

# Sidebar content
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


#Main page content
if st.session_state.page is None:

    # Show the default "chat-style" welcome screen
    st.title("What can I help with?")
    st.write("Hi there! Your AI Energy Analyst here 🙂. Here are a couple of things I can do at the moment.")
    
    st.write("1. I have access to market protocols, energy and ancillary service prices, supply mix and actual load data for ERCOT, PJM, CAISO and NYISO markets")
    st.write("2. I can pull actual revenues for grid-scale batteries in ERCOT and help you with revenue benchmarking")
    st.write("3. I can run optimal battery dispatch models and help you evaluate potential levered and unlevered IRRs for battery projects based on whatever " \
    "assumptions you'd like to make")
    st.write("4. I'm really good at creating custom briefs to help you stay on top of energy market trends that are most important to you")
    "[Check out this blog to see updates on my new capabilities](https://www.tume.ai)."

    if (st.session_state.authenticated == False) & (st.session_state.subscribed == False):
        st.write("**To get full access to my capabilities, you'd need to subscribe for $40/month. Otherwise, you'd only be able to ask me 5 questions" \
        " per day.**")
        
        if st.button("**Sign in or Get full access for $40/month**"):
            st.session_state.page = "auth"
            st.rerun()

    elif (st.session_state.authenticated == True) & (st.session_state.subscribed == False):

        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.write(f"🤖 You said: {user_input}")

        st.write("**You are currently signed in with a 5 questions per day limit**")

    elif (st.session_state.authenticated == True) & (st.session_state.subscribed == True):

        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.write(f"🤖 You said: {user_input}")

        st.write("**You are currently signed in and you have full access to my current capabilities!**")

    
    st.write("If there are specific things you'd like me to know so that I can help you with related tasks, you can reach out to my tutors at tume@tume.ai. Thanks!")


elif st.session_state.page == "auth":
    st.title("🔐 Login or Sign Up")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            user = user_store.get(email)
            if user and user["password"] == password:
                st.success(f"Welcome back, {user['email']}!")
                st.session_state.page = None
                st.session_state.authenticated = True
                if user['subscribed'] == True:
                    st.session_state.subscribed = True
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    with col2:
        if st.button("Sign Up"):
            if not email or not password:
                st.warning("Please enter both email and password.")
            elif email in user_store:
                st.warning("User already exists. Try logging in.")
            else:
                st.session_state.signup_email = email
                st.session_state.signup_password = password
                st.session_state.page = "signup_details"
                st.rerun()

elif st.session_state.page == "signup_details":
    st.title("📝 Complete Your Sign Up")

    st.markdown("We'll use these details to set up your account:")

    email = st.text_input("Email", value=st.session_state.signup_email, disabled=False)
    password = st.text_input("Password", value=st.session_state.signup_password, type="password", disabled=False)

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Signup & Subscribe"):
            if not first_name or not last_name:
                st.warning("Please fill out your full name.")
            else:
                user_store[email] = {
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name
                }
                st.success("Redirecting to Stripe checkout to complete signup and subscription...")

                # Redirect to Stripe
                js = f"window.open('{STRIPE_CHECKOUT_URL}','_blank').focus();"
                st.components.v1.html(f"<script>{js}</script>", height=0)

                st.markdown("After completing payment, come back and login!")

    with col2:

        if st.button("Signup Only"):
            if not first_name or not last_name:
                st.warning("Please fill out your full name.")
            else:
                user_store[email] = {
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name
                }
                st.success("Signup complete!")
                st.session_state.page = None
                st.session_state.authenticated = True
                st.session_state.subscribed = False
                st.rerun()

    #if st.button("🔙 Back"):
        #st.session_state.page = "auth"
        #st.rerun()

# Show content based on what was clicked
elif st.session_state.page == "markets":
    st.title("Energy Markets Data Explorer")
    st.write("I have access to market protocols, energy and ancillary service prices, supply mix and actual load data for ERCOT, PJM, CAISO and NYISO markets. "
    "Feel free to ask me anything about those markets.")
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.write(f"🤖 You said: {user_input}")

elif st.session_state.page == "batteries":
    st.title("BESS Benchmarks and Returns Analyzer")
    st.write("I can pull actual revenues for FTM grid-scale batteries in ERCOT. I can also run optimal revenue analysis and dispatch with only energy"
    " arbitrage in ERCOT, PJM, NYISO and CAISO. I'll be able to do optimal revenue stacking for both FTM and BTM batteries across regulated and competitive markets very soon. "
    "Let me know what you need.")
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.write(f"🤖 You said: {user_input}")

elif st.session_state.page == "briefs":
    st.title("Market Trends and Briefs Generator")
    st.write("Let me know what energy market topics or trends you'd like to keep an eye on and when and how frequently you'd like to get your briefs. "
    "You'd need to subscribe to be able to do this.")
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.write(f"🤖 You said: {user_input}")


