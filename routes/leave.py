from flask import Blueprint, request, jsonify
from models import db, Leave, LeaveAction
from utils.jwt_utils import token_required

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/leave', methods=['POST'])
@token_required(role='Employee')
def apply_leave():
    data = request.get_json()
    leave = Leave(
        employee_id=request.user                                                                                    ['user_id'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(leave)
    db.session.commit()
    return jsonify({'message': 'Leave request submitted'})

@leave_bp.route('/leave', methods=['GET'])
@token_required(role='Employee')
def list_user_leaves():
    leaves = Leave.query.filter_by(employee_id=request.user['user_id']).all()
    return jsonify([{
        'id': l.id,
        'start_date': l.start_date,
        'end_date': l.end_date,
        'status': l.status
    } for l in leaves])

@leave_bp.route('/leave/pending', methods=['GET'])
@token_required(role='Manager')
def list_pending_leaves():
    leaves = Leave.query.filter_by(status='Pending').all()
    return jsonify([{
        'id': l.id,
        'employee_id': l.employee_id,
        'start_date': l.start_date,
        'end_date': l.end_date
    } for l in leaves])

@leave_bp.route('/leave/<int:leave_id>/approve', methods=['PUT'])
@token_required(role='Manager')
def approve_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = 'Approved'
    db.session.add(LeaveAction(leave_id=leave.id, manager_id=request.user['user_id'], action='Approved'))
    db.session.commit()
    return jsonify({'message': 'Leave approved'})

@leave_bp.route('/leave/<int:leave_id>/reject', methods=['PUT'])
@token_required(role='Manager')
def reject_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = 'Rejected'
    db.session.add(LeaveAction(leave_id=leave.id, manager_id=request.user['user_id'], action='Rejected'))
    db.session.commit()
    return jsonify({'message': 'Leave rejected'})