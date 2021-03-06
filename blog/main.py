from flask import Flask, request,url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import *
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Blog(db.Model):
    user = db.Column(db.String(50),nullable = False,primary_key=True)
    post = db.Column(db.String(100),nullable =False)
    
    def __init__(self,user,post):
        self.user = user
        self.post = post


@app.route("/")
def home():
    content = Blog.query.all()
    return render_template("home.html",content=content)

@app.route('/add',methods = ['POST'])
def add():
    user = request.form.get('user')
    post = request.form.get('post')
    entry = Blog(user = user,post=post)
    db.session.add(entry)
    db.session.commit()
    return redirect("/")

@app.route('/delete/<string:content_user>')
def delete(content_user):
    content=Blog.query.get(content_user)
    if not content:
        return redirect("/")
    db.session.delete(content)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)