from flask import Flask, render_template, request, session, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import joblib
import torch
import os
from authentication import *
from reviews import *

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management

logos_folder = os.path.join(os.getcwd(), 'static')  # Updated folder name to 'static'

# Define paths to the models
sentiment_model_path = "sentiment_model"
salary_model_path = "tuned_linear_model.joblib"

# Load the models on startup
sentiment_tokenizer, sentiment_model = AutoTokenizer.from_pretrained(
    sentiment_model_path), AutoModelForSequenceClassification.from_pretrained(sentiment_model_path)
salary_model = joblib.load(salary_model_path)

# Load the dataset (replace "new_pred.csv" with the actual file name)
df = pd.read_csv("new_pred.csv")

# Directly encode categorical values based on the logic used in your Jupyter Notebook
target_ordinal_company = df.groupby('Company')['AvgSalary'].mean().to_dict()
target_ordinal_job = df.groupby('Job Profile')['AvgSalary'].median().to_dict()


def get_sentiment_color(sentiment_prediction):
    if sentiment_prediction == 1:
        return "red"
    elif sentiment_prediction == 2:
        return "orange"
    elif sentiment_prediction == 3:
        return "yellow"
    elif sentiment_prediction == 4:
        return "green"
    elif sentiment_prediction == 5:
        return "blue"
    else:
        return "black"  # Default color if sentiment prediction is out of range


@app.route('/')
def home():
    # Get unique job profiles for dropdown
    job_profiles = df['Job Profile'].unique().tolist()

    return render_template('index.html', sentiment_prediction=None, salary_prediction=None, text='', job_profile='',
                           company='', experience_required='', job_profiles=job_profiles, logos_folder=logos_folder)


@app.route('/predict_sentiment', methods=['POST'])
def predict_sentiment():
    if request.method == 'POST':
        text = request.form['text']
        print(f"Received text for sentiment prediction: {text}")

        # Tokenize input text for sentiment analysis
        inputs = sentiment_tokenizer(text, return_tensors='pt')

        # Make prediction using sentiment analysis model
        outputs = sentiment_model(**inputs)
        sentiment_prediction = torch.argmax(outputs.logits, dim=1).item() + 1

        print(f"Predicted sentiment: {sentiment_prediction}")

        # Retrieve user's information from the session or authentication
        # For demonstration purposes, let's assume the user information is retrieved
        user = 'User1'  # Replace with actual user information

        # Retrieve company name from the session or form data
        company = session.get('company', '')

        # Insert sentiment analysis results into the database
        insert_review(user, company, text, sentiment_prediction)

        # Retain salary-related session data
        job_profile = session.get('job_profile', '')
        experience_required = session.get('experience_required', '')
        salary_prediction = session.get('salary_prediction', '')

        # Pass form data back to template
        return render_template('index.html', sentiment_prediction=sentiment_prediction,
                               salary_prediction=salary_prediction,
                               text=text, job_profile=job_profile, company=company,
                               experience_required=experience_required, get_sentiment_color=get_sentiment_color)


@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    if request.method == 'POST':
        # Extract features from the form for salary prediction
        job_profile = request.form['job_profile']
        company = request.form['company']
        experience_required = float(request.form['experience_required'])

        print(
            f"Received form data for salary prediction - Job Profile: {job_profile}, Company: {company}, Experience Required: {experience_required}")

        # Map categorical features to ordinal values based on training data
        job_profile_mapped = target_ordinal_job.get(job_profile, 0)
        company_mapped = target_ordinal_company.get(company, 0)

        # Check if the provided job profile and company are in the mappings
        if job_profile_mapped and company_mapped:
            # Create a DataFrame with the input features
            input_data = pd.DataFrame([[job_profile_mapped, company_mapped, experience_required]],
                                      columns=['Job Profile', 'Company', 'ExperienceRequired'])
            # Make prediction using the salary prediction model
            salary_prediction = int(salary_model.predict(input_data)[0])
            print(f"Predicted salary: {salary_prediction}")

            # Convert NumPy array to list before storing in session
            # salary_prediction_list = salary_prediction.tolist()

            # Save form data to session
            session['job_profile'] = job_profile
            session['company'] = company
            session['experience_required'] = experience_required
            session['salary_prediction'] = salary_prediction  # Use the converted list

            # Get unique job profiles for dropdown
            job_profiles = df['Job Profile'].unique().tolist()

            # Pass form data back to template
            return render_template('index.html', sentiment_prediction=None, salary_prediction=salary_prediction,
                                   job_profile=job_profile, company=company, experience_required=experience_required,
                                   job_profiles=job_profiles)
        else:
            return render_template('result_salary.html', prediction='Invalid input')


@app.route('/get_job_profiles', methods=['POST'])
def get_job_profiles():
    if request.method == 'POST':
        company_name = request.json['company_name']
        selected_job_profiles = df[df['Company'] == company_name]['Job Profile'].unique().tolist()
        return jsonify(job_profiles=selected_job_profiles)


@app.route('/loginpage', methods=['POST', 'GET'])
def loginpage():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        username = request.form.get('username')
        passwd = request.form.get('password')
        fullname = login_acc(username, passwd)[0][0]
        return render_template('index.html')
    except:
        return render_template('login.html', login_msg=f"Invalid Creds")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/signupsucess', methods=['GET', 'POST'])
def signupsucess():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        list = [name, email, username, password]
        account_creation(list)
        return render_template('signup.html', account_created=f"Account Created")
    except ValueError as e:
        return render_template('signup.html', account_created=f"Error Occurred")


@app.route('/logout', methods=['GET'])
def logout():
    return render_template('login.html', login_msg=f"Logout Successfully")


@app.route('/user_reviews')
def user_review():
    connection = sqlite3.connect('res/reviews.db')
    cursor = connection.cursor()

    # Execute a query to fetch reviews from the database
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template('user_reviews.html', reviews=reviews)


if __name__ == '__main__':
    create_table('userbase')
    create_review_table()
    app.run(debug=True)
