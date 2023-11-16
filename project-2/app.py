from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import math
import json


with open("main.json", "r") as c:
    paras = json.load(c)["paras"]

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/todolist"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    desc = db.Column(db.String(160), nullable=False)


@app.route("/")
def home():
    # todo_list = []

    # if request.args.get('page'):
    #     todo_list = Todo.query.filter_by().all()
    #     last = len(todo_list) // int(paras['no_of_todos'])

    # page = request.args.get('page')
    # if (not str(page).isnumeric()):
    #     page = 1

    # page = int(page)
    # todo_list = todo_list[(page-1)*int(paras['no_of_todos']): (page - 1) *
    #                       int(paras['no_of_todos']) + int(paras['no_of_todos'])]

    # # pagination logic
    # prev = ""
    # next = ""
    # if page == 1:
    #     prev = "#"
    #     next = "/?page=" + str(page+1)
    # elif page == last:
    #     prev = "/?page=" + str(page-1)
    #     next = "#"
    # else:
    #     prev = "/?page=" + str(page-1)
    #     next = "/?page=" + str(page+1)

    # return render_template('index.html', paras=paras, todo_list=todo_list, prev=prev, next=next)

    todo_list = Todo.query.filter_by().all()
    last = math.ceil(len(todo_list) / int(paras["no_of_todos"]))
    # len(todo_list) // int(paras['no_of_todos']) == 0:

    page = request.args.get("page")
    if not str(page).isnumeric():
        page = 1

    page = int(page)
    todo_list = todo_list[
        (page - 1) * int(paras["no_of_todos"]) : (page - 1) * int(paras["no_of_todos"])
        + int(paras["no_of_todos"])
    ]

    # pagination logic
    if page == 1:
        next = "/?page=" + str(page + 1) if (page + 1) <= last else "#"
        prev = "#"

    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        next = "/?page=" + str(page + 1)
        prev = "/?page=" + str(page - 1)

        # if page == 1 and len(todo_list) // int(paras['no_of_todos']) != 0:
        #     prev = "#"
        #     next = "/?page=" + str(page+1)

        # todo_list = Todo.query.all()
    return render_template(
        "index.html", paras=paras, todo_list=todo_list, prev=prev, next=next
    )


@app.route("/add", methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        entry = Todo(title=title, desc=desc)
        db.session.add(entry)
        db.session.commit()

    return render_template("add.html")


@app.route("/delete/<string:sno>", methods=["GET", "POST"])
def delete(sno):
    todo_list = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo_list)
    db.session.commit()
    return redirect("/")


app.run(debug=True)
