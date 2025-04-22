from flask import render_template
from app import app
"""
Представления - обработчики, которые отвечают на запросы веб-браузера,
Представления в Flask пишутся как Python функции.
Каждая функция представления сопоставляется с одним или несколькими URL
"""

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # выдуманный пользователь
    posts = [ # список выдуманных постов
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)
