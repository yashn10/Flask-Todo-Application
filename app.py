from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.no} - {self.title}"


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    todos = Todo.query.all()
    print(todos)
    return render_template('index.html', todos = todos)


@app.route("/products")
def products():
    todos = Todo.query.all()
    print(todos)
    return "<p>Hello, products page!</p>"


@app.route("/update/<int:no>", methods=['GET', 'POST'])
def update(no):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(no=no).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todos = Todo.query.filter_by(no=no).first()
    return render_template('update.html', todos=todos)


@app.route("/delete/<int:no>")
def delete(no):
    todos = Todo.query.filter_by(no=no).first()
    db.session.delete(todos)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
