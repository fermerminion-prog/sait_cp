from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Разрешаем запросы с любых источников (чтобы работало при открытии html файла)
CORS(app)

# --- НАСТРОЙКИ TELEGRAM ---
# Вставь сюда токен, который дал BotFather
TELEGRAM_TOKEN = "8518583079:AAGJkbGkFOjDdiXZLW21378JPPR-eBE8sk4"
# Вставь сюда свой ID (числом или строкой)
CHAT_ID = "6778337830"

@app.route('/send-order', methods=['POST'])
def send_order():
    try:
        # Получаем данные из JSON, который прислал JS
        data = request.json
        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указано')

        # Формируем текст сообщения
        message_text = (
            f"🔔 <b>Новая заявка с сайта!</b>\n\n"
            f"👤 <b>Имя:</b> {name}\n"
            f"📞 <b>Телефон:</b> {phone}"
        )

        # Отправляем запрос в Telegram API
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML" # Чтобы работало жирное выделение
        }

        tg_response = requests.post(url, json=payload)

        if tg_response.status_code == 200:
            return jsonify({"status": "success", "message": "Заявка отправлена"})
        else:
            print(f"Ошибка Telegram: {tg_response.text}")
            return jsonify({"status": "error", "message": "Ошибка отправки в Telegram"}), 500

    except Exception as e:
        print(f"Ошибка сервера: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Запускаем сервер на порту 5000
    app.run(debug=True, port=5000)