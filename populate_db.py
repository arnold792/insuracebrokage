from app import app, db
from models import Client, Policy, Claim, Payment, Underwriter, Agent, Accident
from datetime import datetime, timedelta

def populate_db():
    # Clear existing data
    db.session.query(Payment).delete()
    db.session.query(Claim).delete()
    db.session.query(Accident).delete()
    db.session.query(Policy).delete()
    db.session.query(Client).delete()
    db.session.query(Agent).delete()
    db.session.query(Underwriter).delete()

    # Create sample agents
    agents = [
        Agent(name='John Smith', email='john@agency.com', phone='555-0101', commission_rate=0.10),
        Agent(name='Sarah Wilson', email='sarah@agency.com', phone='555-0102', commission_rate=0.12),
        Agent(name='Mike Johnson', email='mike@agency.com', phone='555-0103', commission_rate=0.11)
    ]
    db.session.add_all(agents)

    # Create sample underwriters
    underwriters = [
        Underwriter(name='David Brown', email='david@insurance.com', specialty='Life Insurance'),
        Underwriter(name='Lisa Chen', email='lisa@insurance.com', specialty='Auto Insurance'),
        Underwriter(name='James Wilson', email='james@insurance.com', specialty='Home Insurance')
    ]
    db.session.add_all(underwriters)

    # Create sample clients
    clients = [
        Client(name='Alice Cooper', email='alice@email.com', phone='555-0201', address='123 Main St'),
        Client(name='Bob Marshall', email='bob@email.com', phone='555-0202', address='456 Oak Ave'),
        Client(name='Carol White', email='carol@email.com', phone='789 Pine Rd')
    ]
    db.session.add_all(clients)
    db.session.commit()

    # Create sample policies
    policies = [
        Policy(
            policy_number='POL001',
            type='Life',
            premium=1200.00,
            coverage_amount=100000.00,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            status='Active',
            client_id=clients[0].id,
            underwriter_id=underwriters[0].id
        ),
        Policy(
            policy_number='POL002',
            type='Auto',
            premium=800.00,
            coverage_amount=50000.00,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            status='Active',
            client_id=clients[1].id,
            underwriter_id=underwriters[1].id
        )
    ]
    db.session.add_all(policies)
    db.session.commit()

    # Create sample claims
    claims = [
        Claim(
            claim_amount=5000.00,
            status='Pending',
            description='Car accident damage',
            client_id=clients[1].id,
            policy_id=policies[1].id
        )
    ]
    db.session.add_all(claims)

    # Create sample payments
    payments = [
        Payment(
            amount=1200.00,
            payment_date=datetime.now(),
            payment_method='Credit Card',
            client_id=clients[0].id
        ),
        Payment(
            amount=800.00,
            payment_date=datetime.now(),
            payment_method='Bank Transfer',
            client_id=clients[1].id
        )
    ]
    db.session.add_all(payments)

    # Create sample accidents
    accidents = [
        Accident(
            date=datetime.now() - timedelta(days=5),
            description='Minor collision at intersection',
            location='Main St & 5th Ave',
            client_id=clients[1].id
        )
    ]
    db.session.add_all(accidents)

    db.session.commit()
    print("Database populated with sample data!")

if __name__ == '__main__':
    with app.app_context():
        populate_db()
