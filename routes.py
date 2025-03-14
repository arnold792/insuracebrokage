from flask import Blueprint, redirect, url_for

# Create blueprint
admin = Blueprint('admin', __name__)

@admin.route('/delete_agent/<int:id>', methods=['GET', 'DELETE'])
def delete_agent(id):
    # Add your agent deletion logic here
    return redirect(url_for('agents'))

@admin.route('/delete_accident/<int:id>', methods=['GET', 'DELETE'])
def delete_accident(id):
    # Add your accident deletion logic here
    return redirect(url_for('accidents'))
