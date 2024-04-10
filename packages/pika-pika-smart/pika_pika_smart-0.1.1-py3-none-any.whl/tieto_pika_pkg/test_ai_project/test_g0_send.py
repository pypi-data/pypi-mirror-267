from tieto_pika_pkg.g0_send import send_msg_by_routing_key

send_msg_by_routing_key("message_body_json", "inform.#.email.#", "5000")
