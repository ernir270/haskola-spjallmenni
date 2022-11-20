"""

"""

import nltk
import random
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from reynir import Greynir
#from reynir_correct import check_single


app = Flask(__name__)
app.static_folder = 'static'


#Fall til þess að tokeniza gögn
def get_data(data_file):
    f = open(data_file,'r', errors='ignore', encoding = "utf-8")
    dataset = f.read()
    return nltk.sent_tokenize(dataset)


#Fall til að sækja stopporð
def get_stopwords(stop_words):
    f = open(stop_words,'r', errors='ignore', encoding = "utf-8")
    stopwords = f.read()
    return nltk.word_tokenize(stopwords)


#Upphaf spjalls
def greet(sentence):
    greet_inputs = ("halló","halló!" "hiya", "daginn", "góðan daginn", "hæ", "hæ!")
    greet_output = ["Halló!", "Hæ!", "Góðan daginn!", "Góðan og margblessaðan daginn!", "Hiya!"]
    for word in sentence.split():
        if word in greet_inputs:
            return random.choice(greet_output)


#Chit chat fall
def conversation(sentence):
    conversation_starters_input = ["hvað segirðu?", "hvað segiru?", "hvað segir kjellinn?", "whatup", "wassup"]
    conversation_starters_output = ["Ferskur, breskur og bandarískur!", "Ég hef aldrei verið betri!", 
                                "Fróandi fínn og fitlandi góður!"]
    if sentence in conversation_starters_input:
        return random.choice(conversation_starters_output)
     

#Fall sem skilar sturlaðri staðreynd
def fact(sentence):
    fact_input = ["segðu mér sturlaða staðreynd", "ertu með sturlaða staðreynd"]
    fact_output = ["Fram til ársins 1984 voru hundar bannaðir í Reykjavík. Þá var lögunum breytt og mátti vera með hunda sumstaðar. Það var ekki fyrr en 2006 sem að banninu var alveg aflétt.",
               "Miðað við höfðatölu er Ísland með fleiri rithöfunda en öll önnur lönd í heiminum!",
               "Bjór var bannaður á Íslandi fram til ársins 1989!",
               "Ísland er með flestu sundlaugar í heiminum – miðað við höfðatölu!",
               "Manneskjan er 1 sentimeter hærri á morgnana en á kvöldin.. það munar um minna",
               "Blóð okkar mannanna ferðast tæplega 20.000 km um líkamann okkar á hverjum degi.",
               "Hnerr ferðast á allt að 160km hraða!"]
    if sentence in fact_input:
        return random.choice(fact_output)


#Uglu fall 
def uglan(sentence):
    uglan_input = ["hvað segir uglan?", "hvað segir uglan í dag?", "hvað segir uglan"]
    uglan_sentence = "Hvað varð um þessar 4ra daga vinnuvikur??"
    if sentence in uglan_input:
        return uglan_sentence


#Initializum TFIDF
def initialize_tfidf(data, stopwords):
    TFIDFVector = TfidfVectorizer(stop_words=stopwords)
    TFIDF_matrix = TFIDFVector.fit_transform(data)
    return TFIDF_matrix


#Náum í indexinn á 
def get_index_response(tfidf_matrix):
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    index_answer = cosine_sim.argsort()[0][-2]
    cosine_sim_flat = cosine_sim.flatten()
    cosine_sim_flat.sort()
    cosine_val = cosine_sim_flat[-2]

    if cosine_val == 0:
        return 0
    else:
        return index_answer


#Notum þetta fall til að checka hvort user input passi inní eitthvað af föllunum fyrir ofan, styttir response fallið
def get_func_response(user_input):
    if(greet(user_input) != None):
        return(greet(user_input))
    elif(fact(user_input) != None):
        return(fact(user_input))
    elif(uglan(user_input) != None):
        return(uglan(user_input))
    elif(conversation(user_input) != None):
        return(conversation(user_input))


#Náum í gagnasafn og stopporð   
data = get_data('hi_dataset.txt')
stopwords = get_stopwords('stopwords.txt')



#Fall sem gefur okkur svar við spurningu notanda
def ugli_response(user_input):
    user_input = user_input.lower()
    user_input.replace("?", "")

    if(user_input != "bæ"):
        if(user_input == "takk" or user_input == "takk fyrir" or user_input =="takk kærlega"):
            return("Ekkert að þakka!")
        else:
            if(get_func_response(user_input) != None):
                return(get_func_response(user_input))
            else:
                data.append(user_input)
                TFIDFVector_matrix = initialize_tfidf(data, stopwords)
                response_index = get_index_response(TFIDFVector_matrix)
                if response_index == 0:
                    data.remove(user_input)
                    return "Fyrirgefðu en ég skil þig ekki"
                else:
                    ugli_answer = data[response_index]
                    data.remove(user_input)
                    return ugli_answer
    else:
        return "Bæ! Vonandi hjálpaði ég þér eitthvað!"                
                

#Sama fall og að ofan nema með málfars leiðréttingu, virkar ekki á windows bara á mac(allavega hjá mér)
def ugli_response_with_spellcheck(user_input):
    #spellcheck = check_single(user_input)
    #user_input = spellcheck.tidy_text
    user_input = user_input.lower()
    user_input.replace("?", "")

    if(user_input != "bæ"):
        if(user_input == "takk" or user_input == "takk fyrir" or user_input =="takk kærlega"):
            return("Ekkert að þakka!")
        else:
            if(get_data(user_input) != None):
                return(greet(user_input))
            else:
                data.append(user_input)
                TFIDFVector_matrix = initialize_tfidf(data, stopwords)
                response_index = get_index_response(TFIDFVector_matrix)
                if response_index == 0:
                    data.remove(user_input)
                    return "Fyrirgefðu en ég skil þig ekki"
                else:
                    ugli_answer = data[response_index]
                    data.remove(user_input)
                    return ugli_answer
    else:
        return "Bæ! Vonandi hjálpaði ég þér eitthvað!" 


@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    #return str(ugli_response_with_spellcheck(userText))
    return str(ugli_response(userText))
