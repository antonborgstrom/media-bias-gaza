# Mediebias-analys av riksmediers rapportering av Israel/Palestina-konflikten

Kodbas för Dagens ETC:s textanalys av artiklar om Israel/Palestina-konflikten efter terrorattacken den 7 oktober 2023.

Inspiration för analys och kod hämtad från Ellen Helker-Nygrens och Stehpan L:s [artikel](https://ellenhelkernygren.substack.com/p/stark-pro-israelisk-bias-i-dagens) och [kod](https://github.com/ellenhn/dn-medie-bias-gaza).

## Resultat
Resultatet från körningarna har analyserats vidare och sammanställts i artiklar i Dagens ETC den 17 september 2024.

## Rådata
All rådata som använts i den här analysen har hämtats från arkivtjänsten Retreiver. Materialet kan inte läggas upp på grund av upphovsrättsskäl, men exempel på formattering finns i articles-example.txt

## Metod
Vi analyserade 7 918 artiklar mellan den 7:e oktober 2023 – 31 augusti 2024 för att få en översikt av de mönster som genomsyrar medierapporteringen i det senaste kriget i Gaza i Aftonbladet, Dagens ETC, Dagens Nyheter, Expressen, Göteborgs-Posten, Svenska Dagbladet, Sveriges Radio, SVT Nyheter och Sydsvenskan.

Denna analys gjordes i två delar: 
 1. Vi undersökte hur ofta israeliska och palestinska dödsfall nämns.
 2. Vi granskade hur ofta olika känsloladdade ord används för att beskriva israeliska och palestinska dödsfall (t ex ”blodig,” ”brutal,” ”massaker”), samt hur ofta andra relevanta ord nämns, inklusive ”antisemitism” och ”islamofobi.”

 ### AI-analys
 För att klassificera vilka meningar som handlar om palestinier respektive israeler har artiklarna analyserats och kategoriserats med hjälp av OpenAI:s modell gpt-4o-2024-08-06. 
 