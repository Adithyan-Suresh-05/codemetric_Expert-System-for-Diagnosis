import tkinter as tk
from tkinter import scrolledtext
import difflib

diagnosis_rules = {
    "not turning on": "Please check if the power cable is connected properly. If you're using a laptop, try charging or hard resetting. If still no luck, it's best to visit a technician.",
    "won't turn on": "It could be a power supply or hardware failure. Please consider consulting a technician for a physical inspection.",
    "black screen": "This might be a serious issue with your display or internal hardware. I suggest seeking help from a computer specialist.",
    "slow performance": "Try closing unnecessary programs, checking for malware, or upgrading your RAM.",
    "overheating": "Make sure your computer is placed in a well-ventilated area. You might need to clean the fans or reapply thermal paste.",
    "wifi not working": "Try restarting your router or reconnecting to the Wi-Fi. Check if the network adapter is enabled.",
    "keyboard not working": "Check the keyboard connection. If wireless, ensure batteries are charged. Try using it on another device.",
    "blue screen": "A blue screen often indicates a critical system error. It's recommended to run diagnostics or consult a professional.",
    "no sound": "Ensure the sound is not muted, and the correct output device is selected. Also check driver settings.",
    "screen flickering": "Try updating your graphics drivers or lowering the refresh rate. If it continues, get it checked.",
}

natural_replies = {
    "problem": "Happy to assist! Can you tell me what exactly is going wrong?",
    "issue": "Sure, I'm here to help. Please describe the issue in more detail.",
    "not working": "I'm here to help. Can you describe what exactly isn't working?",
    "computer is facing": "I'm glad to help. Please tell me more about the issue.",
}

acknowledgements = {
    "yes now it's working": "Great to hear that! Let me know if you face any other issues.",
    "yes it's working": "Awesome! If anything else goes wrong, I'm here.",
    "thanks it's working": "Glad I could help! Is there anything else bothering your system?",
}

def get_bot_response(user_input):
    user_input = user_input.lower()

    for ack in acknowledgements:
        if ack in user_input:
            return acknowledgements[ack]

    for phrase in natural_replies:
        if phrase in user_input:
            return natural_replies[phrase]

    best_match = None
    max_score = 0
    for keywords, response in diagnosis_rules.items():
        key_words = keywords.split()
        score = sum(1 for word in key_words if word in user_input)
        if score > max_score:
            max_score = score
            best_match = response

    if best_match:
        return best_match

    matches = difflib.get_close_matches(user_input, diagnosis_rules.keys(), n=1, cutoff=0.4)
    if matches:
        return diagnosis_rules[matches[0]]

    return "Hmm, I'm not sure about that. It's best to consult a technician if it's a complex issue."

def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"\nYou: {user_input}", "user")
    response = get_bot_response(user_input)
    chat_area.insert(tk.END, f"\nExpertBot: {response}", "bot")
    chat_area.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    chat_area.yview(tk.END)

root = tk.Tk()
root.title("Computer Diagnosis Expert System")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 10))
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")
chat_area.insert(tk.END, "ExpertBot: Hello! Describe your computer problem and I'll try to help you.", "bot")
chat_area.config(state=tk.DISABLED)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=60, font=("Arial", 10))
entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

send_button = tk.Button(root, text="Send", command=send_message, width=10)
send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

root.mainloop()
