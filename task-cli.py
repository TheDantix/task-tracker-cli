import json, time, os
from datetime import datetime

uniqueId = 0

def search(name, var, lst):
    for element in lst:
        if element[name] == var:
            return element
    return None

def searchwith(name, var, lst):
    elements = []
    for element in lst:
        if element[name] == var:
            elements.append(element)
    return elements

def saveData(data):
    with open("data.json", "w") as fdata:
        json.dump(data, fdata)

def mark(id, status):
    element = search("id", id, data["tasks"])
    element["status"] = status
    element["updatedAt"] = time.time()

def getUniqueId():
    global uniqueId
    while (search("id", uniqueId, data["tasks"])):
        uniqueId += 1
    return uniqueId

if not os.path.exists("data.json"):
    with open("data.json", "w") as fdata:
        json.dump({"tasks": []}, fdata)

with open("data.json", "r") as fdata:
    data = json.load(fdata);

print("Hello! Welcome to Task Tracker.\n\nType command help, if you want seeing list all commands.")

while True:
    inp = input(": ")

    command = inp.split()[0]
    arguments = inp.split(' ')[1:]
    
    match command:
        case "help":
            print('''help - Displays list all commands
add [Task description] - Adds task in list
update [ID task] [Новое описание задачи] - Updates current task description
delete [ID task] - Removes task
mark-in-progress [ID task] - Sets task status is "in-progress"
mark-done [ID task] - Sets task status is "done"
list - Displays list all tasks
list [todo, done, in-progress] - Displays list all todo, done or in-progress tasks
                ''')
        case "add":
            task = {"id": getUniqueId(), "description": ' '.join(arguments), "status": "todo", "createdAt": time.time(), "updatedAt": time.time()}
            data["tasks"].append(task)
            
            saveData(data)

            print(f'Task successfully added (ID: {task["id"]})')

        case "update":
            task = search("id", int(arguments[0]), data["tasks"])
            task["description"] = ' '.join(arguments[1:])
            task["updatedAt"] = time.time()

            saveData(data)

        case "delete":
            data["tasks"].remove(search("id", int(arguments[0]), data["tasks"]))

            saveData(data)

        case "mark-in-progress":
            mark(int(arguments[0]), "in-progress")

            saveData(data)

        case "mark-done":
            mark(int(arguments[0]), "done")

            saveData(data)

        case "list":
            if not arguments:
                for task in data["tasks"]:
                    print(f'ID {task["id"]} | {task["description"]} | Status {task["status"]} | Created at {datetime.fromtimestamp(task["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')} | Updated at {datetime.fromtimestamp(task["updatedAt"]).strftime('%Y-%m-%d %H:%M:%S')}')
            else:
                for task in searchwith("status", arguments[0], data["tasks"]):
                    print(f'ID {task["id"]} | {task["description"]} | Status {task["status"]} | Created at {datetime.fromtimestamp(task["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')} | Updated at {datetime.fromtimestamp(task["updatedAt"]).strftime('%Y-%m-%d %H:%M:%S')}')
            
        case _:
            print(f"Command {command} not found")