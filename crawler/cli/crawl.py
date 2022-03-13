import argparse

from crawler.tasks import crawl


def main(args):
    task = crawl(args.url, args.word)
    print(task.id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://www.wikipedia.com')
    parser.add_argument('--word', default='bicycle')
    args = parser.parse_args()

    main(args)
