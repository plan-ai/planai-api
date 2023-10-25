import tiktoken

input_token_price = 1.5 * 10 ^ (-6)
output_token_price = 2 * 10 ^ (-6)
encoding_type = "gpt-3.5-turbo"


def encoding_getter(encoding_type: str):
    """
    Returns the appropriate encoding based on the given encoding type (either an encoding string or a model name).
    """
    if "k_base" in encoding_type:
        return tiktoken.get_encoding(encoding_type)
    else:
        return tiktoken.encoding_for_model(encoding_type)


def tokenizer(string: str, encoding_type: str) -> list:
    """
    Returns the tokens in a text string using the specified encoding.
    """
    encoding = encoding_getter(encoding_type)
    tokens = encoding.encode(string)
    return tokens


def token_counter(string: str, encoding_type: str) -> int:
    """
    Returns the number of tokens in a text string using the specified encoding.
    """
    num_tokens = len(tokenizer(string, encoding_type))
    return num_tokens


def estimate_token_usage(input_chat: str):
    token_input = token_counter(input_chat, encoding_type)
    return token_input * input_token_price + 2 * token_input * output_token_price


def actual_token_usage(input_chat: str, output_chat: str):
    input_token = token_counter(input_chat, encoding_type)
    output_token = token_counter(output_chat, encoding_type)
    return input_token * input_token_price + output_token * output_token_price
