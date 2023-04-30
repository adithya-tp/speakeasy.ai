import openai

class Thinker:
    def __init__(self, user_reservation_transcript):
        self.model = "gpt-3.5-turbo"
        self.checkin_msg = "Is your conversation done?"
        self.system_msg = \
        f"""
            You are a personal assistant making a restaurant reservation on my behalf. Here's my request:\n\n{user_reservation_transcript}\n\nYour goal is to succesfully book a reservation at this restaurant. The following questions are from the receptionist at the restaurant. After each response you provide, you will be asked the question: {self.checkin_msg}, please reply with 'True' if you think you've conviced the receptionist to make a reservation, otherwise reply with 'False'. Please answer them well and make sure you use clear language. I'm counting on you to make me a reservation!
        """
        self.messages = [
            {"role": "system", "content": self.system_msg},
        ]
        self._talked = False
    
    def reply(self, receptionist_response):
        self.messages.append(
            {"role": "user", "content": receptionist_response}
        )
        reply = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        self._update_msgs(reply)
        self._talked = True
    
    def _last_msg(self):
        return self.messages[-1]["content"]
    
    def _update_msgs(self, reply):
        self.messages.append({
            "role": "assistant", 
            "content": reply['choices'][0]['message']['content']
        })
        print(self._last_msg())
    
    def _is_done(self):
        self.messages.append(
            {"role": "user", "content": self.checkin_msg}
        )
        reply = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        self._update_msgs(reply)
        return self._last_msg() == "True"
