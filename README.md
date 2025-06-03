# Lifestyle Survey Application

## Overview
This is a Flask-based web application that allows users to participate in a lifestyle survey and view aggregated results. The application collects information about personal preferences regarding food, entertainment activities, and provides statistical insights from all survey responses.

## Features
- User-friendly survey form with validation
- Data persistence using SQLite database
- Comprehensive results dashboard showing:
  - Total number of surveys
  - Age statistics (average, min, max)
  - Food preference percentages
  - Average ratings for various activities
- Responsive design that works on mobile and desktop devices
- Form validation with helpful error messages

## Installation
1. Ensure you have Python 3.x installed
2. Clone this repository
3. Install the required dependencies
   pip install flask
4. Run the application:
   python app.py
5. Access the application at `http://localhost:5000` in your web browser

## Usage
1. **Submit a Survey**:
- Fill out the survey form with your personal details
- Select your favorite foods
- Rate your preferences for various activities
- Submit the form

2. **View Results**:
- After submission, you'll be redirected to the results page
- View aggregated statistics from all survey responses
- Refresh the page to see updated results

## File Structure
survey-app/
- ├── app.py # Main Flask application
- ├── static/
- │ └── style.css # CSS stylesheet
- ├── templates/
- │ ├── results.html # Results page template
- │ └── survey.html # Survey form template
- └── survey.db # SQLite database (created after first run)


## Dependencies
- Flask (web framework)
- SQLite3 (database)

## Customization
You can customize the application by:
1. Modifying the CSS in `static/style.css`
2. Changing the survey questions in `templates/survey.html`
3. Adjusting the results calculations in `app.py`

## Screenshots
![image](https://github.com/user-attachments/assets/00622c4e-23e1-4514-a647-b007fc8a60ae)
![image](https://github.com/user-attachments/assets/f3454dda-2859-492b-89cf-3cf233c6978b)

## License
This project is open-source and available under the MIT License.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
