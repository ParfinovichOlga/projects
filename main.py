from cp import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Contracts ans projects")
window.geometry('1000x400')
window.config(padx=10, pady=60, background=BACKGROUND_COLOR)

contract = Contract()
project = Project()


# adding new contract
def add_contract():
    name = entry.get()
    showinfo(title="Info", message=contract.create_contract(name))


# adding new contract
def add_project():
    name = entry_1.get()
    showinfo(title="Info", message=project.create_project(name))


# close contract from project's menu
def close_contract():
    name = entry_4.get()
    showinfo(title="Info", message=project.close_contract(name))


# creating table with existing Contracts in another window
def click_1():
    window_2 = Tk()
    window_2.title("Contracts")
    window_2.geometry('600x400')
    all_contracts = contract.get_all_contracts()
    columns = ("id", "name", "creation date", "signin date", "status", "project_id")
    table = ttk.Treeview(window_2, columns=columns, show="headings")
    table.pack(fill=BOTH, expand=1)
    table.heading("id", text="№", anchor=W)
    table.heading("name", text="name", anchor=W)
    table.heading("creation date", text="creation date", anchor=W)
    table.heading("signin date", text="signin date", anchor=W)
    table.heading("status", text="status", anchor=W)
    table.heading("project_id", text="project", anchor=W)
    table.column("#1", stretch=NO, width=35)
    table.column("#2", stretch=NO, width=200)
    table.column("#3", stretch=NO, width=100)
    table.column("#4", stretch=NO, width=100)
    table.column("#5", stretch=NO, width=70)
    table.column("#6", stretch=NO, width=50)
    data = [[n["id"], n['name'], n['creation_date'], n['signing_date'], n['status'], n['project_id']]for n
            in all_contracts]
    for element in data:
        table.insert("", END, values=element)


# creating table with existing Projects in another window
def click_2():
    window_3 = Tk()
    window_3.title("Projects")
    window_3.geometry('600x400')
    all_projects = project.get_all_projects()
    columns = ("id", "name", "creation date", "contracts")
    table = ttk.Treeview(window_3, columns=columns, show="headings")
    table.pack(fill=BOTH, expand=1)
    table.heading("id", text="№", anchor=W)
    table.heading("name", text="name", anchor=W)
    table.heading("creation date", text="creation date", anchor=W)
    table.heading("contracts", text="contracts", anchor=W)
    table.column("#1", stretch=NO, width=35)
    table.column("#2", stretch=NO, width=200)
    table.column("#3", stretch=NO, width=100)
    table.column("#4", stretch=NO, width=400)
    data = [[n["id"], n['name'], n['creation_date'], n['contracts']]for n
            in all_projects]
    for element in data:
        table.insert("", END, values=element)


# creating drop-down list for selection contract to confirm
def create_combox_1():
    def selected(event):
        selection = combobox.get()
        contract.confirm_contract(selection)
    all_contracts = contract.get_all_contracts()
    data = [element['name'] for element in all_contracts]
    combobox = ttk.Combobox(values=data, state="readonly")
    combobox.grid(column=1, row=3)
    combobox.bind("<<ComboboxSelected>>", selected)


# creating drop-down list for selection contract to complete
def create_combox_2():
    def selected(event):
        selection = combobox_2.get()
        contract.complete_contract(selection)
    all_contracts = contract.get_all_contracts()
    data = [element['name'] for element in all_contracts]
    combobox_2 = ttk.Combobox(values=data, state="readonly")
    combobox_2.grid(column=1, row=4)
    combobox_2.bind("<<ComboboxSelected>>", selected)


# creating drop-down list for selection contract for project
def create_combox_3():
    def selected(event):
        project_name = entry_3.get()
        selection = combobox_3.get()
        showinfo(title="Info", message=project.add_contract(project_name, selection))
    all_contracts = contract.get_all_contracts()
    data = [element['name'] for element in all_contracts]
    combobox_3 = ttk.Combobox(values=data, state="readonly")
    combobox_3.grid(column=5, row=4)
    combobox_3.bind("<<ComboboxSelected>>", selected)


# Close program
def close_program():
    if askyesno("Quit", "Do you want to close the program?"):
        window.destroy()


# Contract MENU
label = Label(text="Contracts", background=BACKGROUND_COLOR, font=("Ariel", 25, "italic"), pady=30)
label.grid(column=0, row=0)

label = Label(text="Contract's name", background=BACKGROUND_COLOR, font=("Ariel", 9, "italic"))
label.grid(column=0, row=2)

entry = Entry(width=23)
entry.grid(column=1, row=2)

button = Button(text="Create", background=BACKGROUND_COLOR, width=18, command=add_contract, highlightthickness=0)
button.grid(column=2, row=2)

button = Button(text="Confirm contract", background=BACKGROUND_COLOR, width=18, command=create_combox_1, highlightthickness=0)
button.grid(column=2, row=3)

button = Button(text="Complete contract", background=BACKGROUND_COLOR, width=18, command=create_combox_2,
                highlightthickness=0)
button.grid(column=2, row=4)

# Project MENU
label = Label(text="Projects", background=BACKGROUND_COLOR, font=("Ariel", 25, "italic"))
label.grid(column=4, row=0)

label = Label(text="Project's name", background=BACKGROUND_COLOR, font=("Ariel", 9, "italic"))
label.grid(column=4, row=2)

entry_1 = Entry(width=23)
entry_1.grid(column=5, row=2)

button = Button(text="Create", background=BACKGROUND_COLOR, width=18, command=add_project, highlightthickness=0)
button.grid(column=6, row=2)

label = Label(text="Project's name for adding contract", background=BACKGROUND_COLOR,
              font=("Ariel", 9, "italic"))
label.grid(column=4, row=3)

entry_3 = Entry(width=23)
entry_3.grid(column=5, row=3)

button = Button(text="Add contract", background=BACKGROUND_COLOR, width=18, command=create_combox_3, highlightthickness=0)
button.grid(column=6, row=4)

label = Label(text="Project's name for completing contract", background=BACKGROUND_COLOR,
              font=("Ariel", 9, "italic"))
label.grid(column=4, row=5)

entry_4 = Entry(width=23)
entry_4.grid(column=5, row=5)

button = Button(text="Complete contract", background=BACKGROUND_COLOR, width=18, command=close_contract,
                highlightthickness=0)
button.grid(column=6, row=5)

button = Button(text="All contract", command=click_1, background=BACKGROUND_COLOR, highlightthickness=0)
button.grid(column=0, row=8)

button = Button(text="All projects", command=click_2, background=BACKGROUND_COLOR, highlightthickness=0)
button.grid(column=4, row=8)

close_image = PhotoImage(file="./close1.png")
button = Button(image=close_image, command=close_program, background=BACKGROUND_COLOR, highlightthickness=0,
                width=30, height=30)
button.grid(column=10, row=0)


window.mainloop()