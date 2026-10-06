"""GEMBA-DA prompt (Kocmi & Federmann 2023), reference-free. Single source of truth for the MT LLM judges."""
LANG = {"ende": ("English", "German"), "zhen": ("Chinese", "English")}
TEMPLATE = ('Score the following translation from {src_lang} to {tgt_lang} on a continuous scale from 0 to 100, '
            'where a score of zero means "no meaning preserved" and score of one hundred means "perfect meaning and grammar".\n\n'
            '{src_lang} source: "{source}"\n{tgt_lang} translation: "{hyp}"\nScore: ')

def build_user_message(lp, source, hyp):
    s, t = LANG[lp]
    return TEMPLATE.format(src_lang=s, tgt_lang=t, source=source, hyp=hyp)
