# Executive Productivity Agent

## Overview
An AI-powered productivity assistant designed for executives.

## Features
- View upcoming meetings
- Track pending commitments
- Review email follow-ups
- Ask questions using natural language
- Generate weekly priorities and action items

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- JSON

## How to Run

1. Install dependencies:
   pip install streamlit google-generativeai python-dotenv

2. Add your Gemini API key in `.env`:

   GEMINI_API_KEY=your_api_key_here

3. Run the application:

   streamlit run app.py


   # Executive Productivity Agent

## Project Description

This is a demo project of an AI-powered Executive Productivity Agent built using Python and Streamlit.

The application helps executives manage their productivity by viewing meetings, pending commitments, email follow-ups, and important tasks in one dashboard.

Users can ask natural-language questions about their productivity data and receive relevant responses.

## Important Note

This is a demonstration project created for educational and portfolio purposes.

The project uses the Google Gemini API for AI-powered responses. To run the AI features, users need to provide their own Gemini API key.

### How to Configure Your API Key

1. Create a Gemini API key from Google AI Studio.
2. Create a `.env` file in the project folder.
3. Add the following line:

GEMINI_API_KEY=your_api_key_here

Do not share your API key publicly.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- JSON
- python-dotenv

## Features

- Executive dashboard
- Upcoming meetings
- Pending commitments
- Email follow-ups
- Natural-language AI assistant
- Action-oriented productivity summaries

## How to Run

Install the required packages:

pip install -r requirements.txt

Then run:

streamlit run app.py