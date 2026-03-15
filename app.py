from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Campaign, CampaignUpdate
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

print("DB PATH:", app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)

# [Saad] - Login manager setup kora hoyeche, signin page e redirect korbe
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

# [Saad] - Session management er jonno user load kora hoy ekhane
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# [Saad] - Home page
@app.route('/')
def index():
    campaigns = Campaign.query.filter_by(status="approved").all()  # Module 2.4 [Hridoy] - Sudhu approved campaigns fetch kora hocche public visibility er jonno
    return render_template("index.html", campaigns=campaigns)


# [Saad]  - Notun user registration handle kore
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_pw,
            university_name=request.form['university']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template("signup.html")


# [Saad] - User signin handle kore
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template("signin.html")


# [Saad]  - User logout handle kore
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# [Saad] - User sob essential details diye campaign create korte parbe
# [Saad] - Submit er age sob mandatory field fill kora must
# [Saad] - Notun campaign "pending" hisebe admin review queue e jabe
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if request.method == 'POST':
        campaign = Campaign(
            title=request.form['title'],             # [Saad] - Campaign er title
            description=request.form['description'], # [Saad] - Uddeshyo ar description
            goal_amount=request.form['goal'],        # [Saad] - Funding er goal amount
            duration=request.form['duration'],       # [Saad] - Campaign er duration
            category=request.form['category'],       # [Saad] - Campaign er category
            user_id=current_user.id,                 # [Saad] - Campaign ta logged-in user er sathe link kora hocche
            status="pending"                         # [Saad] - Automatic vabe admin review queue e pathano hocche
        )
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("create_campaign.html")


# [Saad] - Admin sob pending campaigns er review queue dekhte parbe
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return redirect(url_for('index'))
    campaigns = Campaign.query.filter_by(status="pending").all()  # [Saad] - Admin review queue er jonno sob pending campaigns fetch kora hocche
    return render_template("admin_dashboard.html", campaigns=campaigns)


# [Siam] - Campaign creator approve deoar age campaign edit korte parbe
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(id):
    campaign = Campaign.query.get_or_404(id)

    # [Siam] - Sudhu owner edit korte pabe, ar campaign ta pending thakte hobe
    if campaign.user_id != current_user.id or campaign.status != "pending":
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        campaign.title = request.form['title']               # [Siam] - Title update kora hocche
        campaign.description = request.form['description']   # [Siam] - Description update kora hocche
        campaign.goal_amount = request.form['goal']          # [Siam] - Goal amount update kora hocche
        campaign.duration = request.form['duration']         # [Siam] - Duration update kora hocche
        campaign.category = request.form['category']         # [Siam] - Category update kora hocche
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template("edit_campaign.html", campaign=campaign)


# [Siam] - Campaign creator approve hওয়ার age campaign cancel korte parbe
@app.route('/cancel/<int:id>')
@login_required
def cancel_campaign(id):
    campaign = Campaign.query.get_or_404(id)

    # [Siam] - Sudhu owner cancel korte pabe, ar campaign ta pending thakte hobe
    if campaign.user_id == current_user.id and campaign.status == "pending":
        campaign.status = "cancelled"  # [Siam] - Status cancelled kora holo
        db.session.commit()

    return redirect(url_for('dashboard'))


# [Siam] - Admin campaign approve korte parbe
@app.route('/approve/<int:id>')
@login_required
def approve(id):
    if current_user.role == "admin":
        campaign = Campaign.query.get(id)
        campaign.status = "approved"  # [Siam] - Status approved kora holo;
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


# [Siam] - Admin campaign reject korte parbe
@app.route('/reject/<int:id>')
@login_required
def reject(id):
    if current_user.role == "admin":
        campaign = Campaign.query.get(id)
        campaign.status = "rejected"  # [Siam] - Status rejected kora holo;
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)