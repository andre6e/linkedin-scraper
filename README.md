# 00data-collection
Social Network Analysis 2020 project group repository.

Commits history sul repo non ufficiale utilizzato in fase di partenza reperibile [qui](https://github.com/andre6e/SNA_2020_Fedele_Cavalieri_Olivotto_Guiducci). 


## Descrizione data collection
Scraping data off of LinkedIn is against their User Agreement. This is purely intended for educational purposes.

Obbiettivo di questa fase è raccogliere un grosso numero di url per profili linkedin.
Lo scraping viene fatto tramite l'utilizzo di selenium.
E' stato fatto uso dell'account premium SALES di linkedin.
La collection è stata fatta filtrando su territorio italiano, per diversi settori e scaricando 2500 url (limite massimo definito da linkedin) per ogni fascia di "numero di dipendenti" aziendali.
La seconda fase è quella di scaricare i dati relativi alle posizoni lavorative e l'ultima istruzione dei profili stessi.

## Contenuto repository
Le due sotto cartelle contengono i progetti python utili a raggiungere i due obiettivi sopra descritti.
Entrambi i progetti sono configurabili tramite config file.
In entrambi i progetti il file main.py rappresenta l'entry point dello script.

* premium-urls-scraper: scarica lista di url di profili personali (SALES LIKEDIN URLS)
* profile-data-scraper: scarica dati dai profili a partire dalle url (SALES LINKEDIN PROFILES)
