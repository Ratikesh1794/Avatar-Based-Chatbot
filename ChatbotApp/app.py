import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import bot

class VoiceBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Bot GUI")
        
        # Load and display the avatar image
        avatar_image = Image.open("D:/AI PA/ChatbotApp/static/avatar.jpg")
        self.avatar_photo = ImageTk.PhotoImage(avatar_image)
        self.avatar_label = tk.Label(root, image=self.avatar_photo)
        self.avatar_label.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_bot)
        self.start_button.pack(pady=20)
        
        self.output_text = tk.Text(root, wrap=tk.WORD, height=10)  # Adjust the height value as needed
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        self.bot_thread = None
        
    def start_bot(self):
        self.start_button.config(state=tk.DISABLED)
        self.bot_thread = Thread(target=self.conversation)
        self.bot_thread.start()
    
    def conversation(self):
        self.display_greeting()
        while(True):
            user_input = bot.listen()
            if(user_input == "exit"):
                Exit_statement = "OK! Remember, I am always there for you! Have a good day."
                self.update_output(Exit_statement)
                bot.speak(Exit_statement)
                self.root.after(1000, self.close_gui)  # Close the GUI after a delay
                break  # Exit the loop
            else:
                user_id = '111'  # Change this to the desired user ID
                user_facial_expression = bot.get_facial_expression()
                user_personality = bot.get_user_personality(user_id)
                
                if user_personality:
                    print(f"User {user_id}'s personality traits:", user_personality)
                else:
                    print(f"User {user_id} not found in the personality data.")  # Assuming you have a function for this
                    user_personality = bot.get_user_personality()  # Assuming you have a function for this
                
                response = bot.generate_empathetic_response(user_input, user_facial_expression, user_personality)
                self.update_output("You: " + user_input)
                self.update_output("Bot: " + response)
                bot.speak(response)
            
    def display_greeting(self):
        Greeting = "Hello, this is Buddy! How can I help you?"
        self.update_output("Bot: " + Greeting)
        bot.speak(Greeting)
        
    def update_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        
    def close_gui(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceBotGUI(root)
    root.mainloop()
