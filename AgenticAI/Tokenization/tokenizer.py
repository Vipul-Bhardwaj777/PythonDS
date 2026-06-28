import tiktoken

text = "Hii Vipul, whats up!"

tokenizer = tiktoken.encoding_for_model("gpt-4o")

tokens_ = tokenizer.encode(text)

print("Encoded Tokens:", tokens_)

dec = tokenizer.decode(tokens_)

print("Decoded Tokens:", dec)
