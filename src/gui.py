from tkinter import *
from tkinter import ttk, simpledialog, filedialog
from tkinter import messagebox as mb
from tkcalendar import Calendar
import datetime
import locale
import os
from task import *

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.db = Data()
        self.main_table_name = ""
        self.table_name_get()
        self.db.create_tables(self.main_table_name)
        self.current_date = datetime.now()
        day = self.current_date.strftime('%A')
        weekday_number = self.current_date.weekday()
        date_day_month = self.current_date.strftime('%d %B')
        date_day_month = date_day_month[:-1] + "я"
        day_text = f"{day.title()} ({date_day_month})"

        if self.db.check_days(self.main_table_name):
            self.days = self.db.notify_time(self.main_table_name)[0][0]

        self.title("Менеджер задач")
        self.geometry("1000x700")
        self.frame1 = Frame(self, borderwidth=1, highlightthickness=1, highlightbackground="grey", relief=RIDGE)
        self.frame1.pack(side=LEFT, fill=Y)
        frame2 = Frame(self, borderwidth=1, highlightthickness=1, highlightbackground="grey", relief=RIDGE)
        frame2.pack(side=TOP, fill=X)
        label1 = Label(frame2, text=day_text, font="-weight bold ")
        label1.pack(side=RIGHT, pady=5)
        options = ["Уведомления", "Импорт", "Экспорт"]
        set_menu = Menu(tearoff=0)
        set_menu.add_command(label="Уведомления", command=lambda: self.options_notify())
        set_menu.add_command(label="Импорт", command=lambda: self.imp())
        set_menu.add_command(label="Экспорт", command=lambda: self.export())
        menu = Menu()
        menu.add_cascade(label="Настройки", menu=set_menu)
        set_menu = Menu()
        self.config(menu=menu)
        self.frame3 = Frame(self, borderwidth=1, highlightthickness=1, highlightbackground="grey", relief=RIDGE)
        self.frame3.pack(side=TOP, fill=X)
        frame4 = Frame(self, borderwidth=1, highlightthickness=1, highlightbackground="grey", relief=RIDGE)
        frame4.pack(side=BOTTOM, fill=X)
        button1 = Button(frame4, width=5, text="+", command=lambda: self.adding(), cursor="hand2")
        button1.pack(side=LEFT)
        label2 = Label(frame4, text="Добавить задачу", font="-weight bold", width=15)
        label2.pack(side=LEFT, padx=5)
        self.display_categories()
        self.display_tasks(self.db.view_tasks(self.main_table_name))
        if self.db.check_days(self.main_table_name):
            self.notification()
        self.mainloop()

    def table_name_set(self):
        try:
            with open('table_name.txt', 'w') as f:
                f.write(self.main_table_name)
        except Exception as e:
            print(f"Ошибка записи файла: {e}")

    def table_name_get(self):
        try:
            with open('table_name.txt', 'r') as f:
                self.main_table_name = f.read()
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")

    def options_notify(self):
        OptionsNotify(self)

    def important(self, event):
        self.display_tasks(self.db.important_cat(self.main_table_name))

    def all(self, event):
        self.display_tasks(self.db.view_tasks(self.main_table_name))

    def recent(self, event):
        self.display_tasks(self.db.recent(self.main_table_name))

    def done(self, event):
        self.display_tasks(self.db.done(self.main_table_name))

    def add_category(self):
        category = simpledialog.askstring("Добавление категории", "Введите название категории:")
        if category:
            self.db.add_cat(self.main_table_name, category)
        self.display_categories()

    def delete_category(self):
        categories = self.db.view_categories(self.main_table_name)
        DeleteCategory(self, categories)

    def cat_custom(self, category):
        self.display_tasks(self.db.category_custom(self.main_table_name, category, ))

    def display_categories(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()
        label1 = Label(self.frame1, text="Категории", font="weight 14 bold", width=10)
        label1.pack(side=TOP, pady=5, padx=5)
        separator = ttk.Separator(self.frame1, orient="horizontal")
        separator.pack(fill=X)
        label2 = Label(self.frame1, text="Все", font="weight 12 bold", cursor="hand2")
        label2.bind("<ButtonRelease-1>", self.all)
        label2.pack(anchor=NW, pady=5, padx=8)
        label3 = Label(self.frame1, text="Важные", font="weight 12 bold", cursor="hand2")
        label3.pack(anchor=NW, pady=5, padx=8)
        label3.bind("<ButtonRelease-1>", self.important)
        label4 = Label(self.frame1, text="Ближайшие", font="weight 12 bold", cursor="hand2")
        label4.bind("<ButtonRelease-1>", self.recent)
        label4.pack(anchor=NW, pady=5, padx=8)
        label5 = Label(self.frame1, text="Выполненные", font="weight 12 bold", cursor="hand2")
        label5.bind("<ButtonRelease-1>", self.done)
        label5.pack(anchor=NW, pady=5, padx=8)
        button1 = Button(self.frame1, width=17, text="X", font="weight 10 bold", command=lambda: self.delete_category())
        button1.pack(side=BOTTOM)
        button2 = Button(self.frame1, width=17, text="+", font="weight 10 bold", command=lambda: self.add_category())
        button2.pack(side=BOTTOM)
        categories = self.db.view_categories(self.main_table_name)
        for category in categories:
            label = Label(self.frame1, text=category, font="weight 12 bold", cursor="hand2")
            label.pack(anchor=NW, pady=5, padx=8)
            label.bind("<ButtonRelease-1>", lambda event, cat=category[0]: self.cat_custom(cat))

    def display_tasks(self, tasks):
        for widget in self.frame3.winfo_children():
            widget.destroy()
        for t in tasks:
            name, descr, deadline, priority, category, status = t
            dead = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
            timediff = dead - self.current_date
            txt = "дн."
            color = "black"
            deadline_text = f"Через {str(timediff.days)} {txt}"
            if status == 1:
                color = "green"
                deadline_text = ""
            if timediff.days < 0 and status == 0:
                color = "red"
                deadline_text = f"Просрочено на {abs(timediff.days)} {txt}"
            if timediff.days == 0 and status == 0:
                deadline_text = f"Cегодня в {str(dead)[10:16]}"
            if 1 >= timediff.days > 0 and status == 0:
                deadline_text = f"Завтра в {str(dead)[10:16]}"
            task_label = ttk.Label(
                self.frame3,
                text=f"{name}\n{deadline_text}",
                cursor="hand2",
                font="-weight bold",
                foreground=color
            )
            task_label.pack(side=TOP, pady=5)
            task_label.bind("<ButtonRelease-1>", lambda event, task_inf=t: self.task_info(task_inf))
            task_separator = ttk.Separator(self.frame3, orient="horizontal")
            task_label.pack(fill=BOTH, expand=1, padx=10, pady=5)
            task_separator.pack(fill=X, padx=10, pady=5)

    def adding(self):
        add = AddWindow(self)

    def closing(self):
        self.display_tasks(self.db.view_tasks(self.main_table_name))
        self.display_categories()

    def task_info(self, task_inf):
        info = TaskInfo(self, task_inf)

    def notification(self):
        day_change = timedelta(days=self.days)
        date = self.current_date + day_change
        date = date.strftime('%d-%m-%Y')
        print(date)
        due_tasks = self.db.get_notify(self.main_table_name, date)
        if due_tasks:
            message = "Напоминание:\n"
            for task in due_tasks:
                dead = datetime.strptime(task[1], '%d-%m-%Y %H:%M')
                timediff = dead - self.current_date
                message += f"- {task[0]} осталось: {timediff.days} дн.\n"
            mb.showwarning("Уведомление", message)

    def export(self):
        try:
            export_path = filedialog.asksaveasfilename(defaultextension=".csv")
            rows = self.db.export(self.main_table_name)
            if export_path:
                with open(export_path, 'w') as f:
                    for row in rows:
                        f.write(','.join(map(str, row)) + '\n')
        except Exception as e:
            print(f"Ошибка записи файла: {e}")

    def imp(self):
        try:
            file_types = [("CSV files", "*.csv")]
            import_path = filedialog.askopenfile(defaultextension=".csv", filetypes=file_types)
            if import_path:
                filename_without_extension = os.path.splitext(os.path.basename(import_path.name))[0]
                self.main_table_name = filename_without_extension
                self.table_name_set()
                self.db.importing(self.main_table_name, import_path)
                restart()
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")


def restart():
    mb.showwarning("Уведомление", "Перезапустите приложение")


def empty_error():
    mb.showerror("Ошибка", "Обязательные поля(*) не должны быть пустыми")


class AddWindow(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Добавление")
        self.geometry("300x650")
        frame1 = Frame(self)
        frame1.pack(side=TOP, fill=X, padx=5, pady=5)
        label1 = Label(frame1, text="Название*", font="weight 12 bold", width=10)
        label1.pack(anchor=NW, pady=5)
        self.entry1 = Entry(frame1, font="weight 10")
        self.entry1.pack(anchor=NW, fill=X, pady=5, padx=5)
        label2 = Label(frame1, text="Описание*", font="weight 12 bold", width=10)
        label2.pack(anchor=NW, pady=5)
        self.entry2 = Entry(frame1, font="weight 10")
        self.entry2.pack(anchor=NW, fill=X, pady=5, padx=5)
        label3 = Label(frame1, text="Срок", font="weight 12 bold", width=10)
        label3.pack(anchor=W, pady=5)
        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X, padx=5, pady=5)
        label4 = Label(frame2, text="Дата", font="weight 10 bold", width=10)
        label4.pack(anchor=NW, pady=5)
        self.cal = Calendar(frame2, selectmode="day", year=2023, month=11, day=24)
        self.cal.pack(padx=10, pady=10)
        label5 = Label(frame2, text="Время", font="weight 10 bold", width=10)
        label5.pack(anchor=NW, pady=5)
        self.hours_spin = Spinbox(frame2, from_=00, to=23, width=5, wrap=True)
        self.hours_spin.pack(side=LEFT, padx=10)
        self.minutes_spin = Spinbox(frame2, from_=0, to=59, width=5, wrap=True)
        self.minutes_spin.pack(side=LEFT)
        frame3 = Frame(self)
        frame3.pack(side=TOP, fill=X, padx=5, pady=5)
        label6 = Label(frame3, text="Приоритет*", font="weight 12 bold", width=10)
        label6.pack(anchor=NW)
        priorities = ["Высокий", "Средний", "Низкий"]
        categories = self.main_window.db.view_categories(self.main_window.main_table_name)
        self.combobox1 = ttk.Combobox(frame3, values=priorities)
        self.combobox1.pack(anchor=NW, padx=5)
        label7 = Label(frame3, text="Категория", font="weight 12 bold", width=10)
        label7.pack(anchor=NW)
        self.combobox2 = ttk.Combobox(frame3, values=categories)
        self.combobox2.pack(anchor=NW, padx=5)
        frame4 = Frame(self)
        frame4.pack(side=TOP, fill=X, padx=5, pady=5)
        button = Button(frame4, width=8, text="Добавить", font="weight 10 bold", command=lambda: self.add())
        button.pack(side=TOP, pady=15)

    def add(self):
        db = Data()
        name = self.entry1.get()
        discr = self.entry2.get()
        date = datetime.strptime(self.cal.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")
        deadline = f"{date} {int(self.hours_spin.get()):02d}:{int(self.minutes_spin.get()):02d}"
        priority = self.combobox1.get()
        category = self.combobox2.get()
        if not name or not discr or not priority:
            empty_error()
        else:
            db.add_task(self.main_window.main_table_name, name, discr, deadline, priority, category)
            self.protocol("WM_DELETE_WINDOW", self.main_window.closing())
            self.destroy()


class TaskInfo(Toplevel):
    def __init__(self, main_window, task_inf):
        super().__init__()
        self.db = main_window.db
        self.main_window = main_window
        self.title("Подробнее")
        self.geometry("500x400")
        name, descr, deadline, priority, category, status = task_inf
        date = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
        day = date.strftime('%A')
        date = date.strftime('%d %B')
        date = date[:-1] + "я"
        time = deadline[10:16]
        frame1 = Frame(self, width=500, height=100, borderwidth=1, highlightthickness=1, highlightbackground="grey",
                       relief=RIDGE)
        frame1.pack(side=TOP, fill=BOTH)
        label1 = Label(frame1, text=name, font="weight 20 bold")
        label1.pack(anchor=NW)
        label2 = Label(frame1, text=f"{date}, {day}", font="weight 15 bold")
        label2.pack(anchor=NW)
        label3 = Label(frame1, text=f"в {time}", font="weight 12 bold")
        label3.pack(anchor=NW)
        frame2 = Frame(self, width=500, height=200, borderwidth=1, highlightthickness=1, highlightbackground="grey",
                       relief=RIDGE)
        frame2.pack(side=TOP, fill=BOTH, expand=1)
        label4 = Label(frame2, text=descr, font="weight 10")
        label4.pack(anchor=NW)
        frame3 = Frame(self, width=500, height=100, borderwidth=1, highlightthickness=1, highlightbackground="grey",
                       relief=RIDGE)
        frame3.pack(side=TOP, fill=BOTH, pady=1)
        label5 = Label(frame3, text=f"Приоритет: {priority}", font="weight 12 bold")
        label5.pack(anchor=NW)
        frame4 = Frame(self, width=500, height=100, borderwidth=1, highlightthickness=1, highlightbackground="grey",
                       relief=RIDGE)
        frame4.pack(side=TOP, fill=BOTH, pady=1)
        button1 = Button(frame4, width=8, text="Изменить", font="weight 10 bold", command=lambda: self.redact(task_inf))
        button1.pack(side=LEFT)
        button2 = Button(frame4, width=8, text="Удалить", font="weight 10 bold", command=lambda: self.delete(name))
        button2.pack(side=RIGHT)

    def redact(self, task_inf):
        redact = Redact(self, task_inf)

    def delete(self, name):
        ans = mb.askyesno(title="Подтверждение", message="Вы уверены, что хотите удалить задачу?")
        if ans:
            self.db.delete_task(self.main_window.main_table_name, name)
            self.closing()

    def closing(self):
        self.destroy()
        self.main_window.closing()


class Redact(Toplevel):
    def __init__(self, task_info, info):
        super().__init__()
        self.task_info = task_info
        name, descr, deadline, priority, category, status = info
        self.choice = IntVar()
        self.choice.set(status)
        day = deadline[8:10]
        month = deadline[5:7]
        year = deadline[:4]
        hour = deadline[11:13]
        minute = deadline[14:]
        self.title("Изменение")
        self.geometry("300x720")
        frame1 = Frame(self)
        frame1.pack(side=TOP, fill=X, padx=5, pady=5)
        label1 = Label(frame1, text="Название*", font="weight 12 bold", width=10)
        label1.pack(anchor=NW, pady=5)
        self.entry1 = Entry(frame1, font="weight 10")
        self.entry1.insert(0, name)
        self.entry1.pack(anchor=NW, fill=X, pady=5, padx=5)
        label2 = Label(frame1, text="Описание*", font="weight 12 bold", width=10)
        label2.pack(anchor=NW, pady=5)
        self.entry2 = Entry(frame1, font="weight 10")
        self.entry2.insert(0, descr)
        self.entry2.pack(anchor=NW, fill=X, pady=5, padx=5)
        label3 = Label(frame1, text="Срок", font="weight 12 bold", width=10)
        label3.pack(anchor=W, pady=5)
        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X, padx=5, pady=5)
        label4 = Label(frame2, text="Дата", font="weight 10 bold", width=10)
        label4.pack(anchor=NW, pady=5)
        self.cal = Calendar(frame2, selectmode="day", year=int(year), month=int(month), day=int(day))
        self.cal.pack(padx=10, pady=10)
        label5 = Label(frame2, text="Время", font="weight 10 bold", width=10)
        label5.pack(anchor=NW, pady=5)
        self.hours_spin = Spinbox(frame2, from_=00, to=23, width=5, wrap=True)
        self.hours_spin.pack(side=LEFT, padx=10)
        self.hours_spin.delete(0, "end")
        self.hours_spin.insert(0, hour)
        self.minutes_spin = Spinbox(frame2, from_=0, to=59, width=5, wrap=True)
        self.minutes_spin.pack(side=LEFT)
        self.minutes_spin.delete(0, "end")
        self.minutes_spin.insert(0, minute)
        frame3 = Frame(self)
        frame3.pack(side=TOP, fill=X, padx=5, pady=5)
        label6 = Label(frame3, text="Приоритет*", font="weight 12 bold", width=10)
        label6.pack(anchor=NW)
        priorities = ["Высокий", "Средний", "Низкий"]
        categories = self.task_info.db.view_categories(self.task_info.main_window.main_table_name)
        self.combobox1 = ttk.Combobox(frame3, values=priorities)
        self.combobox1.pack(anchor=NW, padx=5)
        self.combobox1.insert(0, priority)
        label7 = Label(frame3, text="Категория", font="weight 12 bold", width=10)
        label7.pack(anchor=NW, pady=5)
        self.combobox2 = ttk.Combobox(frame3, values=categories)
        self.combobox2.pack(anchor=NW, padx=5)
        self.combobox2.insert(0, categories)
        label8 = Label(frame3, text="Статус", font="weight 12 bold", width=10)
        label8.pack(anchor=NW, pady=5)
        yes_button = Radiobutton(frame3, text="Выполнено", variable=self.choice, value=1)
        yes_button.pack(side=LEFT)
        no_button = Radiobutton(frame3, text="Не выполнено", variable=self.choice, value=0)
        no_button.pack(side=RIGHT)
        frame4 = Frame(self)
        frame4.pack(side=TOP, fill=X, padx=5, pady=5)
        button1 = Button(frame4, width=8, text="Изменить", font="weight 10 bold", command=lambda: self.redact())
        button1.pack(side=LEFT, pady=15, padx=10)
        button2 = Button(frame4, width=8, text="Отмена", font="weight 10 bold", command=lambda: self.cancel())
        button2.pack(side=RIGHT, pady=15, padx=10)

    def redact(self):
        name = self.entry1.get()
        discr = self.entry2.get()
        date = datetime.strptime(self.cal.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")
        deadline = f"{date} {int(self.hours_spin.get()):02d}:{int(self.minutes_spin.get()):02d}"
        priority = self.combobox1.get()
        category = self.combobox2.get()
        status = self.choice.get()
        if not name or not discr or not priority:
            empty_error()
        else:
            self.task_info.db.change_task(self.task_info.main_window.main_table_name, name, discr, deadline, priority,
                                          category, status)
            self.protocol("WM_DELETE_WINDOW", self.task_info.closing())
            self.destroy()

    def cancel(self):
        self.destroy()


class DeleteCategory(Toplevel):
    def __init__(self, main_window, categories):
        super().__init__()

        self.main_window = main_window

        self.title("Удаление категории")
        self.geometry("300x150")

        self.label = Label(self, text="Выберите категорию для удаления:")
        self.label.pack(pady=10)

        self.combobox = ttk.Combobox(self, values=categories, state="readonly")
        self.combobox.pack(pady=10)

        self.delete_button = Button(self, text="Удалить", command=lambda: self.delete())
        self.delete_button.pack(pady=10)

    def delete(self):
        category = self.combobox.get()
        if category:
            self.main_window.db.delete_category(category)
            self.protocol("WM_DELETE_WINDOW", self.main_window.closing())
            self.destroy()


def error_message():
    mb.showerror("Ошибка", "Поле не должно быть пустым")


class OptionsNotify(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title("Настройки уведомлений")
        self.geometry("300x150")

        self.label = Label(self, text="Выберите за сколько дней необходимо напомнить")
        self.label.pack(pady=10)

        self.spinbox = ttk.Spinbox(self, from_=1, to=31, width=5, wrap=True)
        self.spinbox.pack(pady=10)

        self.save_button = Button(self, text="Сохранить", command=lambda: self.save())
        self.save_button.pack(pady=10)

    def save(self):
        days = self.spinbox.get()
        if not days:
            error_message()
        else:
            self.main_window.days = days
            self.main_window.db.change_notify(self.main_window.main_table_name, days)
            self.destroy()
