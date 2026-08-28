import os
from dotenv import load_dotenv
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
FIREBASE_CONFIG = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}

#Configure and Connext to Firebase
def log_in(email,password):

    firebase=pyrebase.initialize_app(FIREBASE_CONFIG)
    auth=firebase.auth()

    #Login function

    print("Log in...")
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        result = "Successfully logged in!"
    except:
        print("Invalid email or password")
        result = "Invalid email or password"

    return result

#Signup Function
def sign_up(email,password,fullName):

    firebase=pyrebase.initialize_app(FIREBASE_CONFIG)
    auth=firebase.auth()

    print("Sign up...")
    
    auth.create_user_with_email_and_password(email, password)
    # login()
        # Initialize Firebase with your service account key file and database URL


    try:
        # Load the Firebase credentials from the JSON file
        cred = credentials.Certificate("key.json")

        # Initialize the Firebase app
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })

        # Get a reference to the 'chatbot1' node
        ref = db.reference('/chatbot1')

        # Extract the username from the email
        username = email.split("@")[0]

        # Set the user details in the database
        users_ref = ref.child(username).set({
            'fullName': fullName,
            'chat_history': None
        })
        
        # Set the 'chat_history' attribute for the user to None
        # users_ref.set({
        #     'chat_history': "ffffff"
        # })
        print("Chat history created successfully.")

    except Exception as e:
        print("Error:", e)

    # print("Email already exists")
    return "Successfully Signing up..."

