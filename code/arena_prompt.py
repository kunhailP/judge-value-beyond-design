"""Pairwise judge prompt for the LMArena block (MT-Bench / AlpacaEval style). Single source of truth."""
MAX_RESP_TOK = 1500   # per response
MAX_PROMPT_TOK = 800  # user instruction

TEMPLATE = (
    "You are a helpful and impartial assistant evaluating the quality of two AI assistant responses "
    "to the same user instruction.\n\n"
    "[User Instruction]\n{prompt}\n[End of User Instruction]\n\n"
    "[Response A]\n{resp_a}\n[End of Response A]\n\n"
    "[Response B]\n{resp_b}\n[End of Response B]\n\n"
    "Which response better follows the user's instruction and is more helpful, accurate and well written? "
    "Do not let the order or the length of the responses influence your judgment. "
    "Even if both responses are similar, you must pick one. Answer with exactly one letter, A or B, and nothing else."
)

def truncate(tok, text, n):
    ids = tok.encode(text, add_special_tokens=False)
    if len(ids) <= n:
        return text
    return tok.decode(ids[:n], skip_special_tokens=True) + " [...]"

def build_user_message(tok, prompt, resp_a, resp_b):
    return TEMPLATE.format(prompt=truncate(tok, prompt, MAX_PROMPT_TOK),
                           resp_a=truncate(tok, resp_a, MAX_RESP_TOK),
                           resp_b=truncate(tok, resp_b, MAX_RESP_TOK))
