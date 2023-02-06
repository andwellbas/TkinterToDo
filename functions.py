import pickle
import sqlite3
import random
import tkinter
import tkinter.messagebox


def create_sql_table():
    conn = sqlite3.connect("quests.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE Quests (QuestID INTEGER PRIMARY KEY NOT NULL, QuestName TEXT)''')

    conn.commit()
    conn.close()


def created_quests():
    quest_list = []
    con = sqlite3.connect("quests.db")
    cur = con.cursor()

    cur.execute('''SELECT * FROM Quests''')
    results = cur.fetchall()
    for row in results:
        quest_list.append(f"{row[0]:2}: {row[1]}")

    con.close()

    return quest_list


def add_quest_to_db(quest):
    try:
        conn = sqlite3.connect("quests.db")
        cur = conn.cursor()

        cur.execute('''INSERT INTO Quests (QuestName) VALUES (?)''', (quest,))

        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        create_sql_table()

        add_quest_to_db(quest)


def add_random_quest():
    input_file = open("random_quests.dat", "rb")
    todo_list = pickle.load(input_file)
    input_file.close()
    add_quest_to_db(random.choice(todo_list))


def delete_completed_quest(quest_id):
    con = sqlite3.connect("quests.db")
    cur = con.cursor()
    cur.execute('''DELETE FROM Quests WHERE QuestID == ?''', (quest_id,))
    con.commit()


def plus_vault_point():
    input_file = open("points_vault.dat", "rb")
    point = pickle.load(input_file)
    input_file.close()

    output_file = open("points_vault.dat", "wb")
    point += 1
    pickle.dump(point, output_file)
    output_file.close()


def check_score():
    try:
        input_file = open("points_vault.dat", "rb")
        point = int(pickle.load(input_file))
        input_file.close()
        return point

    except FileNotFoundError:
        point = 0
        output_file = open("points_vault.dat", "wb")
        pickle.dump(point, output_file)
        output_file.close()

        return point


def check_id():
    conn = sqlite3.connect("quests.db")
    cur = conn.cursor()
    cur.execute('''SELECT QuestID FROM Quests''')
    results = cur.fetchall()

    ids_list = []
    for i in results:
        ids_list.append(i[0])

    return ids_list


def show_information():
    tkinter.messagebox.showinfo("About the program",
                                "The program allows you to create quests for yourself or take random ones.\n"
                                "\n"
                                "You have 3 options\n\n"
                                "1) Adding your own quests\n"
                                "To do this, enter the quest itself in the field above the"
                                "buttons and click the 'Add Quest' button.\n\n"
                                "2) Adding a random quest\n"
                                "To do this, just click on the 'Add Random Quest' button.\n\n"
                                "3) Complete the quest\n"
                                "To do this, enter the quest number in the field above the buttons and click the"
                                "'Complete Quest' button.")
