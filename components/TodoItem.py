from flet import *

class TodoItem(UserControl):

    def __init__(self, id, name, isCompleted, getTodos, deleteTodo, db):
        super().__init__()
        self.id = id
        self.name = name
        self.isCompleted = isCompleted
        self.getTodos = getTodos
        self.delete = deleteTodo
        self.db = db

    def build(self):
        self.checkbox = Checkbox(value = self.isCompleted, on_change = self.changeStatus)
        self.text = Text(value = str(self.name), size = 30)
        self.editBtn = IconButton(icon = icons.EDIT, on_click = self.showEdit)
        self.deleteBTn = IconButton(icon = icons.DELETE, on_click = self.deleteTodo)
        self.editInput = TextField(value = str(self.name))
        self.savebtn = IconButton(icon = icons.CHECK, on_click = self.updateTodo)
        self.cancelbtn = IconButton(icon = icons.CANCEL, on_click = self.cancel)
        
        self.itemrow =  Container(
            border = border.all(3.0, colors.BLACK) if self.isCompleted else border.all(1.0, colors.BLACK),
            border_radius = 15,
            height = 50,
            content = Row(controls = [
            self.checkbox,
            self.text,
            Row(controls = [
                self.editBtn,
                self.deleteBTn
            ])
        ], width = 500, alignment = MainAxisAlignment.SPACE_BETWEEN))

        self.editrow = Row(controls = [
            self.editInput,
            self.savebtn,
            self.cancelbtn
        ], width = 500, alignment = MainAxisAlignment.CENTER, visible = False)

        return Column(controls = [
            self.itemrow,
            self.editrow
        ])

    def showEdit(self, e):
        self.itemrow.visible = False
        self.editrow.visible = True
        self.update()

    def cancel(self, e):
        self.itemrow.visible = True
        self.editrow.visible = False
        self.update()

    def updateTodo(self, e):
        newName = str(self.editInput.value)
        todo_ref = self.db.collection(u'todos').document(self.id)
        todo_ref.update({
            u'name' : newName
        })
        self.editrow.visible = False
        self.itemrow.visible = True
        self.getTodos()
    
    def deleteTodo(self, e):
        self.db.collection(u'todos').document(self.id).delete()
        self.getTodos()

    def changeStatus(self, e):
        todo_ref = self.db.collection(u'todos').document(self.id)
        if self.checkbox.value == True:
            todo_ref.update({
                u'isCompleted' : not self.isCompleted
            })
        else:
            todo_ref.update({
                u'isCompleted' : not self.isCompleted
            })
        self.getTodos()
