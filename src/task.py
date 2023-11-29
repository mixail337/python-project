import csv
import datetime
import sqlite3
from datetime import datetime, timedelta


class Data:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('task_manager.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Ошибка подключения базы данных: {e}")
            self.connection.rollback()
        except Exception as e:
            print(f"Непредвиденная ошибка подключения базы данных: {e}")
            self.connection.rollback()

    def create_tables(self, main_table_name):
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {main_table_name} "
                                f"(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                f"task_name TEXT NOT NULL,"
                                f"task_description TEXT NOT NULL,"
                                f"task_deadline TEXT NOT NULL,"
                                f"task_priority TEXT NOT NULL,"
                                f"task_category TEXT NOT NULL,"
                                f"status BOOL)")
            category_table_name = f"{main_table_name}_Categories"
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {category_table_name}("
                                f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                f"cat_name TEXT NOT NULL)")
            day_table_name = f"{main_table_name}_Days"
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {day_table_name}("
                                f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                f"days INTEGER)")

        except sqlite3.Error as e:
            print(f"Ошибка создания таблицы: {e}")
            self.connection.rollback()
        except Exception as e:
            print(f"Непредвиденная ошибка создания таблицы: {e}")
            self.connection.rollback()

    def view_tasks(self, main_table_name):
        try:
            self.cursor.execute(f"SELECT task_name, task_description, task_deadline, task_priority, "
                                f"task_category, status "
                                f"FROM {main_table_name} WHERE status = 0")
            tasks = self.cursor.fetchall()
            return tasks
        except sqlite3.Error as e:
            print(f"Ошибка отображения: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения: {e}")

    def add_task(self, main_table_name, name, description, deadline, priority, task_category=" ", status=0):
        try:
            self.cursor.execute(
                f"INSERT INTO {main_table_name} (task_name, task_description, task_deadline, task_priority, "
                f"task_category, status) "
                f"VALUES (?, ?, ?, ?, ?, ?)", (name, description, deadline, priority, task_category, status))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка добавления записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка добавления записи: {e}")

    def change_task(self, main_table_name, name, description, deadline, priority, category, status=0):
        try:
            self.cursor.execute(
                f"UPDATE {main_table_name}  SET task_name = ?, task_description = ?, task_deadline = ?,"
                f" task_priority = ?, task_category = ?, status = ? "
                f"WHERE task_name =?", (name, description, deadline, priority, category, status, name))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка изменения записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка изменения записи: {e}")

    def delete_task(self, main_table_name, name):
        try:
            self.cursor.execute(f"DELETE FROM {main_table_name} WHERE task_name = ?", (name,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка удаления записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка удаления записи: {e}")

    def drop(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS Days")
        self.connection.commit()

    def important_cat(self, main_table_name):
        try:
            self.cursor.execute(f"SELECT task_name, task_description, task_deadline, task_priority, task_category,"
                                f" status "
                                f"FROM {main_table_name} WHERE task_priority = 'Высокий' AND status = 0")
            important = self.cursor.fetchall()
            return important
        except sqlite3.Error as e:
            print(f"Ошибка отображения записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения записи: {e}")

    def recent(self, main_table_name):
        try:
            today = datetime.now().date()
            day = today + timedelta(days=2)
            today = today.strftime('%Y-%m-%d')
            day = day.strftime('%Y-%m-%d')
            query1 = f"SELECT task_name, task_description, task_deadline, task_priority, task_category, status " \
                     f"FROM {main_table_name} " \
                     f"WHERE STRFTIME('%Y-%m-%d', task_deadline) BETWEEN '{today}' AND '{day}' AND status = 0"
            self.cursor.execute(query1)
            recent = self.cursor.fetchall()
            return recent
        except sqlite3.Error as e:
            print(f"Ошибка отображения записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения записи: {e}")

    def done(self, main_table_name):
        try:
            self.cursor.execute(f"SELECT task_name, task_description, task_deadline, task_priority, task_category,"
                                f" status "
                                f"FROM {main_table_name} WHERE status = 1")
            done = self.cursor.fetchall()
            return done
        except sqlite3.Error as e:
            print(f"Ошибка отображения записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения записи: {e}")


    def category_custom(self, main_table_name, category):
        try:
            self.cursor.execute(
                f"SELECT task_name, task_description, task_deadline, task_priority, task_category, status "
                f"FROM {main_table_name} WHERE task_category = ? AND status = 0", (category,))
            cat = self.cursor.fetchall()
            return cat
        except sqlite3.Error as e:
            print(f"Ошибка отображения записи: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения записи: {e}")

    def add_cat(self, main_table_name, name):
        try:
            category = f"{main_table_name}_Categories"
            self.cursor.execute(f"INSERT INTO {category} (cat_name) VALUES (?)", (name,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка добавления категории: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка добавления категории: {e}")

    def view_categories(self, main_table_name):
        try:
            category = f"{main_table_name}_Categories"
            self.cursor.execute(f"SELECT cat_name FROM {category}")
            categories = self.cursor.fetchall()
            self.connection.commit()
            return categories
        except sqlite3.Error as e:
            print(f"Ошибка отображения категории: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка отображения категории: {e}")

    def delete_category(self, main_table_name, name):
        try:
            category = f"{main_table_name}_Categories"
            self.cursor.execute(f"DELETE FROM {category} WHERE cat_name = ?", (name,))
            self.cursor.execute(f"UPDATE {main_table_name} SET task_category = ? WHERE task_category = ?", ("", name))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка удаления категории: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка удаления категории: {e}")

    def set_notify(self, main_table_name):
        try:
            d = f"{main_table_name}_Days"
            self.cursor.execute(f"INSERT INTO {d} (days) VALUES (?)", (2,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка установки напоминания: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка установки напоминания: {e}")

    def get_notify(self, main_table_name, current_date):
        try:
            self.cursor.execute(f"SELECT task_name, task_deadline FROM {main_table_name} "
                                f"WHERE substr(task_deadline, 1, 10) = ?", (current_date,))
            due_task = self.cursor.fetchall()
            self.connection.commit()
            return due_task
        except sqlite3.Error as e:
            print(f"Ошибка напоминания: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка напоминания: {e}")

    def notify_time(self, main_table_name):
        try:
            d = f"{main_table_name}_Days"
            self.cursor.execute(f"SELECT days FROM {d} WHERE id = 1")
            days = self.cursor.fetchall()
            self.connection.commit()
            return days
        except sqlite3.Error as e:
            print(f"Ошибка получения срока напоминания: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка получения срока напоминания: {e}")

    def change_notify(self, main_table_name, day):
        try:
            d = f"{main_table_name}_Days"
            self.cursor.execute(f"UPDATE {d} SET days =? WHERE id = 1", (day,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка изменения срока напоминания: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка изменения срока напоминания: {e}")

    def export(self, main_table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {main_table_name}")
            export = self.cursor.fetchall()
            self.connection.commit()
            return export
        except sqlite3.Error as e:
            print(f"Ошибка экспорта данных: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка экспорта данных: {e}")

    def check_days(self, main_table_name):
        try:
            d = f"{main_table_name}_Days"
            self.cursor.execute(f"SELECT COUNT(*) FROM {d}")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"Ошибка проверки напоминания: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка проверки напоминания: {e}")

    def check_empty(self, main_table_name):
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {main_table_name}")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"Ошибка проверки главной таблицы: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка проверки главной таблицы: {e}")

    def importing(self, main_table_name, file_name):
        try:
            lines = file_name.readlines()
            for line in lines:
                values = line.strip().split(',')
                self.cursor.execute(f"INSERT INTO {main_table_name} "
                                    f"(id, task_name, task_description, task_deadline, task_priority, "
                                    f"task_category, status) "
                                    f"VALUES (?,?,?,?,?,?,?)", values)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка импорта данных: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка импорта данных: {e}")

    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"Непредвиденная ошибка при очистке: {e}")


