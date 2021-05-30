from argparse import ArgumentParser


def get_option(question="長所", wordsLength=300):
    argparser = ArgumentParser()
    argparser.add_argument('-q', '--question', type=str,
                           default=question,
                           help='Specify keyword of question')
    argparser.add_argument('-l', '--length', type=int,
                           default=wordsLength,
                           help='Specify length of output words')
    return argparser.parse_args()