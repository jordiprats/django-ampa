import html2text
html = '<html><body>Hola,<br>Des de l\'AMPA em demanen si podeu revisar les dades del vostre fill i donar el consentiment als delegats per fer-les servir per contactar amb vosaltres per temes del cole:<br><br><a href="http://ampa.systemadmin.es/alumnes/'+'">http://ampa.systemadmin.es/alumnes/'+'</a><br><br>Cal marcar la opció de cessió de dades per cada un dels pares, si voleu, rectificar si hi ha alguna dada incorrecte i al final hi ha també la opció per confirmar que les dades són correctes<br><br>Si us plau, no contesteu a aquest email, per qualsevol dubte contacteu amb el vostre delegat pels canals habituals<br><br>salutacions,</body></html>'

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
print(text_maker.handle(html))
