import clipboard
def getClipboardText():
    #clipboard.copy("abc") #to set clipboard to something
    return clipboard.paste()

text=getClipboardText()
print(text)
