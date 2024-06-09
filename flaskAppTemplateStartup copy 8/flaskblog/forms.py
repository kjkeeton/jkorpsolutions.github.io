from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Email

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
