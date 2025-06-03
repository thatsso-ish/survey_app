from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS surveys
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  full_name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  dob TEXT NOT NULL,
                  contact TEXT NOT NULL,
                  pizza INTEGER DEFAULT 0,
                  pasta INTEGER DEFAULT 0,
                  pap_wors INTEGER DEFAULT 0,
                  other_food TEXT,
                  movies_rating INTEGER,
                  radio_rating INTEGER,
                  eat_out_rating INTEGER,
                  tv_rating INTEGER,
                  submission_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Survey form route
@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        errors = validate_survey(request.form)
        if errors:
            return render_template('survey.html', errors=errors)
        
        save_survey(request.form)
        return redirect(url_for('results'))
    
    return render_template('survey.html', errors=None)

def validate_survey(form_data):
    errors = []
    required_fields = ['full_name', 'email', 'dob', 'contact']
    for field in required_fields:
        if not form_data.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    if form_data.get('dob'):
        dob = datetime.strptime(form_data['dob'], '%Y-%m-%d')
        age = (datetime.now() - dob).days // 365
        if age < 5 or age > 120:
            errors.append("Age must be between 5 and 120 years")
    
    if not any(form_data.get(food) for food in ['pizza', 'pasta', 'pap_wors']):
        errors.append("Please select at least one favorite food")
    
    rating_fields = ['movies_rating', 'radio_rating', 'eat_out_rating', 'tv_rating']
    for field in rating_fields:
        if not form_data.get(field):
            errors.append(f"Please rate '{field.replace('_rating', '').replace('_', ' ')}'")
    
    return errors

def save_survey(form_data):
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO surveys 
                 (full_name, email, dob, contact, pizza, pasta, pap_wors, other_food,
                  movies_rating, radio_rating, eat_out_rating, tv_rating, submission_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (form_data['full_name'],
               form_data['email'],
               form_data['dob'],
               form_data['contact'],
               1 if form_data.get('pizza') else 0,
               1 if form_data.get('pasta') else 0,
               1 if form_data.get('pap_wors') else 0,
               form_data.get('other_food', ''),
               int(form_data['movies_rating']),
               int(form_data['radio_rating']),
               int(form_data['eat_out_rating']),
               int(form_data['tv_rating']),
               datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Results route
@app.route('/results')
def results():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM surveys')
    total_surveys = c.fetchone()[0]
    
    if total_surveys == 0:
        conn.close()
        return render_template('results.html', no_data=True)
    
    c.execute('''SELECT dob FROM surveys''')
    dob_list = [datetime.strptime(row[0], '%Y-%m-%d') for row in c.fetchall()]
    ages = [(datetime.now() - dob).days // 365 for dob in dob_list]
    avg_age = round(sum(ages) / len(ages), 1)
    max_age = max(ages)
    min_age = min(ages)
    
    c.execute('SELECT SUM(pizza), SUM(pasta), SUM(pap_wors) FROM surveys')
    pizza, pasta, pap_wors = c.fetchone()
    pizza_pct = round((pizza / total_surveys) * 100, 1)
    pasta_pct = round((pasta / total_surveys) * 100, 1)
    pap_wors_pct = round((pap_wors / total_surveys) * 100, 1)
    
    c.execute('''SELECT AVG(movies_rating), AVG(radio_rating), 
                        AVG(eat_out_rating), AVG(tv_rating) 
                 FROM surveys''')
    avg_movies, avg_radio, avg_eat_out, avg_tv = [round(val, 1) for val in c.fetchone()]
    
    conn.close()
    
    return render_template('results.html',
                         no_data=False,
                         total_surveys=total_surveys,
                         avg_age=avg_age,
                         max_age=max_age,
                         min_age=min_age,
                         pizza_pct=pizza_pct,
                         pasta_pct=pasta_pct,
                         pap_wors_pct=pap_wors_pct,
                         avg_movies=avg_movies,
                         avg_radio=avg_radio,
                         avg_eat_out=avg_eat_out,
                         avg_tv=avg_tv)

if __name__ == '__main__':
    app.run(debug=True)