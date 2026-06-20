import asyncio
import pickle
import os
import json
from googleapiclient.discovery import build

last_assignment = {}
SEEN_PATH = '/data/seen_assignments.json' if os.environ.get('RAILWAY_ENVIRONMENT') else os.path.join(os.path.dirname(__file__), '..', 'seen_assignments.json')

def load_seen():
    if os.path.exists(SEEN_PATH):
        with open(SEEN_PATH, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_PATH, 'w') as f:
        json.dump(list(seen), f)

seen_assignments = load_seen()

def get_classroom_service():
    token_path = os.path.join(os.path.dirname(__file__), '..', 'token.pickle')
    with open(token_path, 'rb') as f:
        creds = pickle.load(f)
    return build('classroom', 'v1', credentials=creds)

async def watch_classroom(app, chat_id):
    service = get_classroom_service()
    while True:
        try:
            courses = service.courses().list(courseStates=['ACTIVE']).execute()
            for course in courses.get('courses', []):
                cid = course['id']
                cname = course['name']

                works = service.courses().courseWork().list(courseId=cid).execute()
                for work in works.get('courseWork', []):
                    wid = work['id']
                    if wid not in seen_assignments:
                        seen_assignments.add(wid)
                        save_seen(seen_assignments)
                        title = work.get('title', 'Untitled')
                        due = work.get('dueDate', {})
                        description = work.get('description', 'No description provided.')
                        due_str = f"{due.get('day')}/{due.get('month')}/{due.get('year')}" if due else 'No due date'
                        work_type = work.get('workType', 'ASSIGNMENT')

                        type_map = {
                            'ASSIGNMENT': 'Upload/Written',
                            'SHORT_ANSWER_QUESTION': 'Short Answer',
                            'MULTIPLE_CHOICE_QUESTION': 'Multiple Choice'
                        }
                        readable_type = type_map.get(work_type, work_type)

                        last_assignment[chat_id] = {
                            'course': cname,
                            'title': title,
                            'type': readable_type,
                            'due': due_str,
                            'description': description
                        }

                        msg = (
                            f"📚 *New Assignment!*\n"
                            f"Course: {cname}\n"
                            f"Title: {title}\n"
                            f"Type: {readable_type}\n"
                            f"Due: {due_str}\n\n"
                            f"Description: {description}\n\n"
                            f"Want me to work on it?\n/yes or /skip"
                        )
                        await app.bot.send_message(
                            chat_id=chat_id,
                            text=msg,
                            parse_mode='Markdown'
                        )
        except Exception as e:
            print(f"Classroom error: {e}")
        await asyncio.sleep(60)