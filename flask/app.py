from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
key = os.urandom(21)
app.secret_key = key


URI = 'sqlite:///note.db'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Note(db.Model):
  __tablename__ = 'notes'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30), unique=True)
  body = db.Column(db.String(300))
  date = db.Column(db.DateTime, nullable=False, default=datetime.now())



@app.cli.command('initialize_DB')
def initialize_DB():
  db.create_all()

@app.route('/')
def index():
  title = '一覧画面'
  all_data = Note.query.all()
  return render_template('index.html', title=title, all_data=all_data)

@app.route('/create')
def create():
  title = '新規作成'
  return render_template('create.html', title=title)


@app.route('/register', methods={'post'})
def register():
  title = request.form['title']
  if title:
    body = request.form['body']
    register_data = Note(title=title, body=body)
    db.session.add(register_data)
    db.session.commit()
    flash('登録できました')
    return redirect(url_for('index'))
  else:
    flash('作成できませんでした。入力内容を確認してください。')
    return redirect(url_for('index'))

@app.route('/detail')
def detail():
  title = '詳細画面'
  id = request.args.get('id')
  print(id)
  data = Note.query.get(id)
  return render_template('detail.html', title=title, data=data)


@app.route('/edit')
def edit():
  title = '編集画面'
  id = request.args.get('id')
  edit_data = Note.query.get(id)
  return render_template('edit.html', title=title, edit_data=edit_data)

@app.route('/update', methods=['POST'])
def update():
  id = request.form['id']
  org_data = Note.query.get(id)
  org_data.title = request.form['title']
  org_data.body = request.form['body']
  db.session.merge(org_data)
  db.session.commit()
  flash('更新しました')
  return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
  delete_data = Note.query.get(id)
  db.session.delete(delete_data)
  db.session.commit()
  flash('削除しました')
  return redirect(url_for('index'))
