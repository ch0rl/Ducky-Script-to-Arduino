from tkinter import messagebox

STARTER = "DigiKeyboard."

conversions = {
	"TAB": "KEY_TAB",
	"ENTER": "KEY_ENTER",
	"MENU": "KEY_SHIFT, KEY_F10",
	"UP": "KEY_UP_ARROW",
	"DOWN": "KEY_DOWN_ARROW",
	"LEFT": "KEY_LEFT_ARROW",
	"RIGHT": "KEY_RIGHT_ARROW"
}

wholeString = ""  # To avoid writing half the file when encountering an unrecognised command

with open("infile.txt", "r") as f:
	text = f.read()

with open("outfile.txt", "w") as f:
	f.write("""#include <DigiKeyboard.h>\n\nvoid setup() {
	DigiKeyboard.sendKeyStroke(0);
	DigiKeyboard.delay(500);""")
	for i in text.split("\n"):
		# These cases need different endings so the dictionary cannot be used
		if i.startswith("STRING"):
			string = STARTER + "print(\"" + i[7:] + "\");"
		elif i.startswith("REM"):
			string = "//" + i[3:]
		elif i.startswith("DELAY"):
			string = STARTER + "delay(" + i[6:] + ");"
		elif i.startswith("GUI") or i.startswith("WINDOWS") or i.startswith("WIN"):
			string = STARTER + "sendKeyStroke(KEY_" + i[-1].upper() + ", MOD_GUI_LEFT);"
		elif i.startswith("ALT"):
			string = STARTER + "sendKeyStroke(KEY_LEFT_ALT, KEY_" + i[-1].upper() + ");"
		elif i.startswith("CTRL") or i.startswith("CONTROL"):
			string = STARTER + "sendKeyStroke(MOD_CONTROL_LEFT, KEY_" + i[-1].upper() + ");"
		# If not the ones above, try use the dictionary
		else:
			try:
				string = STARTER + "sendKeyStroke(" + conversions[i] + ");"
			except KeyError:
				messagebox.showerror("Bad command", "Command \"%s\" not recognised" % i)
				break
		wholeString += "\n	" + string
	f.write("""%s\n}\n\nvoid loop() {\n\n}""" % wholeString)
