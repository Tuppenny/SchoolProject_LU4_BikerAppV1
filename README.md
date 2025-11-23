README – Biker Haaglanden Fietsverhuur Applicatie - Over dit project

De Biker Haaglanden desktopapplicatie is een CustomTkinter- gebaseerde GUI-oplossing voor het beheren van fietsverhuur, schademeldingen en reparaties.
De applicatie bevat zowel een klantenkant als een medewerkersportaal, inclusief reserveringenbeheer en interne werkprocessen.

Dit project is geschreven in Python 3.11 en ge


Benodigdheden
Om de applicatie te draaien heb je het volgende nodig:
  - Python 3.10 of hoger
  - pip (wordt standaard meegeleverd met Python)
  - De Python-libraries:
      - customtkinter
      - pyinstaller

Installatie: (Terminal / CMD / PowerShell)

1. Ga naar de projectmap

        cd jouw/map/SchoolProject_LU4_BikerApp/


2. (Aanbevolen) Maak een virtual environment

        python -m venv venv


3. Activeer de virtual environment
   
    Windows:

        venv\Scripts\activate
    Mac/Linux:

        source venv/bin/activate

4. Installeer alle benodigde libraries 

         pip install customtkinter


        pip install pyinstaller


5. Start de applicatie

        python main.py


Applicatie uitvoeren via PyCharm:

1. Open PyCharm
2. Klik File → Open en selecteer de projectmap
3. PyCharm vraagt: “Would you like to create a virtual environment?” → Yes
4. Ga naar File → Settings → Project → Python Interpreter
5. Controleer of customtkinter is geïnstalleerd
6. Anders klik op + en zoek op customtkinter, kies Install
7. Run de applicatie: Klik rechts bovenin op de groene ► Run main


Als je tabelwijzigingen hebt doorgevoerd in de code, verwijder het oude .db bestand en start de applicatie opnieuw.

Optioneel: EXE bouwen:

Gebruik PyInstaller:

    pyinstaller --noconfirm --windowed --onefile main.py


De .exe verschijnt in:

    /dist/main.exe

Let op:
1. Na aanpassingen in code moet je een nieuwe .exe maken.

2. De database wordt niet ingebakken; de app maakt een nieuwe naast de .exe.

BELANGRIJK VOOR NAVIGEREN VAN APPLICATIE:

Medewerkers login:

Voor toegang tot het medewerkersportaal is de volgende demo‐account beschikbaar:

Gebruikersnaam:

    admin

Wachtwoord:

    admin

Overzichtstabellen verversen:

Als je een nieuwe reservering, schademelding of reparatie hebt toegevoegd maar deze niet direct ziet in de tabel, klik dan op de Refresh-knop in het betreffende overzicht.
Deze knop haalt de meest recente gegevens opnieuw op uit de database.

Database wordt automatisch aangemaakt:

Het bestand:

    biker.db 
wordt automatisch aangemaakt wanneer de applicatie wordt gestart.
Als je foutmeldingen krijgt met ontbrekende kolommen, verwijder dan het bestand biker.db en start de applicatie opnieuw. De database wordt dan opnieuw opgebouwd.

Let op bij .exe builds:

Wanneer je wijzigingen aan de scripts maakt, wordt de .exe niet automatisch bijgewerkt.
Je moet PyInstaller opnieuw uitvoeren om een nieuwe versie van de applicatie te bouwen.

Datumformaat:

Bij het aanmaken of afronden van reserveringen moet de datum altijd handmatig ingevoerd worden in het formaat:

    dd-mm-jjjj

Let op: Popupvensters kunnen achter het hoofdscherm verschijnen

Sommige meldingen en bevestigingsvensters (zoals “Bekijken”, “Verwijderen?”, “Afronden”, of foutmeldingen) openen als losse popupvensters. Afhankelijk van het besturingssysteem en vensterindeling kunnen deze popups soms achter het hoofdvenster terechtkomen.

Als je merkt dat de applicatie niet reageert:

1. Controleer of er een popup achter het hoofdvenster actief is

2. Minimaliseer het hoofdvenster om deze zichtbaar te maken

3. Klik de popup eerst weg om verder te kunnen gaan

Ik adviseer gebruikers om het applicatievenster niet volledig schermvullend te maken om dit te voorkomen.