import pref_table
import schulze
import os
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

alternatives = []
ballots = []
weigths = []


def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


def show(title, text):
    dialog = Gtk.MessageDialog(
        transient_for=window,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(text)
    dialog.run()

    dialog.destroy()


def _next(event):
    window.set_title("Alternatives")
    labelExp.destroy()
    buttonExp.destroy()
    grid.attach(labelAltHelp, 1, 0, 1, 1)
    grid.attach(entryAlt, 1, 1, 1, 1)
    grid.attach(blank, 1, 2, 1, 1)
    grid.attach(blank_too, 1, 4, 1, 1)
    grid.attach(buttonPrev, 0, 3, 1, 1)
    grid.attach(buttonNext, 2, 3, 1, 1)
    grid.attach(labelAlt, 1, 3, 1, 1)
    grid.attach(buttonEndAlt, 1, 5, 1, 1)
    window.resize(1, 1)
    window.show_all()


def _page(string, buttons, number):
    if not "\n".join(string.split("\n")[(number - 1) * 10 : number * 10]):
        buttons[0].set_sensitive(False)
    else:
        buttons[0].set_sensitive(True)
    if not "\n".join(string.split("\n")[(number + 1) * 10 : (number + 2) * 10]):
        buttons[1].set_sensitive(False)
    else:
        buttons[1].set_sensitive(True)
    window.resize(1, 1)
    return "\n".join(string.split("\n")[number * 10 : (number + 1) * 10])


def _prevpage(event, ballot=0):
    if ballots:
        global numberBallot
        numberBallot -= 1
        labelAlt.set_label(_page(pageString, (ballotPrev, ballotNext), numberBallot))
        return
    global number
    number -= 1
    labelAlt.set_label(_page(pageString, (buttonPrev, buttonNext), number))


def _nextpage(event, ballot=0):
    if ballots:
        global numberBallot
        numberBallot += 1
        labelAlt.set_label(_page(pageString, (ballotPrev, ballotNext), numberBallot))
        return
    global number
    number += 1
    labelAlt.set_label(_page(pageString, (buttonPrev, buttonNext), number))


def _add_alt(event):
    global pageString
    candidate = entryAlt.get_text()
    if candidate in alternatives:
        show(f"You already added {candidate} !", "")
        return
    entryAlt.set_text("")
    alternatives.append(candidate)
    pageString += f"\n{len(alternatives)} : {candidate}"
    labelAlt.set_label(_page(pageString, (buttonPrev, buttonNext), number))


def _end_alt(event):
    global number, pageString
    window.set_title("Vote")
    labelAltHelp.destroy()
    entryAlt.destroy()
    buttonEndAlt.destroy()
    blank.destroy()
    number, pageString = 0, ""
    grid.attach(labelBallotsHelp, 1, 5, 1, 1)
    grid.attach(entryBallots, 1, 6, 1, 1)
    grid.attach(blank_again_again, 1, 7, 1, 1)
    grid.attach(ballotPrev, 0, 8, 1, 1)
    grid.attach(ballotLabel, 1, 8, 1, 1)
    grid.attach(ballotNext, 2, 8, 1, 1)
    grid.attach(blank_again, 2, 9, 1, 1)
    grid.attach(END_EVERYTHING, 1, 10, 1, 1)
    window.resize(1, 1)
    window.show_all()


def string_to_ballot(string):
    ballot, number = string.split(",")[0], int(string.split(",")[1])
    ballot = ballot.split("+")
    ballot = [i.split("-") for i in ballot]
    for i in range(len(ballot)):
        ballot[i] = list(set(ballot[i]))
        for j in range(len(ballot[i])):
            try:
                entry = ballot[i][j]
                int(entry)
                assert int(entry) <= len(
                    alternatives
                ), "Well, that'll never be seen, so wassup ?"
                ballot[i][j] = int(entry)
            except:
                return None, None
    for i in range(len(ballot)):
        for j in ballot[i]:
            if j in pref_table.concat_lists(ballot[min(i + 1, len(ballot)) :], level=1):
                return None, None
    string_ballot = "+".join(["-".join(map(str, i)) for i in ballot])
    return ballot, string_ballot, number


def _add_ballot(event):
    string_ballot = entryBallots.get_text()
    try:
        ballot, string_ballot, howmany = string_to_ballot(string_ballot)
        assert ballot and string_ballot and howmany, "Gaspard's definitely's a cutie"
    except:
        show("Erreur de syntaxe", "")
        return
    if ballot in ballots:
        show("Ce scrutin a déjà été entré", "")
        return
    ballots.append(ballot)
    weigths.append(howmany)
    global pageBallot
    pageBallot += f"\n{string_ballot}"
    ballotLabel.set_label(_page(pageBallot, (ballotPrev, ballotNext), numberBallot))
    entryBallots.set_text("")


def _end_like_like_you_know_like_everything(event):
    global length
    length = len(alternatives)
    window.set_title("Résultats")
    labelBallotsHelp.destroy()
    labelAlt.destroy()
    buttonNext.destroy()
    buttonPrev.destroy()
    ballotNext.destroy()
    ballotPrev.destroy()
    entryBallots.destroy()
    END_EVERYTHING.destroy()
    ballotLabel.destroy()
    blank.destroy()
    blank_too.destroy()
    blank_again_again.destroy()
    blank_again.destroy()
    winner = schulze.main(pref_table.main(length, ballots, weigths))

    winner = "Liste des vainqueurs : \n" + "\n".join(
        map(alternatives.__getitem__, winner),
    )
    winnar = Gtk.Label(label=winner)
    grid.attach(winnar, 0, 0, 1, 1)
    window.resize(1, 1)
    window.show_all()


window = Gtk.Window()
window.set_title("Explications")
window.set_wmclass("Scrutin de Condorcet", "Scrutin de Condorcet")
window.set_icon_from_file(get_resource_path("voting.png"))

grid = Gtk.Grid()
box = Gtk.Box(spacing=20)

labelExp = Gtk.Label(
    label="""Vous devez choisir des alternatives et les entrer. 
Ensuite, vous devez mettre des TYPES de scrutin 
en cochant les cases correspondant aux préférences 
de chacun. Enfin, il vous faut entrer le nombre de 
chaque type de scrutin."""
)
buttonExp = Gtk.Button(label="Suivant")

labelAltHelp = Gtk.Label(label="Entrez l'alternative suivante")
entryAlt = Gtk.Entry()
pageString = "Ajoutées jusque là :"
number = 0
labelAlt = Gtk.Label(label=pageString)
buttonPrev = Gtk.Button(label="<")
buttonNext = Gtk.Button(label=">")
buttonEndAlt = Gtk.Button(label="Voter")
blank = Gtk.Label(label="\n")
blank_too = Gtk.Label(label="\n")
_page(pageString, (buttonPrev, buttonNext), number)

buttonPrev.set_valign(Gtk.Align.CENTER)
buttonNext.set_valign(Gtk.Align.CENTER)

numberBallot = 0
pageBallot = "Jusqu'ici : "
blank_again = Gtk.Label(label="\n")
blank_again_again = Gtk.Label(label="\n")
labelBallotsHelp = Gtk.Label(
    label="""Rappel pour la syntaxe : 
[alternative]-[alternative]-...+
[alternative]+...+[alternative],nombre. 
- pour l'égalité entre 2 
alternatives, + pour la 
préférence des alternatives à 
droite sur les alternatives à 
gauche. Nombre pour le nombre 
de scrutins de ce type"""
)
entryBallots = Gtk.Entry()
ballotPrev = Gtk.Button(label="<")
ballotNext = Gtk.Button(label=">")
ballotLabel = Gtk.Label(label=pageBallot)

END_EVERYTHING = Gtk.Button(label="Terminé (sûr ?)")

ballotPrev.set_valign(Gtk.Align.CENTER)
ballotNext.set_valign(Gtk.Align.CENTER)

grid.attach(labelExp, 0, 0, 1, 1)
grid.attach(buttonExp, 1, 1, 1, 1)

buttonExp.connect("clicked", _next)
buttonPrev.connect("clicked", _prevpage)
buttonNext.connect("clicked", _nextpage)
ballotPrev.connect("clicked", _prevpage, 1)
ballotNext.connect("clicked", _nextpage, 1)
buttonEndAlt.connect("clicked", _end_alt)
END_EVERYTHING.connect("clicked", _end_like_like_you_know_like_everything)
entryAlt.connect("activate", _add_alt)
entryBallots.connect("activate", _add_ballot)
window.connect("delete-event", Gtk.main_quit)

grid.set_margin_top(20)
grid.set_margin_bottom(20)
box.pack_start(grid, True, True, 20)
window.add(box)
window.show_all()

Gtk.main()
