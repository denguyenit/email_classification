import re
import spacy
nlp = spacy.load('en_core_web_sm')

def check_greeting(paragraph):
    greetings= ['hello', 'dear', 'dears', 'hi', 'morning', 'hey', 'afternoon', 'guys']
    paragraph = re.sub("[^A-Za-z ]", " ", paragraph)
    paragraph = paragraph.lower().strip()
    words = paragraph.split()
    if len(words) <= 4:
        for word in words:
            if word in greetings:
                return True    

def check_sign(paragraph):
    signs = ['regard','regards', 'thank', 'thanks','thankyou','thx', 'sincerely', 'cheers', 'best', 'bests', 'yours', 'faithfully']
    paragraph = re.sub("[^A-Za-z ]", " ", paragraph)
    paragraph = paragraph.lower().strip()
    words = paragraph.split()
    if len(words) <= 3:
        for word in words:
            if word in signs:
                return True    

def split_paragraph_and_remove_null(string):
    paragraphs = string.split("\r\n")
    for p in paragraphs:
        if len(str(p))==0:
            paragraphs.remove(p)
    return paragraphs

def find_body_email(string):
    paragraphs = split_paragraph_and_remove_null(string)
    start = -1
    end = len(paragraphs)
    for index, p in enumerate(paragraphs):
        if index == 0 and check_sign(p): continue
        if check_greeting(p):
            start = index
        if check_sign(p):
            end = index
            break  
    paragraphs = paragraphs[start+1:end] 
    return '\n'.join(paragraphs)

def clean_special_paragraph(string):
    regex_email ='\S+@\S+'
    regex_url = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*|((www\.)[\S]+( |\s))"

    paragraphs = string.split("\n")
    clean_pr =[]
    for p in paragraphs:
        x = re.findall(r'^From:|^To:|^Date:|^Sent:|^Subject:|^Cc:', p)
        if x:
            clean_pr.append(p)
    for p in clean_pr:
        paragraphs.remove(p)
    new_paragraps = []
    for p in paragraphs:
        clean = re.sub(r"\[[^\]]*\]", " ", p)
        clean = re.sub(regex_email, " ", clean)
        clean = re.sub(regex_url, " ", clean)
        new_paragraps.append(clean)
    return "\n".join(new_paragraps)

def lower(string):
    string = string.lower()
    return string

def clean_special(string):
    #clean html
    string = re.compile(r'<.*?>').sub(' ', string)

    string = re.sub(r"n\'t|n\?t", " not", string)
    string = re.sub(r"\'re|\?re", " are", string)
    string = re.sub(r"\'s|\?s", " is", string)
    string = re.sub(r"\'d|\?d", " would", string)
    string = re.sub(r"\'ll|\?ll", " will", string)
    string = re.sub(r"\''t|\?t", " not", string)
    string = re.sub(r"\'ve|\?ve", " have", string)
    string = re.sub(r"\'m|\?m", " am", string)
    string = re.sub(r"can\'t|can\?t", "can not", string)
    
    return string

def clean_special_character_whilespaces_and_number(string):
    string = re.sub(r"[^a-zA-Z0-9 ]", " ", string)
    string = re.sub(r'\d', ' ', string) 
    string = re.sub(r'\s+', ' ', string) 
    return string.strip()

def remove_stopwords(string):
    return " ".join([token.text for token in nlp(string) if not token.is_stop])

def lemmatize(string):
    return ' '.join([tok.lemma_.title() if tok.is_title else tok.lemma_ for tok in nlp(string)])

def remove_one_and_two_characters(string):
    return " ".join([token.text for token in nlp(string) if len(str(token))>2])

def pre_processing(body_email):
    doc = nlp(body_email)
    output = []
    for sent in doc.sents:
        sent = str(sent)
        sent = lower(sent)
        sent = clean_special(sent)
        sent = clean_special_character_whilespaces_and_number(sent)
        sent = remove_stopwords(sent)
        sent = lemmatize(sent)
        sent = remove_one_and_two_characters(sent)
        output.append(sent)
    return " ".join(output)
