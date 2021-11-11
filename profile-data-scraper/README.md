# LinkedIn profile-data-scraper
Linkedin scraper per account free.
Permette di scaricare gli url di un tot di utenti settabile tramite il file config.ini

## Disclaimer
Scraping data off of LinkedIn is against their User Agreement. This is purely intended for educational purposes.

## Dependencies 
It is based on selenium 

## How to use
First, download the Chrome Driver from [here](http://chromedriver.chromium.org/) and extract it into the driver folder.

Finally, to scrape users run
```python3 main.py```

Prende i csv dalla cartella 'import' e ne salva la versione con dati risultanti da scraping nella cartella 'export'.
I nomi dei file da importare vanno specificati nel config.ini tramite parametro CSV_NAMES (possono essere piu di uno)