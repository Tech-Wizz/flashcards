import csv
import tkinter as tk

class FlashcardGUI:
    def __init__(self, master):
        self.master = master
        self.flashcards = []
        self.current_card = 0
        self.create_widgets()
        self.load_flashcards()

    def create_widgets(self):
        # Create a canvas widget for the flashcard
        self.flashcard_canvas = tk.Canvas(self.master, width=500, height=300, bg='white')
        self.flashcard_canvas.grid(row=0, column=0, columnspan=2)

        # Question label
        self.question_label = tk.Label(self.flashcard_canvas, text="", bg='white')
        self.flashcard_canvas.create_window(250, 150, window=self.question_label)

        # Answer label
        self.answer_label = tk.Label(self.flashcard_canvas, text="", bg='white')
        self.flashcard_canvas.create_window(250, 150, window=self.answer_label)

        # Flashcard rectangle
        self.flashcard_rect = self.flashcard_canvas.create_rectangle(50, 50, 450, 250, outline='black', width=2)

        # Flip button
        self.flip_button = tk.Button(self.master, text="Flip", command=self.flip_card)
        self.flip_button.grid(row=1, column=0)

        # Next button
        self.next_button = tk.Button(self.master, text="Next", command=self.next_card)
        self.next_button.grid(row=1, column=1)

        # Add button
        self.add_button = tk.Button(self.master, text="Add", command=self.add_card)
        self.add_button.grid(row=2, column=0)

        # Question entry
        self.question_text = tk.Label(self.master, text="Question:")
        self.question_text.grid(row=3, column=0, sticky='w')
        self.question_entry = tk.Entry(self.master)
        self.question_entry.grid(row=3, column=1, sticky='nsew')

        # Answer entry
        self.answer_text = tk.Label(self.master, text="Answer:")
        self.answer_text.grid(row=4, column=0, sticky='w')
        self.answer_entry = tk.Entry(self.master)
        self.answer_entry.grid(row=4, column=1, sticky='nsew')

        # Set resize behavior
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def load_flashcards(self):
        with open('flashcards.csv') as flashcards_file:
            flashcards_reader = csv.reader(flashcards_file)
            for row in flashcards_reader:
                self.flashcards.append(row)

        self.show_question()

    def show_question(self):
        self.question_label.configure(text=self.flashcards[self.current_card][0])
        self.answer_label.configure(text="")
        self.flashcard_canvas.coords(self.question_label, 250, 120)
        self.flashcard_canvas.itemconfigure(self.flashcard_rect, state='normal')
        self.flashcard_canvas.lift(self.flashcard_rect)
        self.flashcard_canvas.lift(self.question_label)
        self.flip_button.configure(text="Flip")

    def show_answer(self):
        self.answer_label.configure(text=self.flashcards[self.current_card][1])
        self.flashcard_canvas.coords(self.answer_label, 250, 180)
        self.flashcard_canvas.lift(self.answer_label)
        self.flip_button.configure(text="Flip back")

    def flip_card(self):
        if self.answer_label["text"] == "":
            self.show_answer()
        else:
            self.show_question()

    def next_card(self):
        self.current_card = (self.current_card + 1) % len(self.flashcards)
        self.show_question()

    def add_card(self):
        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()

        if question and answer:
            with open('flashcards.csv', mode='a', newline='') as flashcards_file:
                flashcards_writer = csv.writer(flashcards_file)
                flashcards_writer.writerow([question, answer])
                self.flashcards.append([question, answer])
                self.question_entry.delete(0, tk.END)
                self.answer_entry.delete(0, tk.END)
                self.current_card = len(self.flashcards) - 1
                self.show_question()

    def clear_entries(self):
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flashcards")

    app = FlashcardGUI(root)

    root.mainloop()
