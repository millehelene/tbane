"""
T-banespillet – lær Oslo-T-banens linjer utenatt!




Velg en linje (eller tilfeldig), og skriv inn stasjonene 
i riktig rekkefølge fra endestasjon til endestasjon.

Kommandoer underveis:
    hint     – viser én bokstav til av riktig svar (maks 3 per stasjon)
    avslutt  – avslutter runden
"""

import random

# ---------------------------------------------------------------------------
# Linjedata. Stasjonene står i kjørerekkefølge fra første til siste endestasjon.
# Linje 5 kjører én runde rundt Ringen, så noen stasjoner kommer to ganger.
# Sjekk mot Ruters offisielle linjekart hvis noe endrer seg.
# ---------------------------------------------------------------------------



SENTRUM = ["Majorstuen", "Nationaltheatret", "Stortinget",
           "Jernbanetorget", "Grønland", "Tøyen"]

HOLMENKOLLBANEN = ["Frognerseteren", "Voksenkollen", "Lillevann", "Skogen",
                   "Voksenlia", "Holmenkollen", "Besserud", "Midtstuen",
                   "Skådalen", "Vettakollen", "Gulleråsen", "Gråkammen",
                   "Slemdal", "Ris", "Gaustad", "Vinderen", "Steinerud",
                   "Frøen"]

ØST_TIL_BRYNSENG = ["Ensjø", "Helsfyr", "Brynseng"]

LAMBERTSETERBANEN = ["Høyenhall", "Manglerud", "Ryen", "Brattlikollen",
                     "Karlsrud", "Lambertseter", "Munkelia", "Bergkrystallen"]

RØABANEN = ["Østerås", "Lijordet", "Eiksmarka", "Ekraveien", "Røa",
            "Hovseter", "Holmen", "Makrellbekken", "Smestad", "Borgen"]

FURUSETBANEN = ["Hellerud", "Tveita", "Haugerud", "Trosterud", "Lindeberg",
                "Furuset", "Ellingsrudåsen"]

KOLSÅSBANEN = ["Kolsås", "Hauger", "Gjettum", "Avløs", "Haslum", "Gjønnes",
               "Bekkestua", "Ringstabekk", "Jar", "Bjørnsletta", "Åsjordet",
               "Ullernåsen", "Montebello", "Smestad", "Borgen"]

ØSTENSJØBANEN = ["Godlia", "Skøyenåsen", "Oppsal", "Ulsrud", "Bøler",
                 "Bogerud", "Skullerud", "Mortensrud"]

# Grorudbanen fra Økern og ut til Vestli
GRORUDBANEN = ["Økern", "Risløkka", "Vollebekk", "Linderud", "Veitvet",
               "Rødtvet", "Kalbakken", "Ammerud", "Grorud", "Romsås",
               "Rommen", "Stovner", "Vestli"]

SOGNSVANNSBANEN = ["Sognsvann", "Kringsjå", "Holstein", "Østhorn", "Tåsen",
                   "Berg", "Ullevål stadion", "Forskningsparken", "Blindern"]

# Ringen vest: Majorstuen -> Sinsen (motsatt vei av listen under)
RINGEN_VEST = ["Blindern", "Forskningsparken", "Ullevål stadion",
               "Nydalen", "Storo", "Sinsen"]

LINJER = {
    "1": HOLMENKOLLBANEN + SENTRUM + ØST_TIL_BRYNSENG + LAMBERTSETERBANEN,

    "2": RØABANEN + SENTRUM + ØST_TIL_BRYNSENG + FURUSETBANEN,

    "3": KOLSÅSBANEN + SENTRUM + ØST_TIL_BRYNSENG + ØSTENSJØBANEN,

    "4": (list(reversed(LAMBERTSETERBANEN)) + list(reversed(ØST_TIL_BRYNSENG))
          + list(reversed(SENTRUM)) + RINGEN_VEST + ["Løren"] + GRORUDBANEN),

    "5": (SOGNSVANNSBANEN + SENTRUM                       # inn til sentrum
          + ["Carl Berners plass", "Sinsen", "Storo",     # runden i Ringen
             "Nydalen", "Ullevål stadion", "Forskningsparken", "Blindern"]
          + SENTRUM                                       # gjennom sentrum igjen
          + ["Carl Berners plass", "Hasle"] + GRORUDBANEN),
}

MAKS_HINT = 3


# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------

def normaliser(tekst):
    """Gjør sammenligning tilgivende: store/små bokstaver, mellomrom,
    bindestrek og æøå skrevet som ae/o/a spiller ingen rolle."""
    tekst = tekst.lower().strip()
    for fra, til in [("æ", "ae"), ("ø", "o"), ("å", "a"), ("aa", "a"),
                     ("oe", "o"), ("-", ""), (" ", ""), (".", "")]:
        tekst = tekst.replace(fra, til)
    return tekst


def er_riktig(svar, fasit):
    return normaliser(svar) == normaliser(fasit)


def velg_linje():
    """Lar spilleren velge linje 1–5 eller en tilfeldig."""
    print("\nHvilken linje vil du øve på?")
    for nr, stasjoner in LINJER.items():
        print(f"  {nr}: {stasjoner[0]} – {stasjoner[-1]}")
    print("  t: tilfeldig linje")

    while True:
        valg = input("> ").strip().lower()
        if valg in LINJER:
            return valg
        if valg == "t":
            nr = random.choice(list(LINJER))
            print(f"Spillet valgte linje {nr}!")
            return nr
        print("Skriv 1, 2, 3, 4, 5 eller t.")


def velg_retning(linjenr):
    """Lar spilleren velge kjøreretning, eller tilfeldig."""
    stasjoner = LINJER[linjenr]
    print(f"\nHvilken retning?")
    print(f"  1: mot {stasjoner[-1]}")
    print(f"  2: mot {stasjoner[0]}")
    print("  t: tilfeldig")

    while True:
        valg = input("> ").strip().lower()
        if valg == "t":
            valg = random.choice(["1", "2"])
        if valg == "1":
            return list(stasjoner)
        if valg == "2":
            return list(reversed(stasjoner))
        print("Skriv 1, 2 eller t.")


def spør_om_stasjon(spørsmål, fasit, statistikk):
    """Spør til spilleren svarer riktig. Returnerer False hvis de avslutter."""
    hint_brukt = 0
    while True:
        svar = input(f"{spørsmål} ").strip()

        if svar.lower() == "avslutt":
            return False

        if svar.lower() == "hint":
            if hint_brukt < MAKS_HINT:
                hint_brukt += 1
                statistikk["hint"] += 1
                synlig = fasit[:hint_brukt]
                skjult = "_" * (len(fasit) - hint_brukt)
                print(f"  Hint: {synlig}{skjult}")
            else:
                print("  Ingen flere hint for denne stasjonen – prøv deg!")
            continue

        if er_riktig(svar, fasit):
            print(f"  ✔ Riktig – {fasit}!")
            return True

        statistikk["feil"] += 1
        print("  ✘ Feil, prøv igjen (eller skriv 'hint').")


# ---------------------------------------------------------------------------
# Selve spillet
# ---------------------------------------------------------------------------

def spill_runde():
    linjenr = velg_linje()
    stasjoner = velg_retning(linjenr)
    statistikk = {"feil": 0, "hint": 0}

    print(f"\n=== Linje {linjenr} mot {stasjoner[-1]} "
          f"({len(stasjoner)} stopp) ===")
    print("Skriv 'hint' for hjelp, 'avslutt'.\n")

    if not spør_om_stasjon("Hvilken stasjon starter du på?",
                           stasjoner[0], statistikk):
        print("Runden avsluttet.")
        return

    for i in range(1, len(stasjoner)):
        print(f"\n[{i}/{len(stasjoner) - 1}] Du er på {stasjoner[i - 1]}.")
        if not spør_om_stasjon("Neste stasjon?", stasjoner[i], statistikk):
            print(f"Runden avsluttet. Du kom til {stasjoner[i - 1]}.")
            return

    print(f"\n🚇 Endestasjon {stasjoner[-1]}! Hele linje {linjenr} klart!")
    print(f"Feil: {statistikk['feil']}   Hint brukt: {statistikk['hint']}")
    if statistikk["feil"] == 0 and statistikk["hint"] == 0:
        print("Perfekt runde – du er klar for førerhuset!")


TOGTEGNING = r"""
___________   _______________________________________^__
 ___   ___ |||  ___   ___   ___    ___ ___  |   __  ,----\
|   | |   |||| |   | |   | |   |  |   |   | |  |  | |_____\
|___| |___|||| |___| |___| |___|  | O | O | |  |  |        \
           |||                    |___|___| |  |__|         )
___________|||______________________________|______________/
           |||                                        /--------
-----------'''---------------------------------------'
"""
 

def main():
    print("=" * 45)
    print("   T-BANESPILLET – lær linjene i Oslo")
    print("=" * 45)
    print(TOGTEGNING)

    while True:
        spill_runde()
        igjen = input("\nVil du spille igjen? (j/n) ").strip().lower()
        if igjen not in ("j", "ja"):
            print("Takk for nå – god tur!")
            break


if __name__ == "__main__":
    main()
