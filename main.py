from flask import Flask, request, Response
from telegram import Bot
import os

app = Flask(__name__)
# Telegram Bot API set my API_KEY Integration
TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
bot = Bot(token=TELEGRAM_BOT_API_KEY)


def activity_type(event):
    activity_str = 'la actividad'
    if event['objecttable'] == 'assign' or event['other']['modulename'] == 'assign':
        activity_str = 'la actividad assignación'
    if event['objecttable'] != 'course_modules':
        if event['other']['modulename'] == 'quiz':
            activity_str = 'la actividad quiz'
        if event['other']['modulename'] == 'choice':
            activity_str = 'la actividad elección'
        if event['other']['modulename'] == 'chat':
            activity_str = 'la conversación'
        if event['other']['modulename'] == 'book':
            activity_str = 'el libro'
    return activity_str


def build_message(course, event, instance):
    activity_str = activity_type(event)
    if event['action'] == 'updated':
        return f'En el curso {course["fullname"]} se actualizó {activity_str} "{instance["name"]}"'
    if event['action'] == 'created':
        return f'En el curso {course["fullname"]} se creó {activity_str} "{instance["name"]}"'


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    request_data = request.get_json(force=True)
    subs = request_data['subscriptors']
    instance = request_data['context_instance']
    event = request_data['event']
    course = request_data['course']
    subs = [*subs.values()]
    # logging.error(request_data)
    message = build_message(course, event, instance)
    for sub in subs:
        send_state = bot.send_message(sub['telegram_chat_id'], message)
    # send_state = bot.send_message(telegram_chat_id, message)
    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
