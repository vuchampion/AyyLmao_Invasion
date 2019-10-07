import sys

class Scores:
    def __init__(self, msg):
        pass
    def read_file(self):
        f = open("Highscores/Highscores.txt")
        f.read()
        #Perform operations
        f.close()

    def write_file(self, msg):
        f = open("Highscores/Highscores.txt", 'w')
        f.write(msg)
        f.close()
