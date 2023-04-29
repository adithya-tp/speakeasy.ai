import click
from utils import speak

@click.command
@click.option('--to', help="The recipient's phone number")
def main(to):
    bot = speak.SpeakieBot()
    bot.call(
        to=to
    )


if __name__ == '__main__':
    main()