import subprocess
import hashlib
import json
import requests
import datetime
import time

FMT = "%Y-%m-%d %H:%M"

WORKSECTION_API_KEY = ""
WORKSECTION_COMPANY_URL = ""
WORKSECTION_ACTION_NAME = "get_all_tasks"


def get_current_time(FMT):
    return datetime.datetime.now().strftime(FMT)


def string_to_md5_hash():
    string = WORKSECTION_ACTION_NAME + WORKSECTION_API_KEY
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def get_worksection_api_url():
    worksection_api_hash = string_to_md5_hash()
    return WORKSECTION_COMPANY_URL + "/api/admin/?action=get_all_tasks&show_subtasks=1&hash=" + worksection_api_hash


def get_tasks():
    worksection_api_url = get_worksection_api_url()
    response = requests.get(worksection_api_url)
    json_data = json.loads(response.text)

    return json_data['data']


def filter_tasks_by_status(status, tasks):
    return list(filter(lambda task: task['status'] == status, tasks))


def check_task(task):
    created_at = task['date_added']
    if 'tags' in task:
        tags = task['tags']
        if 'Bug' in tags:
            first_time = datetime.datetime.strptime(created_at, FMT)
            last_time = datetime.datetime.strptime(current_time, FMT)

            value = last_time - first_time
            if value.total_seconds() / 60 < 1:
                subprocess.call(["afplay", "audio.wav"])
                return True
    return False


while True:
    time_begin = time.time()
    current_time = get_current_time(FMT)

    tasks = filter_tasks_by_status('active', get_tasks())

    for task in tasks:
        if check_task(task):
            break
        if 'child' in task:
            child = task['child']
            for child_task in child:
                if check_task(child_task):
                    break

    time_end = time.time()
    time_elapsed = time_end - time_begin
    time.sleep(60 - time_elapsed)
