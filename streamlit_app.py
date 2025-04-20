import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
import base64
import re
import json

#st.sidebar.image("tume_logo.png",width=300)


# Backend API URL
signup_url = "https://5132-2600-8806-350b-a700-c012-7c81-8638-e198.ngrok-free.app/api/auth/signup"
login_url = "https://5132-2600-8806-350b-a700-c012-7c81-8638-e198.ngrok-free.app/api/auth/login"
checkout_url = "https://5132-2600-8806-350b-a700-c012-7c81-8638-e198.ngrok-free.app/api/payment/create-checkout-session"
profile_url = "https://5132-2600-8806-350b-a700-c012-7c81-8638-e198.ngrok-free.app/api/user/me"


#Initializing state variables
if "page" not in st.session_state:
    st.session_state.page = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "session_token" not in st.session_state:
    st.session_state.session_token = None

# Headers
headers = {
    "Authorization": f"Bearer {st.session_state.access_token}",
    "X-Session-Token": st.session_state.session_token  # if your backend expects it
}
headers_login = {
    "Content-Type": "application/json"
}

# Load and encode your logo image
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

        st.write("**You are currently signed in with a 5 questions per day limit**")

    elif (st.session_state.authenticated == True) & (st.session_state.subscribed == True):

        st.write("**You are currently signed in and you have full access to my current capabilities!**")

    
    st.write("If there are specific things you'd like me to know so that I can help you with related tasks, you can reach out to my tutors at tume@tume.ai. Thanks!")
    
    st.write(" ")

    if (st.session_state.authenticated == True):
        col1, col2 , col3 = st.columns(3)
        with col1:
            if st.button("Explore energy markets data"):
                st.session_state.page = "markets"
                st.rerun()
        with col2:
            if st.button("Analyze BESS project returns"):
                st.session_state.page = "batteries"
                st.rerun()
        with col3:
            if st.button("Get customized energy briefs"):
                st.session_state.page = "briefs"
                st.rerun()

# Flow for login page
elif st.session_state.page == "auth":
    st.title("🔐 Login or Sign Up")

    email = st.text_input("Email")
    email_processed = email.lower()
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            
            payload = {
                "username": email_processed,
                "password": password
            }
            
            #payload = json.loads(json.dumps(payload))
            try:
                login_response = requests.post(login_url, json=payload, headers=headers_login)

                if login_response.status_code == 200:
                    st.session_state.access_token = login_response['access_token']
                    st.session_state.session_token = login_response['session_token']
                    profile_response = requests.get(profile_url, headers = headers)
                    st.session_state.page = None
                    st.session_state.authenticated = True
                    if profile_response['is_paid_user'] == 'true':
                        st.session_state.subscribed = True
                    st.rerun()

                elif login_response.status_code == 500:
                    st.error(f"Error: {login_response}")

                else:
                    st.error(f"Error: {login_response.status_code}")
            except Exception as e:
                st.error(f"Request failed: {e}")

    with col2:
        if st.button("Sign Up"):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                st.session_state.signup_email = email_processed
                st.session_state.signup_password = password
                st.session_state.page = "signup_details"
                st.rerun()

# Flow for signup page
elif st.session_state.page == "signup_details":
    st.title("📝 Complete Your Sign Up")

    st.markdown("We'll use these details to set up your account:")

    email = st.text_input("Email", value=st.session_state.signup_email, disabled=False)
    password = st.text_input("Password", value=st.session_state.signup_password, type="password", disabled=False)

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("**Signup & Subscribe**"):
            if not first_name or not last_name:
                st.warning("Please fill out your full name.")
            else:
                payload = {"email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password}
                try:
                    signup_response = requests.post(signup_url, json=payload)

                    if signup_response.status_code == 200:
                        st.session_state.access_token = signup_response['access_token']
                        st.session_state.session_token = signup_response['session_token']
                        checkout_payload = {"success_url":"https://tume.ai",
                                           "cancel_url":"https://tume.ai",
                                           "price_id": "price_1RBnXyQb10U9WeFzRUYDM3Ec"}

                        st.success("Redirecting to Stripe checkout to complete signup and subscription...")
                        payment_response = requests.post(checkout_url, json=checkout_payload, headers=headers)
                        st.session_state.page = 'auth'
                        st.rerun()
                    else:
                        st.error(f"Error: {signup_response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    with col2:

        if st.button("**Signup Only**"):
            if not first_name or not last_name:
                st.warning("Please fill out your full name.")
            else:
                payload = {"email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password}
                try:
                    signup_response = requests.post(signup_url, json=payload)

                    if signup_response.status_code == 200:
                        st.success("Signup complete!")
                        st.session_state.page = 'auth'
                        st.rerun()
                    else:
                        st.error(f"Error: {signup_response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

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
    topic = st.text_input("What energy market topics or trends do you want to track?", placeholder="e.g. Ancillary service prices in ERCOT and PJM")
    options_freq = ["Monthly","Weekly", "Daily"]
    options_day = ["Sunday", "Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday"]
    #custom_sources = st.text_input("Are there specific websites you'd like to check?", placeholder="e.g. utilitydive.com")
    frequency = st.selectbox("How often do you want to get updates?", options_freq)
    delivery_day = st.selectbox("What day would you prefer for monthly or weekly delivery?", options_day)
    delivery_time = st.text_input("What delivery time do you prefer (e.g. 07:00 AM EST)?", placeholder="07:00 AM EST")

    pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)\s?EST$"

    if delivery_time:
        if re.fullmatch(pattern, delivery_time .strip().upper()):
            pass
            #st.success(f"Valid time input: {user_input}")
        else:
            st.error("Invalid format. Please use HH:MM AM/PM EST (e.g., 07:00 AM EST)")

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("**Preview custom brief**")
    with col2:
        st.button("**Update custom brief**")
    with col3:
        st.button("**Delete custom brief**")
    


