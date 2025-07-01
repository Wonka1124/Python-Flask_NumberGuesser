from flask import Flask, render_template, request, redirect, url_for, session
import random
import psycopg2

def get_db():
    conn = psycopg2.connect(
        host='localhost',
        database='project1_db',
        user='postgres',
        password='Qaszplkm1'
    )
    return conn 

app = Flask(__name__)
app.secret_key = 'Qaszplkm1'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/username', methods=['GET', 'POST'])
def username(): 
    message = None
    if request.method == 'POST':
        new_name = request.form['username'].strip()
        if not new_name:
            return render_template('index.html', error='Имя не может быть пустым')
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM players WHERE username = %s', (new_name,))
        user = cur.fetchone()
        
        if user:
            message = f'С возвращением, {new_name}!'
        else:
            # Добавляем нового пользователя в базу
            cur.execute('INSERT INTO players (username) VALUES (%s)', (new_name,))
            conn.commit()
            message = 'Похоже, вы тут впервые, добро пожаловать!'
        
        cur.close()
        conn.close()
        
        # Сохраняем имя в сессии и переходим к игре
        session['username'] = new_name
        return redirect(url_for('game'))
    
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Проверяем, есть ли пользователь в сессии
    username = session.get('username')
    if not username:
        return redirect(url_for('username'))
    
    # Получаем user_id из базы
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM players WHERE username = %s', (username,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return redirect(url_for('username'))
    user_id = user[0]

    # Получаем лучшую игру
    cur.execute('SELECT MIN(number_of_guesses) FROM games WHERE user_id = %s', (user_id,))
    best_result = cur.fetchone()
    best_game = best_result[0] if best_result and best_result[0] else None
    cur.close()
    conn.close()

    # Инициализация игры
    if 'secret_number' not in session or 'attempts' not in session:
        session['secret_number'] = random.randint(1, 1000)
        session['attempts'] = 0

    message = None
    
    if request.method == 'POST':
        try:
            user_guess = int(request.form['guess'])
            session['attempts'] += 1
            secret_number = session['secret_number']

            if not (1 <= user_guess <= 1000):
                message = 'Пожалуйста, введите число от 1 до 1000'
            elif user_guess < secret_number:
                message = 'Ваше число больше загаданного'
            elif user_guess > secret_number:
                message = 'Ваше число меньше загаданного'
            else:
                # Угадал!
                attempts = session['attempts']
                # Сохраняем игру в базу
                conn = get_db()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO games (user_id, number_of_guesses, secret_number) VALUES (%s, %s, %s)',
                    (user_id, attempts, secret_number)
                )
                conn.commit()
                cur.close()
                conn.close()
                message = f'Вы угадали! Это было {secret_number}. Количество попыток: {attempts}'
                # Сбросить игру
                session.pop('secret_number')
                session.pop('attempts')
        except ValueError:
            message = 'Введите правильное значение'

    return render_template('game.html', message=message, best_game=best_game)

if __name__ == '__main__':
    app.run(debug=True)