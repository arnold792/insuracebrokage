from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional

class AccidentForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], validators=[DataRequired()])

class UnderwriterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[Optional()])
    license_number = StringField('License Number', validators=[DataRequired()])

class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    payment_date = DateField('Payment Date', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer')
    ])
    policy_id = StringField('Policy ID', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])