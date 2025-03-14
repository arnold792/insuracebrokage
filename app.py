from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from extensions import db
from models import Client, Policy, Claim, Payment, Underwriter, Agent, Accident, Beneficiary
from forms import AccidentForm, PaymentForm, UnderwriterForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arnold#254@localhost/insurance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@app.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client():
    try:
        client = Client(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),
            address=request.form.get('address', ''),
            created_at=datetime.now()
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding client: ' + str(e), 'error')
    return redirect(url_for('clients'))

@app.route('/client/<int:id>')
def get_client(id):
    client = Client.query.get_or_404(id)
    return render_template('client_detail.html', client=client)

@app.route('/client/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.name = request.form['name']
        client.email = request.form['email']
        client.phone = request.form['phone']
        client.address = request.form['address']
        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('clients'))
    return render_template('edit_client.html', client=client)

@app.route('/client/delete/<int:id>', methods=['POST', 'DELETE'])
def delete_client(id):
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting client: ' + str(e), 'error')
    return redirect(url_for('clients'))

@app.route('/policies')
def policies():
    policies = Policy.query.all()
    return render_template('policies.html', policies=policies)

@app.route('/add_policy', methods=['POST'])
def add_policy():
    policy = Policy(
        policy_number=request.form['policy_number'],
        type=request.form['type'],
        premium=float(request.form['premium']),
        client_id=int(request.form['client_id']),
        coverage_amount=float(request.form['coverage_amount']),
        start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
        underwriter_id=int(request.form['underwriter_id'])
    )
    db.session.add(policy)
    db.session.commit()
    flash('Policy added successfully!', 'success')
    return redirect(url_for('policies'))

@app.route('/policy/edit/<int:id>', methods=['GET', 'POST'])
def edit_policy(id):
    policy = Policy.query.get_or_404(id)
    if request.method == 'POST':
        policy.premium = float(request.form['premium'])
        policy.coverage_amount = float(request.form['coverage_amount'])
        policy.status = request.form['status']
        db.session.commit()
        flash('Policy updated successfully!', 'success')
        return redirect(url_for('policies'))
    return render_template('edit_policy.html', policy=policy)

@app.route('/policy/delete/<int:id>')
def delete_policy(id):
    policy = Policy.query.get_or_404(id)
    db.session.delete(policy)
    db.session.commit()
    flash('Policy deleted successfully!', 'success')
    return redirect(url_for('policies'))

@app.route('/claims', methods=['GET', 'POST'])
def claims():
    if request.method == 'GET':
        claims = Claim.query.all()
        return render_template('claims.html', claims=claims)
    
    # POST method
    try:
        data = request.get_json()
        if not data or 'claim_amount' not in data or 'status' not in data or 'description' not in data:
            raise BadRequest('Invalid data')

        claim = Claim(
            client_id=int(data.get('client_id', 0)),
            policy_id=int(data.get('policy_id', 0)),
            claim_amount=float(data['claim_amount']),
            status=data['status'],
            description=data['description']
        )
        db.session.add(claim)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Claim added successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/add_claim', methods=['POST'])
def add_claim_redirect():
    """Redirect /add_claim requests to /claims endpoint for backward compatibility"""
    return claims()

@app.route('/claims/<int:id>', methods=['PUT'])
def update_claim(id):
    try:
        data = request.get_json()
        claim = Claim.query.get_or_404(id)
        claim.claim_amount = float(data['claim_amount'])
        claim.status = data['status']
        claim.description = data['description']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Claim updated successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/claims/<int:id>', methods=['DELETE'])
def delete_claim(id):
    try:
        claim = Claim.query.get_or_404(id)
        db.session.delete(claim)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Claim deleted successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    
@app.route('/agents')
def agents():
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents)

@app.route('/add_agent', methods=['POST'])
def add_agent():
    try:
        agent = Agent(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            commission_rate=float(request.form['commission_rate'])
        )
        db.session.add(agent)
        db.session.commit()
        flash('Agent added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding agent: ' + str(e), 'error')
    return redirect(url_for('agents'))

@app.route('/agent/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)
    if request.method == 'POST':
        agent.name = request.form['name']
        agent.email = request.form['email']
        agent.phone = request.form['phone']
        agent.commission_rate = float(request.form['commission_rate'])
        db.session.commit()
        flash('Agent updated successfully!', 'success')
        return redirect(url_for('agents'))
    return render_template('edit_agent.html', agent=agent)

@app.route('/agent/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    db.session.delete(agent)
    db.session.commit()
    flash('Agent deleted successfully!', 'success')
    return redirect(url_for('agents'))

@app.route('/payments')
def payments():
    payments = Payment.query.all()
    clients = Client.query.all()
    return render_template('payments.html', payments=payments, clients=clients)

@app.route('/payments/<int:id>', methods=['GET'])
def view_payment(id):
    payment = Payment.query.get_or_404(id)
    return jsonify(payment.to_dict())

@app.route('/add_payment', methods=['POST'])
def add_payment():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        # Ensure all required fields are present
        required_fields = ['client_id', 'amount', 'payment_method', 'status']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Create the payment
        payment = Payment(
            client_id=int(data['client_id']),
            amount=float(data['amount']),
            payment_date=datetime.strptime(data.get('payment_date', datetime.utcnow().strftime('%Y-%m-%dT%H:%M')), '%Y-%m-%dT%H:%M'),
            payment_method=data['payment_method'],
            transaction_id=data.get('transaction_id'),  # Optional field
            status=data['status']
        )
        db.session.add(payment)
        db.session.commit()

        if request.is_json:
            return jsonify({'success': True, 'message': 'Payment added successfully!', 'payment': payment.to_dict()})
        else:
            flash('Payment added successfully!', 'success')
            return redirect(url_for('payments'))
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': str(e)}), 400
        else:
            flash(f'Error adding payment: {str(e)}', 'error')
            return redirect(url_for('payments'))

@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    try:
        payment = Payment.query.get_or_404(id)
        data = request.get_json()

        # Update fields if provided
        if 'client_id' in data:
            payment.client_id = int(data['client_id'])
        if 'amount' in data:
            payment.amount = float(data['amount'])
        if 'payment_date' in data:
            payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%dT%H:%M')
        if 'payment_method' in data:
            payment.payment_method = data['payment_method']
        if 'transaction_id' in data:
            payment.transaction_id = data['transaction_id']
        if 'status' in data:
            payment.status = data['status']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Payment updated successfully!', 'payment': payment.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    try:
        payment = Payment.query.get_or_404(id)
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Payment deleted successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
    
@app.route('/underwriters')
def underwriters():
    underwriters = Underwriter.query.all()
    return render_template('underwriters.html', underwriters=underwriters)

@app.route('/add_underwriter', methods=['GET', 'POST'])
def add_underwriter():
    form = UnderwriterForm()
    if form.validate_on_submit():
        underwriter = Underwriter(
            name=form.name.data,
            email=form.email.data,
            specialization=form.specialization.data,
            license_number=form.license_number.data
        )
        db.session.add(underwriter)
        db.session.commit()
        flash('Underwriter added successfully!', 'success')
        return redirect(url_for('underwriters'))
    return render_template('add_underwriter.html', form=form)

@app.route('/underwriter/edit/<int:id>', methods=['GET', 'POST'])
def edit_underwriter(id):
    underwriter = Underwriter.query.get_or_404(id)
    form = UnderwriterForm(obj=underwriter)
    
    if form.validate_on_submit():
        form.populate_obj(underwriter)
        db.session.commit()
        flash('Underwriter updated successfully!', 'success')
        return redirect(url_for('underwriters'))
    return render_template('edit_underwriter.html', form=form, underwriter=underwriter)

@app.route('/underwriter/delete/<int:id>')
def delete_underwriter(id):
    underwriter = Underwriter.query.get_or_404(id)
    db.session.delete(underwriter)
    db.session.commit()
    flash('Underwriter deleted successfully!', 'success')
    return redirect(url_for('underwriters'))

@app.route('/accidents', methods=['GET', 'DELETE'])
def accidents():
    if request.method == 'DELETE':
        return jsonify({'error': 'Direct DELETE on /accidents not allowed'}), 405
    accidents = Accident.query.all()
    form = AccidentForm()  # Create form instance for the modal
    return render_template('accidents.html', accidents=accidents, form=form)

@app.route('/add_accident', methods=['POST'])
def add_accident():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        # Parse date with fallback to current date
        try:
            accident_date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        except (TypeError, ValueError):
            accident_date = datetime.utcnow()

        # Create new accident
        accident = Accident(
            client_id=int(data.get('client_id')),
            date=accident_date,
            description=data.get('description'),
            damage_amount=float(data.get('damage_amount', 0)),
            location=data.get('location'),
            severity=data.get('severity')
        )
        
        db.session.add(accident)
        db.session.commit()

        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Accident recorded successfully',
                'id': accident.id
            }), 201
        else:
            flash('Accident recorded successfully!', 'success')
            return redirect(url_for('accidents'))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        else:
            flash(f'Error recording accident: {str(e)}', 'error')
            return redirect(url_for('accidents'))

@app.route('/update_accident/<int:id>', methods=['PUT'])
def update_accident(id):
    accident = Accident.query.get_or_404(id)
    data = request.get_json()
    
    accident.location = data.get('location', accident.location)
    accident.date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    accident.description = data.get('description', accident.description)
    accident.damage_amount = data.get('damage_amount', accident.damage_amount)
    accident.client_id = data.get('client_id', accident.client_id)
    accident.severity = data.get('severity', accident.severity)
    
    db.session.commit()
    return jsonify({'success': True})
@app.route('/delete_accident/<int:id>', methods=['DELETE'])
def delete_accident(id):
    try:
        accident = Accident.query.get_or_404(id)
        db.session.delete(accident)
        db.session.commit()
        return jsonify({'message': 'Accident record deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/beneficiaries')
def beneficiaries():
    beneficiaries = Beneficiary.query.all()
    return render_template('beneficiaries.html', beneficiaries=beneficiaries)

@app.route('/beneficiary', methods=['POST', 'PUT'])
def add_edit_beneficiary():
    try:
        if request.method == 'POST':
            # Validate input data
            if not all(k in request.form for k in ['client_id', 'policy_id', 'name', 'relationship', 'percentage']):
                flash('Error: Missing required fields', 'error')
                return redirect(url_for('beneficiaries'))

            # Verify client and policy exist first
            client = Client.query.get(int(request.form['client_id']))
            policy = Policy.query.get(int(request.form['policy_id']))
            
            if not client:
                flash('Error: Client does not exist!', 'error')
                return redirect(url_for('beneficiaries'))
            
            if not policy:
                flash('Error: Policy does not exist!', 'error')
                return redirect(url_for('beneficiaries'))

            # Create new beneficiary
            new_beneficiary = Beneficiary(
                name=request.form['name'],
                relationship=request.form['relationship'],
                policy_id=policy.id,
                client_id=client.id,
                percentage=float(request.form['percentage']),
                contact_info=request.form.get('contact_info', '')
            )
            
            db.session.add(new_beneficiary)
            db.session.commit()
            flash('Beneficiary added successfully!', 'success')
            
        elif request.method == 'PUT':
            beneficiary_id = int(request.form['id'])
            beneficiary = Beneficiary.query.get_or_404(beneficiary_id)
            beneficiary.name = request.form['name']
            beneficiary.relationship = request.form['relationship']
            beneficiary.percentage = float(request.form['percentage'])
            beneficiary.contact_info = request.form['contact_info']
            db.session.commit()
            flash('Beneficiary updated successfully!', 'success')

    except ValueError as e:
        db.session.rollback()
        flash(f'Error: Invalid input values - {str(e)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: Could not process beneficiary - {str(e)}', 'error')
    
    return redirect(url_for('beneficiaries'))

@app.route('/beneficiary/delete/<int:id>', methods=['POST'])
def delete_beneficiary(id):
    beneficiary = Beneficiary.query.get_or_404(id)
    db.session.delete(beneficiary)
    db.session.commit()
    flash('Beneficiary deleted successfully!', 'success')
    return redirect(url_for('beneficiaries'))

if __name__ == '__main__':
    app.run(debug=True)
