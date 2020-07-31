with open("infile.txt", "r") as f:
	text = f.read()

with open("outfile.txt", "w") as f:
	f.write("""#include <DigiKeyboard.h>\nvoid setup() {
	DigiKeyboard.sendKeystroke(0);
	DigiKeyboard.delay(500);""")
	for i in text.split("\n"):
		i = i.replace("REM", "//")
		if i[:6] == "STRING":
			i = "DigiKeyboard.print(\"%s\")" % i[7:]
		i = i.replace("GUI", "DigiKeyboard.sendKeystroke(KEY_R, MOD_GUI_LEFT)")
		if i[:5] == "DELAY":
			i = "DigiKeyboard.delay(%s)" % i[6:]
		i = i.replace("ENTER", "DigiKeyboard.sendKeystroke(KEY_ENTER)")
		f.write("\n	%s;" % i)
	f.write("""\n}
\nvoid loop() {\n\n}""")
