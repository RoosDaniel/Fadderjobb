# Fadderjobbsystemet

https://fadderjobb.staben.info/

## Bakgrund

Historiskt sett har det alltid varit svårt att planera fadderjobb
eftersom det saknats ett sätt att delegera småjobb. T.ex. har det krävts faddrar
som står i märkesbacken under första dagen, eller extra riggfaddrar till Hoben.
Den här hemsidan försöker underlätta dessa problem genom att hantera anmälan,
byten, informationsutskick, m.m. automatiskt.

## Funktionalitet

### Allmänt

_En användare kan:_

- Se vilka som är anmälda till vilka fadderjobb.
- Se en topplista över vilka faddrar som har tagit flest poäng.

### Admin

_Admin:_

- Kan skapa nya fadderjobb.
    - Beskrivning
    - Poäng
    - Antal faddrar som behövs
    - Typ av jobb
- Kan stänga ett fadderjobb.
    - Avanmälan kan endast ske om en annan fadder köar för platsen.
    - Finns lediga platser kan faddrar anmäla sig till dessa, trots att jobbet har stängt.

### Fadder

_En fadder:_

- Kan registrera sig på fadderjobb.
- Kan om jobbet är fullt:
    - Ställa sig i kö till jobbet. Den som är först i kön när någon registrerad avregistrerar sig får jobbet.
- Kan efter att anmälan har stängt:
    - Flagga för önskan om avregistrering. Nästa person på tur kommer då få jobbet istället.
- Får mail när:
    - De har fått ett jobb som de köat för.
    - De har tappat ett jobb som de köat för att avanmäla sig till.
- Kan hämta en .ics-länk till en kalender för alla sina jobb.
- Byta jobb med andra faddrar

## Planerat

### Admin

_Admin ska:_

- _Inget planerat_

### Fadder

_En fadder ska:_

- _Inget planerat_

## Deployment

För att köra projektet krävs filen `credentials.json` i root-mappen 
med följande struktur (sentry.io är valfritt):
```json
{
  "email": {
    "user": "",
    "password": ""
  },
  "database": {
    "user": "",
    "password": ""
  },
  "sentry.io": {
    "dsn": ""
  }
}
```

Ytterligare konfiguration görs via följande environment-variabler:

* `DEBUG`

    Default: `False`
    
    Bestämmer om Django ska köras i debug-läge.
    
* `DB_ENGINE`

    Default: `django.db.backends.postgresql_psycopg2`.
    
    Läs mer i
    [dokumentationen](https://docs.djangoproject.com/en/2.1/ref/databases/).

* `DB_NAME`

    Default: `fadderjobb`

* `DB_HOST`

    Default: `localhost`

* `DB_PORT`

    Default: tom

* `EMAIL_HOST`

    Default: `smtp.gmail.com`
    
* `EMAIL_PORT`

    Default: `587`
