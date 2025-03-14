from datetime import datetime
from extensions import db

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    policies = db.relationship('Policy', backref='client', lazy=True)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    claims = db.relationship('Claim', backref='client', lazy=True)
    payments = db.relationship('Payment', backref='client', lazy=True)
    accidents = db.relationship('Accident', backref='client', lazy=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))

class Policy(db.Model):
    __tablename__ = 'policy'
    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    premium = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coverage_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Active')
    underwriter_id = db.Column(db.Integer, db.ForeignKey('underwriter.id'))
    claims = db.relationship('Claim', backref='policy', lazy=True)

class Claim(db.Model):
    __tablename__ = 'claim'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    claim_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    filed_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolution_date = db.Column(db.DateTime)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='Completed')

class Agent(db.Model):
    __tablename__ = 'agent'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    commission_rate = db.Column(db.Float)
    clients = db.relationship('Client', backref='agent', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Underwriter(db.Model):
    __tablename__ = 'underwriter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    policies = db.relationship('Policy', backref='underwriter', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Accident(db.Model):
    __tablename__ = 'accident'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    damage_amount = db.Column(db.Float)
    location = db.Column(db.String(200))
    report_date = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20), nullable=True)

class Beneficiary(db.Model):
    __tablename__ = 'beneficiary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    contact_info = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    policy = db.relationship('Policy', backref='policy_beneficiaries')
    client = db.relationship('Client', backref='client_beneficiaries')

def create_tables():
    """Create all database tables."""
    db.create_all()

if __name__ == '__main__':
    create_tables()
