from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from project.models.models import User, Datasource
from project import db


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/admin')


@admin_blueprint.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        current_user = User.find_by_username(username)
        if not current_user:
            flash('ERROR! user not found.', 'error')
            return redirect(url_for('admin.dashboard'))

        if User.verify_hash(password, current_user.password):
            current_user.authenticated = True
            db.session.add(current_user)
            db.session.commit()
            login_user(current_user)

            return redirect(url_for('admin.dashboard'))
        else:
            db.session.rollback()
            flash('ERROR! Incorrect login credentials.', 'error')

    return render_template('login.html')


@admin_blueprint.route('/admin/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('admin.login'))


@admin_blueprint.route('/admin/')
# @login_required
def dashboard():
    return render_template('dashboard.html')


# USERS ############################################
@admin_blueprint.route('/admin/users')
# @login_required
def users():
    all_user = User.query.all()
    return render_template('users.html', users=all_user)


@admin_blueprint.route('/admin/user_add', methods=['GET', 'POST'])
# @login_required
def user_add():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = User.generate_hash(request.form.get('password'))
            is_admin = request.form.get('is-admin')
            if is_admin:
                new_user = User(username, password, role='admin')
            else:
                new_user = User(username, password)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('admin.users'))

        except IntegrityError:
            db.session.rollback()
            flash('ERROR! username ({}) already exists.'.format(username), 'error')

    return render_template('user_add.html')


@admin_blueprint.route('/admin/user_delete/<user_id>')
# @login_required
def user_delete(user_id):
    user = User.find_by_id(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))


@admin_blueprint.route('/admin/user_edit/<user_id>', methods=['GET', 'POST'])
# @login_required
def user_edit(user_id):
    user = User.find_by_id(user_id)
    if request.method == 'POST':
        try:
            is_admin = request.form.get('is-admin')
            password = request.form.get('password')

            user.username = request.form.get('username')
            user.password = User.generate_hash(password)
            if User.verify_hash(password, current_user.password):
                user.password = password

            user.address = request.form.get('address')
            if is_admin:
                user.role = 'admin'

            db.session.commit()
            return redirect(url_for('admin.users'))

        except IntegrityError:
            db.session.rollback()
            flash('ERROR! username ({}) already exists.'.format(user.username), 'error')

    return render_template('user_edit.html', user=user)

# Data Source ####################################################
@admin_blueprint.route('/admin/datasources')
# @login_required
def datasources():
    allsource = Datasource.query.all()
    return render_template('datasources.html', datasources=allsource)

@admin_blueprint.route('/admin/datasource_add', methods=['GET', 'POST'])
# @login_required
def datasource_add():
    if request.method == 'POST':
        try:
            site_name = request.form.get('site_name')
            site_url = request.form.get('site_url')

            new_datasource = Datasource(site_name, site_url)

            db.session.add(new_datasource)
            db.session.commit()
            return redirect(url_for('admin.datasources'))

        except IntegrityError:
            db.session.rollback()
            flash('ERROR!')

    return render_template('datasource_add.html')


@admin_blueprint.route('/admin/datasource_delete/<datasource_id>')
# @login_required
def datasource_delete(datasource_id):
    datasource = Datasource.find_by_id(datasource_id)
    db.session.delete(datasource)
    db.session.commit()
    return redirect(url_for('admin.datasources'))


@admin_blueprint.route('/admin/datasource_edit/<datasource_id>', methods=['GET', 'POST'])
# @login_required
def datasource_edit(datasource_id):
    datasource = Datasource.find_by_id(datasource_id)
    if request.method == 'POST':
        try:
            datasource.site_name = request.form.get('site_name')
            datasource.site_url = request.form.get('site_url')

            db.session.commit()
            return redirect(url_for('admin.datasources'))

        except IntegrityError:
            db.session.rollback()
            flash('ERROR!')

    return render_template('datasource_edit.html', datasource=datasource)

