import model
import hf


def print_tokens():
    shakespeareModel = model.Model('/Users/jackuchitel/PycharmProjects/flaskProject1/corpora/william_shakespeare_collected_works.txt', 1, 0)
    shakespeareModel.estimate()


if __name__ == '__main__':
    print_tokens()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
