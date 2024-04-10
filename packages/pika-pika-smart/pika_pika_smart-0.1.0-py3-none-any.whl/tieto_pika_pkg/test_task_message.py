from tieto_pika.tieto_pika_pkg.agent import receive_message


def handle_message():
    print("handle_new_message")
    return "handle success!"


if __name__ == '__main__':
    receive_message(handle_message)
