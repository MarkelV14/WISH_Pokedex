Flask beharrezkoa da, horretarako ingurune birtuala sortu behar da eta bertan flask instalatu.

Aplikazioa egiteko terminalean hurrengoa idatzi behar da:

python3 run.py

Administratzaile den kontu bat sortzeko, lehenik goiko komandoa jarri eta behin aplikazioa sortuta hurrengo komando jarri:

python3 create_admin.py


python populate_db.py
python fix_evolutions.py
python fill_weaknesses.py
python run.py



### === Testen exekuzioa === ###

Proiektu honek proba automatizatuen bateria osoa dauka aplikazioaren funtzionalitate kritikoak (Autentikazioa, Pokedex,Pokemonak, Taldeak, Chatbot eta ChangeLog) eta egonkortasuna bermatzeko.

Test hauek exekutatzeko, kodearen estaldura (coverage) neurtzeko eta HTML formatuko txosten zehatza sortzeko, exekutatu hurrengo komandoa proiektuaren erroan:

```bash
pytest --cov=app --html=reporte_final_completo.html

Exekuzioa amaitzean, reporte_final_completo.html fitxategia sortuko da. Fitxategi hau nabigatzailean ireki dezakezu testen emaitzak ikusteko.

=== Aurrebaldintzak ===
Testak exekutatu ahal izateko, ziurtatu beharrezko liburutegiak instalatuta dituzula (pytest eta bere pluginak):

Bash

pip install pytest pytest-cov pytest-html

