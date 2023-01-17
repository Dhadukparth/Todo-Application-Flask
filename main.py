from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = "randome any string"


class todos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    desc = db.Column(db.Text())

    def __repr__(self) -> str:
        return f"{self.title}"

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    alltodos = todos.query.all()
    return render_template('index.html', todos=alltodos)



@app.route('/newTodo', methods=['POST'])
def newTodo():
    title = request.form['new_todo_title']
    desc = request.form['new_todo_description']
    newtodo = todos(title=title, desc=desc)
    db.session.add(newtodo)
    db.session.commit()
    flash('New Todo Create Successfully.')
    return redirect(url_for('home'))


@app.route('/remove/<tid>', methods=['GET'])
def deleteTodo(tid):
    dtodo = todos.query.get(tid)
    db.session.delete(dtodo)
    db.session.commit()
    flash('Delete Successfully.')
    return redirect(url_for('home'))

@app.route('/edit/<tid>', methods=['GET'])
def editTodo(tid):
    etododata = todos.query.get(tid)
    return render_template('update.html', tdata=etododata)


@app.route('/editTodo', methods=['POST'])
def updateTodo():
        eid = request.form['todo_id']
        etitle = request.form['edit_todo_title']
        edesc = request.form['edit_todo_description']

        etodo = todos.query.get(eid)
        etodo.title = etitle
        etodo.desc = edesc
        db.session.commit()

        flash('Update Successfully.')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)