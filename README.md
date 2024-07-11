# MoodWage

![MoodWage](https://github.com/Atulok0506/MOODWAGE/blob/main/moodwage1.png)

## Overview

Welcome to MoodWage, your ultimate tool for predicting salaries and analyzing company sentiment. This project integrates machine learning for salary predictions and natural language processing (NLP) for sentiment analysis, all accessible via Flask APIs.

## Features

- **Salary Prediction**: Predicts salaries based on company name, job profile, and experience using a machine learning model trained on data scraped from AmbitionBox.
  
- **Sentiment Analysis**: Real-time sentiment analysis of company reviews provided by users, using Hugging Face Transformers to analyze sentiment scores and store them in a tabular format.

- **Flask Endpoints**: Implements Flask endpoints for salary prediction, sentiment analysis, sentiment score display, and user authentication.

## Technologies Used

- **Machine Learning**: Linear regression model for salary prediction.
- **NLP**: Hugging Face Transformers for sentiment analysis.
- **Web Development**: Flask framework for creating RESTful APIs and managing user interactions.

## Project Structure

- **Notebooks**: Jupyter notebooks for data scraping, preprocessing, model training, and analysis.
  
- **Data**: Datasets used for training models and storing sentiment analysis results.
  
- **Flask App**: Flask application files, including endpoint definitions and authentication logic.

## Usage

To use MoodWage:

1. **Salary Prediction**:
   - Provide company name, job profile, and experience details to predict salary using the provided Flask endpoint.
  
2. **Sentiment Analysis**:
   - Enter company reviews to obtain real-time sentiment analysis scores through another Flask endpoint.

3. **View Sentiment Scores**:
   - Access an additional Flask endpoint to display aggregated sentiment scores from user reviews.

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or provide feedback to help improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, please contact:

- **Name**: Atul Kishore
- **Email**: atulstar900@gmail.com
- **LinkedIn**: [Atul Kishore on LinkedIn](https://www.linkedin.com/in/atul-kishore-b16991179/)

Thank you for exploring MoodWage! Let's predict and analyze with confidence! 🚀
