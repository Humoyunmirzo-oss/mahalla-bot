import os
import telebot
from telebot import types

# Token serverdagi Environment Variable'dan olinadi
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)


# =========================
# HUDUDLAR
# =========================

regions = {
    "andijon": [
        ("andijon_shahar", "Andijon shahri"),
        ("asaka", "Asaka"),
        ("shahrixon", "Shahrixon"),
        ("marhamat", "Marhamat")
    ],

    "fargona": [
        ("fargona_shahar", "Farg‘ona shahri"),
        ("qoqon", "Qo‘qon"),
        ("margilon", "Marg‘ilon")
    ],

    "toshkent": [
        ("toshkent_shahar", "Toshkent shahri"),
        ("chirchiq", "Chirchiq"),
        ("angren", "Angren"),
        ("olmaliq", "Olmaliq")
    ],

    "samarqand": [
        ("samarqand_shahar", "Samarqand shahri")
    ]
}


# =========================
# HUDUDLAR MENYUSI
# =========================

def regions_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        types.InlineKeyboardButton(
            "🇺🇿 Andijon",
            callback_data="region_andijon"
        ),
        types.InlineKeyboardButton(
            "🇺🇿 Farg‘ona",
            callback_data="region_fargona"
        ),
        types.InlineKeyboardButton(
            "🇺🇿 Toshkent",
            callback_data="region_toshkent"
        ),
        types.InlineKeyboardButton(
            "🇺🇿 Samarqand",
            callback_data="region_samarqand"
        )
    )

    return keyboard


# =========================
# /START
# =========================

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "🏘️ *Mahalla Bot*ga xush kelibsiz!\n\n"
        "📍 Hududingizni tanlang:",
        parse_mode="Markdown",
        reply_markup=regions_keyboard()
    )


# =========================
# HUDUD TANLASH
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("region_")
)
def region_selected(call):

    region = call.data.replace("region_", "")

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for city_id, city_name in regions[region]:
        keyboard.add(
            types.InlineKeyboardButton(
                city_name,
                callback_data=f"city_{city_id}"
            )
        )

    keyboard.add(
        types.InlineKeyboardButton(
            "⬅️ Orqaga",
            callback_data="back_regions"
        )
    )

    bot.edit_message_text(
        "📍 *Hudud tanlandi.*\n\n"
        "Shahar yoki tumanni tanlang:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    bot.answer_callback_query(call.id)


# =========================
# SHAHAR / TUMAN
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("city_")
)
def city_selected(call):

    city_id = call.data.replace("city_", "")

    city_names = {}

    for cities in regions.values():
        for cid, cname in cities:
            city_names[cid] = cname

    city = city_names.get(city_id, "Noma'lum hudud")

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        types.InlineKeyboardButton(
            "🏘️ Mahallalar",
            callback_data=f"mahalla_{city_id}"
        ),
        types.InlineKeyboardButton(
            "📢 E'lonlar",
            callback_data=f"announcements_{city_id}"
        ),
        types.InlineKeyboardButton(
            "📞 Aloqa",
            callback_data=f"contact_{city_id}"
        ),
        types.InlineKeyboardButton(
            "⬅️ Orqaga",
            callback_data="back_regions"
        )
    )

    bot.edit_message_text(
        f"📍 *{city}*\n\n"
        "Kerakli bo‘limni tanlang:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    bot.answer_callback_query(call.id)


# =========================
# MAHALLALAR
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("mahalla_")
)
def mahallas(call):

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "🏘️ *Mahallalar*\n\n"
        "⏳ Test versiyada mahallalar bazasi hali "
        "qo‘shilmagan.",
        parse_mode="Markdown"
    )


# =========================
# E'LONLAR
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("announcements_")
)
def announcements(call):

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "📢 *E'lonlar*\n\n"
        "Hozircha e'lonlar mavjud emas.",
        parse_mode="Markdown"
    )


# =========================
# ALOQA
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("contact_")
)
def contact(call):

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "📞 *Aloqa*\n\n"
        "Test versiya.\n"
        "Aloqa ma'lumotlari keyin qo‘shiladi.",
        parse_mode="Markdown"
    )


# =========================
# ORQAGA
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data == "back_regions"
)
def back_regions(call):

    bot.edit_message_text(
        "📍 Hududingizni tanlang:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=regions_keyboard()
    )

    bot.answer_callback_query(call.id)


# =========================
# ISHGA TUSHIRISH
# =========================

print("🏘️ Mahalla Bot ishga tushdi!")

bot.infinity_polling(
    skip_pending=True,
    timeout=30,
    long_polling_timeout=30
  )
