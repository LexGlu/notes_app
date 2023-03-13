from notes.models import Note
import requests


bot_token = '6107985411:AAGx_Swebcj0xI-hkbJVhQ0BY2wqobLQg20'
webhook_host = 'https://73b0-193-0-217-181.eu.ngrok.io/bot/webhook/'  # ngrok host + path to webhook
set_webhook = f'https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_host}'  # url to set webhook


def start(chat_id):
    message = 'Hello! I am a bot. I can help you to get notes from MyNoteApp. Type /help to see all commands.'
    return send_message(chat_id, message)


def bot_help(chat_id):
    message = 'Available commands:\n/start - start the bot\n/help - show all commands\n' \
              '/note <note_id> - get note by id\n/search <query> - search notes by title\n' \
              '/all - get all notes\n/author <author_id> - get all notes by author id'
    return send_message(chat_id, message)


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response


def get_note_info(chat_id, note_id):
    try:
        note = Note.objects.get(id=note_id)
        message = f'Note {note.title} by {note.author.username}:\n{note.text}'
        return send_message(chat_id, message)
    except Note.DoesNotExist:
        return send_message(chat_id, 'Note not found')


def search_notes(chat_id, query):
    notes = Note.objects.filter(title__icontains=query)
    if notes:
        message = 'Notes found:\n'
        for note in notes:
            message += f'{note.title} by {note.author.username} (id {note.id})\n'
        return send_message(chat_id, message)
    else:
        return send_message(chat_id, 'No notes found')


def get_all_notes(chat_id):
    notes = Note.objects.all()
    if not notes:
        return send_message(chat_id, 'There are no notes yet')
    message = 'All notes:\n'
    for note in notes:
        message += f'{note.title} by {note.author.username} (id {note.id})\n'
    return send_message(chat_id, message)


def get_notes_by_author(chat_id, author):
    # check if user is registered
    user_in_db = Note.objects.filter(author__username=author).exists()
    if not user_in_db:
        return send_message(chat_id, f'{author} is not registered in MyNoteApp yet')
    notes = Note.objects.filter(author__username=author)
    if not notes:
        return send_message(chat_id, f'{author} has no notes yet')
    message = f'{author}\'s notes:\n'
    for note in notes:
        message += f'{note.title} (id {note.id})\n'
    return send_message(chat_id, message)


commands = {'/start': start, '/note': get_note_info, '/help': bot_help, '/search': search_notes, '/all': get_all_notes,
            '/author': get_notes_by_author}




