from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:daniel@localhost/classes' 
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmapanoouolbgw:d48dbfb020e963fcbb8b2160a53a8846c542ed4a92a2f00eab13c45121d690cb@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d1u0deel3jdjmn'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    _class = db.Column(db.String(5))
    note = db.Column(db.Text())

    def __init__(self, title, _class, note):
        self.title = title
        self._class = _class
        self.note = note

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        note = request.form['note']
        title = request.form['title']
        _class = request.form['class']
        if note == '':
            return render_template('index.html', message='NOTE CAN\'T BE EMPTY')

        data = Note(title, _class, note)
        db.session.add(data)
        db.session.commit()
        return render_template('notes.html', note=note, title=title, _class=_class)

@app.route('/notes', methods=['GET'])
def all_notes():
    notes = db.session.query(Note).all()
    return render_template('notes.html', notes=notes)

@app.route('/notes/<_class>', methods=['GET'])
def class_notes(_class):
    notes = db.session.query(Note).filter_by(_class=_class).all()
    return render_template('notes.html', notes=notes)

@app.route('/delete/<note_id>', methods=['DELETE', 'GET'])
def delete(note_id):               
    result = db.session.query(Note).filter_by(id=note_id).first()

    if result is not None:
        db.session.delete(result)
        db.session.commit()
        return render_template('notes.html')
    return render_template('notes.html')

if __name__ == '__main__':
    app.run()
