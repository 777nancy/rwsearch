import argparse
import logging

import mimesis

from rpgetter.utils import config, google, rakuten

logger = logging.getLogger(__name__)


def get_mail_point(args):
    conf = config.JsonConfig(config_json=args.config)
    target_addresses = conf.get_ad_mail_addresses()

    authenticator = google.GoogleAuthenticator(credentials_json=args.credentials, token_pickle=args.token_pickle)
    authenticator.save()

    gmail_manager = google.GmailManager(credentials=authenticator.credentials, max_result=args.num)
    html_bodies = gmail_manager.get_body_by_from_address(target_addresses)
    logger.info(f'ad mails: {len(html_bodies)}')
    if not html_bodies:
        return

    rakuten_session_manager = rakuten.RakutenSessionManager(args.user, args.password, conf)
    point_urls = [rakuten_session_manager.find_url(body) for body in html_bodies]
    logger.info(f'ad urls: {len(point_urls)}')
    if not point_urls:
        return
    for url in point_urls:
        logger.info(f'URL:{url}')
    rakuten_session_manager.get(point_urls)


def get_search_point(args):
    conf = config.JsonConfig(config_json=args.config)
    rakuten_session_manager = rakuten.RakutenSessionManager(args.user, args.password, conf)
    text = mimesis.Text()
    word_list = [text.word() for _ in range(args.num)]

    rakuten_session_manager.search(word_list)


if __name__ == '__main__':
    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument('-u', '--user', required=True, help='Rakuten user id')
    parent_parser.add_argument('-p', '--password', required=True, help='Rakuten Password')
    parent_parser.add_argument('--config', default=None, help='config file path')
    parent_parser.add_argument('--debug', action='store_true', help='debug mode')

    parser = argparse.ArgumentParser(add_help=False)
    sub_parsers = parser.add_subparsers(dest='command', required=True)

    parser_ad_mail = sub_parsers.add_parser('ad-mail', help='click ad-mail url', parents=[parent_parser])
    parser_ad_mail.add_argument('-c', '--credentials', default=None, help='google credentials.json path')
    parser_ad_mail.add_argument('-t', '--token-pickle', default=None, help='google credentials token pickle')
    parser_ad_mail.add_argument('-n', '--num', required=True, default=100, type=int, help='num of mails')
    parser_ad_mail.set_defaults(handler=get_mail_point)

    parser_web_search = sub_parsers.add_parser('web-search', help='search words in rakuten-web-search', parents=[
        parent_parser])
    parser_web_search.add_argument('-n', '--num', required=True, default=30, type=int, help='num of searching words')
    parser_web_search.set_defaults(handler=get_search_point)

    cli_args = parser.parse_args()

    if cli_args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
        level=log_level
    )

    for k, v in cli_args.__dict__.items():
        logger.info(f'{k}: {v}')

    cli_args.handler(cli_args)
