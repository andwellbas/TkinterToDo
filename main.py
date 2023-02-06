import sqlite3
import tkinter
import functions
import tkinter.messagebox


class ToDoGUI:
    def __init__(self):
        #   main window settings
        self.main_window = tkinter.Tk()
        self.main_window.title("Your real life quests")
        self.main_window.resizable(False, False)
        self.main_window.geometry("300x185")
        self.main_window.configure(bg="LightBlue1")
        self.main_window.iconbitmap("book.ico")

        #   main window labels
        self.label_point_info = tkinter.Label(self.main_window, text="Quests completed:", bg="LightBlue1")

        self.label_point_info.place(x=0, y=0)

        self.points = tkinter.IntVar()
        self.points.set(functions.check_score())
        self.score_label = tkinter.Label(self.main_window, textvariable=self.points, bg="LightBlue1")

        self.score_label.place(x=105, y=0)

        #   main window info button
        self.info_button = tkinter.Button(self.main_window, text="?", command=functions.show_information,
                                          bg="LightBlue1")
        self.info_button.place(x=272, y=0, height=20)

        #   quests Frame
        self.outer_frame = tkinter.Frame(self.main_window)
        self.outer_frame.pack(padx=20, pady=20)

        self.inner_frame = tkinter.Frame(self.outer_frame)
        self.inner_frame.pack()

        self.listbox = tkinter.Listbox(self.inner_frame, height=5, width=40)
        self.listbox.pack(side="left")

        self.v_scrollbar = tkinter.Scrollbar(self.inner_frame, orient=tkinter.VERTICAL)
        self.v_scrollbar.pack(side='right', fill=tkinter.Y)

        self.h_scrollbar = tkinter.Scrollbar(self.outer_frame, orient=tkinter.HORIZONTAL)
        self.h_scrollbar.pack(side='bottom', fill=tkinter.X)

        self.v_scrollbar.config(command=self.listbox.yview())
        self.h_scrollbar.config(command=self.listbox.xview())

        self.listbox.config(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.show_quests()

        #   entry frame
        self.entry_frame = tkinter.Frame(self.main_window)
        self.quest_entry = tkinter.Entry(self.entry_frame, width=40)

        self.quest_entry.pack(side="left")
        self.entry_frame.pack()

        #   buttons Frame
        self.buttons_frame = tkinter.Frame(self.main_window)

        self.add_quest_button = tkinter.Button(self.buttons_frame, text="Add Quest",
                                               command=self.add_quest, bg="LightBlue1")
        self.random_quest_button = tkinter.Button(self.buttons_frame, text="Add Random Quest",
                                                  command=self.add_random_quest, bg="LightBlue1")
        self.delete_completed_quest = tkinter.Button(self.buttons_frame, text="Complete quest",
                                                     command=self.complete_quest, bg="LightBlue1")

        self.add_quest_button.pack(side="left")
        self.random_quest_button.pack(side="left")
        self.delete_completed_quest.pack(side="left")

        self.buttons_frame.pack()

        tkinter.mainloop()

    #   shows the contents of the database with quests, if the database is not found then creates it
    def show_quests(self):
        try:
            quests_list = functions.created_quests()
            for quest in quests_list:
                self.listbox.insert(tkinter.END, quest)
        except sqlite3.OperationalError:
            functions.create_sql_table()

    #   adds a random quest to the database
    def add_random_quest(self):
        try:
            self.listbox.delete(0, tkinter.END)

            functions.add_random_quest()

            self.show_quests()
        except FileNotFoundError:
            tkinter.messagebox.showerror("Random Quests File Not Found", "The file with random quests was not found,"
                                                                         " try reinstalling the application and see if"
                                                                         " the random_quests.dat file is in the"
                                                                         " application folder.")

    #   the function removes the quest from the database and adds one point to completed quests
    def complete_quest(self):
        try:
            ids_list = functions.check_id()
            user_id = int(self.quest_entry.get())

            if user_id in ids_list:
                functions.delete_completed_quest(user_id)

                self.listbox.delete(0, tkinter.END)

                self.show_quests()

                self.quest_entry.delete(0, tkinter.END)

                functions.plus_vault_point()

                self.points.set(functions.check_score())

            elif user_id not in ids_list:
                tkinter.messagebox.showinfo("ID not found", "There is no quest with this number")
                self.quest_entry.delete(0, tkinter.END)
        except ValueError:
            tkinter.messagebox.showerror("Value Error", "ID - integer")
            self.quest_entry.delete(0, tkinter.END)

    #   adds a user's quest to the database
    def add_quest(self):
        user_quest = self.quest_entry.get()

        if user_quest != "":
            functions.add_quest_to_db(user_quest)

            self.listbox.delete(0, tkinter.END)

            self.show_quests()

            self.quest_entry.delete(0, tkinter.END)

        elif user_quest == "":
            tkinter.messagebox.showinfo("No Quest", "First you need to write a quest")


if __name__ == '__main__':
    todo = ToDoGUI()
