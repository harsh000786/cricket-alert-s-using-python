from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
import requests
from bs4 import BeautifulSoup
import re

class CricketScore:
    def __init__(self, rootwindow):
        self.rootwindow = rootwindow
        self.rootwindow.geometry('800x500')
        self.rootwindow.title('LIVE CRICKET SCORE')

        # Background image
        self.bg = ImageTk.PhotoImage(file=r'C:\Users\HARSH MHATRE\Downloads\crics.jpg')
        bg = Label(self.rootwindow, image=self.bg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.label = Label(self.rootwindow, text="LIVE SCORE", font=("times new roman", 60), bg="#ADD8E6")
        self.label.pack(pady=(10, 30))  # Padding to separate from top and next widget

        self.var = StringVar()
        self.matches = self.match_details()
        self.data = list(self.matches.keys())

        # Combobox for match selection
        self.cb = Combobox(self.rootwindow, values=self.data, width=50)
        self.cb.pack(pady=20)  # Add padding to create space between the widgets

        # Check Score Button
        self.b1 = Button(self.rootwindow, text="Check Score", font=("times new roman", 15), command=self.show_match_details)
        self.b1.pack(pady=10)  # Padding to create space

    def select(self):
        return self.cb.get()

    def show_match_details(self):
        if hasattr(self, 'frame1'):
            self.frame1.destroy()  # Destroy the previous frame if it exists

        self.frame1 = Frame(self.rootwindow, bg="#ADD8E6")
        self.frame1.pack(pady=20, fill='x', expand=True)  # Fill horizontally and add padding

        selected_match = self.cb.get()
        x = self.matches.get(selected_match, {"match_header": "No Match Selected", "score_card": "", "summary": ""})

        match_header = x['match_header'] if x['match_header'] else "Unknown Match Header"
        score_card = x['score_card'] if x['score_card'] else "Score not available"
        summary = x['summary'] if x['summary'] else "Summary not available"

        Label(self.frame1, text=selected_match + " - " + match_header, font=("times new roman", 15, "bold"), bg="#ADD8E6", bd=0).pack(anchor='w', padx=20, pady=5)
        Label(self.frame1, text="Score Details - " + score_card, font=("times new roman", 10, "bold"), bg="#ADD8E6", fg="black", bd=0).pack(anchor='w', padx=20)
        Label(self.frame1, text="Summary", font=("times new roman", 10, "bold"), bg="#ADD8E6", fg="black", bd=0).pack(anchor='w', padx=20, pady=(10, 0))
        Label(self.frame1, text=summary, font=("times new roman", 10, "bold"), bg="#ADD8E6", fg="black", bd=0).pack(anchor='w', padx=20, pady=5)

    def match_details(self):
        details = self.scrap()
        live_match = {}
        for detail in details:
            live_team_details = {}
            summary = self.match_summary(detail)
            if summary is not None:
                match_header = self.match_header(detail)
                teams = self.team_name(detail)
                score_card = self.team_score(detail)
                live_team_details['summary'] = summary.text
                live_team_details['match_header'] = match_header.text if match_header else None
                live_team_details['score_card'] = score_card[0] + " :: " + score_card[1] if score_card else None
                live_match[teams[0] + " vs " + teams[1]] = live_team_details

        return live_match

    def team_score(self, detail):
        t = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text if detail.find("div", class_="cb-hmscg-bat-txt") else None
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text if detail.find("div", class_="cb-hmscg-bwl-txt") else None
        t.append(team1_details)
        t.append(team2_details)
        return t

    def match_summary(self, detail):
        return detail.find("div", class_="cb-mtch-crd-state")

    def match_header(self, detail):
        return detail.find("div", class_="cb-mtch-crd-hrd")

    def team_name(self, detail):
        t = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text
        team1_index = re.search(r"\d", team1_details).start() if re.search(r"\d", team1_details) else len(team1_details)
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text
        team2_index = re.search(r"\d", team2_details).start() if re.search(r"\d", team2_details) else len(team2_details)
        t.append(team1_details[:team1_index])
        t.append(team2_details[:team2_index])
        return t

    def scrap(self):
        url = "https://www.cricbuzz.com/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        result = soup.find_all(id="match_menu_container")
        return result

def main():
    rootwindow = Tk()
    obj = CricketScore(rootwindow)
    rootwindow.mainloop()

if __name__ == "__main__":
    main()
