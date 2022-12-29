from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, FloatField, HiddenField
from wtforms.validators import DataRequired, regexp, Regexp
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = 'static/images'
Bootstrap(app)

# Create DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///skill-collection.db"
db = SQLAlchemy(app)

date = datetime.now().year


class AddSkill(FlaskForm):
    # id = HiddenField(validators=[DataRequired()])
    skill = StringField(label="Project Name", validators=[DataRequired()])
    overview = StringField(label="Description", validators=[DataRequired()])
    # image_link = StringField(label="Image URL", validators=[DataRequired()])
    # image_link = FileField(label="Choose File", validators=[DataRequired(), Regexp(u'^\\[^/\\].jpg$')])
    image_link = FileField(label="Choose File", validators=[DataRequired()])
    pj_url = StringField(label="Github url", validators=[DataRequired()])
    submit = SubmitField("Done")


# Create Table
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(250), unique=True, nullable=False)
    overview = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(50), nullable=False)
    git_url = db.Column(db.String(100), nullable=False)
    # data = db.Column(db.LargeBinary)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    skills = db.session.query(Skill).all()
    return render_template('index.html', skills=skills, date=date)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    form = AddSkill()
    if form.validate_on_submit():
        file = form.image_link.data # grab the file
        name = file.filename
        split_name = f"{name.split(' ')[0]}"
        new_name = name.replace(file.filename, f"{split_name}.jpg")
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(new_name))) # Then save the file
        with app.app_context():
            new_skill = Skill(skill_name=form.skill.data, overview=form.overview.data, img_url=new_name, git_url=form.pj_url.data)
            db.session.add(new_skill)
            db.session.commit()
        flash("Project uploaded successfully!")
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime
# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Create DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///skill-collection.db"
db = SQLAlchemy(app)

date = datetime.now().year


class AddSkill(FlaskForm):
    # id = HiddenField(validators=[DataRequired()])
    skill = StringField(label="Skill Name", validators=[DataRequired()])
    overview = StringField(label="Enter texts", validators=[DataRequired()])
    image_link = StringField(label="Image URL", validators=[DataRequired()])
    submit = SubmitField("Post")


# Create Table
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(250), unique=True, nullable=False)
    overview = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    skills = db.session.query(Skill).all()
    return render_template('index.html', skills=skills, date=date)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    form = AddSkill()
    if form.validate_on_submit():
        with app.app_context():
            new_skill = Skill(skill_name=form.skill.data, overview=form.overview.data, img_url=form.image_link.data)
            db.session.add(new_skill)
            db.session.commit()
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> github/master
