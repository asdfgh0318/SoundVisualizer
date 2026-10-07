const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.33 x 7.5 in
pres.title = 'Pomiary w komorze';
const INK = '1F2A44', RED = 'D6336C', BLUE = '2B6CB0', MUTED = '5B6578';

// Slide 1: intro, the chamber as it is now
{
  const s = pres.addSlide();
  s.background = { color: '1F2A44' };
  s.addImage({ path: 'photo-chamber.jpg', x: 0, y: 0, w: 5.65, h: 7.5, sizing: { type: 'cover', w: 5.65, h: 7.5 }, altText: 'Komora w obecnej konfiguracji: pierścień z mikrofonami ułożony poziomo wokół stanowiska ze śmigłem, statyw z głośnikiem po lewej, materiał pochłaniający na podłodze, suficie i ścianach' });
  s.addText('W pogoni za okrągłym wykresem biegunowym', { x: 6.3, y: 2.9, w: 6.8, h: 1.4, fontFace: 'Cambria', fontSize: 34, bold: true, color: 'FFFFFF', margin: 0, valign: 'middle', isTextBox: true });
  s.addText('Nasza komora w obecnej konfiguracji (5 października 2026): jedenaście mikrofonów na pierścieniu wokół źródła, materiał pochłaniający na podłodze, suficie i ścianach.', { x: 6.3, y: 6.3, w: 6.3, h: 0.8, fontFace: 'Calibri', fontSize: 14, color: 'AFC3E3', margin: 0, valign: 'top', isTextBox: true });
  s.addNotes('Slajd tytułowy. Zdjęcie (komora_05_10_26.jpg) pokazuje komorę w konfiguracji końcowej (carpet-reordered): pierścień z mikrofonami ułożony poziomo wokół stanowiska ze śmigłem w środku, statyw z głośnikiem po lewej, włóknina na podłodze i suficie, kliny i obłożone słupki na ścianach. Średnica pierścienia 1,68 m (promień 0,84 m), jedenaście mikrofonów UMIK-2.');
}

// Slide 1: the problem
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-red.png', x: 0.6, y: 0.65, w: 6.2, h: 6.2, altText: 'Wykres biegunowy pomiaru śmigła z 31 sierpnia, 20–560 Hz, o postrzępionym kształcie' });
  s.addText('PROBLEM', { x: 7.4, y: 0.9, w: 5.3, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: RED, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Nasz wykres biegunowy jest postrzępiony', { x: 7.4, y: 1.3, w: 5.3, h: 1.3, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Mierzyliśmy śmigło, ustawiając łuk z mikrofonami w płaszczyźnie równoległej do tarczy śmigła.', options: { bullet: true, breakLine: true } },
    { text: 'Śmigło jest symetryczne względem swojej osi, więc każdy mikrofon powinien pokazywać mniej więcej to samo.', options: { bullet: true, breakLine: true } },
    { text: 'Spodziewaliśmy się gładkiego, prawie okrągłego wykresu. Zobaczyliśmy postrzępiony kształt.', options: { bullet: true, bold: true } },
  ], { x: 7.4, y: 2.75, w: 5.3, h: 2.6, fontFace: 'Calibri', fontSize: 16, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 10, isTextBox: true });
  s.addText('6,7 dB', { x: 7.4, y: 5.5, w: 5.3, h: 0.8, fontFace: 'Cambria', fontSize: 48, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('między najgłośniejszym a najcichszym z jedenastu mikrofonów', { x: 7.4, y: 6.3, w: 5.3, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, isTextBox: true });
  s.addText('31 sierpnia 2026, 20–560 Hz, silnik przy 2000 µs. Oś promieniowa 30–76 dB, taka sama jak w raporcie.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(2), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Dane: pomiar bazowy z 31 sierpnia 2026 (łuk ułożony poziomo, oś śmigła pionowo), śmigło przy PWM 2000, poziom całkowity 20–560 Hz na mikrofon, odczytany z fabrycznymi plikami kalibracyjnymi, tak jak był mierzony. Rozrzut skuteczny wokół średniej 2,05 dB, rozstęp 6,7 dB (63,9 do 70,6 dB SPL). Oś promieniowa 30–76 dB jest taka sama jak na wykresach w raporcie, więc ta sama czerwona krzywa może być pokazana obok pomiaru z 30 września na dalszym slajdzie. Na osi 0–80 dB ta sama krzywa wygląda na okrąglejszą.');
}



// Slide 2: what we did to fix it
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('NAPRAWA', { x: 0.6, y: 0.5, w: 6, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Co zrobiliśmy: każdy mikrofon, jeden głośnik', { x: 0.6, y: 0.9, w: 12.1, h: 0.8, fontFace: 'Cambria', fontSize: 32, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  // set-up: loudspeaker -> UMIK-2, capsule end towards the loudspeaker
  s.addImage({ path: 'photo-source.jpg', x: 0.9, y: 2.0, w: 2.1, h: 2.45, sizing: { type: 'cover', w: 2.1, h: 2.45 }, altText: 'Nasz głośnik: drukowana kula z głośnikiem o średnicy 8 cm' });
  s.addText('Nasz głośnik', { x: 0.6, y: 4.55, w: 2.7, h: 0.35, fontFace: 'Calibri', fontSize: 16, color: INK, align: 'center', margin: 0, isTextBox: true });
  s.addText('tony, 62 Hz–16 kHz', { x: 3.35, y: 2.55, w: 2.4, h: 0.35, fontFace: 'Calibri', fontSize: 14, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: 3.45, y: 3.25, w: 2.2, h: 0, line: { color: RED, width: 3, dashType: 'dash', endArrowType: 'triangle' } });
  s.addImage({ path: 'umik2-photo.png', x: 5.9, y: 2.75, w: 5.2, h: 1.405, altText: 'Mikrofon pomiarowy UMIK-2, kapsuła po lewej stronie zwrócona do głośnika' });
  s.addText('Mikrofon UMIK-2, kapsuła zwrócona do głośnika', { x: 5.9, y: 4.3, w: 6.8, h: 0.35, fontFace: 'Calibri', fontSize: 16, bold: true, color: BLUE, margin: 0, isTextBox: true });
  // settings
  s.addText([
    { text: '97 tonów na mikrofon, 62 Hz–16 kHz, 12 na oktawę (przemiatanie krokowe)', options: { bullet: true, breakLine: true } },
    { text: 'Jeden ton naraz: 0,7 s ustalania, 2 s zapisu (6 s poniżej 250 Hz)', options: { bullet: true, breakLine: true } },
    { text: 'Mikrofony wymieniane po kolei: ta sama pozycja, głośnik i poziom', options: { bullet: true, breakLine: true } },
    { text: 'Jeden mikrofon zmierzony trzy razy jako odniesienie', options: { bullet: true } },
  ], { x: 0.6, y: 5.2, w: 7.0, h: 1.65, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 5, isTextBox: true });
  // result
  s.addText([
    { text: '4,01', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '0,02 dB', options: { color: BLUE } },
  ], { x: 8.2, y: 5.05, w: 4.6, h: 0.75, fontFace: 'Cambria', fontSize: 40, bold: true, margin: 0, isTextBox: true });
  s.addText('rozrzut między jedenastoma mikrofonami dla tego samego dźwięku', { x: 8.2, y: 5.8, w: 4.6, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('7 z 11 fabrycznych plików odbiegało średnio o 0,8–2,6 dB', { x: 8.2, y: 6.35, w: 4.6, h: 0.5, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Sesja kalibracyjna 16 września 2026, amplituda głośnika 0,03 pełnej skali. Zdjęcie UMIK-2: karta produktu miniDSP.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('3', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Procedura (calibrator/session.py, sesja 16.09.2026): każdą z jedenastu kapsuł UMIK-2 podłączano po kolei w tym samym punkcie montażu przed głośnikiem i mierzono 97 tonów krokowych od 62 Hz do 16 kHz (około 12 na oktawę), amplituda 0,03, próbkowanie 48 kHz, 0,7 s na ustabilizowanie i 2 s zapisu na ton (6 s poniżej 250 Hz). Kapsułę 810-8904 zmierzono trzy razy w całości (18:21, 18:30, 20:43) jako odniesienie. Różnicę każdej kapsuły względem odniesienia dodano do jej krzywej kalibracyjnej; współczynniki czułości zostały takie jak w plikach fabrycznych. Wzorcem jest średnia czterech kapsuł, których pliki fabryczne zgadzają się z pomiarem (810-8900, 810-8903, 811-1896, 811-2321). Rozrzut 4,01 → 0,02 dB pochodzi z notatek projektu: to sprawdzenie w tej samej sesji, bo poprawki pochodzą z tej sesji, a poziom bezwzględny nie jest zakotwiczony (potrzebny kalibrator 94 dB). Siedem kapsuł ma średnie odchylenie powyżej 0,6 dB w funkcji częstotliwości, od 0,76 do 2,59 dB; najgorsza pojedyncza częstotliwość to 3,48 dB (811-1892), z pliku CORRECTIONS-2026-09-16.csv.');
}

// Slide 3: the waterfalls of the calibration, before and after
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-mic-slide-pl.png', x: 0.3, y: 0.3, w: 8.06, h: 6.4, altText: 'Mapy każdego mikrofonu w funkcji częstotliwości dla dwóch pomiarów: pliki fabryczne (góra), z poprawkami (środek), efekt poprawki (dół)' });
  s.addText('WYNIK', { x: 8.95, y: 0.7, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Poprawka usuwa przesunięcia mikrofonów', { x: 8.95, y: 1.05, w: 3.9, h: 1.7, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Góra', options: { bold: true } }, { text: ': pliki fabryczne. ' }, { text: 'Środek', options: { bold: true } }, { text: ': z poprawkami. ' }, { text: 'Dół', options: { bold: true } }, { text: ': co zmieniła poprawka.', options: { breakLine: true } },
    { text: 'Pasek przez wszystkie częstotliwości to jeden mikrofon, który pokazuje za głośno lub za cicho. W środkowym rzędzie go nie ma.', options: { bullet: true, breakLine: true } },
    { text: 'Obraz pomieszczenia zostaje: przesuwają się całe wiersze, a nie struktura częstotliwościowa.', options: { bullet: true } },
  ], { x: 8.95, y: 2.85, w: 3.9, h: 2.7, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 8, isTextBox: true });
  s.addText([
    { text: '4,3', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '0,8 dB', options: { color: BLUE } },
  ], { x: 8.95, y: 5.55, w: 3.9, h: 0.7, fontFace: 'Cambria', fontSize: 36, bold: true, margin: 0, isTextBox: true });
  s.addText('różnica między najgłośniejszym a najcichszym mikrofonem dla tego samego dźwięku: pliki fabryczne → z poprawkami (początek dnia 3; stan końcowy 4,1 → 1,0 dB)', { x: 8.95, y: 6.25, w: 3.9, h: 0.6, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Dwa pomiary z 25 września 2026: początek dnia 3 (po lewej) i konfiguracja końcowa (po prawej).', { x: 0.6, y: 6.95, w: 8.0, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('4', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Ten sam rysunek co w rozdziale 1 raportu, narysowany większy. Te same dwa pomiary skalibrowano na dwa sposoby: plikami fabrycznymi i poprawkami zmierzonymi 16 września. Rozstęp to zakres średnich poziomów kapsuł: 4,3 do 0,8 dB na początku dnia 3 i 4,1 do 1,0 dB w konfiguracji końcowej. Błąd pomieszczenia poniżej 3 kHz: 2,277 do 1,997 dB oraz 1,736 do 1,387 dB. Zmiana to głównie przesunięcie każdej kapsuły, więc głównie przesuwa całe wiersze.');
}

// Slide 4: the chamber treatments, day 3 start against the final state
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-wf-slide-pl.png', x: 0.3, y: 0.3, w: 7.59, h: 6.45, altText: 'Mapy każdego mikrofonu w funkcji częstotliwości: początek dnia 3, stan końcowy i różnica między nimi' });
  s.addText('KOMORA', { x: 8.95, y: 0.5, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Zabiegi wyrównują niskie częstotliwości', { x: 8.95, y: 0.85, w: 3.9, h: 1.2, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addChart(pres.charts.BAR, [
    { name: 'Początek dnia 3', labels: ['250–400', '400–630', '630–1000', '1000–1600', '1600–3000', '5000–6400'], values: [3.33, 2.57, 1.57, 0.8, 0.87, 1.04] },
    { name: 'Stan końcowy', labels: ['250–400', '400–630', '630–1000', '1000–1600', '1600–3000', '5000–6400'], values: [1.99, 1.52, 1.47, 0.85, 0.96, 1.17] },
  ], {
    x: 8.85, y: 2.05, w: 4.1, h: 2.75, barDir: 'col', barGrouping: 'clustered', chartColors: ['D6336C', '2B6CB0'], showLegend: true, legendPos: 'b', legendFontSize: 11, legendColor: INK, legendFontFace: 'Calibri',
    showTitle: true, title: 'Błąd pomieszczenia w pasmach (dB, pasmo w Hz)', titleFontSize: 12, titleColor: INK, titleFontFace: 'Calibri',
    catAxisLabelFontSize: 10, catAxisLabelColor: INK, catAxisLabelFontFace: 'Calibri', valAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valAxisLabelFontFace: 'Calibri', valAxisMinVal: 0, valAxisMaxVal: 4, valAxisMajorUnit: 1,
    valGridLine: { color: 'E3E7EE', size: 0.5 }, catGridLine: { style: 'none' }, barGapWidthPct: 50,
    showValue: true, dataLabelFontSize: 9, dataLabelColor: INK, dataLabelFontFace: 'Calibri', dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd',
  });
  s.addText([
    { text: '2,00', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '1,39 dB', options: { color: BLUE } },
  ], { x: 8.95, y: 4.85, w: 3.9, h: 0.65, fontFace: 'Cambria', fontSize: 34, bold: true, margin: 0, isTextBox: true });
  s.addText('błąd pomieszczenia poniżej 3 kHz', { x: 8.95, y: 5.5, w: 3.9, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  s.addText('Poprawiliśmy niskie częstotliwości (poniżej 630 Hz) o 1,2 dB: błąd spadł z 3,0 do 1,8 dB, czyli o 40 %. Powyżej 1 kHz tylko nieznaczne zmiany.', { x: 8.95, y: 5.85, w: 3.9, h: 0.95, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('25 września 2026. W ciągu dnia głośnik przesuwano i wrócił mniej więcej do punktu wyjścia; położenia nie zapisano. Błąd pomieszczenia: wartość skuteczna różnicy jedenastu mikrofonów od ich średniej.', { x: 0.6, y: 6.85, w: 11.4, h: 0.45, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('5', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Ta sama para co na stronie 3 raportu (day3-a o 13:17, carpet-reordered o 19:15, oba 25 września), odczytana z poprawionymi plikami mikrofonów. Błąd pomieszczenia to wartość skuteczna odchylenia jedenastu mikrofonów od ich średniej, w paśmie. Poniżej 630 Hz błąd skuteczny spadł z 2,98 do 1,78 dB (1,2 dB, 40 %); między 1 a 3 kHz zmienił się z 0,84 na 0,91 dB. Początek dnia 3: 3,33; 2,57; 1,57; 0,80; 0,87; 1,04 dB; stan końcowy: 1,99; 1,52; 1,47; 0,85; 0,96; 1,17 dB dla pasm 250–400, 400–630, 630–1000, 1000–1600, 1600–3000 i 5000–6400 Hz. Zastrzeżenie z raportu: w ciągu dnia głośnik przesuwano celowo (20 cm bliżej, do płaszczyzny pierścienia, 5 cm do tyłu), po czym wrócił mniej więcej do pozycji wyjściowej, której nie zapisano. Pochylenie mapy zmieniło się z −0,41 na −0,63, a średni poziom wzrósł o 1,16 dB, więc zysk to zabiegi plus niewielka, nieznana różnica położenia źródła, a część może wynikać z głośniejszego dźwięku bezpośredniego. Czysta para z nieruszanym źródłem to 24 września: pusta podłoga 2,054 do dywanu 1,317 dB.');
}

// Thinsulate ring wrap slide: left out of the deck on request; build it with WRAP_SLIDE=1
if (process.env.WRAP_SLIDE) {
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('THE RING WRAP', { x: 0.6, y: 0.5, w: 6, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Thinsulate on the ring hardly matters', { x: 0.6, y: 0.85, w: 12.1, h: 0.8, fontFace: 'Cambria', fontSize: 32, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Size of the change in room error (dB)', { x: 0.6, y: 1.9, w: 7.2, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addChart(pres.charts.BAR, [{ name: 'Change in room error (dB)', labels: ['Tripod wrap partly off (23 Sep)', 'Ring wrap, first part off (23 Sep)', 'Ring wrap, more off (23 Sep)', 'Rest of ring wrap off (24 Sep)', 'Handling alone (typical)', 'Carpet on the empty floor (24 Sep)'], values: [0.004, 0.018, 0.002, 0.014, 0.04, 0.737] }], {
    x: 0.5, y: 2.25, w: 7.7, h: 4.55, barDir: 'bar', chartColors: ['9AA5B8', '9AA5B8', '9AA5B8', '9AA5B8', 'C9CFDA', BLUE], catAxisOrientation: 'maxMin', catAxisLabelPos: 'low', catAxisLabelFrequency: 1,
    showLegend: false, showTitle: false, catAxisLabelFontSize: 13, catAxisLabelColor: INK, catAxisLabelFontFace: 'Calibri',
    valAxisMinVal: 0, valAxisMaxVal: 0.9, valAxisMajorUnit: 0.3, valAxisLabelFontSize: 12, valAxisLabelColor: MUTED, valAxisLabelFontFace: 'Calibri', valAxisLabelFormatCode: '0.0',
    valGridLine: { color: 'E3E7EE', size: 0.5 }, catGridLine: { style: 'none' }, barGapWidthPct: 45,
    showValue: true, dataLabelFontSize: 13, dataLabelColor: INK, dataLabelFontFace: 'Calibri', dataLabelFormatCode: '0.000', dataLabelPosition: 'outEnd',
  });
  s.addText('0.02 dB', { x: 8.6, y: 1.95, w: 4.2, h: 0.9, fontFace: 'Cambria', fontSize: 48, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('at most: the largest change in room error from taking any Thinsulate wrap off the ring or the tripod, in four cases.', { x: 8.6, y: 2.9, w: 4.2, h: 1.0, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Three cases got slightly worse, one slightly better: no clear effect.', options: { bullet: true, breakLine: true } },
    { text: 'The same state measured twice differs by 0.006–0.015 dB, and handling by about 0.04 dB.', options: { bullet: true, breakLine: true } },
    { text: 'The carpet on the empty floor changed the error 40 times more.', options: { bullet: true } },
  ], { x: 8.6, y: 4.1, w: 4.2, h: 2.6, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 8, isTextBox: true });
  s.addText('Runs: foam-out → tripod-unwrapped → ring-unwrapped → -2 (23 Sep); wall-direct-absorber → ring-bare (24 Sep). Carpet: 2.054 → 1.317 dB.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('6', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Source: README of the chamber trials (docs/analysis/chamber-treatments-2026-09-23) and the loudspeaker sessions, room error below 3 kHz. 23 Sep: foam-out 1.3837 to tripod-unwrapped 1.3874 (+0.004, some wrapping off the tripod legs); to ring-unwrapped 1.4057 (+0.018, part of the ring wrapping removed; a new hub mounting preset from there); to ring-unwrapped-2 1.4076 (+0.002, more of the ring unwrapped). 24 Sep, speaker on the wall (a different geometry): wall-direct-absorber 2.2193 to ring-bare 2.2054 (-0.014), the rest of the ring wrap removed, 10 minutes apart; map change 0.36 dB spread over all capsules. Three of the four changes are slightly worse, one slightly better. The README concludes the ring wrap is worth a little only at the high end, and that the best state measured was tripod bare and ring wrapped. Repeat floor 0.006-0.015 dB, handling about 0.04 dB (README). Carpet on the empty floor: 24 Sep floor-no-wedges 2.054 to chaotic-carpet 1.317 dB (-0.737), source unmoved. 0.737 / 0.018 = 40.');
}

// Slide 6: the band table of the evaluation, colour graded
{
  const T = JSON.parse(require('fs').readFileSync('table.json', 'utf8'));
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('OCENA', { x: 8.95, y: 0.5, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Pasmo po paśmie względem tolerancji ISO', { x: 8.95, y: 0.85, w: 3.9, h: 1.3, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const GRID = { type: 'solid', pt: 0.75, color: '9AA5B8' }, SEP = { type: 'solid', pt: 2, color: '4A5568' };
  const H = (t, extra = {}) => ({ text: t, options: Object.assign({ bold: true, fontFace: 'Calibri', fontSize: 12, color: INK, align: 'center', valign: 'middle', border: [GRID, GRID, GRID, GRID] }, extra) });
  const C = (t, fill, o = {}) => ({ text: t, options: Object.assign({ fontFace: 'Calibri', fontSize: 14, color: INK, align: 'center', valign: 'middle', fill: fill ? { color: fill } : undefined, border: [GRID, GRID, GRID, GRID] }, o) });
  const rows = [
    [H('Pasmo'), H('Limit'), H('Tony'), H('Początek dnia 3', { colspan: 2, color: RED, border: [GRID, GRID, GRID, SEP] }), H('Stan końcowy', { colspan: 2, color: BLUE, border: [GRID, GRID, GRID, SEP] })],
    [H('Hz'), H('± dB'), H('w paśmie'), H('najgorszy mikr., dB', { border: [GRID, GRID, GRID, SEP] }), H('komórki w limicie'), H('najgorszy mikr., dB', { border: [GRID, GRID, GRID, SEP] }), H('komórki w limicie')],
  ];
  T.rows.forEach((r) => rows.push([C(String(r.band), null, { bold: true }), C(r.limit.toFixed(1).replace('.', ','), null), C(String(r.tones), null), C(r.gdev.toFixed(2).replace('.', ','), r.gdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.gcells + ' %', r.gcellsc), C(r.xdev.toFixed(2).replace('.', ','), r.xdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.xcells + ' %', r.xcellsc)]));
  s.addTable(rows, { x: 0.6, y: 0.5, w: 7.9, colW: [0.85, 0.8, 0.85, 1.4, 1.3, 1.4, 1.3], rowH: [0.36, 0.32].concat(Array(T.rows.length).fill(0.43)), margin: [0.02, 0.04, 0.02, 0.04] });
  // colour key
  s.addText('Skala kolorów', { x: 8.95, y: 2.35, w: 3.9, h: 0.3, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, isTextBox: true });
  T.scale.forEach((c, i) => s.addShape(pres.shapes.RECTANGLE, { x: 8.95 + i * 0.78, y: 2.7, w: 0.78, h: 0.3, fill: { color: c }, line: { color: 'FFFFFF', width: 1 } }));
  s.addText('0', { x: 8.95, y: 3.03, w: 0.78, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('na limicie', { x: 8.95 + 2 * 0.78 - 0.1, y: 3.03, w: 0.98, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('≥ 2×', { x: 8.95 + 4 * 0.78 - 0.1, y: 3.03, w: 0.98, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('Najgorszy mikrofon jako ułamek limitu. Komórki: zielony 100 %, żółty 50 %, czerwony 0 %.', { x: 8.95, y: 3.35, w: 3.9, h: 0.55, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  // scorecard
  const g = T.card.g, x = T.card.x;
  s.addText([
    { text: 'Pasma ponad limitem (z 13): ' }, { text: `${g.over13} → ${x.over13}`, options: { bold: true, breakLine: true } },
    { text: 'Komórki w limicie (13 pasm): ' }, { text: `${g.cells13} % → ${x.cells13} %`, options: { bold: true } },
  ], { x: 8.95, y: 4.1, w: 3.9, h: 1.5, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 6, isTextBox: true });
  s.addText('* Pasma częściowe: zmierzono tylko tony powyżej 5 kHz (4 i 5 tonów). Zakres 3–5 kHz pominięto z powodu głośnika: jego membrana ma tryb kołyszący około 4,4 kHz. Wartości ISO służą jako analogia, nie jako kwalifikacja pomieszczenia.', { x: 8.95, y: 5.75, w: 3.9, h: 1.15, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('6', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Ta sama tabela co na stronie 4 raportu. Każde pasmo tercjowe oceniono względem wartości tolerancji dla komory bezechowej z tabeli 1 normy ISO 5305 (także ISO 3745 w ujęciu Cunefare 2003): ±1,5 dB dla 125–630 Hz, ±1,0 dB dla 800–5000 Hz. Liczba to odchylenie średniej pasma najgorszego mikrofonu od średniej łuku, w dB; kolor to ta liczba jako ułamek limitu. „Komórki w limicie” liczy komórki ton × mikrofon mieszczące się w limicie (3 tony × 11 mikrofonów = 33 komórki przy 250 Hz, gdzie siatka zaczyna się od 257 Hz). To analogia: normy używają przemieszczanego mikrofonu i badają zanik z odległością, my mamy jedenaście stałych mikrofonów na jednym promieniu. Pomieszczenie jest wygłuszone, ale nie zakwalifikowane. W tolerancji od 1250 Hz na początku dnia 3 i od 2000 Hz w stanie końcowym, do 2500 Hz. Wiersze z gwiazdką (5000 i 6300 Hz) są częściowe: 4 i 5 tonów powyżej 5 kHz, limit ±1,0 dB przy 5000 Hz i ±1,5 dB przy 6300 Hz (ISO 5305, tabela 1). Oba są ponad limitem w obu stanach (1,24 i 1,23 dB; 1,59 i 1,77 dB). Pasm 3150 i 4000 Hz nie pokazano: brak tonów między 3 a 5 kHz z powodu trybu kołyszącego kuli przy około 4,4 kHz. Zastrzeżenie: położenia głośnika nie zapisano w ciągu dnia.');
}

// Slide 7: the same polar with the 30 Sep measurement on top
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-both-pl.png', x: 0.6, y: 0.5, w: 5.95, h: 6.34, altText: 'Wykres biegunowy 20–560 Hz: postrzępiony czerwony kształt z 31 sierpnia i gładszy niebieski z 30 września' });
  s.addText('PORÓWNANIE', { x: 7.4, y: 0.9, w: 5.3, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('31 sierpnia i 30 września na tych samych osiach', { x: 7.4, y: 1.3, w: 5.3, h: 1.3, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Czerwony: 31 sierpnia, fabryczne pliki mikrofonów. Niebieski: 30 września, pliki z poprawkami. Dwa różne śmigła.', options: { bullet: true, breakLine: true } },
    { text: 'Między pomiarami śmigło zamontowano w przeciwną stronę, więc ciąg jest skierowany odwrotnie. Nie spodziewamy się, że to zmieni dźwięk.', options: { bullet: true, breakLine: true } },
    { text: 'Kształt z 30 września jest gładszy.', options: { bullet: true, bold: true } },
  ], { x: 7.4, y: 2.75, w: 5.3, h: 2.6, fontFace: 'Calibri', fontSize: 16, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 10, isTextBox: true });
  s.addText([
    { text: '6,7', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '4,0 dB', options: { color: BLUE } },
  ], { x: 7.4, y: 5.5, w: 5.3, h: 0.8, fontFace: 'Cambria', fontSize: 48, bold: true, margin: 0, isTextBox: true });
  s.addText('między najgłośniejszym a najcichszym mikrofonem', { x: 7.4, y: 6.3, w: 5.3, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, isTextBox: true });
  s.addText('20–560 Hz, silnik przy 2000 µs. Różne śmigła i warunki pracy, więc poziomów nie wolno porównywać; porównujemy kształty.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(7), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Niebieski: pomiar śmigła z 30 września (11,7 V, 7,3 A, ciąg −4 N), odczytany z poprawkami mikrofonów z 16 września. Rozrzut skuteczny wokół średniej 1,45 dB wobec 2,05 dB dla 31 sierpnia; rozstęp 4,0 dB (55,5 do 59,6 dB SPL) wobec 6,7 dB. Niebieski jest o około 11 dB niższy, ale nie można tego przypisać napięciu zasilania (niebieski miał wyższe napięcie): pomiary wykonano różnymi śmigłami, a kierunek ciągu był odwrócony, więc poziomów nie wolno porównywać. Rozstęp 4 dB niebieskiego to trend: głośniej na dole. Uczciwe zastrzeżenie: po zastosowaniu tej samej kalibracji do pomiarów z 1–2 września są one mniej więcej tak samo okrągłe jak z 30 września, więc większość poprawy względem wcześniejszych pomiarów bazowych pochodzi z kalibracji mikrofonów, nie z pomieszczenia.');
}


// Slide 8: the material measurements overlaid
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-materials-pl.png', x: 0.45, y: 0.45, w: 6.37, h: 6.35, altText: 'Wykres biegunowy pięciu wariantów materiałowych przy 2000 mikrosekundach: bez materiału, korek, guma, filc i filc z gumą' });
  s.addText('MATERIAŁY', { x: 7.6, y: 0.7, w: 5.2, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Pomiary materiałów przy 2000 µs', { x: 7.6, y: 1.05, w: 5.2, h: 1.3, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const items = [
    ['Bez materiału', 74.2, '1F2A44'],
    ['Filc + guma', 78.7, '7048E8'],
    ['Korek', 78.7, '2F9E44'],
    ['Filc', 79.5, '1098AD'],
    ['Guma', 80.6, 'F08C00'],
  ];
  s.addText('Średni poziom z jedenastu mikrofonów', { x: 7.6, y: 2.55, w: 5.2, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  items.forEach(([name, mean, col], i) => {
    const y = 2.9 + i * 0.46;
    s.addShape(pres.shapes.OVAL, { x: 7.6, y: y + 0.07, w: 0.26, h: 0.26, fill: { color: col }, line: { color: col, width: 0 } });
    s.addText(name, { x: 8.05, y, w: 2.6, h: 0.4, fontFace: 'Calibri', fontSize: 18, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(mean.toFixed(1).replace('.', ',') + ' dB', { x: 10.6, y, w: 2.2, h: 0.4, fontFace: 'Calibri', fontSize: 18, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  });
  s.addText('+4,5 do +6,4 dB', { x: 7.6, y: 5.3, w: 5.2, h: 0.8, fontFace: 'Cambria', fontSize: 40, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('głośniej niż bez materiału, średnio', { x: 7.6, y: 6.08, w: 5.2, h: 0.35, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, isTextBox: true });
  s.addText('Przy −90°, w strumieniu wylotowym (poza wykresem), wszystkie pięć spotyka się przy 94–98 dB.', { x: 7.6, y: 6.45, w: 5.2, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  s.addText('2 października 2026, śmigło 5-calowe, poziom całkowity 100 Hz–10 kHz, 2000 µs, pliki z poprawkami. Oś 65–90 dB.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('8', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Zestawy pomiarowe z 2 października 2026 w repozytorium danych: 2004__5in3b__unset__v1-naked-horizontal, ...cork__v1-cork-horizontal, ...rubber__v1-rubber, ...felt__v1-felt, ...felt-rubber__v1-felt-rubber. Każdy zapis to krok PWM 2000; poziom na mikrofon to poziom całkowity 100 Hz–10 kHz w dB SPL, odczytany z poprawionymi plikami mikrofonów (wszystkie po 16 września). Wykres jest odbity do 360 stopni. Średnia z jedenastu pozycji: bez materiału 74,2, korek 78,7, guma 80,6, filc 79,5, filc z gumą 78,7 dB. Przy −90 stopni (strumień wylotowy) wszystkie pięć mieści się w 93,7–98,3 dB. Slajd pokazuje poziomy tak, jak zmierzono; punktów pracy (napięcie, ciąg) tu nie porównywano.');
}

pres.writeFile({ fileName: 'chamber-slides-pl.pptx' }).then(() => console.log('written'));
