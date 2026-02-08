import re
import textwrap

def sanitize_filename(filename):
    clean = re.sub(r'[\\/*?:"<>|]', "", filename)
    return clean.strip()[:150]

def generate_bibtex(result):
    """
    result: arxiv.Result 对象
    """
    short_id = result.get_short_id()
    try:
        first_author = result.authors[0].name.split(' ')[-1].lower()
    except:
        first_author = "unknown"
    year = result.published.year
    first_word = result.title.split(' ')[0].lower()
    first_word = re.sub(r'[^a-z]', '', first_word)
    
    cite_key = f"{re.sub(r'[^a-z]', '', first_author)}{year}{first_word}"
    authors = " and ".join([a.name for a in result.authors])
    
    return textwrap.dedent(f"""
    @misc{{{cite_key},
      title={{{result.title}}}, 
      author={{{authors}}},
      year={{{year}}},
      eprint={{{short_id}}},
      archivePrefix={{arXiv}},
      primaryClass={{{result.primary_category}}},
      url={{{result.entry_id}}}
    }}
    """).strip()