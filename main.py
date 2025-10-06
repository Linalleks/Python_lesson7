import ptbot
from decouple import config
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='',
                       suffix='', length=15, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, bot, total, author_id, message_id):
    if secs_left == total:
        return
    answer = f"Осталось секунд: \
        {secs_left}\n{render_progressbar(total, secs_left)}"
    bot.update_message(author_id, message_id, answer)


def notify_start(author_id, user_message, bot):
    message_id = bot.send_message(author_id, 'Запускаю таймер...')
    set_time = parse(user_message) + 1
    bot.create_countdown(
        set_time,
        notify_progress,
        bot=bot,
        total=set_time,
        author_id=author_id,
        message_id=message_id
    )
    bot.create_timer(set_time, notify_end, author_id=author_id, bot=bot)


def notify_end(author_id, bot):
    bot.send_message(author_id, "Время вышло")


def main():
    bot = ptbot.Bot(config('TG_TIMER_BOT_TOKEN'))
    bot.reply_on_message(notify_start, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
