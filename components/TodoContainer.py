from flet import *
from .TodoItem import TodoItem

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./todoservicekey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class TodoContainer(UserControl):

    def build(self):
        self.input = TextField(label = "Todo Name", width = 390)
        self.addBtn = ElevatedButton(text = "+", on_click = self.addTodo)
        self.dd = Dropdown(
            width = 390,
            on_change = self.filter_todos,
            options=[
                dropdown.Option("All"),
                dropdown.Option("Completed"),
                dropdown.Option("Incomplete")
            ]
        )

        row = Row(controls = [
            self.input,
            self.addBtn
        ])

        self.todoList = ListView(height = 400, spacing = 15)

        return Column(controls = [
            row,
            self.dd,
            self.todoList
        ])
    
    def did_mount(self):
        self.getTodos()

    def filter_todos(self, e):
        todos = db.collection(u'todos')
        if(self.dd.value == "All"):
            self.getTodos()

        elif(self.dd.value == "Done"):
            completed_todos = todos.where(u'status', u'isCompleted', u'==', True).stream()
            self.todoList.controls.clear()
            for todo in completed_todos:
                self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
                self.update()
        
        elif(self.dd.value == "In Progress"):
            completed_todos = todos.where(u'status', u'isCompleted', u'==', True).stream()
            self.todoList.controls.clear()
            for todo in completed_todos:
                self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
                self.update()

        elif(self.dd.value == "Started"):
            completed_todos = todos.where(u'status', u'isCompleted', u'==', True).stream()
            self.todoList.controls.clear()
            for todo in completed_todos:
                self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
                self.update()
        
        elif(self.dd.value == "Done"):
            completed_todos = todos.where(u'status', u'isCompleted', u'==', True).stream()
            self.todoList.controls.clear()
            for todo in completed_todos:
                self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
                self.update()
                
        else:
            completed_todos = todos.stream()
            self.todoList.controls.clear()
            for todo in completed_todos:
                self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
                self.update()

    def getTodos(self):
        todos = db.collection(u'todos').stream()
        self.todoList.controls.clear()
        for todo in todos:
            self.todoList.controls.append(TodoItem(todo.id,
                                                   todo.to_dict()['name'],
                                                   todo.to_dict()['isCompleted'],
                                                   self.getTodos,
                                                   self.deleteTodo,
                                                   db))
            self.update()

    def addTodo(self, e):
        #self.todoList.controls.append(TodoItem(self.input.value, self.deleteTodo))
        doc_ref = db.collection("todos").document()
        doc_ref.set({
            u'name' : str(self.input.value),
            u'isCompleted' : False
        })
        
        self.input.value = ""
        self.getTodos()

    def deleteTodo(self, todo):
        self.todoList.controls.remove(todo)
        self.update()