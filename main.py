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
		if i[:6] == "STRING":
			string = STARTER + "print(\"" + i[7:] + "\");"
		elif i[:3] == "REM":
			string = "//" + i[3:]
		elif i[:5] == "DELAY":
			string = STARTER + "delay(" + i[6:] + ");"
		elif i[:3] == "GUI" or i[:7] == "WINDOWS" or i[:3] == "WIN":
			string = STARTER + "sendKeyStroke(KEY_" + i[-1].upper() + ", MOD_GUI_LEFT);"
		elif i[:3] == "ALT":
			string = STARTER + "sendKeyStroke(KEY_LEFT_ALT, KEY_" + i[-1].upper() + ");"
		elif i[:4] == "CTRL" or i[:7] == "CONTROL":
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
