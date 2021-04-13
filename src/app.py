from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

import sys
import sqlite3


class UserfileModel(object):
    def __init__(self):
        # Create or open the database for user files in the file system
        self._db = sqlite3.connect('../data/user-files.sqlite3')
        self._db.row_factory = sqlite3.Row

        # Attempt to open the file table. If that fails, create a new file table        
        try:
            one_file = self._db.cursor().execute("SELECT * from userfiles").fetchone()
        except:
            if(self._db.cursor().rowcount != 1):
                self._db.cursor().execute('''
                CREATE TABLE userfiles(
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    date TEXT,
                    author TEXT,
                    content TEXT)
                ''')
            self._db.commit()

        self.current_id = None

    # define Read/Write actions
    def add(self, Userfile):
        self._db.cursor().execute('''
            INSERT INTO userfiles(filename, date, author, content)
            VALUES(:filename, :date, :author, :content)''',
                                  Userfile)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT filename, id from userfiles").fetchall()

    def get_userfile(self, userfile_id):
        return self._db.cursor().execute(
            "SELECT * from userfiles WHERE id=:id", {"id": userfile_id}).fetchone()

    def get_current_userfile(self):
        if self.current_id is None:
            return {"filename": "", "date": "", "author": "", "content": ""}
        else:
            return self.get_userfile(self.current_id)

    def update_current_userfile(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE userfiles SET filename=:filename, date=:date,
                author=:author, content=:content WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_userfile(self, userfile_id):
        self._db.cursor().execute('''
            DELETE FROM userfiles WHERE id=:id''', {"id": userfile_id})
        self._db.commit()

        
# list screen
class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       title="List of user files")
        # Save from the model that accesses the userfiles database.
        self._model = model

        # Create the form for displaying the list of userfiles.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="userfiles",
            on_change=self._on_pick)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit File")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["userfiles"]
        raise NextScene("Edit File")

    def _delete(self):
        self.save()
        self._model.current_id = self.data["userfiles"]
        raise NextScene("Delete File")
        # self._model.delete_userfile(self.data["userfiles"])
        # self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

        
# edit screen
class UserfileView(Frame):
    def __init__(self, screen, model):
        super(UserfileView, self).__init__(screen,
                                          screen.height * 2 // 2,
                                          screen.width * 2 // 2,
                                          hover_focus=True,
                                          title="File Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the userfiles database.
        self._model = model

        # Create the form for displaying the list of userfiles.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("File Name:", "filename"))
        layout.add_widget(Text("Date:", "date"))
        layout.add_widget(Text("Author:", "author"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Content:", "content", as_string=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(UserfileView, self).reset()
        self.data = self._model.get_current_userfile()

    def _ok(self):
        self.save()
        self._model.update_current_userfile(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")

        
# delete confirmation screen
class DeleteConfirmView(Frame):
    def __init__(self, screen, model):
        super(DeleteConfirmView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          title="Delete File?",
                                          reduce_cpu=True)
        # Save off the model that accesses the userfiles database.
        self._model = model

        # Create the form for displaying the list of userfiles.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("File to delete:", "filename"))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(DeleteConfirmView, self).reset()
        self.data = self._model.get_current_userfile()
        

    def _ok(self):
        self.save()
        self._model.delete_userfile(self._model.current_id)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")

# load views
def load_views(screen, scene):
    scenes = [
        Scene([ListView(screen, userfiles)], -1, name="Main"),
        Scene([UserfileView(screen, userfiles)], -1, name="Edit File"),
        Scene([DeleteConfirmView(screen, userfiles)], -1, name="Delete File")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)

userfiles = UserfileModel()
last_scene = None
while True:
    try:
        Screen.wrapper(load_views, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
