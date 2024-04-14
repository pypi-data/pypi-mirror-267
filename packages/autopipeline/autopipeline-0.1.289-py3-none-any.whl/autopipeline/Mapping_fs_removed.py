import openai
import os
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
import textstat
import re
import csv
import ast
import time

from PIL import Image
from gensim import corpora, models
from nltk.tokenize import word_tokenize
from summarizer import Summarizer
import json
import copy
from flair.models import SequenceTagger
from flair.data import Sentence
from textblob import TextBlob
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from graphviz import Digraph
from PIL import Image
from IPython.display import display, update_display
from .util import num_tokens_from_string, num_tokens_from_messages, num_tokens_from_functions

from importlib import resources

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.api_key)

OPENAI_ORGANIZATION = "org-5rFbX7p7v2H4Sk1C8xb17aea"
os.environ["OPENAI_ORG"] = OPENAI_ORGANIZATION
openai.organization=os.environ["OPENAI_ORG"]

def check_alias(enum, all_description, new_description, verbose):
    # print(enum)
    # print(all_description)
    # print(new_description)
    messages = [
        {
            "role": "system",
            "content": '''The user is going to provide you with the following:
            (1) Existing table columns;
            (2) Detailed description for each existing column;
            (3) Detailed description for the new column to be added;
            '''
            + 
            '''Your task is to check whether there already exists a column in the given table that contains the EXACTLY same information as the column to be added.
                If yes, you should reply with that specific column; if no, you should reply with an empty string.
                In either cases, you should provide the rationale.
                Your output format can ONLY be "True"/"False" + "#" + "{column name}"/"" + "#{rationale}"
                '''
        },
        {
            "role": "user",
            "content": '''Existing table columns: ['text']'''  
            + '''. The detailed description for each existing column: 'text' column contains the posts to be analyzed; '''
            + '''. The detailed description for the new column to be added: 'text_emotion' column provides emotion identified from the 'text' column. IMPORTANT: emotion values of the 'text_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'.'''
        },
        {
            "role": "assistant",
            "content": "False##The description for the new column does not match any of the existing columns.",
        },
        {
            "role": "user",
            "content": '''Existing table columns: ['text', 'text_emotion']'''  
            + '''. The detailed description for each existing column: 'text' column contains the posts to be analyzed; 'text_emotion' column provides emotion identified from the 'text' column. IMPORTANT: emotion values of the 'text_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'; '''
            + '''. The detailed description for the new column to be added: 'text_sentiment' column is the sentiment of the content of the 'text' column. IMPORTANT: sentiment values of 'text_sentiment' column can only be either 'pos', 'neg', or 'other'.'''
        },
        {
            "role": "assistant",
            "content": "False##Although 'emotion' and 'sentiment' seem to be of same meaning, they (1) are not EXACTLY the same, and (2) have different values. Thus, the description for the new column does not match any of the existing columns.",
        },
        {
            "role": "user",
            "content": '''Existing table columns: ['text', 'headline', 'text_emotion']'''  
            + '''. The detailed description for each existing column: 'text' column contains the posts to be analyzed; 'text_emotion' column provides emotion identified from the 'text' column. IMPORTANT: emotion values of the 'text_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'; '''
            + '''. The detailed description for the new column to be added: 'headline_emotion' column provides emotion identified from the 'headline' column. IMPORTANT: emotion values of the 'headline_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'. '''
        },
        {
            "role": "assistant",
            "content": "False##The new column contains emotion from the 'headline' column, while the existing column contains emotion from the 'text' column. Thus, the description for the new column does not match any of the existing columns.",
        },
        {
            "role": "user",
            "content": '''Existing table columns: ['text', 'emotion']'''  
            + '''. The detailed description for each existing column: 'text' column contains the posts to be analyzed; 'emotion' column provides emotion identified from the 'text' column. IMPORTANT: emotion values of the 'emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'; '''
            + '''. The detailed description for the new column to be added: 'text_emotion' column provides emotion identified from the 'text' column. IMPORTANT: emotion values of the 'text_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'. '''
        },
        {
            "role": "assistant",
            "content": "True#emotion#The new column 'text_emotion' to be added contains exactly the same information as the existing 'emotion' column.",
        },
        {
            "role": "user",
            "content": '''Existing table columns: ''' + str(enum) 
            + '''. The detailed description for each existing column: ''' + all_description 
            + '''. The detailed description for the new column to be added: ''' + new_description
        }
    ]

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4-0613",
        messages=messages,
    )
    if verbose:
        num_token_msg = num_tokens_from_messages(messages, "gpt-4-0613")
        print("Number of tokens of messages for 'check_alias': ", num_token_msg)

    res = response.choices[0].message['content']
    if verbose:
        print(res)
    res_ls = res.split("#")
    if res_ls[0] != "True":
        return ""
    return res_ls[1]

def base_table_gen(filename=None): 
    # If no filename is specified, use the packaged data
    if filename is None:
        # Open the file as a file-like object using resources.open_text
        with resources.open_text('autopipeline.data', 'base.csv') as file:
            base_table = pd.read_csv(file)
    else:
        # If a filename is specified, read from that file
        base_table = pd.read_csv(filename)
    enum = base_table.columns.tolist()
    description = "'id' column is the document ID, starts with 0; 'pdf_orig' column is the path to the pdf file of the document file; "
    return base_table, enum, description

def get_hate(table, column, enum, description, verbose, dot):
    # if os.path.exists("data/implicit_hate_v1_stg1_posts.tsv"):
    #     df = pd.read_csv("data/implicit_hate_v1_stg1_posts.tsv", delimiter='\t')
    #     table[column+'_hate'] = df['class']
    # else:
    #     table[column+'_hate'] = "Undefined"
    new_description = "'"+column+"_hate' column contains 'explicit_hate', 'implicit_hate', or 'not_hate' as values to indicate whether the '"+column+"' column' contains hate speech - "+"IMPORTANT: both 'implicit_hate' and 'explicit_hate' imply that the '"+column+"' column contains hate speech; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_hate")
        return table, enum, description, dot
    if os.path.exists("data/hate_full.tsv"):
        df = pd.read_csv("data/hate_full.tsv", delimiter='\t')
        table[column+'_hate'] = df['class']
    else:
        table[column+'_hate'] = "Undefined"
    enum.append(column+"_hate")
    description += " " + "'"+column+"_hate' column contains 'explicit_hate', 'implicit_hate', or 'not_hate' as values to indicate whether the '"+column+"' column' contains hate speech - "+"IMPORTANT: both 'implicit_hate' and 'explicit_hate' imply that the '"+column+"' column contains hate speech; "

    # update graph
    dot.node(column+"_hate")
    dot.edge(column, column+"_hate", "get_hate")

    return table, enum, description, dot

def get_hate_class(table, column, enum, description, verbose, dot):
    # if os.path.exists("data/implicit_hate_v1_stg2_posts.tsv"):
    #     df = pd.read_csv("data/implicit_hate_v1_stg2_posts.tsv", delimiter='\t')
    #     table[column+'_implicit_hate_class'] = df['implicit_class']
    # else:
    #     table[column+'_implicit_hate_class'] = "Undefined"
    new_description = "'"+column+"_implicit_hate_class' column provides implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_class' column can only be one of 'white_grievance', 'incitement', 'inferiority', 'irony', 'stereotypical', 'threatening', or 'other'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_hate_class")
        return table, enum, description, dot
    if os.path.exists("data/hate_full.tsv"):
        df = pd.read_csv("data/hate_full.tsv", delimiter='\t')
        table[column+'_implicit_hate_class'] = df['implicit_class']
    else:
        table[column+'_implicit_hate_class'] = "Undefined"
    enum.append(column+"_implicit_hate_class")
    description += " " + "'"+column+"_implicit_hate_class' column provides implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_class' column can only be one of 'white_grievance', 'incitement', 'inferiority', 'irony', 'stereotypical', 'threatening', or 'other'; "

    # update graph
    dot.node(column+"_implicit_hate_class")
    dot.edge(column, column+"_implicit_hate_class", "get_hate_class")

    return table, enum, description, dot

def get_hate_target(table, column, enum, description, verbose, dot):
    # if os.path.exists("data/implicit_hate_v1_stg2_posts.tsv"):
    #     df = pd.read_csv("data/implicit_hate_v1_stg2_posts.tsv", delimiter='\t')
    #     table[column+'_implicit_hate_class'] = df['implicit_class']
    # else:
    #     table[column+'_implicit_hate_class'] = "Undefined"
    new_description = "'"+column+"_implicit_hate_target' column provides the target of implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_target' column are free label texts, and thus it's more preferrable to use partial or fuzzy comparisons; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_hate_target")
        return table, enum, description, dot
    if os.path.exists("data/hate_full.tsv"):
        df = pd.read_csv("data/hate_full.tsv", delimiter='\t')
        table[column+'_implicit_hate_target'] = df['target']
    else:
        table[column+'_implicit_hate_target'] = "Undefined"
    enum.append(column+"_implicit_hate_target")
    description += " " + "'"+column+"_implicit_hate_target' column provides the target of implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_target' column are free label texts, and thus it's more preferrable to use partial or fuzzy comparisons; "

    # update graph
    dot.node(column+"_implicit_hate_target")
    dot.edge(column, column+"_implicit_hate_target", "get_hate_target")

    return table, enum, description, dot

def get_hate_implied(table, column, enum, description, verbose, dot):
    # if os.path.exists("data/implicit_hate_v1_stg2_posts.tsv"):
    #     df = pd.read_csv("data/implicit_hate_v1_stg2_posts.tsv", delimiter='\t')
    #     table[column+'_implicit_hate_class'] = df['implicit_class']
    # else:
    #     table[column+'_implicit_hate_class'] = "Undefined"
    new_description = "'"+column+"_implicit_hate_implied' column provides the implied statement of implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_implied' column are free label texts, and thus it's more preferrable to use partial or fuzzy comparisons; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_hate_implied")
        return table, enum, description, dot
    if os.path.exists("data/hate_full.tsv"):
        df = pd.read_csv("data/hate_full.tsv", delimiter='\t')
        table[column+'_implicit_hate_implied'] = df['implied_statement']
    else:
        table[column+'_implicit_hate_implied'] = "Undefined"
    enum.append(column+"_implicit_hate_implied")
    description += " " + "'"+column+"_implicit_hate_implied' column provides the implied statement of implicit hate speech identified from the '"+column+"' column' - "+"IMPORTANT: the values of '" +column+"_implicit_hate_implied' column are free label texts, and thus it's more preferrable to use partial or fuzzy comparisons; "

    # update graph
    dot.node(column+"_implicit_hate_implied")
    dot.edge(column, column+"_implicit_hate_implied", "get_hate_implied")

    return table, enum, description, dot

def get_misinfo(table, column, enum, description, verbose, dot):
    def misinfo(document):
        MODEL = "jy46604790/Fake-News-Bert-Detect"
        clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)
        result = clf(document)
        if result[0]['label'] == 'LABEL_0':
            return 'misinfo'
        else:
            return 'real'
    new_description = "'"+column+"_misinfo' column provides information about whether the '"+column+"' column' contains misinformation (i.e., fake contents) - "+"IMPORTANT: the values of '" +column+"_misinfo' column can only be either 'misinfo' or 'real': 'misinfo' means the '"+column+"' column contains misinformation; 'real' means the content of the '"+column+"' column is real; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_misinfo")
        return table, enum, description, dot
    if os.path.exists("data/test_annot_all.tsv"):
        df = pd.read_csv("data/test_annot_all.tsv", delimiter='\t')
        table[column+'_misinfo'] = df['gold_label']
    else:
        table[column+'_misinfo'] = table[column].apply(misinfo)
    enum.append(column+"_misinfo")
    description += " " + "'"+column+"_misinfo' column provides information about whether the '"+column+"' column' contains misinformation (i.e., fake contents) - "+"IMPORTANT: the values of '" +column+"_misinfo' column can only be either 'misinfo' or 'real': 'misinfo' means the '"+column+"' column contains misinformation; 'real' means the content of the '"+column+"' column is real; "

    # update graph
    dot.node(column+"_misinfo")
    dot.edge(column, column+"_misinfo", "get_misinfo")

    return table, enum, description, dot

def get_emotion(table, column, enum, description, verbose, dot):
    def emotion(document):
        # Load the tokenizer and model from Hugging Face Hub
        tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")
        model = AutoModelForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")

        # Create a pipeline for emotion classification
        emotion_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

        res = emotion_classifier(document)

        return res['label']
    
    # new_description = "'"+column+"_emotion' column provides emotion identified from the '"+column+"' column'."+"IMPORTANT: emotion values of '" +column+"_emotion' column can only be either 'sadness', 'joy', 'love', 'anger', 'fear', or 'surprise'; "
    # col = check_alias(enum, description, new_description, verbose)
    # if len(col) > 0:
    #     dot.edge(column, col, "get_emotion")
    #     return table, enum, description, dot
    # if os.path.exists("data/merged_training.pkl"):
    #     df = pd.read_pickle("data/merged_training.pkl")
    #     table[column+'_emotion'] = df['emotions']
    # else:
    #     table[column+'_emotion'] = table[column].apply(emotion)
    # description += " " + "'"+column+"_emotion' column provides emotion identified from the '"+column+"' column'."+"IMPORTANT: emotion values of '" +column+"_emotion' column can only be either 'sadness', 'joy', 'love', 'anger', 'fear', or 'surprise'; "

    new_description = "'"+column+"_emotion' column provides emotion identified from the '"+column+"' column'."+"IMPORTANT: emotion values of '" +column+"_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_emotion")
        return table, enum, description, dot
    if os.path.exists("data/emotion_trigger.tsv"):
        df = pd.read_csv("data/emotion_trigger.tsv", delimiter='\t')
        table[column+'_emotion'] = df['emotion']
    else:
        table[column+'_emotion'] = table[column].apply(emotion)
    description += " " + "'"+column+"_emotion' column provides emotion identified from the '"+column+"' column'."+"IMPORTANT: emotion values of '" +column+"_emotion' column can only be either 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'; "
    enum.append(column+"_emotion")

    # update graph
    dot.node(column+"_emotion")
    dot.edge(column, column+"_emotion", "get_emotion")
    
    return table, enum, description, dot

def get_trigger(table, column, emotion, enum, description, verbose, dot):
    assert emotion.endswith('emotion')
    new_description = "'"+column+"_trigger' column provides trigger identified from column '"+column+"' that triggers the emotion as described in the '"+emotion+"'."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_trigger")
        dot.edge(emotion, col, "get_trigger")
        return table, enum, description, dot
    if os.path.exists("data/emotion_trigger.tsv"):
        df = pd.read_csv("data/emotion_trigger.tsv", delimiter='\t')
        table[column+'_trigger'] = df['trigger']
    else:
        table[column+'_trigger'] = 'Undefined'
    description += " " + "'"+column+"_trigger' column provides trigger identified from column '"+column+"' that triggers the emotion as described in the '"+emotion+"'."
    enum.append(column+"_trigger")

    # update graph
    dot.node(column+"_trigger")
    dot.edge(column, column+"_trigger", "get_trigger")
    dot.edge(emotion, column+"_trigger", "get_trigger")

    return table, enum, description, dot

def get_condition(user_query, table, column, enum, description, verbose, dot):
    def class_gpt(document):
        messages = [
            {
                "role": "system",
                "content": "Given a text: " + document 
                + ''', Your task is to check whether the text satisfies the condition(s) listed in the user query.
                    If it satisfies, you should output "True"; else, you should output "False".
                    IMPORTANT: No contents other than "True"/"False" are allowed to be output.
                    '''
            },
            {
                "role": "user",
                "content": user_query  # Use the user's query
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4-0613",
            messages=messages,
        )
        if verbose:
            num_token_msg = num_tokens_from_messages(messages, "gpt-3.5-turbo")
            print("Number of tokens of messages for 'get_condition': ", num_token_msg)
        
        res = response.choices[0].message['content']
        if res != "True" and res != "False":
            res = "Undefined"
        return res
    
    new_description = "'"+column+"_class' column provides whether the content in the '"+column+"' column satisfies the conditions of the user query ('True'/'False'/'Undefined'): "+ user_query+";"
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_condition")
        return table, enum, description, dot

    table[column+'_class'] = table[column].apply(class_gpt)
    enum.append(column+"_class")
    description += " " + "'"+column+"_class' column provides whether the content in the '"+column+"' column satisfies the conditions of the user query ('True'/'False'/'Undefined'): "+ user_query+";"

    # update graph
    dot.node(column+"_class")
    dot.edge(column, column+"_class", "get_condition")

    return table, enum, description, dot


def pdf_to_text(table, column, enum, description, verbose, dot):
    def ocr(pdf_path):
        # Open the PDF file
        # with resources.path('autopipeline.data', pdf_file_name) as pdf_path:
        #     pdf_document = fitz.open(pdf_path)
        pdf_document = fitz.open(pdf_path)

        # Initialize an empty string to store text
        text = ""

        # Iterate over pages
        for page_number in range(pdf_document.page_count - 4):
            # Get the page
            page = pdf_document[page_number]

            # Convert the page to an image
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

            # Perform OCR on the image
            page_text = pytesseract.image_to_string(image, lang='eng')

            ls = page_text.split("\n\n")

            ls = ls[1:]

            ls = [line.replace("\n", " ") for line in ls]

            page_text = '\n'.join(ls)

            # Append the extracted text to the overall text
            text += page_text

        # Close the PDF document
        pdf_document.close()

        # print(text)

        return text
    
    def pdf_extract(pdf_path):
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Initialize an empty string to store text
        text = ""

        # Iterate over pages
        for page_number in range(pdf_document.page_count):
            # Get the page
            page = pdf_document[page_number]

            # Get text from the page
            page_text = page.get_text("text")

            # Append the extracted text to the overall text
            text += page_text

        # Close the PDF document
        pdf_document.close()

        # print(text)

        return text
    
    new_description = "'"+column+"_text' column is the plain text content of the '" + column +"' column; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "pdf_to_text")
        return table, enum, description, dot
    table[column+'_text'] = table[column].apply(ocr)
    enum.append(column+'_text')
    description += " "+"'"+column+"_text' column is the plain text content of the '" + column +"' column; "

    # update graph
    dot.node(column+"_text")
    dot.edge(column, column+"_text", "pdf_to_text")

    return table, enum, description, dot

# break into paragraphs: this might pose challenge in our mapping since every row might have different number
# "I want to know the attitude of MORITZ, Circuit Judge"
def para_sep(table, column, enum, description, verbose, dot):
    def sep(row):
        # Tokenize and preprocess the document
        paragraphs = [paragraph.strip() for paragraph in row[column].split('\n') if paragraph.strip()]
        rows = []
        for para_id, paragraph in enumerate(paragraphs):
            new_row = copy.deepcopy(row)
            new_row[column+'_segment'] = paragraph
            new_row[column+'_segmentid'] = para_id
            rows.append(new_row)
        res = pd.DataFrame(rows)
        #print(res)
        return res
    new_description = f"'{column}_segment' column stores the paragraph segments of the '" + column +"column', the original text has empty value; "
    col0 = check_alias(enum, description, new_description, verbose)
    if len(col0) == 0:
        # Apply the function to each row and collect the results in a list
        result_df = pd.concat(table.apply(lambda row: sep(row), axis=1).tolist())
        table[column+'_segment'] = ""
        table = pd.concat([table, result_df[column+'_segment']])
        enum.append(column+'_segment')
        description += " "+f"'{column}_segment' column stores the paragraph segments of the '" + column +"column', the original text has empty value; "
        dot.node(column+"_segment")
        dot.edge(column, column+"_segment", "para_sep")
    else:
        dot.edge(column, col0, "para_sep")

    new_description = f"'{column}_segmentid' column stores the paragraph index according to the order of the '" + column +"_segment' column, starts with 0, and the original text has value -1 (should be removed when performing functions related to paragraphs); "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "para_sep")
        return table, enum, description, dot
    if len(col0) != 0:
        result_df = pd.concat(table.apply(lambda row: sep(row), axis=1).tolist())
    table[column+'_segmentid'] = -1
    # Concatenate the original DataFrame and the result
    table = pd.concat([table, result_df[column+'_segmentid']])
    enum.append(column+'_segmentid')
    description += " "+f"'{column}_segmentid' column stores the paragraph index according to the order of the '" + column +"_segment' column, starts with 0, and the original text has value -1 (should be removed when performing functions related to paragraphs); "

    # # Apply the sep function to the specified column
    # segments = table[column].apply(sep)

    # # Create new columns for each segment
    # for i in range(len(segments[0])):
    #     col_name = f"{column}_segment{i + 1}"
    #     enum.append(column+'_segment'+str(i+1))
    #     description += " "+f"'{column}_segment{i + 1}' column is the {i+1}-th segment of the '" + column +"' column; "
    #     table[col_name] = segments.apply(lambda x: x[i] if i < len(x) else None)

    # update graph
    # dot.node(column+"_segment")
    dot.node(column+'_segmentid')
    # dot.edge(column, column+"_segment", "para_sep")
    dot.edge(column, column+"_segmentid", "para_sep")

    return table, enum, description, dot

def get_ner(table, column, enum, description, verbose, dot):
    def ner(row):
        document = row[column]
        # Load the pre-trained Flair NER model for English
        ner_model = SequenceTagger.load('ner')

        # Create a Flair Sentence
        sentence = Sentence(document)

        # Run NER on the sentence
        ner_model.predict(sentence)

        rows = []

        for entity in sentence.get_spans('ner'):
            new_row = copy.deepcopy(row)
            new_row[column+'_ner_type'] = entity.get_labels()[0].value
            new_row[column+'_ner_val'] = entity.text
            rows.append(new_row)
        res = pd.DataFrame(rows)
        #print(res)
        return res
    
    new_description = "'"+column+"_ner_type' column gives the type of the name entities recognized (NER) in the "+column+" column. IMPORTANT: all the NER in the '" +column+"_ner_type' column are in the form of three letters: 'PER' (person), 'LOC' (location), 'GPE' (geopolitical entities), etc."
    col0 = check_alias(enum, description, new_description, verbose)
    if len(col0) == 0:
        # Apply the function to each row and collect the results in a list
        result_df = pd.concat(table.apply(lambda row: ner(row), axis=1).tolist())
        table[column+'_ner_type'] = ""
        table = pd.concat([table, result_df[column+'_ner_type']])
        enum.append(column+'_ner_type')
        description += " "+"'"+column+"_ner_type' column gives the type of the name entities recognized (NER) in the "+column+" column. IMPORTANT: all the NER in the '" +column+"_ner_type' column are in the form of three letters: 'PER' (person), 'LOC' (location), 'GPE' (geopolitical entities), etc."
        dot.node(column+"_ner_type")
        dot.edge(column, column+"_ner_type", "get_ner")
    else:
        dot.edge(column, col0, "get_ner")

    new_description = "'"+column+"_ner_val' column gives the value of the name entities recognized (NER) in the "+column+" column. e.g. 'UNITED STATES', 'MOHAMED BAK'."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_ner")
        return table, enum, description, dot
    if len(col0) != 0:
        result_df = pd.concat(table.apply(lambda row: ner(row), axis=1).tolist())
    table[column+'_ner_val'] = ""
    # Concatenate the original DataFrame and the result
    table = pd.concat([table, result_df[column+'_ner_val']])
    enum.append(column+'_ner_val')
    description += " "+"'"+column+"_ner_val' column gives the value of the name entities recognized (NER) in the "+column+" column. e.g. 'UNITED STATES', 'MOHAMED BAK'."

    # update graph
    # dot.node(column+"_ner_type")
    dot.node(column+"_ner_val")
    # dot.edge(column, column+"_ner_type", "get_ner")
    dot.edge(column, column+"_ner_val", "get_ner")

    return table, enum, description, dot

def get_summary(table, column, enum, description, verbose, dot):
    def summary(document):
        # Create a BERT Extractive Summarizer
        bertsum_model = Summarizer()
        # Summarize the legal document
        if isinstance(document, list):
            summary = [bertsum_model(doc) for doc in document]
        else:
            summary = bertsum_model(document)
        return summary
    assert column == "story_orig"
    new_description = "'"+column+"_summary' column provides summaries of the '"+column+"' column;"
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_summary")
        return table, enum, description, dot
    
    if os.path.exists("data/story.csv"):
        df = pd.read_csv('data/story.csv')
        table[column+'_summary'] = df['summary']
    else:
        table[column+'_summary'] = table[column].apply(summary)
    enum.append(column+"_summary")
    description += " " + "'"+column+"_summary' column provides summaries of the '"+column+"' column;"

    dot.node(column+"_summary")
    dot.edge(column, column+"_summary", "get_summary")

    return table, enum, description, dot

def get_fk(table, column, enum, description):
    def fk(document):
        return textstat.flesch_kincaid_grade(document)

    table[column+'_fk'] = table[column].apply(fk)
    enum.append(column+"_fk")
    description += " " + "'"+column+"_fk' column calculates the Flesch-Kincaid (F-K) readability score of the '"+column+"' column, with a higher score representing lower readability;"
    return table, enum, description

def get_ttr(table, column, enum, description):
    def ttr(document):
        tokens = re.findall(r'\b\w+\b', document.lower())
        types = set(tokens)
        ttr = len(types) / len(tokens) if tokens else 0
        return ttr

    table[column+'_ttr'] = table[column].apply(ttr)
    enum.append(column+"_ttr")
    description += " " + "'"+column+"_ttr' column calculates the Type-Token Ratio (TTR) of the '"+column+"' column, with a higher score representing greater lexical diversity;"
    return table, enum, description

def get_similarity(table, column, enum, description, primary_id, secondary_id):
    def similarity(doc1):
        # Locate the document in the table using doc_id and para_id
        doc2 = table.loc[(table['id'] == int(primary_id)) & (table[column+'id'] == int(secondary_id)), column].values[0]
        
        # If doc2 is not found or empty, return 0
        if not doc2:
            return 0

        vectorizer = TfidfVectorizer()

        # Vectorize the documents
        tfidf_matrix = vectorizer.fit_transform([doc1, doc2])

        # Calculate cosine similarity
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return sim[0][0]

    # Apply the similarity function to each row in the specified column
    table[column + '_similarity_' + str(primary_id) + '_' + str(secondary_id)] = table[column].apply(similarity)

    # Update the enum and description
    enum.append(column + '_similarity_' + str(primary_id) + '_' + str(secondary_id))
    description += f" '{column}_similarity_{primary_id}_{secondary_id}' column calculates the cosine similarity between the '{column}' column of all the documents and the reference document specified by id={primary_id} and {column}_id={secondary_id};"

    return table, enum, description

def get_keyword(table, column, enum, description, verbose, dot):
    def lda(document):
        if document == "":
            return ""
        # Preprocessing the document
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in word_tokenize(document.lower()) if word.isalpha() and word not in stop_words]
        
        # Creating a dictionary and corpus for LDA
        dictionary = corpora.Dictionary([tokens])
        corpus = [dictionary.doc2bow(tokens)]

        # Applying LDA model
        lda_model = models.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=10)

        # Extracting keywords from the topic
        topic_words = lda_model.show_topic(0, topn=5)
        keywords = [word for word, _ in topic_words]
        return ', '.join(keywords)
    
    new_description = " '" + column + "_keyword' column provides LDA-based keyword identification of the '" + column + "' column;"
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_keyword")
        return table, enum, description

    table[column+'_keyword'] = table[column].apply(lda)
    enum.append(column+"_keyword")
    description += " '" + column + "_keyword' column provides LDA-based keyword identification of the '" + column + "' column;"

    dot.node(column+"_keyword")
    dot.edge(column, column+"_keyword", "get_keyword")

    return table, enum, description, dot

def get_sentiment(table, column, enum, description, verbose, dot):
    def sentiment(document):
        blob = TextBlob(document)
        polarity = blob.sentiment.polarity
        
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'
    new_description = "'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'pos', 'neg', or 'other'; "
    # assert column == 'sentence_no'
    # new_description = "'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'pos', 'neg', or 'neu'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_sentiment")
        return table, enum, description, dot
    if os.path.exists("data/stance.csv"):
        with open("data/stance.csv", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        df = pd.DataFrame(data[1:], columns=data[0])
        table[column+'_sentiment'] = df['Sentiment']
    else:
        table[column+'_sentiment'] = table[column].apply(sentiment)
    if os.path.exists("data/attackable.csv"):
        with open("data/attackable.csv", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        df = pd.DataFrame(data[1:], columns=data[0])
        table[column+'_sentiment'] = df['sentiment']
    else:
        table[column+'_sentiment'] = table[column].apply(sentiment)
    enum.append(column+"_sentiment")
    description += " "+"'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'pos', 'neg', or 'neu'; "
    # description += " "+"'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'Positive', 'Negative', or 'Neutral'; "
    description += " "+"'"+column+"_sentiment' column is the sentiment of the content of the '" + column +"' column. IMPORTANT: sentiment values of '" +column+"_sentiment' column can only be either 'pos', 'neg', or 'other'; "
    #description += " Correct Example: table[table['"+column+"_sentiment'] == 'Positive']; Incorrect Example: table[table['"+column+"_sentiment'] == 'positive']; "

    dot.node(column+"_sentiment")
    dot.edge(column, column+"_sentiment", "get_sentiment")

    return table, enum, description, dot

def get_stance(table, column, target, enum, description, verbose, dot):   
    assert target == 'Target'
    new_description = "'"+column+"_stance' column describes the stance of the content of the '" + column +"' column towards the target topic in the '"+target+"' column. IMPORTANT: stance values of '" +column+"_stance' column can only be either 'AGAINST', 'FAVOR', or 'NONE'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_stance")
        dot.edge(target, col, "get_stance")
        return table, enum, description, dot
    if os.path.exists("data/stance.csv"):
        with open("data/stance.csv", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        df = pd.DataFrame(data[1:], columns=data[0])
        table[column+'_stance'] = df['Stance']
    else:
        table[column+'_stance'] = "Undefined"
    enum.append(column+"_stance")
    description += " "+"'"+column+"_stance' column describes the stance of the content of the '" + column +"' column towards the target topic in the '"+target+"' column. IMPORTANT: stance values of '" +column+"_stance' column can only be either 'AGAINST', 'FAVOR', or 'NONE'; "

    dot.node(column+"_stance")
    dot.edge(column, column+"_stance", "get_stance")
    dot.edge(target, column+"_stance", "get_stance")

    return table, enum, description, dot

def get_dog_whistle(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_dog_whistle' column is the dog whistle term extracted from the '" + column +"' column."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_dog_whistle")
        return table, enum, description, dot
    if os.path.exists("data/dogwhistle.tsv"):
        df = pd.read_csv("data/dogwhistle.tsv", on_bad_lines='skip', delimiter='\t')
        table[column+'_dog_whistle'] = df['Dogwhistle']
    else:
        table[column+'_dog_whistle'] = "Undefined"
    enum.append(column+"_dog_whistle")
    description += " "+"'"+column+"_dog_whistle' column is the dog whistle term extracted from the '" + column +"' column."

    dot.node(column+"_dog_whistle")
    dot.edge(column, column+"_dog_whistle", "get_dog_whistle")

    return table, enum, description, dot

def get_dog_whistle_persona_ingroup(table, column, enum, description, verbose, dot):
    assert column == 'Linguistic Context_dog_whistle'
    new_description = "'"+column+"_persona_ingroup' contains the persona/in-group of the dog whistle term in the '" + column +"' column."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_dog_whistle_persona_ingroup")
        return table, enum, description, dot
    if os.path.exists("data/dogwhistle.tsv"):
        df = pd.read_csv("data/dogwhistle.tsv", on_bad_lines='skip', delimiter='\t')
        table[column+'_persona_ingroup'] = df['Persona/In-Group']
    else:
        table[column+'_persona_ingroup'] = "Undefined"
    enum.append(column+"_persona_ingroup")
    description += " "+"'"+column+"_persona_ingroup' contains the persona/in-group of the dog whistle term in the '" + column +"' column."
    # description += "IMPORTANT: the persona/in-group value can only be one of 'transphobic', 'white supremacist', 'antisemitic', 'racist', 'anti-Latino', 'climate change denier', 'religious', 'conservative', 'Islamophobic', 'anti-vax', 'anti-Asian', 'anti-liberal', 'homophobic', 'anti-LGBTQ', 'liberal', 'misogynistic', 'xenophobic', or 'anti-GMO'; "

    dot.node(column+"_persona_ingroup")
    dot.edge(column, column+"_persona_ingroup", "get_dog_whistle_persona_ingroup")

    return table, enum, description, dot

def get_dog_whistle_type(table, column, enum, description, verbose, dot):
    assert column == 'Linguistic Context_dog_whistle'
    new_description = "'"+column+"_type' contains the type of the dog whistle term in the '" + column +"' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_dog_whistle_type")
        return table, enum, description, dot
    if os.path.exists("data/dogwhistle.tsv"):
        df = pd.read_csv("data/dogwhistle.tsv", on_bad_lines='skip', delimiter='\t')
        table[column+'_type'] = df['Type']
    else:
        table[column+'_type'] = "Undefined"
    enum.append(column+"_type")
    description += " "+"'"+column+"_type' contains the type of the dog whistle term in the '" + column +"' column. "
    #description += "IMPORTANT: the type value can only be one of 'persona signal (shared culture)', 'persona signal (self-referential)', 'persona signal (symbol)', 'arbitrary target group label', 'concept (policy)', 'stereotype-based target group label', 'humor/mockery/sarcasm', 'concept (values)', 'representative (Bogeyman)', 'concept (other)', 'phonetic-based target group label', 'stereotype-based descriptor', 'persona signal (in-group label)'; "

    dot.node(column+"_type")
    dot.edge(column, column+"_type", "get_dog_whistle_type")

    return table, enum, description, dot

def get_positive_reframing(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_pr' contains the positive reframing version of the '" + column +"' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_positive_reframing")
        return table, enum, description, dot
    if os.path.exists("data/positive-reframing.csv"):
        df = pd.read_csv('data/positive-reframing.csv')
        table[column+'_pr'] = df['positive_reframing']
    else:
        table[column+'_pr'] = "Undefined"
    enum.append(column+"_pr")
    description += " "+"'"+column+"_pr' contains the positive reframing version of the '" + column +"' column. "

    dot.node(column+"_pr")
    dot.edge(column, column+"_pr", "get_positive_reframing")

    return table, enum, description, dot

def get_premise(table, column, type, term, enum, description, verbose, dot):
    assert type == 'type'
    assert term == 'term'

    new_description = "'"+column+"_premise_entail' contains the premises (literal texts) that entail the hypothesis (figurative texts) contained in the '" + column +"' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) == 0:
        if os.path.exists("data/figurative.csv"):
            df = pd.read_csv('data/figurative.csv')
            table[column+'_premise_entail'] = df['premise_e']
        else:
            table[column+'_premise_entail'] = "Undefined"
        enum.append(column+'_premise_entail')
        description += " "+"'"+column+"_premise_entail' contains the premises (literal texts) that entail the hypothesis (figurative texts) contained in the '" + column +"' column. "
        dot.node(column+"_premise_entail")
        dot.edge(column, column+"_premise_entail", "get_premise")
        dot.edge(type, column+"_premise_entail", "get_premise")
        dot.edge(term, column+"_premise_entail", "get_premise")
    else:
        dot.edge(column, col, "get_premise")
        dot.edge(type, col, "get_premise")
        dot.edge(term, col, "get_premise")
    
    new_description = "'"+column+"_premise_contradict' contains the premises (literal texts) that contradict the hypothesis (figurative texts) contained in the '" + column +"' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_premise")
        dot.edge(type, col, "get_premise")
        dot.edge(term, col, "get_premise")
        return table, enum, description, dot
    if os.path.exists("data/figurative.csv"):
        df = pd.read_csv('data/figurative.csv')
        table[column+'_premise_contradict'] = df['premise_c']
    else:
        table[column+'_premise_contradict'] = "Undefined"
    enum.append(column+'_premise_contradict')
    description += " "+"'"+column+"_premise_contradict' contains the premises (literal texts) that contradict the hypothesis (figurative texts) contained in the '" + column +"' column. "

    # dot.node(column+"_premise_entail")
    # dot.edge(column, column+"_premise_entail", "get_premise")
    # dot.edge(type, column+"_premise_entail", "get_premise")
    # dot.edge(term, column+"_premise_entail", "get_premise")
    dot.node(column+"_premise_contradict")
    dot.edge(column, column+"_premise_contradict", "get_premise")
    dot.edge(type, column+"_premise_contradict", "get_premise")
    dot.edge(term, column+"_premise_contradict", "get_premise")

    return table, enum, description, dot

def get_premise_explanation(table, column, hypothesis, type, term, label, enum, description, verbose, dot):
    assert hypothesis == 'hypothesis'
    assert label in ["contradict", "entail"]
    assert label in column
    assert type == 'type'
    assert term == 'term'

    if label == "contradict":
        new_description = "'"+column+"_explanation' contains the explanation of the premises (literal texts) that contradict the hypothesis (figurative texts) contained in the '" + column +"' column. "
        col = check_alias(enum, description, new_description, verbose)
        if len(col) > 0:
            dot.edge(column, col, "get_premise_explanation")
            dot.edge(hypothesis, col, "get_premise_explanation")
            dot.edge(label, col, "get_premise_explanation")
            dot.edge(type, col, "get_premise_explanation")
            dot.edge(term, col, "get_premise_explanation")
            return table, enum, description, dot
        if os.path.exists("data/figurative.csv"):
            df = pd.read_csv('data/figurative.csv')
            table[column+'_explanation'] = df['explanation_c']
        else:
            table[column+'_explanation'] = "Undefined"
        enum.append(column+'_explanation')
        description += " "+"'"+column+"_explanation' contains the explanation of the premises (literal texts) that contradict the hypothesis (figurative texts) contained in the '" + column +"' column. "
    else:
        new_description = "'"+column+"_explanation' contains the explanation of the premises (literal texts) that entail the hypothesis (figurative texts) contained in the '" + column +"' column. "
        col = check_alias(enum, description, new_description, verbose)
        if len(col) > 0:
            dot.edge(column, col, "get_premise_explanation")
            dot.edge(hypothesis, col, "get_premise_explanation")
            dot.edge(label, col, "get_premise_explanation")
            dot.edge(type, col, "get_premise_explanation")
            dot.edge(term, col, "get_premise_explanation")
            return table, enum, description, dot
        if os.path.exists("data/figurative.csv"):
            df = pd.read_csv('data/figurative.csv')
            table[column+'_explanation'] = df['explanation_e']
        else:
            table[column+'_explanation'] = "Undefined"
        enum.append(column+'_explanation')
        description += " "+"'"+column+"_explanation' contains the explanation of the premises (literal texts) that entail the hypothesis (figurative texts) contained in the '" + column +"' column. "

    dot.node(column+"_explanation")
    dot.edge(column, column+"_explanation", "get_premise_explanation")
    dot.edge(hypothesis, column+"_explanation", "get_premise_explanation")
    dot.edge(label, column+"_explanation", "get_premise_explanation")
    dot.edge(type, column+"_explanation", "get_premise_explanation")
    dot.edge(term, column+"_explanation", "get_premise_explanation")

    return table, enum, description, dot

def get_change_opinion(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_change_opinion' contains the whether the post in the '" + column +"' column is persuaded and changed their opinion. IMPORTANT: the '"+column+"_change_opinion' column contains boolean values, where True for posts that changed their opinion, False for posts that do not change their opinion."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_change_opinion")
        return table, enum, description, dot
    if os.path.exists("data/persuasive.jsonlist"):
        df = pd.read_json('data/persuasive.jsonlist', lines=True)
        table[column+'_change_opinion'] = df['delta_label']
    else:
        table[column+'_change_opinion'] = "Undefined"
    enum.append(column+'_change_opinion')
    description += " "+"'"+column+"_change_opinion' contains the whether the post in the '" + column +"' column is persuaded and changed their opinion. IMPORTANT: the '"+column+"_change_opinion' column contains boolean values, where True for posts that changed their opinion, False for posts that do not change their opinion."

    dot.node(column+"_change_opinion")
    dot.edge(column, column+"_change_opinion", "get_change_opinion")

    return table, enum, description, dot

def get_persuasion_effect(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_persuasion_effect' contains the persuasion effects of the post included in the '" + column +"' column. IMPORTANT: the '"+column+"_persuasion_effect' column contains numerical values ranging from 0.0 to 1.0, where 0.0 stands for the least persuasive, and 1.0 stands for the most persuasive."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_persuasion_effect")
        return table, enum, description, dot
    if os.path.exists("data/persuasive-17.csv"):
        df = pd.read_csv('data/persuasive-17.csv')
        table[column+'_persuasion_effect'] = df['persuasion_effect']
    else:
        table[column+'_persuasion_effect'] = "Undefined"
    enum.append(column+"_persuasion_effect")
    description += " "+"'"+column+"_persuasion_effect' contains the persuasion effects of the post included in the '" + column +"' column. IMPORTANT: the '"+column+"_persuasion_effect' column contains numerical values ranging from 0.0 to 1.0, where 0.0 stands for the least persuasive, and 1.0 stands for the most persuasive."

    dot.node(column+"_persuasion_effect")
    dot.edge(column, column+"_persuasion_effect", "get_persuasion_effect")

    return table, enum, description, dot

def get_intent(table, column, enum, description, verbose, dot):
    assert column == 'headline'
    new_description = "'"+column+"_intent' column provides writers' intent for the texts in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_intent")
        return table, enum, description, dot
    if os.path.exists("data/test_annot_all.tsv"):
        df = pd.read_csv("data/test_annot_all.tsv", delimiter='\t')
        table[column+'_intent'] = df['writer_intent']
    else:
        table[column+'_intent'] = "Undefined"
    enum.append(column+"_intent")
    description += " " + "'"+column+"_intent' column provides writers' intent for the texts in the '"+column+"' column'; "

    dot.node(column+"_intent")
    dot.edge(column, column+"_intent", "get_intent")

    return table, enum, description, dot

def get_reader_perception(table, column, enum, description, verbose, dot):
    assert column == 'headline'
    new_description = "'"+column+"_reader_perception' column provides readers' perceptions for the texts in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_reader_perception")
        return table, enum, description, dot
    if os.path.exists("data/test_annot_all.tsv"):
        df = pd.read_csv("data/test_annot_all.tsv", delimiter='\t')
        table[column+'_reader_perception'] = df['effect_on_reader']
    else:
        table[column+'_reader_perception'] = "Undefined"
    enum.append(column+"_reader_perception")
    description += " " + "'"+column+"_reader_perception' column provides readers' perceptions for the texts in the '"+column+"' column'; "

    dot.node(column+"_reader_perception")
    dot.edge(column, column+"_reader_perception", "get_reader_perception")

    return table, enum, description, dot

def get_spread_likelihood(table, column, enum, description, verbose, dot):
    assert column.endswith('_reader_perception')
    new_description = "'"+column+"_spread' column contains the (numerical) likelihood to spread based on the reader perceptions provided in the '"+column+"' column'; IMPORTANT: the '"+column+"_spread' column contains numerical values ranging from 0.0 to 5.0, where 0.0 stands for the least likely to spread, and 5.0 stands for the most likely to spread."
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_spread_likelihood")
        return table, enum, description, dot
    if os.path.exists("data/test_annot_all.tsv"):
        df = pd.read_csv("data/test_annot_all.tsv", delimiter='\t')
        table[column+'_spread'] = df['spread']
    else:
        table[column+'_spread'] = "Undefined"
    enum.append(column+"_spread")
    description += " " + "'"+column+"_spread' column contains the (numerical) likelihood to spread based on the reader perceptions provided in the '"+column+"' column'; IMPORTANT: the '"+column+"_spread' column contains numerical values ranging from 0.0 to 5.0, where 0.0 stands for the least likely to spread, and 5.0 stands for the most likely to spread."

    dot.node(column+"_spread")
    dot.edge(column, column+"_spread", "get_spread_likelihood")

    return table, enum, description, dot

def get_reader_action(table, column, enum, description, verbose, dot):
    assert column.endswith('_intent')
    new_description = "'"+column+"_reader_action' column contains the inferred readers' actions based on the writers' intent provided in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_reader_action")
        return table, enum, description, dot
    if os.path.exists("data/test_annot_all.tsv"):
        df = pd.read_csv("data/test_annot_all.tsv", delimiter='\t')
        table[column+'_reader_action'] = df['reader_action']
    else:
        table[column+'_reader_action'] = "Undefined"
    enum.append(column+"_reader_action")
    description += " " + "'"+column+"_reader_action' column contains the inferred readers' actions based on the writers' intent provided in the '"+column+"' column'; "

    dot.node(column+"_reader_action")
    dot.edge(column, column+"_reader_action", "get_reader_action")
    
    return table, enum, description, dot

def get_dialect(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_dialect' column contains the identified categorical dialect features identified from the sentences in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_dialect")
        return table, enum, description, dot
    if os.path.exists('data/dialect.csv'):
        df = pd.read_csv('data/dialect.csv')
        table[column+'_dialect'] = df['dialect']
    else:
        table[column+'_dialect'] = "Undefined"
    enum.append(column+"_dialect")
    description += " " + "'"+column+"_dialect' column contains the identified categorical dialect features identified from the sentences in the '"+column+"' column'; "

    dot.node(column+"_dialect")
    dot.edge(column, column+"_dialect", "get_dialect")

    return table, enum, description, dot

def get_disclosure(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_disclosure' column contains the disclosure act types of the sentences in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_disclosure")
        return table, enum, description, dot
    if os.path.exists('data/disclosure.csv'):
        df = pd.read_csv('data/disclosure.csv')
        table[column+'_disclosure'] = df['disclosure']
    else:
        table[column+'_disclosure'] = "Undefined"
    enum.append(column+"_disclosure")
    description += " " + "'"+column+"_disclosure' column contains the disclosure act types of the sentences in the '"+column+"' column'; "

    dot.node(column+"_disclosure")
    dot.edge(column, column+"_disclosure", "get_disclosure")

    return table, enum, description, dot

def get_semantic(table, word, word_type, index, sentence1, sentence2, enum, description, verbose, dot):
    assert word == "word"
    assert word_type == "word_type"
    assert index == "index"
    assert sentence1 == "example_1"
    assert sentence2 == "example_2"

    new_description = "'"+word+"_semantic' column contains whether the word in the '"+word+"' column of type in the '"+word_type+" column'  has the same semantic in sentences in the '"+sentence1+"' column and the '"+sentence2+"' column, with indexes in the '"+index+"' column. IMPORTANT: the values in the '"+word+"_semantic' column can either be 'T', meaning that the semantic in the two sentences are the same, or 'F', meaning that the semantic in the two sentences are different. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(word, col, "get_semantic")
        dot.edge(word_type, col, "get_semantic")
        dot.edge(index, col, "get_semantic")
        dot.edge(sentence1, col, "get_semantic")
        dot.edge(sentence2, col, "get_semantic")
        return table, enum, description, dot
    if os.path.exists('data/semantic.csv'):
        df = pd.read_csv('data/semantic.csv')
        table[word+'_semantic'] = df['semantic_consistency']
    else:
        table[word+'_semantic'] = "Undefined"
    enum.append(word+"_semantic")
    description += " " + "'"+word+"_semantic' column contains whether the word in the '"+word+"' column of type in the '"+word_type+" column'  has the same semantic in sentences in the '"+sentence1+"' column and the '"+sentence2+"' column, with indexes in the '"+index+"' column. IMPORTANT: the values in the '"+word+"_semantic' column can either be 'T', meaning that the semantic in the two sentences are the same, or 'F', meaning that the semantic in the two sentences are different. "

    dot.node(word+'_semantic')
    dot.edge(word, word+'_semantic', "get_semantic")
    dot.edge(word_type, word+'_semantic', "get_semantic")
    dot.edge(index, word+'_semantic', "get_semantic")
    dot.edge(sentence1, word+'_semantic', "get_semantic")
    dot.edge(sentence2, word+'_semantic', "get_semantic")

    return table, enum, description, dot

def get_emotional_reaction_level(table, column, column_post, enum, description, verbose, dot):
    assert column == "response_post"
    assert column_post == "seeker_post"
    new_description = "'"+column+"_emotional_reaction' column contains the numerical level of communication strength in terms of emotional reaction for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_emotion_reaction' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_emotional_reaction_levels")
        dot.edge(column_post, col, "get_emotional_reaction_levels")
        return table, enum, description, dot
    if os.path.exists('data/empathy.csv'):
        df = pd.read_csv('data/empathy.csv')
        table[column+'_emotional_reaction'] = df['emotional_reactions_level']
    else:
        table[column+'_emotional_reaction'] = "Undefined"
    enum.append(column+"_emotional_reaction")
    description += " " + "'"+column+"_emotional_reaction' column contains the numerical level of communication strength in terms of emotional reaction for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_emotion_reaction' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "

    dot.node(column+'_emotional_reaction')
    dot.edge(column, column+'_emotional_reaction', "get_emotional_reaction_levels")
    dot.edge(column_post, column+'_emotional_reaction', "get_emotional_reaction_levels")

    return table, enum, description, dot

def get_exploration_level(table, column, column_post, enum, description, verbose, dot):
    assert column == "response_post"
    assert column_post == "seeker_post"
    new_description = "'"+column+"_exploration' column contains the numerical level of communication strength in terms of exploration for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_exploration' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_exploration_level")
        dot.edge(column_post, col, "get_exploration_level")
        return table, enum, description, dot
    if os.path.exists('data/empathy.csv'):
        df = pd.read_csv('data/empathy.csv')
        table[column+'_exploration'] = df['exploration_level']
    else:
        table[column+'_exploration'] = "Undefined"
    enum.append(column+"_exploration")
    description += " " + "'"+column+"_exploration' column contains the numerical level of communication strength in terms of exploration for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_exploration' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "

    dot.node(column+'_exploration')
    dot.edge(column, column+'_exploration', "get_exploration_level")
    dot.edge(column_post, column+'_exploration', "get_exploration_level")

    return table, enum, description, dot

def get_intepretation_level(table, column, column_post, enum, description, verbose, dot):
    assert column == "response_post"
    assert column_post == "seeker_post"
    new_description = "'"+column+"_intepretation' column contains the numerical level of communication strength in terms of intepretation for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_intepretation' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_intepretation_level")
        dot.edge(column_post, col, "get_intepretation_level")
        return table, enum, description, dot
    if os.path.exists('data/empathy.csv'):
        df = pd.read_csv('data/empathy.csv')
        table[column+'_intepretation'] = df['intepretation_level']
    else:
        table[column+'_intepretation'] = "Undefined"
    enum.append(column+"_intepretation")
    description += " " + "'"+column+"_intepretation' column contains the numerical level of communication strength in terms of intepretation for the response post in the '"+column+"' column' towards the sad post in the '"+column_post+"' column. IMPORTANT: the numerical values in the '"+column+"_intepretation' column are integers 0, 1, and 2, with 0 denotes the weakest level of communication, and 2 denotes the strongest level of communication. "

    dot.node(column+'_intepretation')
    dot.edge(column, column+'_intepretation', "get_intepretation_level")
    dot.edge(column_post, column+'_intepretation', "get_intepretation_level")

    return table, enum, description, dot

def get_politeness(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_polite' column contains whether the text in the '"+column+"' column' is polite or not. IMPORTANT: the values in the '"+column+"_polite' column can only be either 'T', meaning that the text is polite, or 'F', meaning that the text is not polite. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_politeness")
        return table, enum, description, dot
    if os.path.exists('data/politeness.csv'):
        df = pd.read_csv('data/politeness.csv')
        table[column+'_polite'] = df['polite']
    else:
        table[column+'_polite'] = "Undefined"
    enum.append(column+"_polite")
    description += " " + "'"+column+"_polite' column contains whether the text in the '"+column+"' column' is polite or not. IMPORTANT: the values in the '"+column+"_polite' column can only be either 'T', meaning that the text is polite, or 'F', meaning that the text is not polite. "

    dot.node(column+'_polite')
    dot.edge(column, column+'_polite', "get_politeness")

    return table, enum, description, dot

def get_humor(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_humor' column contains whether the text in the '"+column+"' column' is funny or not. IMPORTANT: the values in the '"+column+"_humor' column can only be either 'T', meaning that the text is funny, or 'F', meaning that the text is not funny. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_humor")
        return table, enum, description, dot
    if os.path.exists('data/humor.csv'):
        df = pd.read_csv('data/humor.csv')
        table[column+'_humor'] = df['humor']
    else:
        table[column+'_humor'] = "Undefined"
    enum.append(column+"_humor")
    description += " " + "'"+column+"_humor' column contains whether the jokes in the '"+column+"' column' is funny or not. IMPORTANT: the values in the '"+column+"_humor' column can only be either 'T', meaning that the joke is funny, or 'F', meaning that the joke is not funny. "

    dot.node(column+'_humor')
    dot.edge(column, column+'_humor', "get_humor")

    return table, enum, description, dot

def get_toxic(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_toxic' column contains whether the text in the '"+column+"' column' will become toxic in the future or not. IMPORTANT: the values in the '"+column+"_toxic' column can only be either True, meaning that the text will become toxic in the future, or False, meaning that the text will not become toxic in the future. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_toxic")
        return table, enum, description, dot
    if os.path.exists('data/toxic.csv'):
        df = pd.read_csv('data/toxic.csv')
        table[column+'_toxic'] = df['toxic']
    else:
        table[column+'_toxic'] = "Undefined"
    enum.append(column+"_toxic")
    description += " " + "'"+column+"_toxic' column contains whether the text in the '"+column+"' column' will become toxic in the future or not. IMPORTANT: the values in the '"+column+"_toxic' column can only be either True, meaning that the text will become toxic in the future, or False, meaning that the text will not become toxic in the future. "

    dot.node(column+'_toxic')
    dot.edge(column, column+'_toxic', "get_toxic")

    return table, enum, description, dot

def get_trope(table, column, enum, description, verbose, dot):
    assert column == "Quotes"
    new_description = "'"+column+"_trope' column contains which trope type is the character who has the quotes in the '"+column+"' column'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_trope")
        return table, enum, description, dot
    if os.path.exists('data/tropes.csv'):
        df = pd.read_csv('data/tropes.csv')
        table[column+'_trope'] = df['TropesHuman']
    else:
        table[column+'_trope'] = "Undefined"
    enum.append(column+"_trope")
    description += " " + "'"+column+"_trope' column contains which trope type is the character who has the quotes in the '"+column+"' column'. "

    dot.node(column+'_trope')
    dot.edge(column, column+'_trope', "get_trope")

    return table, enum, description, dot

def get_event_argument(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_event_argument' column contains the event arguments extracted from the text in the '"+column+"' column'; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_event_argument")
        return table, enum, description, dot
    if os.path.exists('data/event_argument.csv'):
        df = pd.read_csv('data/event_argument.csv')
        table[column+'_event_argument'] = df['event_argument']
    else:
        table[column+'_event_argument'] = "Undefined"
    enum.append(column+"_event_argument")
    description += " " + "'"+column+"_event_argument' column contains the event arguments extracted from the text in the '"+column+"' column'; "

    dot.node(column+'_event_argument')
    dot.edge(column, column+'_event_argument', "get_event_argument")

    return table, enum, description, dot

def get_ideology_doc(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_ideology_doc' column contains the ideology of the document whose link is provided in the '"+column+"' column'; IMPORTANT: the categorical ideology values in the '"+column+"_ideology_doc' column can only be one of 0 (meaning left), 1 (meaning neutral), or 2 (meaning right). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_ideology_doc")
        return table, enum, description, dot
    if os.path.exists('data/ideology_document.tsv'):
        df = pd.read_csv("data/ideology_document.tsv", delimiter='\t')
        table[column+'_ideology_doc'] = df['bias']
    else:
        table[column+'_ideology_doc'] = "Undefined"
    enum.append(column+"_ideology_doc")
    description += " " + "'"+column+"_ideology_doc' column contains the ideology of the document whose link is provided in the '"+column+"' column'; IMPORTANT: the categorical ideology values in the '"+column+"_ideology_doc' column can only be one of 0 (meaning left), 1 (meaning neutral), or 2 (meaning right). "

    dot.node(column+'_ideology_doc')
    dot.edge(column, column+'_ideology_doc', "get_ideology_doc")

    return table, enum, description, dot

def get_ideology_sent(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_ideology_sent' column contains the ideology of the sentence in the '"+column+"' column'; IMPORTANT: the categorical ideology values in the '"+column+"_ideology_sent' column can only be one of 'Conservative', 'Liberal', or 'Neutral'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_ideology_sent")
        return table, enum, description, dot
    if os.path.exists('data/ibc.csv'):
        df = pd.read_csv("data/ibc.csv")
        table[column+'_ideology_sent'] = df['leaning']
    else:
        table[column+'_ideology_sent'] = "Undefined"
    enum.append(column+"_ideology_sent")
    description += " " + "'"+column+"_ideology_sent' column contains the ideology of the sentence in the '"+column+"' column'; IMPORTANT: the categorical ideology values in the '"+column+"_ideology_sent' column can only be one of 'Conservative', 'Liberal', or 'Neutral'. "

    dot.node(column+'_ideology_sent')
    dot.edge(column, column+'_ideology_sent', "get_ideology_sent")

    return table, enum, description, dot

def story_gen(table, column, enum, description, verbose, dot):
    assert column.endswith('_summary')
    new_description = "'"+column+"_new_story' column contains the generated stories based on the summary provided in the '" + column + "' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "story_gen")
        return table, enum, description, dot
    if os.path.exists("data/story.csv"):
        df = pd.read_csv('data/story.csv')
        table[column+'_new_story'] = df['story_gen']
    else:
        table[column+'_new_story'] = "Undefined"
    enum.append(column+"_new_story")
    description += " " + "'"+column+"_new_story' column contains the generated stories based on the summary provided in the '" + column + "' column. "

    dot.node(column+'_new_story')
    dot.edge(column, column+'_new_story', "story_gen")

    return table, enum, description, dot

def get_event(table, column, enum, description, verbose, dot):
    assert column == 'sent'
    new_description = "'"+column+"_event_prob' column contains the probability of the text in the '"+column+"' column containing new events. IMPORTANT: the values in the '"+column+"_event_prob' column are floating point values ranging from 0.0 (the least likely to include events) to 1.0 (the most likely to include events). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_event")
        return table, enum, description, dot
    if os.path.exists('data/events.csv'):
        df = pd.read_csv('data/events.csv')
        table[column+'_event_prob'] = df['eventOrNot']
    else:
        table[column+'_event_prob'] = "Undefined"
    enum.append(column+"_event_prob")
    description += " " + "'"+column+"_event_prob' column contains the probability of the text in the '"+column+"' column containing new events. IMPORTANT: the values in the '"+column+"_event_prob' column are floating point values ranging from 0.0 (the least likely to include events) to 1.0 (the most likely to include events). "

    dot.node(column+"_event_prob")
    dot.edge(column, column+"_event_prob", "get_event")

    return table, enum, description, dot

def get_event_major(table, column, event, enum, description, verbose, dot):
    assert event.endswith('_event_prob')
    assert column == 'sent'
    new_description = "'"+column+"_event_major_prob' column contains the probability of events in the text in the '"+column+"' column being major events. IMPORTANT: the values in the '"+column+"_event_major_prob' column are floating point values ranging from 0.0 (the least likely to include events) to the value in the '"+event+"' column (the most likely to include events). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_event_major")
        dot.edge(event, col, "get_event_major")
        return table, enum, description, dot
    if os.path.exists('data/events.csv'):
        df = pd.read_csv('data/events.csv')
        table[column+'_event_major_prob'] = df['majorBin']
    else:
        table[column+'_event_major_prob'] = "Undefined"
    enum.append(column+"_event_major_prob")
    description += " " + "'"+column+"_event_major_prob' column contains the probability of events in the text in the '"+column+"' column being major events. IMPORTANT: the values in the '"+column+"_event_major_prob' column are floating point values ranging from 0.0 (the least likely to include events) to the value in the '"+event+"' column (the most likely to include events). "

    dot.node(column+"_event_major_prob")
    dot.edge(column, column+"_event_major_prob", "get_event_major")
    dot.edge(event, column+"_event_major_prob", "get_event_major")

    return table, enum, description, dot

def get_event_expected(table, column, event, enum, description, verbose, dot):
    assert event.endswith('_event_prob')
    assert column == 'sent'
    new_description = "'"+column+"_event_expected_prob' column contains the probability of events in the text in the '"+column+"' column being events as expected. IMPORTANT: the values in the '"+column+"_event_expected_prob' column are floating point values ranging from 0.0 (the least likely to include events) to the value in the '"+event+"' column (the most likely to include events). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_event_expected")
        dot.edge(event, col, "get_event_expected")
        return table, enum, description, dot
    if os.path.exists('data/events.csv'):
        df = pd.read_csv('data/events.csv')
        table[column+'_event_expected_prob'] = df['expectedBin']
    else:
        table[column+'_event_expected_prob'] = "Undefined"
    enum.append(column+"_event_expected_prob")
    description += " " + "'"+column+"_event_expected_prob' column contains the probability of events in the text in the '"+column+"' column being events as expected. IMPORTANT: the values in the '"+column+"_event_expected_prob' column are floating point values ranging from 0.0 (the least likely to include events) to the value in the '"+event+"' column (the most likely to include events). "

    dot.node(column+"_event_expected_prob")
    dot.edge(column, column+"_event_expected_prob", "get_event_expected")
    dot.edge(event, column+"_event_expected_prob", "get_event_expected")

    return table, enum, description, dot

def get_story_type(table, column, storyIx, sentIx, event, event_major, event_expected, enum, description, verbose, dot):
    assert column == 'sent'
    assert storyIx == 'storyIx'
    assert sentIx == 'sentIx'
    assert event.endswith('_event_prob')
    assert event_major.endswith('_event_major_prob')
    assert event_expected.endswith('_event_expected_prob')

    new_description = "'"+column+"_story_type' column contains the type of story in the text in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_story_type' column are categorical values being one of 'imagined', 'recalled', or 'retold'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_story_type")
        dot.edge(storyIx, col, "get_story_type")
        dot.edge(sentIx, col, "get_story_type")
        dot.edge(event, col, "get_story_type")
        dot.edge(event_major, col, "get_story_type")
        dot.edge(event_expected, col, "get_story_type")
        return table, enum, description, dot
    if os.path.exists('data/events.csv'):
        df = pd.read_csv('data/events.csv')
        table[column+'_story_type'] = df['memType']
    else:
        table[column+'_story_type'] = "Undefined"
    enum.append(column+"_story_type")
    description += " " + "'"+column+"_story_type' column contains the type of story in the text in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_story_type' column are categorical values being one of 'imagined', 'recalled', or 'retold'. "

    dot.node(column+"_story_type")
    dot.edge(column, column+"_story_type", "get_story_type")
    dot.edge(storyIx, column+"_story_type", "get_story_type")
    dot.edge(sentIx, column+"_story_type", "get_story_type")
    dot.edge(event, column+"_story_type", "get_story_type")
    dot.edge(event_major, column+"_story_type", "get_story_type")
    dot.edge(event_expected, column+"_story_type", "get_story_type")

    return table, enum, description, dot

def get_strategy(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_strategy' column contains the emotional support strategy to be used in response to the seekers' need in the text in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_strategy' column are categorical values of strategy types being either 'Question', 'Restatement or Paraphrasing', 'Reflection of feelings', 'Self-disclosure', 'Affirmation and Reassurance', 'Providing Suggestions', 'Information', and 'Others'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_strategy")
        return table, enum, description, dot
    if os.path.exists('data/emotional_support.csv'):
        df = pd.read_csv('data/emotional_support.csv')
        table[column+'_strategy'] = df['strategy']
    else:
        table[column+'_strategy'] = "Undefined"
    enum.append(column+"_strategy")
    description += " " + "'"+column+"_strategy' column contains the emotional support strategy to be used in response to the seekers' need in the text in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_strategy' column are categorical values of strategy types being either 'Question', 'Restatement or Paraphrasing', 'Reflection of feelings', 'Self-disclosure', 'Affirmation and Reassurance', 'Providing Suggestions', 'Information', or 'Others'. "

    dot.node(column+"_strategy")
    dot.edge(column, column+"_strategy", "get_strategy")

    return table, enum, description, dot

def get_supporter_response(table, column, strategy, enum, description, verbose, dot):
    assert column == "seeker"
    assert strategy.endswith('strategy')
    new_description = "'"+column+"_supporter_reponse' column contains the emotional support response to the seekers' need in the text in the '"+column+"' column; "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_supporter_reponse")
        dot.edge(strategy, col, "get_supporter_reponse")
        return table, enum, description, dot
    if os.path.exists('data/emotional_support.csv'):
        df = pd.read_csv('data/emotional_support.csv')
        table[column+'_supporter_reponse'] = df['supporter']
    else:
        table[column+'_supporter_reponse'] = "Undefined"
    enum.append(column+"_supporter_reponse")
    description += " " + "'"+column+"_supporter_reponse' column contains the emotional support response to the seekers' need in the text in the '"+column+"' column; "

    dot.node(column+"_supporter_reponse")
    dot.edge(column, column+"_supporter_reponse", "get_supporter_reponse")
    dot.edge(strategy, column+"_supporter_reponse", "get_supporter_reponse")

    return table, enum, description, dot

def get_smile(table, column, enum, description, verbose, dot):
    assert column == 'id'
    new_description = "'"+column+"_smile' column contains whether the person smiled (True) in the video in the '"+column+"' column or not (False). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_smile")
        return table, enum, description, dot
    if os.path.exists('data/deception.csv'):
        df = pd.read_csv('data/deception.csv')
        table[column+'_smile'] = df['Smile']
    else:
        table[column+'_smile'] = "Undefined"
    enum.append(column+"_smile")
    description += " " + "'"+column+"_smile' column contains whether the person smiled (True) in the video in the '"+column+"' column or not (False). "

    dot.node(column+"_smile")
    dot.edge(column, column+"_smile", "get_smile")

    return table, enum, description, dot

def get_scowl(table, column, enum, description, verbose, dot):
    assert column == 'id'
    new_description = "'"+column+"_scowl' column contains whether the person scowled (True) in the video in the '"+column+"' column or not (False). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_scowl")
        return table, enum, description, dot
    if os.path.exists('data/deception.csv'):
        df = pd.read_csv('data/deception.csv')
        table[column+'_scowl'] = df['Scowl']
    else:
        table[column+'_scowl'] = "Undefined"
    enum.append(column+"_scowl")
    description += " " + "'"+column+"_scowl' column contains whether the person scowled (True) in the video in the '"+column+"' column or not (False). "

    dot.node(column+"_scowl")
    dot.edge(column, column+"_scowl", "get_scowl")

    return table, enum, description, dot

def get_deception(table, column, smile, scowl, enum, description, verbose, dot):
    assert column == 'id'
    assert smile.endswith('smile')
    assert scowl.endswith('scowl')
    new_description = "'"+column+"_deception' column contains whether the person deceived in the video in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_deception' column are categorical values being either 'deceptive' or 'truthful'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_deception")
        dot.edge(smile, col, "get_deception")
        dot.edge(scowl, col, "get_deception")
        return table, enum, description, dot
    if os.path.exists('data/deception.csv'):
        df = pd.read_csv('data/deception.csv')
        table[column+'_deception'] = df['class']
    else:
        table[column+'_deception'] = "Undefined"
    enum.append(column+"_deception")
    description += " " + "'"+column+"_deception' column contains whether the person deceived in the video in the '"+column+"' column. IMPORTANT: the values in the '"+column+"_deception' column are categorical values being either 'deceptive', meaning that the person deceived, or 'truthful', meaning that the person did not deceive. "

    dot.node(column+"_deception")
    dot.edge(column, column+"_deception", "get_deception")
    dot.edge(smile, column+"_deception", "get_deception")
    dot.edge(scowl, column+"_deception", "get_deception")

    return table, enum, description, dot

def get_relationship(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_relationship' column contains the relationship between the two people in the conversation in the '"+column+"' column being either 'social' or 'romance'. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_relationship")
        return table, enum, description, dot
    if os.path.exists('data/relationship.csv'):
        df = pd.read_csv('data/relationship.csv')
        table[column+'_relationship'] = df['relationship-category']
    else:
        table[column+'_relationship'] = "Undefined"
    enum.append(column+"_relationship")
    description += " " + "'"+column+"_relationship' column contains the relationship between the two people in the conversation in the '"+column+"' column being either 'social' or 'romance'. "

    dot.node(column+"_relationship")
    dot.edge(column, column+"_relationship", "get_relationship")

    return table, enum, description, dot

def get_bias_score(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_bias_score' column contains the (numerical) bias score of the word in the '"+column+"' column. "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_bias_score")
        return table, enum, description, dot
    if os.path.exists('data/adjectives_williamsbest.csv'):
        df = pd.read_csv('data/adjectives_williamsbest.csv')
        table[column+'_bias_score'] = df['transformed_score']
    else:
        table[column+'_bias_score'] = "Undefined"
    enum.append(column+"_bias_score")
    description += " " + "'"+column+"_bias_score' column contains the (numerical) bias score of the word in the '"+column+"' column. "

    dot.node(column+"_bias_score")
    dot.edge(column, column+"_bias_score", "get_bias_score")

    return table, enum, description, dot

def get_request_succeed(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_request_succeed' column contains whether the request in the '"+column+"' column succeeded (True) or not (False). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_request_succeed")
        return table, enum, description, dot
    if os.path.exists('data/requests.csv'):
        df = pd.read_csv('data/requests.csv')
        table[column+'_request_succeed'] = df['request_succeed']
    else:
        table[column+'_request_succeed'] = "Undefined"
    enum.append(column+"_request_succeed")
    description += " " + "'"+column+"_request_succeed' column contains whether the request in the '"+column+"' column succeeded (True) or not (False). "

    dot.node(column+"_request_succeed")
    dot.edge(column, column+"_request_succeed", "get_request_succeed")

    return table, enum, description, dot

def get_deep_fake(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_deep_fake' column contains whether the video in the '"+column+"' column is fake (True) or not (False). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_deep_fake")
        return table, enum, description, dot
    if os.path.exists('data/deepfake.csv'):
        df = pd.read_csv('data/deepfake.csv')
        table[column+'_deep_fake'] = df['fake']
    else:
        table[column+'_deep_fake'] = "Undefined"
    enum.append(column+"_deep_fake")
    description += " " + "'"+column+"_deep_fake' column contains whether the video in the '"+column+"' column is fake (True) or not (False). "

    dot.node(column+"_deep_fake")
    dot.edge(column, column+"_deep_fake", "get_deep_fake")

    return table, enum, description, dot

def get_power(table, column, enum, description, verbose, dot):
    new_description = "'"+column+"_power' column contains whether the conversation in the '"+column+"' column is in the position of power (True) or not (False). "
    col = check_alias(enum, description, new_description, verbose)
    if len(col) > 0:
        dot.edge(column, col, "get_power")
        return table, enum, description, dot
    if os.path.exists('data/power.csv'):
        df = pd.read_csv('data/power.csv')
        table[column+'_power'] = df['power']
    else:
        table[column+'_power'] = "Undefined"
    enum.append(column+"_power")
    description += " " + "'"+column+"_power' column contains whether the conversation in the '"+column+"' column is in the position of power (True) or not (False). "

    dot.node(column+"_deep_fake")
    dot.edge(column, column+"_deep_fake", "get_deep_fake")

    return table, enum, description, dot

def schema_gpt_tree(user_query, column_description, description, function_chain, function_list, verbose):
    functions = [  
                    {
                "name": "get_deep_fake",
                "description": 
                ''' 
                This function takes in one of the columns as input, detects whether the video in that column is fake or not, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains videos to classify whether they are fake, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_misinfo",
                "description": "This function takes in one of the columns as input, applies misinformation detection on the content of that column, and generates an additional column labeling the content as 'misinfo' (misinformation detected) or 'real' (no misinformation detected).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to apply misinformation detection. You have to select one column in the 'enum' field to apply misinformation detection based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_hate",
                "description": "This function takes in one of the columns as input, applies (high-level) hate speech detection on the content of that column, and generates an additional column labeling the content as 'implicit_hate', 'explicit_hate', or 'not_hate'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to apply (high-level) hate speech detection. You have to select one column in the 'enum' field to apply (high-level) hate speech detection based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_smile",
                "description": "This function takes in one of the columns containing videos as input, applies smile detection on the person inside the videos in that column, and generates an additional column to include those. IMPORTANT: this function has to be executed at least once before calling 'get_deceptive'. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the video to apply smile detection. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_scowl",
                "description": "This function takes in one of the columns containing videos as input, applies scowl detection on the person inside the videos in that column, and generates an additional column to include those. IMPORTANT: this function has to be executed at least once before calling 'get_deceptive'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the video to apply scowl detection. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_deception",
                "description": "This function takes in one of the columns containing videos, one column containing whether the person in the video smiled or not, and one column containing whether the person in the video scowled or not as input, applies deception detection on the person inside the videos in that column, and generates an additional column to include those. IMPORTANT: this function has to be executed after at least one call of 'get_smile'; this function has to be executed after at least one call of 'get_scowl'. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the video to apply deception detection. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        },
                        "smile": {
                            "type": "string",
                            "description": "The column that contains information about whether the person in the video smiled or not. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        },
                        "scowl": {
                            "type": "string",
                            "description": "The column that contains information about whether the person in the video scowled or not. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column", "smile", "scowl"]
                }
            },
                    {
                "name": "get_supporter_response",
                "description": 
                ''' 
                This function takes in one of the columns of the texts that need emotional support and one column of strategy to be used as input, generates response that provides emotional support, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed after at least one call of 'get_strategy'. 
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains texts that need emotional support, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "strategy": {
                        "type": "string",
                        "description": "the column that contains the type of strategy for emotional support, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "strategy"]
            },
                    {
                "name": "get_summary",
                "description": 
                ''' 
                This function takes in one of the columns as input, summarizes the contents in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed at least once before calling 'story_gen'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to summarize, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_intent",
                "description": 
                ''' 
                This function takes in one of the columns that contain the text to be analyzed as input, retrieve the intent of the writer of text in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed at least once before calling 'get_reader_action'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column of text based on which writers' intents are ANALYZED from, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
                    {
                "name": "story_gen",
                "description": 
                ''' 
                This function takes in one of the columns of story summaries as input, generate a story based on the summaries in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed after at least one call of 'get_summary'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains story summaries, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
                    {
                "name": "get_event",
                "description": 
                ''' 
                This function takes in one of the columns as input, calculates the (numerical) probability that the contents in that column contain new events, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed at least once before calling 'get_event_expected'; this function has to be executed at least once before calling 'get_event_major'; this function has to be executed at least once before calling 'get_story_type'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to calculate the probability of containing new events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_event_major",
                "description": 
                ''' 
                This function takes in one of the columns as input, calculates the (numerical) probability that the contents in that column contain major events, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed after at least one call of 'get_event'; this function has to be executed at least once before calling 'get_story_type'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to calculate the probability of containing new major events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "event": {
                        "type": "string",
                        "description": "the column that contains the probability of containing new events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "event"]
            },
            {
                "name": "get_event_expected",
                "description": 
                ''' 
                This function takes in one of the columns as input, calculates the (numerical) probability that the contents in that column contain events that are as expected, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed after at least one call of 'get_event'; this function has to be executed at least once before calling 'get_story_type'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to calculate the probability of containing new events that are as expected, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "event": {
                        "type": "string",
                        "description": "the column that contains the probability of containing new events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "event"]
            },
            {
                "name": "get_persuasion_effect",
                "description": 
                ''' 
                This function takes in one of the columns as input, calculates the (numerical) persuasion effect score of the contents in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to calculate persuasion effect score, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_bias_score",
                "description": 
                ''' 
                This function takes in one of the columns as input, calculates the (numerical) bias score of the word in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to calculate bias score, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_spread_likelihood",
                "description": 
                ''' 
                This function takes in one of the columns of readers' perceptions as input, calculates the (numerical) spread likelihood based on readers' perceptions in that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query. If there is no column denoting readers' perceptions, this function should not be selected. IMPORTANT: this function has to be executed after at least one call of 'get_reader_perception'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains readers' perceptions to calculate the spread likelihood, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
                    {
                "name": "get_emotional_reaction_level",
                "description": 
                ''' 
                This function takes in one column of original sad post and one column of response post as input, calculates the (numerical) level of communication strength in terms of emotional reaction for the contents in the response post column, and generate an additional column to include the integer level. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
                    "column_post": {
                        "type": "string",
                        "description": "the column that includes the original sad post, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "column": {
                        "type": "string",
                        "description": "the column that includes the reponse, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "column_post"]
            },
            {
                "name": "get_exploration_level",
                "description": 
                ''' 
                This function takes in one column of original sad post and one column of response post as input, calculates the (numerical) level of communication strength in terms of exploration for the contents in the response post column, and generate an additional column to include the integer level. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
                    "column_post": {
                        "type": "string",
                        "description": "the column that includes the original sad post, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "column": {
                        "type": "string",
                        "description": "the column that includes the reponse, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "column_post"]
            },
            {
                "name": "get_intepretation_level",
                "description": 
                ''' 
                This function takes in one column of original sad post and one column of response post as input, calculates the (numerical) level of communication strength in terms of intepretation for the contents in the response post column, and generate an additional column to include the integer level. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
                    "column_post": {
                        "type": "string",
                        "description": "the column that includes the original sad post, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "column": {
                        "type": "string",
                        "description": "the column that includes the reponse, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column", "column_post"]
            },
                    {
                "name": "get_semantic",
                "description": 
                ''' 
                This function takes in a word, the type of the word, two sentences, and the indexes in the sentences as input, classifies whether the word in the two sentences has the same semantic, and generates an additional column that includes 'T' or 'F' accordingly. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
                    "word": {
                        "type": "string",
                        "description": "the column that includes the word to classify semantic, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "word_type": {
                        "type": "string",
                        "description": "the column that includes the type of the word, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "sentence1": {
                        "type": "string",
                        "description": "the column that includes the first sentence to inspect semantics, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "sentence2": {
                        "type": "string",
                        "description": "the column that includes the second sentence to inspect semantics, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "index": {
                        "type": "string",
                        "description": "the column that includes indexes of the word in the two sentences, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["word", "word_type", "sentence1", "sentence2", "index"]
            },
            {
                "name": "get_request_succeed",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the requests in that column succeeded or not, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains requests to classify whether they succeeded, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_power",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the conversation in that column is in the position of power or not, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains conversations to classify whether they are in the position of power, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_change_opinion",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the contents in that column changes opinion, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify whether the content would change their opinion, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_relationship",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies if the conversation happens between social or romance type of relationship, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify the type of relationship of the conversation, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_humor",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the contents in that column is funny, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify whether the content is funny, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_politeness",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the contents in that column is polite, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify whether the content is polite, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_toxic",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies whether the contents in that column will become toxic in the future, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify whether the content will become toxic in the future, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            # {
            #     "name": "get_sentiment",
            #     "description": "This function takes in one of the columns as input, applies sentiment analysis on the content of that column, and generates an additional column labeling the content as 'pos', 'neg', or 'other'. Don't select this if none of the columns matches the user query.",
            #     "parameters": {
            #         "type": "object",
            #         "properties": {
            #             "column": {
            #                 "type": "string",
            #                 "description": "The column to apply sentiment analysis. You have to select one column in the 'enum' field to apply sentiment analysis based on the description: "+description,
            #                 "enum": column_description
            #             }
            #         },
            #         "required": ["column"]
            #     }
            # },
            {
                "name": "get_condition",
                "description": "This function takes in one of the columns as input, checks whether the contents of that column satisfy the conditions provided in the user query, and generates an additional column labeling the content as 'True' or 'False' or 'Undefined'. This function should only be called if all other functions cannot help to support user query. Don't select this if (1) there are other functions that can provide such a condition check or (2) there are no explicit conditions listed in the user query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to check conditions. You have to select one column in the 'enum' field to apply condition check based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
                    {
                "name": "get_stance",
                "description": 
                ''' 
                This function takes in one column of text and one column of target topic as input, extracts the stance in the text column that towards the target topic, and generates a new column to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to identify stance towards the target topic, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "target": {
                        "type": "string",
                        "description": "the column that includes the target topic, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },

                    }
                },
                "required": ["column", "target"]
            },
            {
                "name": "get_ideology_doc",
                "description": "This function takes in one of the columns that contains the links to documents as input, applies document-level ideology classification on that column, and generates an additional column labeling the content as 0 (meaning left), 1 (meaning neutral), or 2 (meaning right).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the links to documents to apply document-level ideology classification. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_ideology_sent",
                "description": "This function takes in one of the columns that contains texts as input, applies sentence-level ideology classification on that column, and generates an additional column labeling the content as 'Conservative', 'Liberal', or 'Neutral'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the texts to apply sentence-level ideology classification. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
                    {
                "name": "get_story_type",
                "description": 
                ''' 
                This function takes in one column of sentence, one column of story index of where the sentence belong, one column of sentence index of that sentence, one column of the probability of the sentence containing new events, one column of probability of the sentence containing major new events, and one column of probabiliy of the sentence containing new events as expected as input, classifies the story type of the sentence into 'imagined', 'recalled', or 'retold', and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed after at least one call of 'get_event'; this function has to be executed after at least one call of 'get_event_major'; this function has to be executed after at least one call of 'get_event_expected'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify story type, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "storyIx": {
                        "type": "string",
                        "description": "the column that contains the story index of the sentence, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "sentIx": {
                        "type": "string",
                        "description": "the column that contains the sentence index of the sentence, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "event": {
                        "type": "string",
                        "description": "the column that contains the probability of the sentence containing new events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "event_major": {
                        "type": "string",
                        "description": "the column that contains the probability of the sentence containing new major events, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "event_expected": {
                        "type": "string",
                        "description": "the column that contains the probability of the sentence containing new events that are expected, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    }
                },
                "required": ["column", "storyIx", "sentIx", "event", "event_major", "event_expected"]
            },
            {
                "name": "get_dialect",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies the dialect features identified from the content of that column, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify the dialect features, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_disclosure",
                "description": 
                ''' 
                This function takes in one of the columns as input, classifies the content of that column into different disclosure acts, and generate an additional column to include those. Don't select this if none of the columns matches the user query.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to classify the disclosure acts, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
   
            # {
            #     "name": "get_emotion",
            #     "description": "This function takes in one of the columns as input, applies emotion classification on the content of that column, and generates an additional column labeling the content as 'anticipation', 'anger', 'fear', 'sadness', 'joy', 'trust', or 'disgust'. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed at least once before calling 'get_trigger'.",
            #     "parameters": {
            #         "type": "object",
            #         "properties": {
            #             "column": {
            #                 "type": "string",
            #                 "description": "The column to apply emotion detection. You have to select one column in the 'enum' field to apply emotion classification based on the description: "+description,
            #                 "enum": column_description
            #             }
            #         },
            #         "required": ["column"]
            #     }
            # },
            {
                "name": "get_emotion",
                "description": "This function takes in one of the columns as input, applies emotion classification on the content of that column, and generates an additional column labeling the content as 'sadness', 'joy', 'love', 'anger', 'fear', or 'surprise'. Don't select this if none of the columns matches the user query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to apply emotion detection. You have to select one column in the 'enum' field to apply emotion classification based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_trope",
                "description": "This function takes in one of the columns that contains the quotes of a character as input, applies trope classification based on the content of the quotes, and generates an additional column to include those.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column that contains the quotes of a character. You have to select one column in the 'enum' field based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_hate_class",
                "description": "This function takes in one of the columns as input, applies (fine-grained) implicit hate speech classification on the content of that column, and generates an additional column labeling the content as 'white_grievance', 'incitement', 'inferiority', 'irony', 'stereotypical', 'threatening', or 'other'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to apply (fine-grained) implicit hate speech classification. You have to select one column in the 'enum' field to apply (fine-grained) implicit hate speech classification based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
                "name": "get_dog_whistle_persona_ingroup",
                "description": 
                ''' 
                This function takes in one of the columns of dog whistle terms, obtain the target persona/in-group of that dog whistle term, and generate an additional column to include those. IMPORTANT: this function has to be executed after at least one call of 'get_dog_whistle'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column of dog whistle terms to obtain the target persona/in-group, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_dog_whistle_type",
                "description": 
                ''' 
                This function takes in one of the columns of dog whistle terms, obtain the type of that dog whistle term, and generate an additional column to include those. IMPORTANT: this function has to be executed after at least one call of 'get_dog_whistle'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column of dog whistle terms to obtain the type, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_strategy",
                "description": 
                ''' 
                This function takes in one of the columns of the texts that need emotional support as input, classifies which type of emotional support strategy is needed, and generate an additional column to include those. Don't select this if none of the columns matches the user query. IMPORTANT: this function has to be executed at least once before calling 'get_supporter_response'. 
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains texts that need emotional support, you have to select one in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
                    {
                "name": "get_event_argument",
                "description": 
                ''' 
                This function takes in one of the columns as input, get the event arguments recognized in that column, and generate additional rows and columns to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to apply event argument extraction, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,

                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_ner",
                "description": 
                ''' 
                This function takes in one of the columns as input, get the name entities recognized in that column, and generate additional rows and columns to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to apply NER analysis, you have to select one column in the 'enum' field to apply NER analysis based on the description: "+description,
                        "enum": column_description,

                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_keyword",
                "description": 
                ''' 
                This function takes in one of the columns as input, get the top 5 keywords recognized in that column, and generate an additional column to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to apply keyword recognition, you have to select one column in the 'enum' field to apply keyword recognition based on the description: "+description,
                        "enum": column_description,

                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_trigger",
                "description": 
                ''' 
                This function takes in one column of text and one column of emotion class as input, extracts the trigger in the text column that triggers a specific emotion in the emotion class column, and generates a new column to include those. IMPORTANT: this function has to be executed after at least one call of 'get_emotion'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to extract triggering sentence for a specific emotion, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "emotion": {
                        "type": "string",
                        "description": "the column that describes emotion class, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },

                    }
                },
                "required": ["column", "emotion"]
            },
            {
                "name": "get_dog_whistle",
                "description": 
                ''' 
                This function takes in one of the columns as input, extract the dog whistle term in that column, and generate an additional column to include those. IMPORTANT: this function has to be executed at least once before calling 'get_dog_whistle_type', this function has to be executed at least once before calling 'get_dog_whistle_persona_ingroup'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column to extract dog whistle term, you have to select one in the 'enum' field to summarize based on the description: "+description,
                        "enum": column_description,
                    }
                    }
                },
                "required": ["column"]
            },
        {
                "name": "get_hate_target",
                "description": "This function takes in one of the columns as input, applies implicit hate speech target identification on the content of that column, and generates an additional column of free text labeling the target identified from the content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "The column to apply implicit hate speech target identification. You have to select one column in the 'enum' field to apply implicit hate speech target identification based on the description: "+description,
                            "enum": column_description
                        }
                    },
                    "required": ["column"]
                }
            },
            {
            "name": "get_hate_implied",
            "description": "This function takes in one of the columns as input, applies implicit hate speech implied statement extraction on the content of that column, and generates an additional column of free text labeling the implied statement extracted from the content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply implicit hate speech implied statement extraction. You have to select one column in the 'enum' field to apply implicit hate speech implied statement extraction based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
            },
            {
            "name": "get_positive_reframing",
            "description": "This function takes in one of the columns as input, extract the positive aspects of the content of that column and transforms it into a positive reframing version, and generates an additional column of positive reframing version of the content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply positive reframing. You have to select one column in the 'enum' field to apply positive reframing based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
            },
            {
                "name": "get_premise",
                "description": 
                ''' 
                This function takes in one column of figurative text, one column of figurative type, and one column of figurative term as input, extracts the literal text, i.e., the premise, of the figurative text column, and generates a new column to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column of figurative texts to extract premises from, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "type": {
                        "type": "string",
                        "description": "the column that contains the figurative types of the figurative texts, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "term": {
                        "type": "string",
                        "description": "the column that contains the figurative terms of the figurative texts, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    }
                },
                "required": ["column", "type", "term"]
            },
            {
                "name": "get_premise_explanation",
                "description": 
                ''' 
                This function takes in one column of premise of figurative text, one column of the original figurative text, one column of figurative type, one column of figurative term as input, and one parameter labelling whether the premises entail or contract original figurative texts as input, extracts the explanations of literal texts, i.e., the premises, of the figurative text column, and generates a new column to include those.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column of premises of figurative texts to extract explanation from, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "hypothesis": {
                        "type": "string",
                        "description": "the column of original figurative texts, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "type": {
                        "type": "string",
                        "description": "the column that contains the figurative types of the figurative texts, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "term": {
                        "type": "string",
                        "description": "the column that contains the figurative terms of the figurative texts, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,
                    },
                    "label": {
                        "type": "string",
                        "description": "parameter defining whether the explanation is retrieved from premises that entail or contraduct figurative texts, you have to select one value in the 'enum' field.",
                        "enum": ["entail", "contradict"],
                    },
                    }
                },
                "required": ["column", "hypothesis", "type", "term", "label"]
            },
            {
                "name": "get_reader_action",
                "description": 
                ''' 
                This function takes in one of the columns that contains writers' intent as input, get the reader action inferred from the writers' intent of that column, and generate an additional column to include those. IMPORTANT: this function has to be executed after at least one call of 'get_intent'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains writers' intent to infer readers' action from, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,

                    }
                    }
                },
                "required": ["column"]
            },
            {
                "name": "get_reader_perception",
                "description": 
                ''' 
                This function takes in one of the columns of text as input, infers readers' perceptions of text in that column, and generates an additional column to include those. IMPORTANT: this function has to be executed at least once before calling 'get_spread_likelihood'.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {"column": {
                        "type": "string",
                        "description": "the column that contains text to infer readers' perceptions from, you have to select one column in the 'enum' field based on the description: "+description,
                        "enum": column_description,

                    }
                    }
                },
                "required": ["column"]
            },
    {
            "name": "para_sep",
            "description": "This function takes in one of the columns as input, split the text according to paragraphs, and generates an additional rows and columns to store the list of paragraphs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply paragraph split. You have to select one column in the 'enum' field to apply paragraph-level split based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
        },
        {
            "name": "pdf_to_text",
            "description": 
            ''' 
            This function takes in one of the columns as input, transforms the pdf in that column into plain text, and generate an additional column to store the plain text. Don't select this if none of the columns match the user query.
            ''',
            "parameters": {
                "type": "object",
                "properties": {"column": {
                    "type": "string",
                    "description": "the column to apply pdf to text transformation, you have to select one column in the 'enum' field to apply pdf to text transformation based on the description: "+description,
                    "enum": column_description,

                }
                }
            },
            "required": ["column"]
        },  
        {
            "name": "get_sentiment",
            "description": "This function takes in one of the columns as input, applies sentiment analysis on the content of that column, and generates an additional column labeling the content as 'pos', 'neg', or 'other'. Don't select this if none of the columns matches the user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to apply sentiment analysis. You have to select one column in the 'enum' field to apply sentiment analysis based on the description: "+description,
                        "enum": column_description
                    }
                },
                "required": ["column"]
            }
        },    
        {
            "name": "null",
            "description": "This function should be called when the table already contains all the necessary information to complete the user query. IMPORTANT: filter conditions related to numerical (such as range/percentile/etc.) doesn't require additional function calls, so this function should be called in cases when numerical value filters are the only operations to be applied.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The placeholder parameter. It can only be 'null'",
                        "enum": ["null"]
                    }
                },
                "required": ["column"]
            }
        } 
    ]
    
    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-16k",
        model="gpt-4-turbo-preview",
        messages=messages,
        functions = functions,
        function_call = "auto",
    )

    if verbose:
        num_token_msg = num_tokens_from_messages(messages, "gpt-4-turbo-preview")
        num_token_func = num_tokens_from_functions(functions, "gpt-4-turbo-preview")
        print("Number of tokens of messages for 'schema_gpt': ", num_token_msg)
        print("Number of tokens of functions for 'schema_gpt': ", num_token_func)


    return response.choices[0].message

def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def table_gen_pd(user_query, table, enum, description, status, function_chain, verbose):
    start_time = time.time()
    function_list = []
    dot = Digraph(comment='graph')
    for c in enum:
        dot.node(c)
    if is_notebook():
        display_handle = display(dot, display_id=True)
    while True:
        response = schema_gpt_tree(user_query + " I am given a table with the following columns: " + description, enum, description, function_chain, function_list, verbose)
        # print(response)
        if "function_call" not in response:
            if "content" in response:
                feedback = response["content"]
            else:
                feedback = ""
            return table, enum, description, True, feedback
        func = response["function_call"]
        f = func["name"]
        function_list.append(f)
        if f == "null":
            break
        function_dict = json.loads(func["arguments"])
        if f != "get_semantic":
            col = function_dict["column"]
            if col == "null":
                break
        # if f == "get_similarity":
        #     primary_id = function_dict["primary_id"]
        #     secondary_id = function_dict["secondary_id"]
        #     table, enum, description = globals()[f](table, col, enum, description, primary_id, secondary_id)
        if f == "get_trigger":
            emotion = function_dict["emotion"]
            table, enum, description, dot = globals()[f](table, col, emotion, enum, description, verbose, dot)
        elif f == "get_stance":
            target = function_dict["target"]
            table, enum, description, dot = globals()[f](table, col, target, enum, description, verbose, dot)
        elif f == "get_supporter_response":
            strategy = function_dict["strategy"]
            table, enum, description, dot = globals()[f](table, col, strategy, enum, description, verbose, dot)
        elif f == "get_class":
            table, enum, description, dot = globals()[f](user_query, table, col, enum, description, verbose, dot)
        elif f == "get_premise_explanation":
            hypothesis = function_dict["hypothesis"]
            type = function_dict["type"]
            term = function_dict["term"]
            label = function_dict["label"]
            table, enum, description, dot = globals()[f](table, col, hypothesis, type, term, label, enum, description, verbose, dot)
        elif f == "get_premise":
            type = function_dict["type"]
            term = function_dict["term"]
            table, enum, description, dot = globals()[f](table, col, type, term, enum, description, verbose, dot)
        elif f == "get_semantic":
            word = function_dict["word"]
            word_type = function_dict["word_type"]
            index = function_dict["index"]
            sentence1 = function_dict["sentence1"]
            sentence2 = function_dict["sentence2"]
            table, enum, description, dot = globals()[f](table, word, word_type, index, sentence1, sentence2, enum, description, verbose, dot)
        elif f == "get_story_type":
            storyIx = function_dict["storyIx"]
            sentIx = function_dict["sentIx"]
            event = function_dict["event"]
            event_major = function_dict["event_major"]
            event_expected = function_dict["event_expected"]
            table, enum, description, dot = globals()[f](table, col, storyIx, sentIx, event, event_major, event_expected, enum, description, verbose, dot)
        elif f == "get_deception":
            smile = function_dict["smile"]
            scowl = function_dict["scowl"]
            table, enum, description, dot =globals()[f](table, col, smile, scowl, enum, description, verbose, dot)
        elif f in ["get_emotional_reaction_level", "get_exploration_level", "get_intepretation_level"]:
            column_post = function_dict["column_post"]
            table, enum, description, dot = globals()[f](table, col, column_post, enum, description, verbose, dot)
        elif f in ["get_event_major", "get_event_expected"]:
            event = function_dict["event"]
            table, enum, description, dot = globals()[f](table, col, event, enum, description, verbose, dot)
        else:
            table, enum, description, dot = globals()[f](table, col, enum, description, verbose, dot)
        
        # displaying the dot graph
        if is_notebook():
            update_display(dot, display_id=display_handle.display_id) # for jupyter notebook
        else:
            output_path = dot.render(filename='./data/dot_graph', format='png', cleanup=True)
            img = Image.open(output_path)
            img.show()
    if verbose:
        print(table)
        print("Execution Time = ", time.time() - start_time)
    # print(description)
    status.append("table augmented")
    return table, enum, description, status, False, ""

# def table_gen_pd(user_query, table, enum, description, status):
#     while True:
#         response = schema_gpt(user_query + " I am given a table with the following columns: " + description, enum, description)
#         # print(response)
#         if "function_call" not in response:
#             if "content" in response:
#                 feedback = response["content"]
#             else:
#                 feedback = ""
#             return table, enum, description, True, feedback
#         func = response["function_call"]
#         f = func["name"]
#         if f == "null":
#             break
#         function_dict = json.loads(func["arguments"])
#         col = function_dict["column"]
#         if col == "null":
#             break
#         # if f == "get_similarity":
#         #     primary_id = function_dict["primary_id"]
#         #     secondary_id = function_dict["secondary_id"]
#         #     table, enum, description = globals()[f](table, col, enum, description, primary_id, secondary_id)
#         if f == "get_trigger":
#             emotion = function_dict["emotion"]
#             table, enum, description = globals()[f](table, col, emotion, enum, description)
#         elif f == "get_stance":
#             target = function_dict["target"]
#             table, enum, description = globals()[f](table, col, target, enum, description)
#         elif f == "get_class":
#             table, enum, description = globals()[f](user_query, table, col, enum, description)
#         else:
#             table, enum, description = globals()[f](table, col, enum, description)
#     print(table)
#     # print(description)
#     status.append("table augmented")
#     return table, enum, description, status, False, ""

if __name__ == "__main__":
    query = "I want to remove biases."
    table, enum, description = base_table_gen()
    status = []
    table, enum, description, _, __ = table_gen_pd(query, table, enum, description, status)
    # print(table)
    # print(enum)
    # # # print(description)
    # table, enum, description = pdf_to_text(table, 'pdf_orig', enum, description)
    # table, enum, description = get_keyword(table, 'pdf_orig_text', enum, description)
    # print(table)
    # # print(table)
    # print(enum)
    # # print(description)
    # table, enum, description = para_sep(table, 'pdf_orig_text', enum, description)
    # print(table)
    # print(enum)
    # # print(description)
    # # table, enum, description = get_summary(table, 'pdf_orig_text_segment1', enum, description)
    # # print(table)
    # # print(enum)
    # # print(description)



