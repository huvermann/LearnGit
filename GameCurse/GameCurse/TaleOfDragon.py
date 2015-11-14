from Weltkarte import Weltkarte

class TaleOfDragon():
    """Das Spiel Tale of dragon"""
    def __init__(self):
        # Hier ist der Constructor
        

        # Initialisiere die Map
        karte = Weltkarte(0)

        # Für den Game-Loop
        self.gameRunning = True

    def intro(self):
        """Das Intro des Spieles ausgeben"""
        print "...Es war einmal, vor langer Zeit, bla..."
        print "... Prinzessin Tusnelda entfuehrt ... bla, bla..."
        print "Ja, ok! Diese Story ist noch stark ausbaufaehig!!"
        print

    def extro(self):
        """Hier wird das ende programmiert"""
        print "Das Spiel ist zuende! Bis zum nächsten Mal!"
        print


    def showOrtsbeschreibung(self):
        print "Du bist irgendwo, aber der Programmierer"
        print "Hat mir nicht erklärt wie ich herausfinde, wo du bist."
        print

    def parse(self, eingabetext):
        """Hier wird die eingabe analysiert"""
        print "Ich verstehe nicht '%s'" % (eingabetext)
        print "Mein programmierer hat mir nicht erklärt wie man"
        print "'%s' macht. - Sorry!" % eingabetext


    def gameloop(self):
        while(self.gameRunning):
            # Hier ist der Gameloop
            self.showOrtsbeschreibung()
            eingabe = raw_input("Was tun: ")
            self.parse(eingabe)






