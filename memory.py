chat_history = []

def save_message(role, message):
    chat_history.append({
        "role": role,
        "content": message
    })

def get_history():
    return chat_history

def clear_history():
    chat_history.clear()
