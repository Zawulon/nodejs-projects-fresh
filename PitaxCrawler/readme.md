Projekt przygotowany do tzw. "Crawlingu" stron w celu weryfikacji czy znajdują się na nich odopowiednie linki.


# Spis treści
1. [Wymagania systemu](#requirements)
2. [Komponenty](#components)
    1. [Docker Engine](#docker)
    2. [Python](#python)
    3. [Scrapy](#scrapy)
3. [Jak uruchomić](#getting_started)
    1. [Infrastruktura](#infrastructure)
    2. [Crawler](#crawler)
4. [Wyniki](#craling_results)
    1. [Logi](#filelogs)
    2. [Baza danych](#sqlite)
5. [Jak to działa](#howto)
    1. [Data analizy](#reportdate)
    2. [Baza danych](#dbsetting)
    3. [Źródła przeszukiwanych stron](#urllist)
    4. [Pliki logów](#logs) 
    5. [Statystyki](#stats)
6. [Raportowanie](#reporting)
    1. [Last3Days](#last3)
    2. [LastWeek](#lastweek)
    3. [Custom](#custom)
7. [Problemy i ich rozwiązywanie](#issues)
    1. [False positives](#falsepos)


## Wymagania systemu: <a name="requirements"></a>
- Docker Engine (https://www.docker.com/)
- Python (https://www.python.org/)
- Scrapy (https://scrapy.org/)

## Komponenty <a name="components"></a>
### Docker Engine <a name="docker"></a>
    > Docker version 18.03.1-ce, build 9ee9f40
![Alt text](docs/docker_version_tested.png?raw=true "Docker version project was tested.")

### Python <a name="python"></a>
    > Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)] on win32)

### Scrapy <a name="scrapy"></a>
    > Scrapy 1.5.0

## Jak uruchomić <a name="getting_started"></a>
### Uruchamimy "infrastrukturę" <a name="infrastructure"></a> odpowiedzialną za renderowanie stron. Większość stron www wykonuje całą masę skryptów ładowanych dynamicznie. W celu zapewnienia załadowania skryptów i "symulacji" przegląradki został użyty pakiet "scrapy-splash". Będąc w poniższej lokalizacji uruchamiamy komendę:
    > \PitaxCrawler\pitax\pitax\spiders\aquarium> docker-compose up


Wynikiem czego są 4 kontenery pracujące w trybie klastra o wysokiej dostępności.
HAProxy -> 3 * Scrapy-Splash

### Uruchamimy crawler <a name="crawler"></a>
    > \PitaxCrawler\pitax\pitax\spiders> scrapy runspider toscrape-test2.py

## Jak to działa <a name="howto"></a>
### settings.py <a name="reportdate" > </a>
Tu mamy kilka dat, które są w różnych formatach ale generalnie służą do wyznaczenia jednej spójnej daty wykonania operacji "crawlingu"

    > import datetime
    > report_datetime = datetime.datetime.now()
    > dateTimeString = report_datetime.strftime("%Y%m%d_%H-%M-%S")
    > report_datetime_sql = report_datetime.strftime("%Y-%m-%d %H:%M:%S")

Wyznaczany jest folder do którego będą zapisane wszystkie pobrane strony z listy linków.
    
    > LOG_FOLDER = "logs/%s" % dateTimeString

Wyznaczany jest plik logu - tu można znaleźć wszystkie szczegóły procesu - błędy pobierania, itp.

    > LOG_FILE = "logs/PitaxCrawler_%s.log" % dateTimeString

### settings.py <a name="dbsetting" > </a>
W potoku przetwarzania podpięty 'Sqlite3Pipeline'. Odpowiedzialny za zapis wyników do bazy danych.

    > ITEM_PIPELINES = {
    'pitax.pipelines.Sqlite3Pipeline': 300,
    }

Co do szczegółów to nazwa bazy i nazwa tabeli do zapisu:

    > SQLITE_FILE = 'sqlite.db'
    > SQLITE_TABLE = 'PitaxCrawlResult'

### <a name="urllist">url.txt</a>
Wejście do programu stanowi lista linków zapisanych w pliku: url.txt

    > with open("url.txt", "rt") as f:
         start_urls = [url.strip() for url in f.readlines()]

### Obsługiwane statusy HTTP

    > handle_httpstatus_list = [502,504,404,301,200]

### Domyślnie ustawiony jest 90 sekundowy timeuot na poszczególna stronę.

    > def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'timeout': 90})

### Przyszukiwane linki zawierające "pitax.pl" albo "iwop.pl"

    > quotes = response.xpath('(//a[contains(@href, "pitax.pl")])|(//a[contains(@href, "iwop.pl")])')
            
### <a name="logs">Pliki logów</a>
W katalogu logs przy każdym uruchomieniu powstaje plim z logiem, np: 

    > PitaxCrawler_20180711_21-38-55.log
W pliku tym można prześledzić proces "crawlingu" i szukać potencjalnych problemów, np: błędów w konfiguracji, błedów przy uruchamianiu w pythonie, itp. 

Wszystkie strony poddane analizie w tym przebiegu w trakcie wykonywania sa zapisywane w katalogu:

    > 20180711_21-38-55

po zakończeniu procesu zawartość katalogu jest kasowana i zarchiwizowane do pliku:

    >  20180711_21-38-55.zip

### <a name="stats">Statystyki</a>
Na zakończenie procesu wyświetlane są statystyki, gdzie w szybki sposób można ocenić wynik.

    > 2018-07-10 00:28:18 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
    > {
    > 'downloader/request_bytes': 756003,
    > 'downloader/request_count': 1397,
    > 'downloader/request_method_count/POST': 1397,
    > 'downloader/response_bytes': 34310944,
    > 'downloader/response_count': 1397,
 ```js   
    > 'downloader/response_status_count/200': 1374,
    > 'downloader/response_status_count/504': 2,
    > 'downloader/response_status_count/502': 21,
    > 'dupefilter/filtered': 10,
 ```
    > 'finish_reason': 'finished',
    > 'finish_time': datetime.datetime(2018, 7, 9, 22, 28, 12, 635107),
    > 'item_scraped_count': 1366,
    > 'log_count/DEBUG': 2772,
    > 'log_count/ERROR': 15,
    > 'log_count/INFO': 126,
    > 'request_depth_count/0': 1381,
    > 'response_received_count': 1381,
    > 'retry/count': 16,
    > 'retry/max_reached': 7,
    > 'retry/reason_count/502 Bad Gateway': 14,
    > 'retry/reason_count/504 Gateway Time-out': 2,
    > 'scheduler/dequeued': 2778,
    > 'scheduler/dequeued/memory': 2778,
    > 'scheduler/enqueued': 2778,
    > 'scheduler/enqueued/memory': 2778,
    > 'spider_exceptions/IndexError': 15,
    > 'splash/render.html/request_count': 1381,
    > 'splash/render.html/response_count/200': 1374,
    > 'splash/render.html/response_count/502': 21,
    > 'splash/render.html/response_count/504': 2,
    > 'start_time': datetime.datetime(2018, 7, 9, 20, 30, 20, 572712)
    > }


## Raportowanie <a name="reporting"></a>

### <a name="last3" >Ostatnie 3 dni </a>
### <a name="lastweek" >Ostatni tydzień</a>
### <a name="custom" >Raport użytkownika</a>


## Problemy i ich rozwiązywanie <a name="issues"></a>
### <a name="falsepos" >False positives </a>

    > select * 
    > from PitaxCrawlResult
    > where crawl_date = '2018-07-09 22:30:20'
    > and crawl_found = 0

Pomimo, że status odpytania strony jest 200 - to po tytule widać, że serwer nie znalazł takiej strony i wyświetla 404 - strony nie znaleziono. W tym przypadku mamy albo błedny link, albo strona już nie istnieje.

![Alt text](docs/false_pos_404.png?raw=true "Return 200 but page was not found.")
