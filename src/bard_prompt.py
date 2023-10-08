from bardapi import Bard
import requests
import os

#Bard Settings
token = os.environ["_bard_api_key"]

answer_style = "Return answers summarized within 150-200 words in a HTML format with no styles, where the title will have <h1> tags, while normal content in <p></p> tags. No information outside of html tags"
questions = [
  f"Please provide one main endangered species living in the lake. {answer_style}",
  # f"Provide a a open url to an image of the animal mentioned previously. Please just give the raw url, without any other words in your reply",
  f"Where did the water come from for this lake? {answer_style}",
  f"How is the water quality nowadays? Any recent articles, written in english or non-english discussig it? {answer_style}",
  f"What are the precautionary steps visitors should take to prevent damaging the lake? {answer_style}",
]

def summarize_about_body_of_water(body_of_water):
  session = requests.Session()
  session.headers = {
              "Host": "bard.google.com",
              "X-Same-Domain": "1",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
              "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
              "Origin": "https://bard.google.com",
              "Referer": "https://bard.google.com/",
          }

  session.cookies.set("__Secure-1PSID", token)
  bard = Bard(token=token, session=session, timeout=120)

  initial_prompt = f"Please answer my upcoming questions regarding {body_of_water}."

  understand_assignment = bard.get_answer(initial_prompt)
  print(understand_assignment)
  print(understand_assignment['content']) 
  
  results = [ bard.get_answer(question)['content'] for question in questions ]

  return results