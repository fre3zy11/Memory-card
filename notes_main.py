#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, 
QPushButton, QHBoxLayout, 
QVBoxLayout, QLabel, 
QMessageBox, QRadioButton, 
QGroupBox, QButtonGroup,
QLineEdit, QTextEdit,
QListWidget, QInputDialog)

import json

notes = {
    "Добро пожаловать!" : {
        "текст": "Это самое лучшее приложение для заметок в мире",
        "теги": ["добро", "инструкция"]
    }
}

with open("notes_data.json", "w") as file:
    json.dump(notes, file)


def add_note():
    note_name, ok = QInputDialog.getText(window, "Добавить заметку", "Название заметки")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = text_field.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        text_field.clear()
        list_notes.addItems(notes)
        list_tags.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = text_tag.text()
        if not text_tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            text_tag.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)



def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        element = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(element)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def search_tag():
    tag = text_tag.text()
    if btr_search.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:   
                notes_filtered[note]=notes[note]
        btr_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btr_search.text() == "Сбросить поиск":
        text_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btr_search.setText('Искать заметки по тегу')
    else:
        pass





app = QApplication([])


window = QWidget()
window.setWindowTitle('Умные Заметки')

text_field = QTextEdit()
text_field.setText('Тут можно что-то написать')

h_layout1 = QHBoxLayout()
text1 = QLabel('Список заметок')
h_layout1.addWidget(text1)

h_layout2 = QHBoxLayout()
list_notes = QListWidget()
h_layout2.addWidget(list_notes)

h_layout3 = QHBoxLayout()
btr_create = QPushButton('Создать заметку')
btr_delete = QPushButton('Удалить заметку')
h_layout3.addWidget(btr_create)
h_layout3.addWidget(btr_delete)

h_layout4 = QHBoxLayout()
btr_save = QPushButton('Сохранить заметку')
h_layout4.addWidget(btr_save)

h_layout5 = QHBoxLayout()
text2 = QLabel('Список тегов')
h_layout5.addWidget(text2)

h_layout6 = QHBoxLayout()
list_tags = QListWidget()
h_layout6.addWidget(list_tags)

h_layout7 = QHBoxLayout()
text_tag = QLineEdit()
text_tag.setPlaceholderText('Введите тег...')
h_layout7.addWidget(text_tag)

h_layout8 = QHBoxLayout()
btr_add = QPushButton('Добавить к заметке')
btr_unpin = QPushButton('Открепить от заметки')
h_layout8.addWidget(btr_add)
h_layout8.addWidget(btr_unpin)


h_layout9 = QHBoxLayout()
btr_search = QPushButton('Искать заметки по тегу')
h_layout9.addWidget(btr_search)

v_layout1 = QVBoxLayout()
v_layout1.addWidget(text_field)
v_layout2 = QVBoxLayout()
v_layout2.addLayout(h_layout1)
v_layout2.addLayout(h_layout2)
v_layout2.addLayout(h_layout3)
v_layout2.addLayout(h_layout4)
v_layout2.addLayout(h_layout5)
v_layout2.addLayout(h_layout6)
v_layout2.addLayout(h_layout7)
v_layout2.addLayout(h_layout8)
v_layout2.addLayout(h_layout9)

main_layout = QHBoxLayout()
main_layout.addLayout(v_layout1)
main_layout.addLayout(v_layout2)
window.setLayout(main_layout)


def show_note():
    key = list_notes.selectedItems()[0].text()
    text_field.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

list_notes.itemClicked.connect(show_note)


with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

btr_create.clicked.connect(add_note)
btr_save.clicked.connect(save_note)
btr_delete.clicked.connect(del_note)
btr_add.clicked.connect(add_tag)
btr_unpin.clicked.connect(del_tag)
btr_search.clicked.connect(search_tag)


window.show()
app.exec()
