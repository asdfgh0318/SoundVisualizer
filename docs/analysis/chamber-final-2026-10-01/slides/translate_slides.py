"""Make build_slides_pl.cjs (Polish text, Polish figures) from build_slides.cjs. Run: python3 translate_slides.py"""
import re
s = open('build_slides.cjs', encoding='utf8').read()
L = {
 'Chamber measurements': 'Pomiary w komorze',
 'The chamber in its current set-up: the microphone ring laid flat around the propeller rig, speaker tripod on the left, absorbing material on floor, ceiling and walls': 'Komora w obecnej konfiguracji: pierścień z mikrofonami ułożony poziomo wokół stanowiska ze śmigłem, statyw z głośnikiem po lewej, materiał pochłaniający na podłodze, suficie i ścianach',
 'Chasing a round polar': 'W pogoni za okrągłym wykresem biegunowym',
 'Our chamber in its current set-up (5 Oct 2026): eleven microphones on a ring around the source, absorbing material on floor, ceiling and walls.': 'Nasza komora w obecnej konfiguracji (5 października 2026): jedenaście mikrofonów na pierścieniu wokół źródła, materiał pochłaniający na podłodze, suficie i ścianach.',
 'Polar plot of the 31 Aug propeller measurement, 20 to 560 Hz, with a jagged outline': 'Wykres biegunowy pomiaru śmigła z 31 sierpnia, 20–560 Hz, o postrzępionym kształcie',
 'THE PROBLEM': 'PROBLEM',
 'Our polar plot is jagged': 'Nasz wykres biegunowy jest postrzępiony',
 'We measured a propeller with the microphone arc in a plane parallel to the propeller disc.': 'Mierzyliśmy śmigło, ustawiając łuk z mikrofonami w płaszczyźnie równoległej do tarczy śmigła.',
 'A propeller is symmetric around its axis, so every microphone should read about the same.': 'Śmigło jest symetryczne względem swojej osi, więc każdy mikrofon powinien pokazywać mniej więcej to samo.',
 'We expected a smooth, nearly round polar. We observed a jagged outline.': 'Spodziewaliśmy się gładkiego, prawie okrągłego wykresu. Zobaczyliśmy postrzępiony kształt.',
 '6.7 dB': '6,7 dB',
 'between the loudest and quietest of the eleven microphones': 'między najgłośniejszym a najcichszym z jedenastu mikrofonów',
 '31 Aug 2026, 20–560 Hz, motor at 2000 µs. Radial axis 30–76 dB, the same as in the report.': '31 sierpnia 2026, 20–560 Hz, silnik przy 2000 µs. Oś promieniowa 30–76 dB, taka sama jak w raporcie.',
 'THE FIX': 'NAPRAWA',
 'What we did: every microphone, one loudspeaker': 'Co zrobiliśmy: każdy mikrofon, jeden głośnik',
 'Our loudspeaker: a printed sphere with an 8 cm driver': 'Nasz głośnik: drukowana kula z głośnikiem o średnicy 8 cm',
 'Our loudspeaker': 'Nasz głośnik',
 'tones, 62 Hz–16 kHz': 'tony, 62 Hz–16 kHz',
 'UMIK-2 measurement microphone, capsule end on the left facing the loudspeaker': 'Mikrofon pomiarowy UMIK-2, kapsuła po lewej stronie zwrócona do głośnika',
 'UMIK-2 microphone, capsule faces the loudspeaker': 'Mikrofon UMIK-2, kapsuła zwrócona do głośnika',
 '97 tones per microphone, 62 Hz to 16 kHz, 12 per octave (a stepped sweep)': '97 tonów na mikrofon, 62 Hz–16 kHz, 12 na oktawę (przemiatanie krokowe)',
 'One tone at a time: 0.7 s to settle, then 2 s recorded (6 s below 250 Hz)': 'Jeden ton naraz: 0,7 s ustalania, 2 s zapisu (6 s poniżej 250 Hz)',
 'Microphones swapped in turn: same position, same loudspeaker, same level': 'Mikrofony wymieniane po kolei: ta sama pozycja, głośnik i poziom',
 'One microphone measured three times as the reference': 'Jeden mikrofon zmierzony trzy razy jako odniesienie',
 '4.01': '4,01', '0.02 dB': '0,02 dB',
 'spread across the eleven microphones for the same sound': 'rozrzut między jedenastoma mikrofonami dla tego samego dźwięku',
 '7 of 11 factory files were off by 0.8–2.6 dB on average': '7 z 11 fabrycznych plików odbiegało średnio o 0,8–2,6 dB',
 'Calibration session 16 Sep 2026, loudspeaker amplitude 0.03 of full scale. UMIK-2 photo: miniDSP product brief.': 'Sesja kalibracyjna 16 września 2026, amplituda głośnika 0,03 pełnej skali. Zdjęcie UMIK-2: karta produktu miniDSP.',
 'Maps of each microphone against frequency for two captures: factory files (top), corrected (middle), effect of the correction (bottom)': 'Mapy każdego mikrofonu w funkcji częstotliwości dla dwóch pomiarów: pliki fabryczne (góra), z poprawkami (środek), efekt poprawki (dół)',
 'THE RESULT': 'WYNIK',
 'The correction removes the microphone offsets': 'Poprawka usuwa przesunięcia mikrofonów',
 'Top': 'Góra', ': factory files. ': ': pliki fabryczne. ', 'Middle': 'Środek', ': corrected. ': ': z poprawkami. ', 'Bottom': 'Dół', ': what the correction changed.': ': co zmieniła poprawka.',
 'A stripe across all frequencies is one microphone reading too loud or too quiet. The middle row has none.': 'Pasek przez wszystkie częstotliwości to jeden mikrofon, który pokazuje za głośno lub za cicho. W środkowym rzędzie go nie ma.',
 'The room pattern stays: whole rows move, not the frequency structure.': 'Obraz pomieszczenia zostaje: przesuwają się całe wiersze, a nie struktura częstotliwościowa.',
 '4.3': '4,3', '0.8 dB': '0,8 dB',
 'gap between the loudest and quietest microphone for the same sound: factory files → corrected (start of day 3; final state 4.1 → 1.0 dB)': 'różnica między najgłośniejszym a najcichszym mikrofonem dla tego samego dźwięku: pliki fabryczne → z poprawkami (początek dnia 3; stan końcowy 4,1 → 1,0 dB)',
 'Two captures from 25 Sep 2026: the start of day 3 (left) and the final configuration (right).': 'Dwa pomiary z 25 września 2026: początek dnia 3 (po lewej) i konfiguracja końcowa (po prawej).',
 'Maps of each microphone against frequency: start of day 3, final state, and the change between them': 'Mapy każdego mikrofonu w funkcji częstotliwości: początek dnia 3, stan końcowy i różnica między nimi',
 'THE CHAMBER': 'KOMORA',
 'The treatments flatten the low end': 'Zabiegi wyrównują niskie częstotliwości',
 'Start of day 3': 'Początek dnia 3', 'Final': 'Stan końcowy',
 'Room error per band (dB, band in Hz)': 'Błąd pomieszczenia w pasmach (dB, pasmo w Hz)',
 '2.00': '2,00', '1.39 dB': '1,39 dB',
 'room error below 3 kHz': 'błąd pomieszczenia poniżej 3 kHz',
 'We improved the low end (below 630 Hz) by 1.2 dB: the error fell from 3.0 to 1.8 dB, 40 % lower. Above 1 kHz only marginal changes.': 'Poprawiliśmy niskie częstotliwości (poniżej 630 Hz) o 1,2 dB: błąd spadł z 3,0 do 1,8 dB, czyli o 40 %. Powyżej 1 kHz tylko nieznaczne zmiany.',
 '25 Sep 2026. The loudspeaker was moved during the day and returned to about its starting point; the position was not documented. Room error: rms difference of the eleven microphones from their average.': '25 września 2026. W ciągu dnia głośnik przesuwano i wrócił mniej więcej do punktu wyjścia; położenia nie zapisano. Błąd pomieszczenia: wartość skuteczna różnicy jedenastu mikrofonów od ich średniej.',
 'THE EVALUATION': 'OCENA',
 'Band by band against the ISO tolerance': 'Pasmo po paśmie względem tolerancji ISO',
 'Band': 'Pasmo', 'Tones': 'Tony', 'per band': 'w paśmie', 'worst mic, dB': 'najgorszy mikr., dB', 'cells in limit': 'komórki w limicie',
 'Colour key': 'Skala kolorów', 'at the limit': 'na limicie', '2× or more': '≥ 2×',
 'Worst microphone as a share of the limit. Cells: green 100 %, yellow 50 %, red 0 %.': 'Najgorszy mikrofon jako ułamek limitu. Komórki: zielony 100 %, żółty 50 %, czerwony 0 %.',
 'Bands clearly over (of 13): ': 'Pasma ponad limitem (z 13): ', 'Cells in limit (13 bands): ': 'Komórki w limicie (13 pasm): ',
 '* Partial bands: only the tones above 5 kHz are measured (4 and 5 tones). 3–5 kHz is left out because of the loudspeaker: its cone has a rocking mode near 4.4 kHz. ISO values are an analogue, not a qualification of the room.': '* Pasma częściowe: zmierzono tylko tony powyżej 5 kHz (4 i 5 tonów). Zakres 3–5 kHz pominięto z powodu głośnika: jego membrana ma tryb kołyszący około 4,4 kHz. Wartości ISO służą jako analogia, nie jako kwalifikacja pomieszczenia.',
 'Polar plot of 20 to 560 Hz: the jagged red 31 Aug outline and the smoother blue 30 Sep outline': 'Wykres biegunowy 20–560 Hz: postrzępiony czerwony kształt z 31 sierpnia i gładszy niebieski z 30 września',
 'COMPARISON': 'PORÓWNANIE',
 '31 Aug and 30 Sep on the same axes': '31 sierpnia i 30 września na tych samych osiach',
 'Red: 31 Aug, factory microphone files. Blue: 30 Sep, corrected files. Two different propellers.': 'Czerwony: 31 sierpnia, fabryczne pliki mikrofonów. Niebieski: 30 września, pliki z poprawkami. Dwa różne śmigła.',
 'The propeller was mounted the other way round between the two, so the thrust points the other way. We do not expect this to change the sound.': 'Między pomiarami śmigło zamontowano w przeciwną stronę, więc ciąg jest skierowany odwrotnie. Nie spodziewamy się, że to zmieni dźwięk.',
 'The 30 Sep outline is smoother.': 'Kształt z 30 września jest gładszy.',
 '6.7': '6,7', '4.0 dB': '4,0 dB',
 'between the loudest and quietest microphone': 'między najgłośniejszym a najcichszym mikrofonem',
 '20–560 Hz, motor at 2000 µs. Different propellers and run conditions, so the levels are not comparable; compare the shapes.': '20–560 Hz, silnik przy 2000 µs. Różne śmigła i warunki pracy, więc poziomów nie wolno porównywać; porównujemy kształty.',
 'Polar plot of five material set-ups at 2000 microseconds: naked, cork, rubber, felt and felt with rubber': 'Wykres biegunowy pięciu wariantów materiałowych przy 2000 mikrosekundach: bez materiału, korek, guma, filc i filc z gumą',
 'THE MATERIALS': 'MATERIAŁY',
 'Material measurements at 2000 µs': 'Pomiary materiałów przy 2000 µs',
 'Bare': 'Bez materiału', 'Cork': 'Korek', 'Rubber': 'Guma', 'Felt': 'Filc', 'Felt + rubber': 'Filc + guma',
 'Mean level over the eleven microphones': 'Średni poziom z jedenastu mikrofonów',
 '+4.5 to +6.4 dB': '+4,5 do +6,4 dB',
 'louder than bare, on average': 'głośniej niż bez materiału, średnio',
 'At −90°, in the outflow (off the plot), all five meet at 94–98 dB.': 'Przy −90°, w strumieniu wylotowym (poza wykresem), wszystkie pięć spotyka się przy 94–98 dB.',
 '2 Oct 2026, 5-inch 3-blade propeller, total level 100 Hz–10 kHz, motor at 2000 µs, corrected microphone files. Radial axis 65–90 dB.': '2 października 2026, śmigło 5-calowe, poziom całkowity 100 Hz–10 kHz, 2000 µs, pliki z poprawkami. Oś 65–90 dB.',
}
N = {  # speaker notes, keyed by the first words
 'Intro slide.': 'Slajd tytułowy. Zdjęcie (komora_05_10_26.jpg) pokazuje komorę w konfiguracji końcowej (carpet-reordered): pierścień z mikrofonami ułożony poziomo wokół stanowiska ze śmigłem w środku, statyw z głośnikiem po lewej, włóknina na podłodze i suficie, kliny i obłożone słupki na ścianach. Średnica pierścienia 1,68 m (promień 0,84 m), jedenaście mikrofonów UMIK-2.',
 'Data: the 31 Aug': 'Dane: pomiar bazowy z 31 sierpnia 2026 (łuk ułożony poziomo, oś śmigła pionowo), śmigło przy PWM 2000, poziom całkowity 20–560 Hz na mikrofon, odczytany z fabrycznymi plikami kalibracyjnymi, tak jak był mierzony. Rozrzut skuteczny wokół średniej 2,05 dB, rozstęp 6,7 dB (63,9 do 70,6 dB SPL). Oś promieniowa 30–76 dB jest taka sama jak na wykresach w raporcie, więc ta sama czerwona krzywa może być pokazana obok pomiaru z 30 września na dalszym slajdzie. Na osi 0–80 dB ta sama krzywa wygląda na okrąglejszą.',
 'Procedure (calibrator': 'Procedura (calibrator/session.py, sesja 16.09.2026): każdą z jedenastu kapsuł UMIK-2 podłączano po kolei w tym samym punkcie montażu przed głośnikiem i mierzono 97 tonów krokowych od 62 Hz do 16 kHz (około 12 na oktawę), amplituda 0,03, próbkowanie 48 kHz, 0,7 s na ustabilizowanie i 2 s zapisu na ton (6 s poniżej 250 Hz). Kapsułę 810-8904 zmierzono trzy razy w całości (18:21, 18:30, 20:43) jako odniesienie. Różnicę każdej kapsuły względem odniesienia dodano do jej krzywej kalibracyjnej; współczynniki czułości zostały takie jak w plikach fabrycznych. Wzorcem jest średnia czterech kapsuł, których pliki fabryczne zgadzają się z pomiarem (810-8900, 810-8903, 811-1896, 811-2321). Rozrzut 4,01 → 0,02 dB pochodzi z notatek projektu: to sprawdzenie w tej samej sesji, bo poprawki pochodzą z tej sesji, a poziom bezwzględny nie jest zakotwiczony (potrzebny kalibrator 94 dB). Siedem kapsuł ma średnie odchylenie powyżej 0,6 dB w funkcji częstotliwości, od 0,76 do 2,59 dB; najgorsza pojedyncza częstotliwość to 3,48 dB (811-1892), z pliku CORRECTIONS-2026-09-16.csv.',
 'Same figure as chapter 1': 'Ten sam rysunek co w rozdziale 1 raportu, narysowany większy. Te same dwa pomiary skalibrowano na dwa sposoby: plikami fabrycznymi i poprawkami zmierzonymi 16 września. Rozstęp to zakres średnich poziomów kapsuł: 4,3 do 0,8 dB na początku dnia 3 i 4,1 do 1,0 dB w konfiguracji końcowej. Błąd pomieszczenia poniżej 3 kHz: 2,277 do 1,997 dB oraz 1,736 do 1,387 dB. Zmiana to głównie przesunięcie każdej kapsuły, więc głównie przesuwa całe wiersze.',
 'Same pair as page 3': 'Ta sama para co na stronie 3 raportu (day3-a o 13:17, carpet-reordered o 19:15, oba 25 września), odczytana z poprawionymi plikami mikrofonów. Błąd pomieszczenia to wartość skuteczna odchylenia jedenastu mikrofonów od ich średniej, w paśmie. Poniżej 630 Hz błąd skuteczny spadł z 2,98 do 1,78 dB (1,2 dB, 40 %); między 1 a 3 kHz zmienił się z 0,84 na 0,91 dB. Początek dnia 3: 3,33; 2,57; 1,57; 0,80; 0,87; 1,04 dB; stan końcowy: 1,99; 1,52; 1,47; 0,85; 0,96; 1,17 dB dla pasm 250–400, 400–630, 630–1000, 1000–1600, 1600–3000 i 5000–6400 Hz. Zastrzeżenie z raportu: w ciągu dnia głośnik przesuwano celowo (20 cm bliżej, do płaszczyzny pierścienia, 5 cm do tyłu), po czym wrócił mniej więcej do pozycji wyjściowej, której nie zapisano. Pochylenie mapy zmieniło się z −0,41 na −0,63, a średni poziom wzrósł o 1,16 dB, więc zysk to zabiegi plus niewielka, nieznana różnica położenia źródła, a część może wynikać z głośniejszego dźwięku bezpośredniego. Czysta para z nieruszanym źródłem to 24 września: pusta podłoga 2,054 do dywanu 1,317 dB.',
 'Same table as page 4': 'Ta sama tabela co na stronie 4 raportu. Każde pasmo tercjowe oceniono względem wartości tolerancji dla komory bezechowej z tabeli 1 normy ISO 5305 (także ISO 3745 w ujęciu Cunefare 2003): ±1,5 dB dla 125–630 Hz, ±1,0 dB dla 800–5000 Hz. Liczba to odchylenie średniej pasma najgorszego mikrofonu od średniej łuku, w dB; kolor to ta liczba jako ułamek limitu. „Komórki w limicie” liczy komórki ton × mikrofon mieszczące się w limicie (3 tony × 11 mikrofonów = 33 komórki przy 250 Hz, gdzie siatka zaczyna się od 257 Hz). To analogia: normy używają przemieszczanego mikrofonu i badają zanik z odległością, my mamy jedenaście stałych mikrofonów na jednym promieniu. Pomieszczenie jest wygłuszone, ale nie zakwalifikowane. W tolerancji od 1250 Hz na początku dnia 3 i od 2000 Hz w stanie końcowym, do 2500 Hz. Wiersze z gwiazdką (5000 i 6300 Hz) są częściowe: 4 i 5 tonów powyżej 5 kHz, limit ±1,0 dB przy 5000 Hz i ±1,5 dB przy 6300 Hz (ISO 5305, tabela 1). Oba są ponad limitem w obu stanach (1,24 i 1,23 dB; 1,59 i 1,77 dB). Pasm 3150 i 4000 Hz nie pokazano: brak tonów między 3 a 5 kHz z powodu trybu kołyszącego kuli przy około 4,4 kHz. Zastrzeżenie: położenia głośnika nie zapisano w ciągu dnia.',
 'Blue: 30 Sep': 'Niebieski: pomiar śmigła z 30 września (11,7 V, 7,3 A, ciąg −4 N), odczytany z poprawkami mikrofonów z 16 września. Rozrzut skuteczny wokół średniej 1,45 dB wobec 2,05 dB dla 31 sierpnia; rozstęp 4,0 dB (55,5 do 59,6 dB SPL) wobec 6,7 dB. Niebieski jest o około 11 dB niższy, ale nie można tego przypisać napięciu zasilania (niebieski miał wyższe napięcie): pomiary wykonano różnymi śmigłami, a kierunek ciągu był odwrócony, więc poziomów nie wolno porównywać. Rozstęp 4 dB niebieskiego to trend: głośniej na dole. Uczciwe zastrzeżenie: po zastosowaniu tej samej kalibracji do pomiarów z 1–2 września są one mniej więcej tak samo okrągłe jak z 30 września, więc większość poprawy względem wcześniejszych pomiarów bazowych pochodzi z kalibracji mikrofonów, nie z pomieszczenia.',
 'Bases of 2 Oct': 'Zestawy pomiarowe z 2 października 2026 w repozytorium danych: 2004__5in3b__unset__v1-naked-horizontal, ...cork__v1-cork-horizontal, ...rubber__v1-rubber, ...felt__v1-felt, ...felt-rubber__v1-felt-rubber. Każdy zapis to krok PWM 2000; poziom na mikrofon to poziom całkowity 100 Hz–10 kHz w dB SPL, odczytany z poprawionymi plikami mikrofonów (wszystkie po 16 września). Wykres jest odbity do 360 stopni. Średnia z jedenastu pozycji: bez materiału 74,2, korek 78,7, guma 80,6, filc 79,5, filc z gumą 78,7 dB. Przy −90 stopni (strumień wylotowy) wszystkie pięć mieści się w 93,7–98,3 dB. Slajd pokazuje poziomy tak, jak zmierzono; punktów pracy (napięcie, ciąg) tu nie porównywano.',
}
dis = s.index('if (process.env.WRAP_SLIDE)'); end = s.index('// Slide 6: the band table')
head, mid, tail = s[:dis], s[dis:end], s[end:]
def tr(part):
    for en, pl in sorted(L.items(), key=lambda kv: -len(kv[0])):
        part = part.replace("'" + en + "'", "'" + pl.replace("'", "\\'") + "'")
    def notes(m):
        t = m.group(1)
        for k, v in N.items():
            if t.startswith(k): return "s.addNotes('" + v.replace("'", "\\'") + "')"
        return m.group(0)
    part = re.sub(r"s\.addNotes\('((?:[^'\\]|\\.)+)'\)", notes, part)
    return part
out = tr(head) + mid + tr(tail)
for a, b in (("'polar-both.png'", "'polar-both-pl.png'"), ("'fig-mic-slide.png'", "'fig-mic-slide-pl.png'"), ("'fig-wf-slide.png'", "'fig-wf-slide-pl.png'"), ("'polar-materials.png'", "'polar-materials-pl.png'"), ("'materials.json'", "'materials-pl.json'"), ("chamber-slides-final.pptx", "chamber-slides-final-pl.pptx")):
    out = out.replace(a, b)
# decimal commas in numbers built in code
out = out.replace("r.gdev.toFixed(2)", "r.gdev.toFixed(2).replace('.', ',')").replace("r.xdev.toFixed(2)", "r.xdev.toFixed(2).replace('.', ',')").replace("r.limit.toFixed(1)", "r.limit.toFixed(1).replace('.', ',')").replace("mean.toFixed(1)", "mean.toFixed(1).replace('.', ',')")
out = out.replace("fontSize: 40, bold: true, color: 'FFFFFF'", "fontSize: 34, bold: true, color: 'FFFFFF'")
for t in ('Nasz wykres biegunowy jest postrzępiony', 'Poprawka usuwa przesunięcia mikrofonów', 'Zabiegi wyrównują niskie częstotliwości', '31 sierpnia i 30 września na tych samych osiach', 'Pasmo po paśmie względem tolerancji ISO', 'Pomiary materiałów przy 2000 µs'):
    i = out.index("'" + t + "'"); j = out.index('fontSize:', i); k = out.index(',', j)
    out = out[:j] + 'fontSize: 26' + out[k:]
open('build_slides_pl.cjs', 'w', encoding='utf8').write(out)
left = re.findall(r"(?:addText|text:)\s*\(?'([^']*[A-Za-z]{4,}[^']*)'", out)
print('written build_slides_pl.cjs')
