import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8156723328:AAF4NgfUZHUvfszZMZ28WBU_9pea1ZYRTz8"

# База данных фильмов
FILMS_DATABASE = {
    "весна на заречной улице": {
        "год": 1956,
        "режиссер": "Феликс Миронер, Марлен Хуциев",
        "ценности": ["коллективизм", "труд", "образование", "романтизм"],
        "анализ": """🎬 <b>Анализ "Весна на Заречной улице"</b>

<b>Ключевые ценности:</b>
• <b>Коллективизм</b> - жизнь в рабочем общежитии, совместное решение проблем
• <b>Труд как самовыражение</b> - учительница Татьяна находит смысл в работе с рабочими
• <b>Образование</b> - вечерняя школа как социальный лифт
• <b>Романтизм</b> - чистота чувств, преодоление социальных барьеров

<b>Значимые сцены:</b>
1. Сцена в общежитии - коллективное обсуждение жизни
2. Урок литературы - спор о настоящем счастье
3. Финал на стройке - метафора строительства новой жизни

<b>Исторический контекст:</b> Фильм снят в период "оттепели", показывает смягчение идеологии.""",
        "цитаты": [
            "«Счастье — это когда тебя понимают»",
            "«Мы не ищем легких путей!»"
        ]
    },
    "доживем до понедельника": {
        "год": 1968,
        "режиссер": "Станислав Ростоцкий",
        "ценности": ["нравственность", "образование", "искренность", "моральный выбор"],
        "анализ": """🎬 <b>Анализ "Доживем до понедельника"</b>

<b>Ключевые ценности:</b>
• <b>Нравственный выбор</b> - учитель Мельников против цинизма коллеги
• <b>Искренность</b> - история с поддельными письмами
• <b>Профессиональный долг</b> - отношение к преподаванию
• <b>Честность перед собой</b> - внутренние конфликты героев

<b>Педагогические аспекты:</b>
• Конфликт традиционных и новых методов обучения
• Проблема авторитета учителя
• Воспитание через литературу и историю""",
        "цитаты": [
            "«Счастье — это когда тебя понимают»",
            "«История — это наука о человеке во времени»"
        ]
    },
    "москва слезам не верит": {
        "год": 1979,
        "режиссер": "Владимир Меньшов",
        "ценности": ["женская самостоятельность", "труд", "семья", "социальная мобильность"],
        "анализ": """🎬 <b>Анализ "Москва слезам не верит"</b>

<b>Ключевые ценности:</b>
• <b>Женская эмансипация</b> - карьерный рост Катерины
• <b>Трудолюбие</b> - путь от рабочей до директора
• <b>Семейные ценности</b> - несмотря на феминистские мотивы
• <b>Социальный прогресс</b> - изменение статуса женщины в обществе

<b>Социальный контекст:</b>
• Показан переход от коллективных к индивидуальным ценностям
• Конфликт "старого" и "нового" в отношениях
• Изменение гендерных ролей в позднем СССР""",
        "цитаты": [
            "«В сорок лет жизнь только начинается»",
            "«Вам нужна не жена, а прислуга»"
        ]
    },
    "офицеры": {
        "год": 1971,
        "режиссер": "Владимир Роговой",
        "ценности": ["патриотизм", "верность долгу", "дружба", "преемственность поколений"],
        "анализ": """🎬 <b>Анализ "Офицеры"</b>

<b>Ключевые ценности:</b>
• <b>Патриотизм</b> - служение Родине как высшая цель
• <b>Воинское братство</b> - дружба Алексея и Ивана
• <b>Преемственность</b> - сын продолжает дело отца
• <b>Жертвенность</b> - готовность отдать жизнь за страну

<b>Идеологический аспект:</b>
• Создание положительного образа офицера-героя
• Оправдание военных конфликтов СССР
• Воспитание молодежи в духе преданности государству""",
        "цитаты": [
            "«Есть такая профессия — Родину защищать»",
            "«Мы в ответе за тех, кого приручили»"
        ]
    },
    "ирония судьбы": {
        "год": 1975,
        "режиссер": "Эльдар Рязанов",
        "ценности": ["романтика", "интеллигентность", "дружба", "случай и судьба"],
        "анализ": """🎬 <b>Анализ "Ирония судьбы, или С легким паром!"</b>

<b>Ключевые ценности:</b>
• <b>Романтическая любовь</b> - случайная встреча как судьба
• <b>Интеллигентность</b> - образ главного героя-филолога
• <b>Дружеская поддержка</b> - помощь друзей в сложной ситуации
• <b>Поиск настоящего чувства</b> - против формализма в отношениях

<b>Социальный подтекст:</b>
• Критика стандартизации жизни в СССР
• Типовые дома как метафора одинаковости
• Поиск индивидуальности в массовом обществе""",
        "цитаты": [
            "«Какое простое и нужное слово — уходи!»",
            "«Я уезжаю в Ленинград и, наверное, никогда не вернусь»"
        ]
    }
}

# База знаний по ценностям
VALUES_DATABASE = {
    "коллективизм": {
        "определение": "Приоритет коллективных интересов над индивидуальными, идея общего блага",
        "проявления": [
            "Совместный труд и отдых",
            "Коллективное принятие решений", 
            "Взаимопомощь и поддержка",
            "Общественная собственность"
        ],
        "фильмы": ["Весна на Заречной улице", "Добровольцы", "Высота", "Коммунист"],
        "исторический_контекст": "Воспитывался через пионерию, комсомол, коллективы на производстве"
    },
    "труд": {
        "определение": "Труд как высшая ценность и смысл жизни, героизм трудовых будней",
        "проявления": [
            "Воспевание рабочих профессий",
            "Труд как самовыражение",
            "Социалистическое соревнование",
            "Ударничество и стахановское движение"
        ],
        "фильмы": ["Высота", "Коммунист", "Весна на Заречной улице", "Большая жизнь"],
        "исторический_контекст": "Индустриализация страны требовала воспитания уважения к труду"
    },
    "патриотизм": {
        "определение": "Любовь к Родине, готовность служить государству и защищать его",
        "проявления": [
            "Воинский долг",
            "Служба Отечеству",
            "Интернациональный долг",
            "Гордость за достижения страны"
        ],
        "фильмы": ["Офицеры", "Щит и меч", "А зори здесь тихие", "Освобождение"],
        "исторический_контекст": "Воспитание в условиях холодной войны и памяти о ВОВ"
    }
}

# Викторина
QUIZ_QUESTIONS = [
    {
        "question": "Какая ценность была центральной в фильме 'Офицеры'?",
        "options": ["Индивидуализм", "Карьерный рост", "Служение Родине", "Материальное благополучие"],
        "correct": 2,
        "explanation": "Фильм воспевает патриотизм и готовность служить Отечеству."
    },
    {
        "question": "Что символизируют типовые дома в 'Иронии судьбы'?",
        "options": ["Прогресс архитектуры", "Стандартизацию жизни", "Роскошь жилья", "Экологичность"],
        "correct": 1,
        "explanation": "Типовые дома показывают одинаковость и обезличенность советского быта."
    },
    {
        "question": "Какая ценность НЕ характерна для фильма 'Весна на Заречной улице'?",
        "options": ["Индивидуализм", "Коллективизм", "Труд", "Образование"],
        "correct": 0,
        "explanation": "Фильм пропагандирует коллективизм, а не индивидуализм."
    },
    {
        "question": "Какой исторический период отражает фильм 'Весна на Заречной улице'?",
        "options": ["Гражданская война", "Индустриализация", "Оттепель", "Перестройка"],
        "correct": 2,
        "explanation": "Фильм снят в 1956 году и отражает период 'оттепели'."
    },
    {
        "question": "Что стало символом женской эмансипации в 'Москва слезам не верит'?",
        "options": ["Карьера Катерины", "Общежитие", "Вечерняя школа", "Дружба с подругами"],
        "correct": 0,
        "explanation": "Путь Катерины от рабочей до директора завода - символ женской самостоятельности."
    },
    {
        "question": "Какая цитата стала знаменитой из фильма 'Доживем до понедельника'?",
        "options": [
            "«Счастье — это когда тебя понимают»",
            "«Любви все возрасты покорны»", 
            "«В сорок лет жизнь только начинается»",
            "«Есть такая профессия — Родину защищать»"
        ],
        "correct": 0,
        "explanation": "Именно фраза «Счастье — это когда тебя понимают» стала культовой."
    },
    {
        "question": "Какой конфликт показан в 'Доживем до понедельника'?",
        "options": [
            "Конфликт поколений",
            "Борьба за власть в школе", 
            "Столкновение традиционных и новых методов обучения",
            "Любовный треугольник"
        ],
        "correct": 2,
        "explanation": "Основной конфликт - между традиционными и новыми подходами к образованию."
    },
    {
        "question": "Что объединяет героев фильма 'Офицеры' на протяжении всей жизни?",
        "options": [
            "Любовь к одной женщине",
            "Служба в одном полку", 
            "Дружба и верность воинскому долгу",
            "Общее дело на гражданке"
        ],
        "correct": 2,
        "explanation": "Дружба и преданность воинскому долгу проходят через всю жизнь героев."
    },
    {
        "question": "Какой социальный лифт показан в 'Весна на Заречной улице'?",
        "options": [
            "Партийная карьера",
            "Вечерняя школа для рабочих", 
            "Переезд в столицу",
            "Брак с представителем высшего класса"
        ],
        "correct": 1,
        "explanation": "Вечерняя школа давала рабочим возможность получить образование и продвинуться."
    },
    {
        "question": "Что критикует 'Ирония судьбы' в советском обществе?",
        "options": [
            "Военную политику",
            "Стандартизацию и обезличенность", 
            "Отсутствие образования",
            "Низкие зарплаты"
        ],
        "correct": 1,
        "explanation": "Фильм мягко критикует стандартизацию жизни через образ одинаковых домов."
    }
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = update.message.from_user.first_name
        
        welcome_text = f"""
🎬 Привет, {user_name}! 
Добро пожаловать в бот «Ценности в советском кинематографе»!

Здесь ты сможешь:
• Изучить ключевые ценности через призму кино
• Получить подборки фильмов по темам
• Найти материал для учебных работ
• Проверить знания в викторине
• Получить анализ конкретных фильмов

Выбери раздел ниже 👇
"""
        
        keyboard = [
            [InlineKeyboardButton("📚 Основные ценности", callback_data="values")],
            [InlineKeyboardButton("🎭 Фильмы по категориям", callback_data="categories")],
            [InlineKeyboardButton("🔍 Анализ фильма", callback_data="film_analysis")],
            [InlineKeyboardButton("📖 Энциклопедия ценностей", callback_data="encyclopedia")],
            [InlineKeyboardButton("❓ Викторина", callback_data="quiz_start")],
            [InlineKeyboardButton("💡 Для учебы", callback_data="study")],
            [InlineKeyboardButton("🎯 Случайный фильм", callback_data="random_film")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")

# Основной обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "values":
            await show_values(query)
        elif data == "categories":
            await show_categories(query)
        elif data == "film_analysis":
            await show_film_analysis_menu(query)
        elif data == "encyclopedia":
            await show_encyclopedia_menu(query)
        elif data.startswith("value_"):
            await show_value_detail(query, data)
        elif data.startswith("film_"):
            await show_film_detail(query, data)
        elif data == "random_film":
            await show_random_film(query)
        elif data == "quiz_start":
            await start_quiz(query, context)
        elif data.startswith("quiz_"):
            await handle_quiz_answer(query, context, data)
        elif data == "study":
            await show_study_materials(query)
        else:
            await show_main_menu(query)
            
    except Exception as e:
        logger.error(f"Ошибка в обработчике кнопок: {e}")
        await query.edit_message_text("Произошла ошибка. Используйте /start для перезапуска.")

async def show_values(query):
    text = """
🏛️ <b>Ключевые ценности в советском кино:</b>

1. <b>Коллективизм</b> - "Один за всех и все за одного"
   • Приоритет общего над личным
   • Взаимопомощь и товарищество

2. <b>Труд как доблесть</b>
   • Героизм трудовых будней
   • Уважение к рабочему человеку

3. <b>Патриотизм и интернационализм</b>
   • Любовь к Родине без национализма
   • Дружба народов

4. <b>Справедливость и правда</b>
   • Борьба за правду против несправедливости
   • Нравственная чистота героев

5. <b>Образование и наука</b>
   • Культ знаний и просвещения
   • Ученый как положительный герой

6. <b>Романтика и любовь</b>
   • Чистота отношений
   • Любовь как духовная ценность
"""
    keyboard = [
        [InlineKeyboardButton("🎭 Примеры фильмов", callback_data="categories")],
        [InlineKeyboardButton("📖 Подробнее о ценностях", callback_data="encyclopedia")],
        [InlineKeyboardButton("🔍 Анализ фильма", callback_data="film_analysis")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_categories(query):
    text = """
🎭 <b>Фильмы по категориям ценностей:</b>

<b>Коллективизм и труд:</b>
• "Весна на Заречной улице" (1956)
• "Высота" (1957) 
• "Коммунист" (1957)

<b>Патриотизм и война:</b>
• "Офицеры" (1971)
• "А зори здесь тихие" (1972)
• "Щит и меч" (1968)

<b>Нравственность и мораль:</b>
• "Доживем до понедельника" (1968)
• "Москва слезам не верит" (1979)

<b>Романтика и комедия:</b>
• "Ирония судьбы" (1975)
• "Служебный роман" (1977)
"""
    keyboard = [
        [InlineKeyboardButton("📚 К ценностям", callback_data="values")],
        [InlineKeyboardButton("🔍 Анализ фильма", callback_data="film_analysis")],
        [InlineKeyboardButton("🎯 Случайный фильм", callback_data="random_film")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_film_analysis_menu(query):
    text = "🔍 <b>Выбери фильм для подробного анализа:</b>"
    keyboard = [
        [InlineKeyboardButton("Весна на Заречной улице", callback_data="film_vesna")],
        [InlineKeyboardButton("Доживем до понедельника", callback_data="film_ponedelnik")],
        [InlineKeyboardButton("Москва слезам не верит", callback_data="film_moscow")],
        [InlineKeyboardButton("Офицеры", callback_data="film_officers")],
        [InlineKeyboardButton("Ирония судьбы", callback_data="film_irony")],
        [InlineKeyboardButton("🎯 Случайный фильм", callback_data="random_film")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_encyclopedia_menu(query):
    text = "📖 <b>Энциклопедия советских ценностей</b>\n\nВыбери ценность для изучения:"
    keyboard = [
        [InlineKeyboardButton("Коллективизм", callback_data="value_kollektivizm")],
        [InlineKeyboardButton("Труд", callback_data="value_trud")],
        [InlineKeyboardButton("Патриотизм", callback_data="value_patriotism")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_value_detail(query, data):
    value_key = data.replace("value_", "")
    value_map = {
        "kollektivizm": "коллективизм",
        "trud": "труд", 
        "patriotism": "патриотизм"
    }
    
    if value_key in value_map:
        value = VALUES_DATABASE[value_map[value_key]]
        text = f"""
📚 <b>{value_map[value_key].title()} в советском кино</b>

<b>Определение:</b> {value['определение']}

<b>Проявления в кино:</b>
{chr(10).join(['• ' + item for item in value['проявления']])}

<b>Фильмы-примеры:</b>
{chr(10).join(['• ' + film for film in value['фильмы']])}

<b>Исторический контекст:</b> {value['исторический_контекст']}
"""
        keyboard = [
            [InlineKeyboardButton("📖 К энциклопедии", callback_data="encyclopedia")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_film_detail(query, data):
    film_key = data.replace("film_", "")
    film_map = {
        "vesna": "весна на заречной улице",
        "ponedelnik": "доживем до понедельника", 
        "moscow": "москва слезам не верит",
        "officers": "офицеры",
        "irony": "ирония судьбы"
    }
    
    if film_key in film_map and film_map[film_key] in FILMS_DATABASE:
        film_data = FILMS_DATABASE[film_map[film_key]]
        
        text = f"""
🎬 <b>{film_map[film_key].title()}</b>

<b>Год:</b> {film_data['год']}
<b>Режиссер:</b> {film_data['режиссер']}
<b>Ценности:</b> {', '.join(film_data['ценности'])}

{film_data['анализ']}

<b>Знаменитые цитаты:</b>
{chr(10).join(['• ' + quote for quote in film_data['цитаты']])}
"""
        keyboard = [
            [InlineKeyboardButton("🔍 Другой фильм", callback_data="film_analysis")],
            [InlineKeyboardButton("📚 К ценностям", callback_data="values")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_random_film(query):
    film_name, film_data = random.choice(list(FILMS_DATABASE.items()))
    text = f"""
🎯 <b>Случайный фильм для изучения:</b>

🎬 <b>{film_name.title()}</b>

<b>Год:</b> {film_data['год']}
<b>Режиссер:</b> {film_data['режиссер']}
<b>Ключевые ценности:</b> {', '.join(film_data['ценности'])}

<b>Краткий анализ:</b>
{film_data['анализ'][:300]}...
"""
    
    # Создаем callback_data для этого фильма
    film_callback_map = {
        "весна на заречной улице": "film_vesna",
        "доживем до понедельника": "film_ponedelnik",
        "москва слезам не верит": "film_moscow", 
        "офицеры": "film_officers",
        "ирония судьбы": "film_irony"
    }
    
    callback_data = film_callback_map.get(film_name, "film_analysis")
    
    keyboard = [
        [InlineKeyboardButton("📖 Полный анализ", callback_data=callback_data)],
        [InlineKeyboardButton("🎯 Другой случайный фильм", callback_data="random_film")],
        [InlineKeyboardButton("🔍 Выбрать фильм", callback_data="film_analysis")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def start_quiz(query, context):
    context.user_data['quiz_score'] = 0
    context.user_data['quiz_current'] = 0
    await send_quiz_question(query, context)

async def send_quiz_question(query, context):
    question_index = context.user_data['quiz_current']
    
    if question_index >= len(QUIZ_QUESTIONS):
        # Викторина завершена
        score = context.user_data['quiz_score']
        total = len(QUIZ_QUESTIONS)
        text = f"<b>Викторина завершена!</b>\nВаш результат: {score}/{total}"
        
        if score == total:
            text += "\n🎉 Отлично! Вы настоящий эксперт по советскому кино!"
        elif score >= total / 2:
            text += "\n👍 Хороший результат!"
        else:
            text += "\n📚 Есть куда расти! Изучайте материалы бота и возвращайтесь!"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Начать заново", callback_data="quiz_start")],
            [InlineKeyboardButton("📚 К разделам", callback_data="main_menu")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return
    
    question = QUIZ_QUESTIONS[question_index]
    text = f"❓ <b>Вопрос {question_index + 1}/{len(QUIZ_QUESTIONS)}</b>\n\n{question['question']}"
    
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f"quiz_answer_{question_index}_{i}")])
    
    keyboard.append([InlineKeyboardButton("↩️ Прервать викторину", callback_data="main_menu")])
    
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_quiz_answer(query, context, data):
    if data.startswith("quiz_answer_"):
        parts = data.split("_")
        question_index = int(parts[2])
        answer_index = int(parts[3])
        
        question = QUIZ_QUESTIONS[question_index]
        is_correct = (answer_index == question['correct'])
        
        if is_correct:
            context.user_data['quiz_score'] += 1
            result_text = "✅ <b>Правильно!</b>"
        else:
            result_text = "❌ <b>Неправильно</b>"
        
        result_text += f"\n\n{question['explanation']}"
        
        # Переходим к следующему вопросу
        context.user_data['quiz_current'] = question_index + 1
        
        if context.user_data['quiz_current'] < len(QUIZ_QUESTIONS):
            keyboard = [[InlineKeyboardButton("➡️ Следующий вопрос", callback_data=f"quiz_next_{context.user_data['quiz_current']}")]]
        else:
            keyboard = [[InlineKeyboardButton("📊 Посмотреть результаты", callback_data="quiz_next_0")]]
        
        await query.edit_message_text(text=result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    
    elif data.startswith("quiz_next_"):
        await send_quiz_question(query, context)

async def show_study_materials(query):
    text = """
💡 <b>Материалы для учебы:</b>

<b>Темы для рефератов:</b>
1. Эволюция образа героя в советском кино 1950-1980 гг.
2. Коллективизм как доминирующая ценность в советском кинематографе
3. Отражение трудовой этики в фильмах о рабочем классе
4. Патриотизм в военном кино СССР

<b>Ключевые термины:</b>
• Социалистический реализм
• Идейно-художественный замысел
• Коллективный герой
• Трудовая доблесть

<b>Методология анализа:</b>
1. Определите основные ценности, продвигаемые фильмом
2. Проанализируйте систему персонажей
3. Изучите визуальные средства выразительности
4. Рассмотрите исторический контекст
"""
    keyboard = [
        [InlineKeyboardButton("🎭 К фильмам", callback_data="categories")],
        [InlineKeyboardButton("📚 К ценностям", callback_data="values")],
        [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def show_main_menu(query):
    text = "Выберите раздел для изучения:"
    keyboard = [
        [InlineKeyboardButton("📚 Основные ценности", callback_data="values")],
        [InlineKeyboardButton("🎭 Фильмы по категориям", callback_data="categories")],
        [InlineKeyboardButton("🔍 Анализ фильма", callback_data="film_analysis")],
        [InlineKeyboardButton("📖 Энциклопедия ценностей", callback_data="encyclopedia")],
        [InlineKeyboardButton("❓ Викторина", callback_data="quiz_start")],
        [InlineKeyboardButton("💡 Для учебы", callback_data="study")],
        [InlineKeyboardButton("🎯 Случайный фильм", callback_data="random_film")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# Обработчик текстовых сообщений для поиска фильмов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text.lower()
        
        # Поиск фильма в базе данных
        for film_name, film_data in FILMS_DATABASE.items():
            if any(word in user_text for word in film_name.split()):
                text = f"""
🎬 <b>Найден фильм: {film_name.title()}</b>

<b>Год:</b> {film_data['год']}
<b>Режиссер:</b> {film_data['режиссер']}
<b>Ценности:</b> {', '.join(film_data['ценности'])}

<b>Краткий анализ:</b>
{film_data['анализ'][:400]}...
"""
                # Определяем callback_data для кнопки
                film_callback_map = {
                    "весна на заречной улице": "film_vesna",
                    "доживем до понедельника": "film_ponedelnik",
                    "москва слезам не верит": "film_moscow",
                    "офицеры": "film_officers", 
                    "ирония судьбы": "film_irony"
                }
                
                callback_data = film_callback_map.get(film_name, "film_analysis")
                keyboard = [[InlineKeyboardButton("📖 Полный анализ", callback_data=callback_data)]]
                
                await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
                return
        
        # Если фильм не найден
        await update.message.reply_text(
            "🔍 <b>Фильм не найден в базе данных.</b>\n\nПопробуйте один из этих вариантов:\n• Весна на Заречной улице\n• Доживем до понедельника\n• Москва слезам не верит\n• Офицеры\n• Ирония судьбы\n\nИли используйте кнопки меню для навигации.",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Ошибка в обработчике сообщений: {e}")
        await update.message.reply_text("Произошла ошибка при обработке запроса.")

# Команда помощи
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
<b>Доступные команды:</b>
/start - начать работу с ботом
/help - показать эту справку

<b>Как использовать бота для учебы:</b>
1. Изучите раздел "Основные ценности"
2. Используйте "Энциклопедию" для углубленного изучения
3. Подберите фильмы по нужной теме
4. Используйте анализ конкретных фильмов
5. Проверьте знания в викторине

<b>Вы также можете просто написать название фильма, и бот найдет его в базе!</b>
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")

def main():
    try:
        # Проверяем токен
        if BOT_TOKEN == "ВАШ_TELEGRAM_BOT_TOKEN":
            print("❌ ОШИБКА: Замените BOT_TOKEN на реальный токен от @BotFather!")
            return
        
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        print("🤖 Бот запускается...")
        print("✅ Если вы видите это сообщение, код работает корректно")
        print("❌ Если бот не отвечает, проверьте токен в переменной BOT_TOKEN")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        print("Проверьте:")
        print("1. Токен бота")
        print("2. Установлены ли все зависимости: pip install python-telegram-bot")
        print("3. Интернет-соединение")

if __name__ == '__main__':
    main()