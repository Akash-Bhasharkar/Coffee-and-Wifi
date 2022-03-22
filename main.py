from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import SelectFieldBase
from wtforms.validators import DataRequired, URL
import csv
from csv import writer
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location', validators=[DataRequired(), URL()])
    open_time = StringField('Cafe opening time', validators=[DataRequired()])
    close_time = StringField('Cafe closing time ', validators=[DataRequired()])
    rating = SelectField('Cafe coffee rating', choices = ['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'],  validators=[DataRequired()])
    wifi  = SelectField('Cafe wifi strength', choices = ['💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'], validators=[DataRequired()])
    power = SelectField('Cafe power outlet', choices = ['🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'], validators = [DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods = ["POST", "GET"] )
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        ignore = ["submit", "csrf_token"]
        list_of_data = [value for (key , value) in form.data.items() if key not in ignore ]
        with open('cafe-data.csv', "a", encoding = "utf8") as csv_file:
             writer_object = writer(csv_file)
             writer_object.writerow(list_of_data)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding = "utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
