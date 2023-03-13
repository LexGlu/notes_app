from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .bot import send_message, commands


@csrf_exempt
def webhook(request):
    json_data = json.loads(request.body)
    message_text = json_data['message']['text']
    chat_id = json_data['message']['chat']['id']

    is_command = message_text.startswith('/')
    is_valid_command = is_command and message_text.split()[0] in commands
    if is_valid_command:
        command = message_text.split()[0]
        try:
            commands[command](chat_id, *message_text.split()[1:])
        except TypeError:
            send_message(chat_id, 'Please provide valid arguments. Type /help to see all commands.')
    elif is_command:
        send_message(chat_id, 'Unknown command. Type /help to see all commands.')
    else:
        send_message(chat_id, "I'm sorry, I don't understand you. Type /help to see all commands.")

    return HttpResponse(status=200)

