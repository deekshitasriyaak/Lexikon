import customtkinter 
from tkinter import*
from tkinter.filedialog import*
from tkinter import font
from PyDictionary import PyDictionary
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from gingerit.gingerit import GingerIt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import openai
import json


a = 'dark'
b='dark-blue'
customtkinter.set_appearance_mode(a)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(b)  # Themes: blue (default), dark-blue, green

canvas=customtkinter.CTk()

#canvas geometry
canvas.geometry(f"{1500}x{850}")
canvas.resizable(True,True)
canvas.config(background="#626567")
canvas.title("Lexikon")


#functions
#savefile function
def savefile():
    new_file=asksaveasfile(mode='w',filetype=[('text files','.txt')])
    if new_file is None:
        return
    text = str(entry.get(1.0,END))
    new_file.write(text)
    new_file.close()
#openfile function
def openfile():
    file=askopenfile(mode="r",filetype = [('text files','*.txt')])
    if file is not None:
        content = file.read()
    if content:
        clearfile()
    entry.insert(INSERT,content)
#clearfile function
def clearfile():
    entry.delete(1.0,END)
# Change Font Size
def font_size_chooser(e):
	our_font.configure(
		size=font_size_listbox.get(font_size_listbox.curselection()))
# Change Font Style
def font_style_chooser(e):
	style = font_style_listbox.get(font_style_listbox.curselection()).lower()

	if style == "bold":
		our_font.configure(weight=style)
	if style == "regular":
		our_font.configure(weight="normal", slant="roman", underline=0, overstrike=0)
	if style == "italic":
		our_font.configure(slant=style)
	if style == "bold/italic":
		our_font.configure(weight="bold", slant="italic")
	if style == "underline":
		our_font.configure(underline=1)
	if style == "strike":
		our_font.configure(overstrike=1)
#font_chooser function
def font_chooser(a):
	our_font.configure(
		family=my_listbox.get(my_listbox.curselection()))

# Designate Our Font
#our_font = font.Font(family="Helvetica", size="15")
our_font = customtkinter.CTkFont(family="Times New Roman", size=20)



#frames
button_frame=customtkinter.CTkFrame(master=canvas,height=30,width=1500,corner_radius=10)
button_frame.place(x=0,y=0)
f1_frame=customtkinter.CTkFrame(master=canvas,height=820,width=437,corner_radius=10)
f1_frame.place(x=0,y=30)
input_frame=customtkinter.CTkFrame(master=canvas,height=820,width=750,corner_radius=10)
input_frame.place(x=438,y=30)
lb_frame=customtkinter.CTkFrame(master=canvas,height=820,width=375,corner_radius=10)
lb_frame.place(x=1190,y=30)


#font_listbox and label
my_listbox = Listbox(lb_frame,selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")    # Add Listbox 
my_listbox.place(x=10,y=680,height=250,width=275)
scroll_mylist=Scrollbar(lb_frame) 
scroll_mylist.place(x=285,y=680,height=250)
my_listbox.config(yscrollcommand = scroll_mylist.set)# to listbox.yview method its yview because
scroll_mylist.config(command = my_listbox.yview)
for f in font.families():         # Add Font Families To Listbox
	my_listbox.insert('end', f)
my_listbox.bind('<ButtonRelease-1>', font_chooser)    # Bind The Listbox


# Size Listbox
l2=customtkinter.CTkLabel(lb_frame,text=("Choose your font and font-size"),font=("Heveltica",12),corner_radius=10)
l2.place(x=175,y=525,anchor=CENTER)
font_size_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")
font_size_listbox.place(x=300,y=680,height=250,width=100)
scroll_fontsize=Scrollbar(lb_frame) 
scroll_fontsize.place(x=400,y=680,height=250)
font_size_listbox.config(yscrollcommand = scroll_mylist.set)# to listbox.yview method its yview because
scroll_fontsize.config(command = font_size_listbox.yview)
font_sizes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 28, 32, 36, 40, 48]   # Add Sizes to Size Listbox
for size in font_sizes:
    font_size_listbox.insert('end', size)
font_size_listbox.bind('<ButtonRelease-1>', font_size_chooser)
    

# Style Listbox
l3=customtkinter.CTkLabel(lb_frame,text=("Choose your font-style"),font=("Heveltica",12))
l3.place(x=175,y=390,anchor=CENTER)
font_style_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")
font_style_listbox.place(x=60,y=520,height=100,width=330)
font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]  # Add Styles To Style Listbox
for style in font_styles:
	font_style_listbox.insert('end', style)	
font_style_listbox.bind('<ButtonRelease-1>', font_style_chooser)

#dictionary
def lookup():
    dict_text.delete(1.0,END)
    dictionary = PyDictionary()
    definition = dictionary.meaning(dict_entry.get())
    for key,value in definition.items():
        dict_text.insert(END, key + '\n\n')
        for values in value:
            dict_text.insert(END, f'- {values}\n\n')    
l5=customtkinter.CTkLabel(f1_frame,text=("Dictionary"),font=('Heveltica',12),corner_radius=10)
l5.place(x=210,y=8,anchor="center")
dict_entry = customtkinter.CTkEntry(f1_frame, width=400, height=40, border_width=1, placeholder_text="Enter A Word", text_color="silver")
dict_entry.place(x=220,y=35,anchor=CENTER)
dict_text = customtkinter.CTkTextbox(f1_frame, height=200, width=400, wrap=WORD)
dict_text.place(x=18,y=60)
dict_button = customtkinter.CTkButton(f1_frame, text="Lookup", command=lookup,width=50, height=35)
dict_button.place(x=360,y=18)

#synonym finder
def synonyms():
    syn_text.delete(1.0,END)
    text=syn_entry.get()
    synonyms = []
    for syn in wordnet.synsets(text):   #for the text we can use entry.get() and then put it here
        for lemma in syn.lemmas():   #lemmas is a word which represents the words the synonym set
            synonyms.append(lemma.name())
    s=set(synonyms)
    for i in s:
        syn_text.insert(END,i + " \n")
l5=customtkinter.CTkLabel(f1_frame,text=("Synonym generator"),font=('Heveltica',12),corner_radius=10)
l5.place(x=210,y=275,anchor="center")
syn_entry = customtkinter.CTkEntry(f1_frame, width=400, height=40, border_width=1, placeholder_text="Enter A Word", text_color="silver")
syn_entry.place(x=220,y=305,anchor=CENTER)
syn_text = customtkinter.CTkTextbox(f1_frame, height=150, width=400, wrap=WORD)
syn_text.place(x=18,y=330)
syn_button = customtkinter.CTkButton(f1_frame, text="Find", command=synonyms,width=50, height=35)
syn_button.place(x=360,y=288)

#Grammar
def spell_check():
    text = entry.get(0.0,END)
    if len(text)>300:
        chat_textbox.insert(END,'\n\n>>>File too big. Please segment it!')
    else:    
        entry.delete(1.0,END)
        corrected_text = GingerIt().parse(text)
        entry.insert(END,corrected_text['result']) 
b6 = customtkinter.CTkButton(f1_frame,width=380,height=60,corner_radius=10,text="Spell check",command=spell_check)
b6.place(x=30,y=600)


#paraphrase
def para():
    openai.api_key = "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"
    text = entry.get(0.0,END)
    entry.insert(END,'_'*100)
    entry.insert(END,"PARAPHRASED TEXT\n")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='Paraphrase this text: "'+text+'"',
            max_tokens=1024, 
            temperature =0.8,
            top_p =0.9
        )
        entry.insert(END," ".join(map(lambda choice: choice["text"], response["choices"])))
    except openai.exceptions.OpenAIError as e:
        entry.insert(END,f'Error: {e}')
    except json.decoder.JSONDecodeError as e:
        entry.insert(END,f'Error: {e}')
b5 = customtkinter.CTkButton(f1_frame,width=380,height=60,corner_radius=10,text="Paraphrase",command = para)
b5.place(x=30,y=700)


#summarize
def summary():
    text = entry.get(0.0,END)
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words("english"))

    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
        for word in filtered_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        for word in word_tokenize(sentence):
            if word.lower() in word_frequencies.keys():
                score += word_frequencies[word.lower()]
        sentence_scores[sentence] = score
    import heapq
    entry.insert(END,'-'*100)
    n=3   #top how many sentences
    summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)
    summary = " ".join(summary_sentences)
    entry.insert(END,'\nSUMMARY\n')
    entry.insert(END,summary)
b6 = customtkinter.CTkButton(f1_frame,width=380,height=60,corner_radius=10,text="Summarize",command=summary)
b6.place(x=30,y=500)


#chat-bot
def chat():
    d = {
        '>>>Hello!':['hi','hello','greetings','good morning'],
        '>>>Thank You! Press Exit':['bye','thank you','quit']
        }
    if chat_entry.get() in ['hi','hello','greetings','good morning','bye','thank you','quit'] :
        for k,v in d.items():
            if chat_entry.get() in v:
                chat_textbox.insert(END,'\n\n')
                chat_textbox.insert(END,k)
    elif  chat_entry.get() == 'K':
        chat_textbox.insert(END,"\n>>>Project description:\nThe aim of the application is to help the users proofread a document by enabling the user to type in the document or upload the document as a text file, as an input and giving the proofread file as the output along with the revised words’ meaning, while using a user friendly and interactive GUI.")
    elif chat_entry.get()== 'E':
        text = entry.get(0.0,END)
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        if scores['compound'] > 0.75:   
            chat_textbox.insert(END,'\n\n>>>  ¯\_◉‿◉_/¯')
        elif scores['compound'] > 0.05 :
            chat_textbox.insert(END,'\n\n>>> ヽ(•‿•)ノ ')
        elif scores['compound'] < -0.25:
            chat_textbox.insert(END,'\n\n>>> (✖╭╮✖)')
        else:
            chat_textbox.insert(END,'\n\n>>> (•ิ_•ิ)')
    elif chat_entry.get()=='light':
        a = 'light'
        customtkinter.set_appearance_mode(a)
        my_listbox = Listbox(lb_frame,selectmode=SINGLE,bg="white",fg="black",relief="sunken")    # Add Listbox 
        my_listbox.place(x=10,y=680,height=250,width=275)
        for f in font.families():      
	        my_listbox.insert('end', f)
        my_listbox.bind('<ButtonRelease-1>', font_chooser)  
        
        font_size_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="white",fg="black",relief="sunken")
        font_size_listbox.place(x=300,y=680,height=250,width=100)
        font_sizes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 28, 32, 36, 40, 48]   # Add Sizes to Size Listbox
        for size in font_sizes:
            font_size_listbox.insert('end', size)
        font_size_listbox.bind('<ButtonRelease-1>', font_size_chooser)
        
        font_style_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="white",fg="black",relief="sunken")
        font_style_listbox.place(x=60,y=520,height=100,width=330)
        font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]  # Add Styles To Style Listbox
        for style in font_styles:
	        font_style_listbox.insert('end', style)	
        font_style_listbox.bind('<ButtonRelease-1>', font_style_chooser)
        chat_textbox.insert(END,'>>>\nChanged to light mode.')
        
    elif  chat_entry.get()=='dark':
        a= 'dark'
        customtkinter.set_appearance_mode(a)
        my_listbox = Listbox(lb_frame,selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")    # Add Listbox 
        my_listbox.place(x=10,y=680,height=250,width=275)
        for f in font.families():         # Add Font Families To Listbox
	        my_listbox.insert('end', f)
        my_listbox.bind('<ButtonRelease-1>', font_chooser)    # Bind The Listbox
        
        font_size_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")
        font_size_listbox.place(x=300,y=680,height=250,width=100)
        font_sizes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 28, 32, 36, 40, 48]   # Add Sizes to Size Listbox
        for size in font_sizes:
            font_size_listbox.insert('end', size)
        font_size_listbox.bind('<ButtonRelease-1>', font_size_chooser)
        
        font_style_listbox = Listbox(lb_frame, selectmode=SINGLE,bg="#292929",fg="white",relief="sunken")
        font_style_listbox.place(x=60,y=520,height=100,width=330)   
        font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]  # Add Styles To Style Listbox
        for style in font_styles:
	        font_style_listbox.insert('end', style)	
        font_style_listbox.bind('<ButtonRelease-1>', font_style_chooser)
        chat_textbox.insert(END,'>>>\nChanged to dark mode.')
        
    else:
        chat_textbox.insert(END,'\n\n>>>ERROR\n\n  1.Enter K to know more about Lexikon \n\n  2. Enter E to generate emoji according to the tone of the paragraph \n\n  3.Enter light or dark to change mode\n')
      
chat_label = customtkinter.CTkLabel(lb_frame,text=("Lexikon Chat-Bot"),font=("Courier",12))
chat_label.place(x=175,y=10,anchor=CENTER)
chat_textbox = customtkinter.CTkTextbox(lb_frame,wrap=WORD,font=("Courier",18))
chat_textbox.place(x=10,y=20,height = 380,width = 400)
chat_entry = customtkinter.CTkEntry(lb_frame, width=300, height=40, border_width=1,placeholder_text="Type here")
chat_entry.place(x=20,y=330)
chat_textbox.insert(END,'>>>Hello! This is Lexikon Chat-Bot\n\n  1.Enter K to know more about Lexikon \n\n  2. Enter E to generate emoji according to the tone of the paragraph \n\n  3.Enter light or dark to change mode\n')
chat_button = customtkinter.CTkButton(lb_frame,height=30,width=70,text="Enter",command=chat)
chat_button.place(x=240,y=335)

#buttons
#open button
b1= customtkinter.CTkButton(button_frame,text="Open",command=openfile)
b1.place(x=0,y=0)
#save button
b2=customtkinter.CTkButton(button_frame,text="Save",command=savefile)
b2.place(x=140,y=0)
#clear button
b3=customtkinter.CTkButton(button_frame,text="Clear",command=clearfile)
b3.place(x=280,y=0)
#exit button
b4=customtkinter.CTkButton(button_frame,text="Exit",command=exit)#exit method is built-in 
b4.place(x=420,y=0)



#input entry and output
l4=customtkinter.CTkLabel(input_frame,text=("Enter the text here"),font=('Heveltica',12),corner_radius=10)
l4.place(x=350,y=8,anchor="center")
entry= customtkinter.CTkTextbox(input_frame,wrap=WORD,font=our_font) #the wrap=word avoids situations wherin few letters of the word are entered in the next line due to lack of space
text = entry.get("0.0", "end")  # get text from line 0 character 0 till the end
entry.place(x=30,y=20,height=900,width=850)

canvas.mainloop()
