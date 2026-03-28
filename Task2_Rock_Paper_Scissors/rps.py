import random
import tkinter as tk

# Game setup
choices = ["rock", "paper", "scissors"]

emoji = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}

user_score = 0
computer_score = 0

# Function to play
def play(user):
    global user_score, computer_score

    computer = random.choice(choices)

    user_label.config(text=f"You: {emoji[user]} {user}")
    comp_label.config(text=f"Computer: {emoji[computer]} {computer}")

    if user == computer:
        result = "It's a tie!"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        result = "You win this round!"
        user_score += 1
    else:
        result = "Computer wins this round!"
        computer_score += 1

    result_label.config(text=result)
    score_label.config(text=f"Score → You: {user_score} | Computer: {computer_score}")

    # Check winner
    if user_score == 3 or computer_score == 3:
        if user_score > computer_score:
            result_label.config(text="🏆 You won the game!")
        else:
            result_label.config(text="💻 Computer won the game!")

        disable_buttons()

# Disable buttons after game ends
def disable_buttons():
    rock_btn.config(state="disabled")
    paper_btn.config(state="disabled")
    scissors_btn.config(state="disabled")

# Restart game
def restart():
    global user_score, computer_score
    user_score = 0
    computer_score = 0

    result_label.config(text="Make your move!")
    score_label.config(text="Score → You: 0 | Computer: 0")
    user_label.config(text="")
    comp_label.config(text="")

    rock_btn.config(state="normal")
    paper_btn.config(state="normal")
    scissors_btn.config(state="normal")

# Create window
root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("400x400")

# Labels
title = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 16, "bold"))
title.pack(pady=10)

user_label = tk.Label(root, text="", font=("Arial", 12))
user_label.pack()

comp_label = tk.Label(root, text="", font=("Arial", 12))
comp_label.pack()

result_label = tk.Label(root, text="Make your move!", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

score_label = tk.Label(root, text="Score → You: 0 | Computer: 0", font=("Arial", 12))
score_label.pack(pady=5)

# Buttons
rock_btn = tk.Button(root, text="🪨 Rock", width=15, command=lambda: play("rock"))
rock_btn.pack(pady=5)

paper_btn = tk.Button(root, text="📄 Paper", width=15, command=lambda: play("paper"))
paper_btn.pack(pady=5)

scissors_btn = tk.Button(root, text="✂️ Scissors", width=15, command=lambda: play("scissors"))
scissors_btn.pack(pady=5)

restart_btn = tk.Button(root, text="🔄 Restart", width=15, command=restart)
restart_btn.pack(pady=15)

# Run app
root.mainloop()