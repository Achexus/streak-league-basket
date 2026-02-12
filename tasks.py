# tasks.py
from datetime import date
from config import XP_VALUES

class TaskItem:
    def __init__(self, task_name, difficulty, is_habit=False):
        self.task = task_name
        self.diff = difficulty # E, M, H
        self.xp = XP_VALUES.get(difficulty, 10)
        self.done = False
        self.is_habit = is_habit

class AgendaItem:
    def __init__(self, event_date, content):
        self.event_date = event_date
        self.content = content

class TaskManager:
    def __init__(self):
        self.habits = []      
        self.daily_tasks = [] 
        self.agenda = []      
        self.yesterday_score = 0
        
    def add_habit(self, name, diff):
        self.habits.append(TaskItem(name, diff, is_habit=True))
        
    def add_task(self, name, diff):
        self.daily_tasks.append(TaskItem(name, diff, is_habit=False))
        
    def toggle_habit(self, index):
        if 0 <= index < len(self.habits):
            self.habits[index].done = not self.habits[index].done
            
    def toggle_task(self, index):
        if 0 <= index < len(self.daily_tasks):
            self.daily_tasks[index].done = not self.daily_tasks[index].done
            
    def remove_task(self, index):
        if 0 <= index < len(self.daily_tasks):
            self.daily_tasks.pop(index)

    def calculate_daily_score(self):
        score = 0
        for h in self.habits:
            if h.done: score += h.xp
            else: score -= h.xp
        for t in self.daily_tasks:
            if t.done: score += t.xp
            else: score -= t.xp
        return score

    def reset_for_new_day(self):
        score = self.calculate_daily_score()
        self.yesterday_score = score
        for h in self.habits:
            h.done = False
        return score

    def check_agenda(self):
        today = date.today()
        return [i.content for i in self.agenda if i.event_date.date() == today]