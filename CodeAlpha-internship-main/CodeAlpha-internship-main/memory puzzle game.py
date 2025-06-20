import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time

CARD_IMAGES = ['images/image1.png', 'images/image2.png', 'images/image3.png', 'images/image4.png', 'images/image5.png', 'images/image6.png', 'images/image7.png', 'images/image8.png']
CARD_BACK_IMAGE = 'images/card_back.png'

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Puzzle Game")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 480
        window_height = 512
        self.root.geometry(f'{window_width}x{window_height}')
        self.root.resizable(False, False)






        # Load and resize images
        self.card_images = [Image.open(img).resize((100, 100)) for img in CARD_IMAGES]
        self.card_images = [ImageTk.PhotoImage(img) for img in self.card_images]
        self.card_back_image = ImageTk.PhotoImage(Image.open(CARD_BACK_IMAGE).resize((100, 100)))

        # Create pairs of cards
        self.cards = self.card_images * 2
        random.shuffle(self.cards)

        # Game variables
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0
        self.total_pairs = len(CARD_IMAGES)
        self.time_limit = 60  # seconds
        self.start_time = time.time()

        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        self.buttons = []
        self.card_status = []  # Track which cards are flipped during the game
        for i in range(4):
            row = []
            status_row = []
            for j in range(4):
                button = tk.Button(self.root, image=self.card_back_image, command=lambda i=i, j=j: self.flip_card(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
                status_row.append(False)  # All cards are initially face down
            self.buttons.append(row)
            self.card_status.append(status_row)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_limit}")
        self.timer_label.grid(row=4, column=0, columnspan=4)

    def flip_card(self, i, j):
        if self.card_status[i][j]:
            return  # If the card is already flipped do nothing

        self.buttons[i][j].config(image=self.cards[i * 4 + j])
        self.card_status[i][j] = True

        if self.first_card is None:
            self.first_card = (i, j)
        elif self.second_card is None:
            self.second_card = (i, j)
            self.root.after(1000, self.check_match)

    def check_match(self):
        if self.cards[self.first_card[0] * 4 + self.first_card[1]] == self.cards[self.second_card[0] * 4 + self.second_card[1]]:
            self.matched_pairs += 1
            if self.matched_pairs == self.total_pairs:
                messagebox.showinfo("Congratulations!", "You've matched all pairs!")
                self.root.quit()
        else:
            self.buttons[self.first_card[0]][self.first_card[1]].config(image=self.card_back_image)
            self.buttons[self.second_card[0]][self.second_card[1]].config(image=self.card_back_image)
            self.card_status[self.first_card[0]][self.first_card[1]] = False
            self.card_status[self.second_card[0]][self.second_card[1]] = False

        self.first_card = None
        self.second_card = None

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        time_left = self.time_limit - int(elapsed_time)
        self.timer_label.config(text=f"Time left: {time_left}")

        if time_left > 0:
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.root.quit()

if __name__ == "__main__":
   
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
