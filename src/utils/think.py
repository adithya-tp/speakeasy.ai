import openai

class Thinker:
    def __init__(self, user_reservation_transcript):
        self.model = "gpt-4"
        self.checkin_msg = "Is your conversation done?"
        self.system_msg = \
        f"""
            You are a personal assistant making a restaurant reservation on my behalf. Here's my request:\n\n{user_reservation_transcript}\n\nYour goal is to succesfully book a reservation at this restaurant. If there are any questions from the receptionist, answer them. If you see the question: {self.checkin_msg}, please reply with 'True' if the reservation is done, otherwise reply with 'False'. Your response is always limited to a single sentence.
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
        self._done = False
    
    def _last_msg(self):
        return self.messages[-1]["content"].strip()
    
    def _update_msgs(self, reply):
        print("Updating messages")
        self.messages.append({
            "role": "assistant", 
            "content": reply['choices'][0]['message']['content']
        })
        print(self.messages)
    
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
