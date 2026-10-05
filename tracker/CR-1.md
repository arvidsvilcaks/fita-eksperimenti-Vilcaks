---
id: CR-1
type: change-request
title: "Personas koda pārbaude iesniegumā"
status: READY
priority: high
reporter: "Reģistrācijas nodaļa (izdomāts)"
owner: "@<github-lietotājvārds>"
contract: "docs/openapi.yaml · POST /submissions · personalCode"
depends_on: []
exported: "2026-09-30 · Ezermalas pieteikumu sistēma (simulācija)"
data_check: "Nav personas datu, iekšējo adrešu vai pielikumu"
---

# CR-1 · Personas koda pārbaude iesniegumā

> Noteikumi vienkāršoti mācību vajadzībām.

## Apraksts (description)

Iesniegumos bieži ir nepareizi personas kodi. Sistēmai jāpārbauda, vai personas kods ir derīgs, un nederīgi iesniegumi jānoraida.

## Pieņemšanas kritēriji (acceptance criteria)

| # | Ievade | Sagaidāmais rezultāts |
|---|---|---|
| 1 |32000000001|201|
| 2 |320000-00001|201, saglabāts bez defises|
| 3 |" 32000000001 "|201 (atstarpes noņemtas)|
| 4 |3200000001|400 INVALID_FORMAT|
| 5 |320000000132|400 INVALID_FORMAT|
| 6 |320000000O1|400 INVALID_FORMAT|
| 7 ||400 REQUIRED|
| 8 |010180-12345|201|
| 9 |3200-0000001|400 INVALID_FORMAT|

## Precizējumi (clarifications)

| Jautājums | Atbilde | Kas atbildēja, kad |
|---|---|---|
|Vai pirms validācijas personas kodam jānoņem sākuma un beigu atstarpes?|Jā, sākuma un beigu atstarpes tiek noņemtas.|Produkta īpašnieks, 05.10.2026.|
|Vai personas kods ar defisi 320000-00001 jāuzglabā ar defisi?|Nē, defise tiek noņemta un personas kods tiek saglabāts formātā 32000000001.|Produkta īpašnieks, 05.10.2026.|
| | | |

## Ārpus tvēruma (out of scope)

- Personas koda derīguma pārbaude pret PMLP vai citu ārēju reģistru; tiek pārbaudīts tikai ievades formāts.

## Komentāri (comments)

- 2026-09-28 · Reģistrācijas nodaļa: "Vakar 12 iesniegumi ar nepareizu kodu. Visi jālabo ar roku."
