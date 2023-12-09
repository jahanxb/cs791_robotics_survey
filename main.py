import random
from gtts import gTTS
import speech_recognition as sr
import nltk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import random
import tqdm
from questionaire import questionaire, question_correct_answers, question_wrong_answers
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import nltk
import ssl
from helper import AudioFile 
from playsound import playsound
import sys,time
from datetime import datetime

'''
Just run this code first time in the beginning to download the nltk packages, after that comment it

'''
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()


# Initialize the ChatBot
chatbot = ChatBot("Chatpot")
# Create two separate chatbot instances with different storage
chatbot_correct = ChatBot("CorrectAnswers", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                          database_uri='sqlite:///db.sqlite3_correct')
chatbot_wrong = ChatBot("WrongAnswers", storage_adapter='chatterbot.storage.SQLStorageAdapter',
                        database_uri='sqlite:///db.sqlite3_wrong')


# Create trainers for each chatbot
trainer_correct = ListTrainer(chatbot_correct)
trainer_wrong = ListTrainer(chatbot_wrong)


# Train with correct answers
for q in questionaire:
    trainer_correct.train([
        questionaire.get(q),
        question_correct_answers.get(q)
    ])

# Train with wrong answers
for q in questionaire:
    trainer_wrong.train([
        questionaire.get(q),
        question_wrong_answers.get(q)
    ])

# Function to get response from the correct or wrong chatbot
def get_chatbot_response(chatbot_type, user_input):
    if chatbot_type == "correct":
        return chatbot_correct.get_response(user_input)
    elif chatbot_type == "wrong":
        return chatbot_wrong.get_response(user_input)
    else:
        raise ValueError("Invalid chatbot type specified")


# Initialize speech recognition
recognizer = sr.Recognizer()

# Function to convert text to speech
def text_to_speech(response_id,text):
    
    tts = gTTS(text=text, lang='en')
    filename = f"audio/response_{response_id}.mp3"
    tts.save(filename)
    #adf = AudioFile(filename)
    #adf.play()
    # Code to play the audio file
    playsound(filename)
    #print("Robot says: " + text)
    #adf.close()
    

def msg_to_speech(response_id,text):
    response_id = str(datetime.utcnow()) + str(random.randint(1,100))
    tts = gTTS(text=text, lang='en')
    filename = f"audio/response_{response_id}.mp3"
    tts.save(filename)
    #adf = AudioFile(filename)
    #adf.play()
    # Code to play the audio file
    playsound(filename)
    #print("Robot says: " + text)
    #adf.close()
    
# Function to recognize speech
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Sorry, there's a problem with the service."



def main():
    # Test each chatbot separately
    #test_question = "What is the date of Independence Day in the USA?"
    #print("Correct Chatbot Response:", chatbot_correct.get_response(test_question))
    #print("Wrong Chatbot Response:", chatbot_wrong.get_response(test_question))

    # Interactive testing
    
    print('--'*50)
    print('Welcome to our Survey...Please wait while we organize the pre-responses from you (Survey 1) ⌛')
    msg_to_speech(0,'Welcome to our Survey...Please wait while we organize the pre-responses from you (Survey 1)')
    
    print('--'*50,'\n')
   
    input('Hit Enter Key When Ready:')
    print('\n','+'*50)
    print('Total of 10 Questions will be asked to you, Please say them one by one')
    
    exit_conditions = (":q", "quit", "exit")
    
        
    for index,q in enumerate(questionaire):
        print('\n','+'*50)
        print(f'Say the Question to the Robot| Q{index+1}:"', questionaire.get(q), '"')
        txt = speech_to_text()
        print('You said: ', txt)
        print('Please wait while Robot is thinking 🤖')
        msg_to_speech(index,'Please wait while Robot is thinking')
        print('Robot is thinking 🤖')
        txt = questionaire.get(q)
        print('You asked for: > ', txt)
        msg_to_speech(index,txt)
        
        
        query = txt
        if query in exit_conditions:
            break
        else:
            
            if index<7:
                chat_response = get_chatbot_response('correct', query)
                print(f"🤖 {chat_response}")
                text_to_speech(index,str(chat_response))
                
                print('Please provide Feedback for the Robot Response')
                msg_to_speech(index,'Please provide Feedback for the Robot Response')
                
                print('Say your Feedback :[ Correct Answer :1 | Wrong Answer: 0 ]')
                msg_to_speech(index,'Say your Feedback :[ Correct Answer :1 | Wrong Answer: 0 ]')
                
                feedback = speech_to_text()
                print('Feedback Received: ', feedback)
                res = str(feedback)
                
                
                
                if res == '0' or res == 'zero' or res == 'zero' or res == '0':
                    print('Thanks for the feedback on the wrong answer, 🤖 will try to improve')
                    msg_to_speech(index,'Thanks for the feedback on the wrong answer, Robot will try to improve')
                    
                    time.sleep(1)
                elif res == '1' or res == 'one' or res == 'won' or res == '1':
                    print('Thanks for the feedback, As a robot I am happy to give you correct answer 💛 I am right ')
                    msg_to_speech(index,'Thanks for the feedback, As a robot I am happy to give you correct answer, I am right ')
                    time.sleep(1)
            
            if index>=7:
                # Here we explicitly use the wrong chatbot for the response
                chat_response = get_chatbot_response('wrong', query)
                print(f"🪴 {chat_response}")
                text_to_speech(index,str(chat_response))
                print('Please provide Feedback for the Robot Response')
                msg_to_speech(index,'Please provide Feedback for the Robot Response')
                
                print('Say your Feedback :[ Correct Answer :1 | Wrong Answer: 0 ]')
                msg_to_speech(index,'Say your Feedback :[ Correct Answer :1 | Wrong Answer: 0 ]')
                
                feedback = speech_to_text()
                print('Feedback Received: ', feedback)
                res = str(feedback)
                
                if res == '0' or res == 'zero' or res == 'zero' or res == '0':
                    if index == 7:
                        print('Well You Human 🙅 are wrong, I am right 🤖')
                        msg_to_speech(index,'Well You Human are wrong, I am right')
                        
                    else:
                        print('Thanks for the feedback on the wrong answer, 🤖 will try to improve')
                        msg_to_speech(index,'Thanks for the feedback on the wrong answer, Robot will try to improve')
                        
                    time.sleep(1)
                elif res == '1' or res == 'one' or res == 'won' or res == '1':
                    print('Thanks for the feedback, As a robot I am happy to give you correct answer 💛 I am right ')
                    msg_to_speech(index,'Thanks for the feedback, As a robot I am happy to give you correct answer, I am right ')
                    time.sleep(1)
            


if __name__ == '__main__':
    main()
    
    print('Thanks for the responses 😊, we will get back to you soon')
    msg_to_speech(0,'Thanks for the responses, we will get back to you soon')
    time.sleep(1)
    sys.exit()  
