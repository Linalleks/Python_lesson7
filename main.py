import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


load_dotenv()
TG_TOKEN = os.environ['TG_TIMER_BOT_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='',
                       suffix='', length=15, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, total, author_id, message_id):
    answer = f"Осталось секунд: \
        {secs_left}\n{render_progressbar(total, secs_left)}"
    bot.update_message(author_id, message_id, answer)
    if secs_left == 0:
        bot.send_message(author_id, "Время вышло")


def notify_start(author_id, incoming_time):
    message_id = bot.send_message(author_id, 'Запускаю таймер...')
    bot.create_timer(
        1,
        start_timer,
        incoming_time=incoming_time,
        author_id=author_id,
        message_id=message_id
    )


def start_timer(incoming_time, author_id, message_id):
    bot.create_countdown(
        parse(incoming_time),
        notify_progress,
        total=parse(incoming_time),
        author_id=author_id,
        message_id=message_id
    )


def main():
    bot.reply_on_message(notify_start)
    bot.run_bot()


if __name__ == '__main__':
    main()
