"""
Keyrum upp spjallmennið hér.
Í terminalinu ætti þetta að koma þegar þið keyrið kóðann:
 -- Running on http://127.0.0.1:2000 --
Á windows ýtið þið ctrl og smellið á linkinn 
og á mac os þá ýtið þið á cmd og smellið á linkinn,
þá ætti notendaviðmót að poppa upp í vafra og
þá er hægt að spjalla við Ugla.
"""

from app.chatbot import app

if __name__ == "__main__":
     
    app.run(port=2000, debug=True)