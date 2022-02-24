from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok
from datetime import datetime

app = Flask(__name__)
run_with_ngrok(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable = True)
    completed = db.Column(db.String(200),nullable = True)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return '<Student %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_content2 = request.form['content2']
        new_task = Todo(content=task_content,completed=task_content2)
     
        
        # try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
        # except:
        #     return "There is an issue"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'cannot delete the item'


@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.completed = request.form['content2']
        print(task_to_update.completed)
        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There is an issue with the code"

    else:
        return render_template('update.html',task = task_to_update)


if __name__ == "__main__":
    app.run()