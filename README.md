# Szakdolgozat
Autó és motor alkatrészt árusító szoftver Python & Tkinter használatával. Egy asztali alkalmazás, amely integrált készletgazdálkodási és nyilvántartó információs rendszert biztosít a felhasználónak.

## Kipróbált környezet
- Windows 11 Pro (25H2)
- Python 3.14
- PostgreSQL 18.3, pgAdmin 4
- A csomagok pontos verziói: `requirements.txt`

## Telepítés
A parancsokat a projekt gyökérmappájából kell futtatni.

1. Virtuális környezet létrehozása és aktiválása:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Függőségek telepítése:
   ```
   pip install -r requirements.txt
   ```
3. Hozz létre egy üres adatbázist PostgreSQL-ben (pl. pgAdminban), pl. `szakdolgozat` néven.
4. Másold le a `.env.example` fájlt `.env` néven, és töltsd ki a saját adatbázis-adataiddal és a kezdő jelszavakkal.
5. Táblák létrehozása és mintaadatok feltöltése:
   ```
   python -m Model.database
   ```

## Indítás
```
python -m Controller.AppController
```

Kezdő felhasználók (a jelszavak a `.env` fájlban megadott értékek):
- `asd3` – admin
- `raktaros` – raktáros

## Tesztek futtatása
```
python -m unittest discover -s Test -p "Test_*.py" -v
```
Az egységtesztek memóriabeli SQLite-adatbázison futnak, ezért nem módosítják a PostgreSQL-adatbázist.

## Verzió
- `v1.0`: a szakdolgozat eredetileg beadott állapota.
- `v1.1`: a konzulensi visszajelzés alapján javított állapot. A szakdolgozat ezt az állapotot írja le.