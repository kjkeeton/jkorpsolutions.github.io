from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Email
from datetime import datetime
import os

app = Flask(__name__)
TEMPLATES_AUTO_RELOAD = True  # Optional: Reload templates on change
template_folder = 'flaskblog/templates'  # Set the template folder if it's different
static_folder = 'flaskblog/static'
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




from datetime import datetime
with app.app_context():
    def create_tables():
        db.create_all()
        if not Service.query.first():
            services = [
            Service(category='Hair', name='Hair Cut', description='Professional hair cutting service.', price=50),
            Service(category='Hair', name='Hair Coloring', description='Expert hair coloring service.', price=100),
            Service(category='Nails', name='Manicure', description='Complete manicure service.', price=30),
            Service(category='Nails', name='Pedicure', description='Relaxing pedicure service.', price=40),
            Service(category='Massage', name='Swedish Massage', description='Relaxing Swedish massage.', price=70),
            Service(category='Massage', name='Deep Tissue Massage', description='Intensive deep tissue massage.', price=90)
        ]
        db.session.bulk_save_objects(services)
        db.session.commit()
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    service = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    comments = db.Column(db.Text, nullable=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    contact_method = db.Column(db.String(50), nullable=False)
    best_time_to_call = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)

class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    service = SelectField('Service', choices=[], validators=[DataRequired()])
    date_time = DateTimeField('Preferred Date and Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    comments = TextAreaField('Additional Comments')
    submit = SubmitField('Schedule Appointment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    contact_method = RadioField('Preferred Contact Method', choices=[('Phone', 'Phone'), ('Email', 'Email')], validators=[DataRequired()])
    best_time_to_call = StringField('Best Time to Call')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    categories = db.session.query(Service.category.distinct()).all()
    services = {category[0]: Service.query.filter_by(category=category[0]).all() for category in categories}
    return render_template('services.html', services=services)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            contact_method=form.contact_method.data,
            best_time_to_call=form.best_time_to_call.data,
            message=form.message.data
        )
        db.session.add(contact_message)
        db.session.commit()
        flash('Your message has been sent. Thank you!')
        return redirect(url_for('thank_you'))
    return render_template('contact.html', form=form)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    form.service.choices = [(service.name, f"{service.name} - ${service.price}") for service in Service.query.all()]
    if form.validate_on_submit():
        appointment = Appointment(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service=form.service.data,
            date_time=form.date_time.data,
            comments=form.comments.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Your appointment has been scheduled.')
        return redirect(url_for('thank_you'))
    return render_template('appointment.html', form=form)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
