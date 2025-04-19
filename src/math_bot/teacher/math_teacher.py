import os
import random
import copy
from aiogram.types import FSInputFile

TASKS_DICT = {
    '2d' : '17',
    '3d' : '14',
    'parametrs' : '18',
    '17' : '17',
    '14' : '14',
    '18' : '18'
}

now_dir = os.path.dirname(__file__).replace("\\", "/")

def get_tasks_list(category):
    standard_category= TASKS_DICT[category]
    with open(
            f'{now_dir}/tasks/{standard_category}/list{standard_category}.txt',
            'r', encoding='utf8') as f:
        tasks_list = f.read().split()
        random.shuffle(tasks_list)
        return tasks_list

def get_task_image_by_num(category, task_id):
    standard_category = TASKS_DICT[category]
    return FSInputFile(f'{now_dir}/tasks/{standard_category}/images/{task_id}.jpg')

def get_answers(category):
    standard_category = TASKS_DICT[category]
    with open(f'{now_dir}/tasks/{standard_category}/list{standard_category}_answers.txt', 'r', encoding='utf8') as f:
        ans_dict = {}
        for s in f:
            key, value = s.split(' @ ')
            ans_dict[key] = value
    return ans_dict

class Teacher:
    def __init__(self):
        self.task_order = {}
        self.task_now = {}
        self.task_id = {}
    def get_task_now_copy(self):
        return copy.deepcopy(self.task_now)
    def get_task_order_copy(self):
        return copy.deepcopy(self.task_order)
    def get_answer(self, chat_id):
        answers_dict = get_answers(self.task_now[chat_id]['category'])
        return answers_dict[self.task_id[chat_id]]
    def is_last_task(self, chat_id):
        if self.task_now[chat_id]['task_index'] + 1 == len(self.task_order[chat_id][self.task_now[chat_id]['category']]):
            return True
    def is_first_task(self, chat_id):
        if self.task_now[chat_id]['task_index'] == 0:
            return True

    def create_task_order(self, chat_id, category):
        standard_category = TASKS_DICT[category]
        if chat_id not in self.task_order:
            self.task_order[chat_id] = {standard_category: get_tasks_list(standard_category)}
        elif standard_category not in self.task_order[chat_id]:
            self.task_order[chat_id][standard_category] = get_tasks_list(standard_category)

        self.task_now[chat_id] = {'category': standard_category, 'task_index': 0}
        self.task_order[chat_id][standard_category] = get_tasks_list(standard_category)
        last_task_id = self.task_order[chat_id][standard_category][0]
        self.task_id[chat_id] = last_task_id
        return last_task_id, get_task_image_by_num(standard_category, last_task_id)

    def refresh_task_order(self, chat_id, category):
        ...

    def get_next_task(self, chat_id):
        category = self.task_now[chat_id]['category']
        if (chat_id not in self.task_order) or (category not in self.task_order[chat_id]):
            return self.create_task_order(chat_id, category)
        else:
            if (self.task_now[chat_id]['task_index'] + 1) > (len(self.task_order[chat_id][category]) - 1):
                return False, False
            else:
                self.task_now[chat_id]['category'] = category
                self.task_now[chat_id]['task_index'] += 1
                last_task_id = self.task_order[chat_id][category][self.task_now[chat_id]['task_index']]
                self.task_id[chat_id] = last_task_id
                return last_task_id, get_task_image_by_num(category, last_task_id)

    def get_prev_task(self, chat_id):
        category = self.task_now[chat_id]['category']
        if (chat_id not in self.task_order) or (category not in self.task_order[chat_id]):
            return self.create_task_order(chat_id, category)
        else:
            if (self.task_now[chat_id]['task_index'] - 1) < 0:
                return False, False
            else:
                self.task_now[chat_id]['category'] = category
                self.task_now[chat_id]['task_index'] -= 1
                last_task_id = self.task_order[chat_id][category][self.task_now[chat_id]['task_index']]
                self.task_id[chat_id] = last_task_id
                return last_task_id, get_task_image_by_num(category, last_task_id)


teacher = Teacher()