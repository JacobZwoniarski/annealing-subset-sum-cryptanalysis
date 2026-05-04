# Plan projektu: subset-sum / Merkle-Hellman / QUBO / annealing

## 1. Cel dokumentu

Ten dokument ma być **punktem startowym do nowej konwersacji i implementacji projektu**. Zawiera:

- precyzyjnie wybrany temat,
- zakres `MVP`,
- architekturę kodu,
- kolejność implementacji,
- plan eksperymentów,
- plan raportu,
- kryteria ukończenia projektu.

Po tym dokumencie nie powinno już być potrzeby wracania do decyzji typu „co właściwie robimy”.

## 2. Ostatecznie wybrany temat

### Tytuł roboczy

**Modelowanie problemu subset-sum jako QUBO i analiza jego rozwiązywania metodami annealingowymi w kontekście kryptosystemu Merkle'a-Hellmana**

### Wersja skrócona

**Kryptoanaliza toy-instancji Merkle'a-Hellmana przez QUBO i annealing**

## 3. Główna idea projektu

Projekt będzie polegał na:

1. implementacji prostego kryptosystemu `Merkle-Hellman`,
2. sprowadzeniu problemu odzyskania wiadomości z publicznego plecaka do postaci `QUBO`,
3. rozwiązaniu tego problemu kilkoma metodami:
   - `brute force` dla małych instancji,
   - ewentualnie `dynamic programming` dla klasycznego `subset-sum`,
   - `exact solver` dla bardzo małych modeli `QUBO`,
   - `simulated annealing`,
   - opcjonalnie `tabu` lub inny solver z ekosystemu `dimod`,
4. porównaniu skuteczności i kosztu obliczeniowego tych podejść.

Projekt ma charakter:

- edukacyjny,
- badawczo-implementacyjny,
- demonstracyjny,
- uczciwie ograniczony do małych i średnich rozmiarów instancji.

## 4. Pytanie badawcze

Najlepsza wersja pytania badawczego:

> Na ile podejście `QUBO + annealing` nadaje się do rozwiązywania małych instancji problemu `subset-sum` występujących w toy-wersji kryptosystemu `Merkle-Hellman`, oraz jak wypada względem prostych metod klasycznych?

## 5. Hipoteza robocza

Rozsądna hipoteza do raportu:

> Dla małych instancji problemu `subset-sum` da się skutecznie odzyskiwać wiadomości metodą opartą o model `QUBO` i solver annealingowy, ale skuteczność oraz koszt obliczeń będą silnie zależne od rozmiaru instancji i jakości kodowania problemu.

To jest dobra hipoteza, bo:

- nie obiecuje za dużo,
- jest testowalna,
- daje miejsce na uczciwe wnioski negatywne.

## 6. Zakres projektu

### 6.1. Co wchodzi do zakresu

Wchodzi do zakresu:

- teoria `subset-sum`,
- teoria i implementacja `Merkle-Hellman`,
- teoria `QUBO`,
- teoria `annealing` w wersji praktycznej,
- redukcja problemu odzyskania bitów wiadomości do `QUBO`,
- benchmark kilku solverów,
- eksperymenty i wykresy,
- raport w stylu naukowym.

### 6.2. Co nie wchodzi do zakresu

Poza zakresem:

- pełna kryptografia postkwantowa,
- fizyczny komputer kwantowy jako wymóg,
- realne łamanie współczesnych bezpiecznych systemów,
- formalny dowód bezpieczeństwa,
- duże instancje przemysłowe,
- publikacyjny „breakthrough”.

## 7. MVP projektu

Minimalna wersja projektu, która ma zostać dowieziona:

1. implementacja `Merkle-Hellman`:
   - generacja kluczy,
   - szyfrowanie,
   - deszyfrowanie legalne,
2. generacja instancji ataku:
   - publiczny wektor wag,
   - ciphertext jako suma podzbioru wag,
3. redukcja odzyskania bitów wiadomości do `QUBO`,
4. implementacja solvera:
   - `brute force`,
   - `simulated annealing`,
5. porównanie obu metod na serii małych instancji,
6. zapis wyników do `CSV`,
7. wygenerowanie co najmniej 3 wykresów do raportu,
8. przygotowanie notebooka demonstracyjnego do prezentacji wyników.

Jeżeli zostanie czas, rozszerzenia:

- `dimod.ExactSolver` dla bardzo małych instancji,
- `tabu sampler`,
- badanie wpływu parametrów annealingu,
- porównanie kilku kodowań `QUBO`.

## 8. Architektura implementacji

### 8.1. Stos technologiczny

Rekomendowany stack:

- `Python 3.12+`,
- zarządzanie środowiskiem: `uv`,
- notebook demonstracyjny: `JupyterLab`,
- testy: `pytest`,
- obliczenia: `numpy`,
- dane eksperymentalne: `pandas`,
- wykresy: `matplotlib`, opcjonalnie `seaborn`,
- `QUBO/BQM`: `dimod`,
- annealing: `neal`,
- opcjonalnie dodatkowe samplery z ekosystemu `dwave-ocean`.

### 8.2. Struktura repozytorium

```text
Projekt_Krypto/
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
│   ├── qkd_tls_pqc_proxy_blueprint.md
│   └── subset_sum_merkle_hellman_qubo_plan.md
├── notebooks/
│   └── 01_demo_visualization.ipynb
├── src/
│   └── annealing_crypto/
│       ├── __init__.py
│       ├── config.py
│       ├── types.py
│       ├── utils.py
│       ├── subset_sum.py
│       ├── merkle_hellman.py
│       ├── qubo.py
│       ├── metrics.py
│       ├── solvers/
│       │   ├── brute_force.py
│       │   ├── exact_qubo.py
│       │   ├── simulated_annealing.py
│       │   └── tabu_optional.py
│       ├── experiments/
│       │   ├── run_benchmark.py
│       │   ├── scenarios.py
│       │   └── export_results.py
│       └── cli/
│           ├── demo.py
│           └── benchmark.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── experiments/
│   ├── configs/
│   ├── raw/
│   ├── processed/
│   └── plots/
└── report/
    ├── main.tex
    ├── bibliography.bib
    └── figures/
```

### 8.3. Odpowiedzialności modułów

`subset_sum.py`

- definicje problemu,
- generacja instancji,
- walidacja rozwiązania.

`merkle_hellman.py`

- generacja klucza prywatnego i publicznego,
- szyfrowanie wiadomości,
- legalne deszyfrowanie,
- generacja instancji ataku.

`qubo.py`

- budowa modelu `QUBO` dla odzyskania wiadomości,
- transformacja do struktury akceptowanej przez `dimod`,
- ewentualna normalizacja wag.

`solvers/`

- każda metoda ma osobny, cienki interfejs:
  - wejście: instancja problemu lub model `QUBO`,
  - wyjście: kandydat rozwiązania, wartość funkcji celu, czas, metadane.

`experiments/`

- uruchamianie serii testów,
- agregacja wyników,
- zapis danych do plików.

`notebooks/`

- notebook ma służyć do demonstracji projektu prowadzącemu,
- ma wczytywać gotowe wyniki z `experiments/raw/` i `experiments/processed/`,
- może uruchamiać małe przykłady pokazowe,
- nie powinien zawierać głównej logiki kryptograficznej ani implementacji solverów.

### 8.4. Rola notebooka Jupyter

Notebook jest dodatkiem prezentacyjnym, nie głównym interfejsem projektu.

Powinien umożliwiać:

- pokazanie przykładowego klucza `Merkle-Hellman`,
- zaszyfrowanie krótkiej wiadomości,
- zbudowanie odpowiadającego modelu `QUBO`,
- uruchomienie małego przykładu solvera annealingowego,
- wczytanie gotowych wyników benchmarku,
- wyświetlenie wykresów bez potrzeby ręcznego odpalania wielu skryptów.

Dobra praktyka:

- notebook importuje funkcje z `src/annealing_crypto/`,
- wszystkie powtarzalne eksperymenty pozostają w skryptach `CLI` i `experiments/`,
- notebook służy do wizualizacji, krótkiego demo i eksploracji wyników.

## 9. Szczegóły merytoryczne implementacji

### 9.1. Problem subset-sum

Dla wag `a_1, ..., a_n` oraz celu `T` szukamy bitów `x_i in {0,1}`, takich że:

`sum(a_i * x_i) = T`

W kontekście `Merkle-Hellman`:

- `a_i` to publiczne wagi,
- `x_i` to bity wiadomości,
- `T` to ciphertext.

### 9.2. Model QUBO

Najprostsza funkcja celu:

`E(x) = (sum(a_i * x_i) - T)^2`

Minimalizacja tej funkcji:

- daje `0`, jeśli znaleziono dokładne rozwiązanie,
- daje dodatnią wartość, jeśli rozwiązanie jest błędne.

To jest bardzo dobre jako `MVP`, bo:

- jest proste,
- łatwe do wytłumaczenia w raporcie,
- nie wymaga dodatkowych ograniczeń.

### 9.3. Merkle-Hellman

Wersja implementacyjna:

1. wygenerować superrosnący ciąg prywatny,
2. wybrać `q > sum(w_i)` oraz `r`, gdzie `gcd(r, q) = 1`,
3. zbudować klucz publiczny:
   - `b_i = (r * w_i) mod q`
4. szyfrowanie:
   - ciphertext = suma tych `b_i`, dla których bit wiadomości = 1
5. legalne deszyfrowanie:
   - użycie odwrotności modularnej `r^{-1} mod q`,
   - odzyskanie superrosnącej sumy,
   - greedy reconstruction.

### 9.4. Cel ataku

Nie łamiemy prywatnego klucza.

Atak w projekcie ma polegać na:

- dostaniu publicznego klucza i ciphertextu,
- potraktowaniu tego jako problemu `subset-sum`,
- próbie odzyskania wektora bitów wiadomości metodą `QUBO + annealing`.

To jest ważne, bo raport ma być spójny: atakujemy wiadomość przez rozwiązanie instancji plecakowej, a nie przez pełną rekonstrukcję tajnego klucza.

## 10. Dokładny plan implementacji

### Etap 0. Przygotowanie repozytorium

Zadania:

- utworzyć `pyproject.toml`,
- dodać strukturę `src/`, `tests/`, `experiments/`, `report/`,
- skonfigurować `pytest`,
- skonfigurować podstawowe narzędzia developerskie.

Kryterium zakończenia:

- projekt instaluje się lokalnie,
- test przykładowy przechodzi,
- da się uruchomić prosty skrypt z `src/`.

### Etap 1. Implementacja klasycznego Merkle-Hellmana

Zadania:

- zaimplementować generację kluczy,
- zaimplementować szyfrowanie wiadomości binarnej,
- zaimplementować legalne deszyfrowanie,
- przygotować testy poprawności.

Kryterium zakończenia:

- dla wielu wiadomości `decrypt(encrypt(m)) == m`.

### Etap 2. Implementacja problemu subset-sum

Zadania:

- osobna reprezentacja instancji,
- funkcja sprawdzająca poprawność rozwiązania,
- generator instancji losowych,
- generator instancji pochodzących z `Merkle-Hellman`.

Kryterium zakończenia:

- można wygenerować kontrolowaną instancję i sprawdzić rozwiązanie.

### Etap 3. Klasyczny baseline

Zadania:

- `brute force` dla małych `n`,
- opcjonalnie `dynamic programming`,
- mierzenie czasu i poprawności.

Kryterium zakończenia:

- istnieje punkt odniesienia dla solvera `QUBO`.

### Etap 4. Budowa QUBO

Zadania:

- zaimplementować funkcję budującą `QUBO` z instancji,
- zweryfikować na małych przykładach, że minimum odpowiada poprawnemu rozwiązaniu,
- dodać testy jednostkowe.

Kryterium zakończenia:

- dla małych instancji `ExactSolver` znajduje rozwiązanie zgodne z klasycznym baseline.

### Etap 5. Solver annealingowy

Zadania:

- podłączyć `neal.SimulatedAnnealingSampler`,
- dobrać podstawowe parametry:
  - liczba odczytów,
  - liczba sweepów,
  - seed,
- przygotować wspólny format wyników.

Kryterium zakończenia:

- solver działa na małych instancjach i zwraca pełne metadane.

### Etap 6. Benchmark

Zadania:

- zdefiniować zestaw rozmiarów instancji, np. `n = 8, 12, 16, 20, 24`,
- dla każdego `n` wykonać serię prób,
- porównać:
  - skuteczność,
  - czas,
  - wartość funkcji celu,
  - odsetek dokładnych trafień.

Kryterium zakończenia:

- wyniki są zapisane w `CSV`,
- da się wygenerować wykresy automatycznie.

### Etap 7. Wykresy i analiza

Zadania:

- wykres `success rate vs n`,
- wykres `runtime vs n`,
- wykres `objective gap vs n` lub histogram energii,
- tabela parametrów eksperymentu.

Kryterium zakończenia:

- powstają gotowe materiały do raportu.

### Etap 8. Raport

Zadania:

- opisać teorię,
- opisać implementację,
- opisać metodologię benchmarku,
- przedstawić wyniki,
- uczciwie omówić ograniczenia.

Kryterium zakończenia:

- raport da się skompilować i przeczytać jako spójną całość.

## 11. Plan testów

### 11.1. Testy jednostkowe

Obowiązkowe:

- superrosnący ciąg jest poprawnie rozpoznawany,
- generacja klucza spełnia warunki `q` i `r`,
- szyfrowanie daje oczekiwaną sumę,
- legalne deszyfrowanie odzyskuje wiadomość,
- funkcja celu `QUBO` daje `0` dla poprawnego rozwiązania,
- `brute force` znajduje prawidłowe rozwiązanie dla małych instancji.

### 11.2. Testy integracyjne

Obowiązkowe:

- wiadomość zaszyfrowana `Merkle-Hellman` daje instancję `subset-sum`,
- ta sama instancja daje zgodne rozwiązanie przez:
  - legalne deszyfrowanie,
  - `brute force`,
  - `QUBO + ExactSolver` dla małych `n`.

### 11.3. Testy eksperymentalne

Obowiązkowe:

- benchmark zapisuje poprawny `CSV`,
- dla ustalonego seeda wyniki są reprodukowalne w granicach przyjętej procedury.

## 12. Metryki

Minimalny zestaw metryk:

- `success_rate`: odsetek przypadków, w których odzyskano dokładną wiadomość,
- `runtime_ms`: czas działania solvera,
- `best_energy`: najlepsza znaleziona wartość funkcji celu,
- `exact_hit`: czy znaleziono rozwiązanie o energii `0`,
- `hamming_distance`: odległość Hamminga od poprawnej wiadomości.

Warto także zapisywać:

- `n`,
- zakres wag,
- typ instancji,
- seed,
- parametry annealingu.

## 13. Zestaw eksperymentów

### Scenariusz A. Random subset-sum

Cel:

- sprawdzić zachowanie solverów na ogólnych instancjach.

### Scenariusz B. Merkle-Hellman toy instances

Cel:

- sprawdzić zachowanie solverów na instancjach rzeczywiście wynikających z kryptosystemu.

### Scenariusz C. Wpływ parametrów annealingu

Cel:

- sprawdzić, czy zwiększenie liczby sweepów lub odczytów poprawia skuteczność.

Minimalny wymagany zestaw do raportu:

- `A` i `B`,
- `C` jako rozszerzenie, jeśli starczy czasu.

## 14. Ryzyka i jak nimi zarządzić

### Ryzyko 1. Za duży zakres

Mitigacja:

- nie dodawać na początku wielu solverów,
- najpierw dowieźć `Merkle-Hellman + brute force + simulated annealing`.

### Ryzyko 2. Problemy z bibliotekami D-Wave

Mitigacja:

- użyć minimalnego zestawu `dimod + neal`,
- nie uzależniać projektu od dostępu do prawdziwego QPU.

### Ryzyko 3. Słabe wyniki annealingu

Mitigacja:

- to nie jest porażka projektu,
- to może być poprawny wynik naukowy,
- trzeba tylko dobrze opisać skalę i ograniczenia.

### Ryzyko 4. Zbyt mało „kryptografii” w raporcie

Mitigacja:

- koniecznie zaimplementować `Merkle-Hellman`,
- pokazać pełen przepływ:
  - klucz,
  - szyfrowanie,
  - ciphertext,
  - atak jako `subset-sum`.

## 15. Plan raportu

### Docelowa długość

Około `8-12` stron tekstu głównego bez bibliografii.

### Proponowana struktura

#### 1. Wstęp

- motywacja,
- związek z kryptografią i wyżarzaniem kwantowym,
- cel pracy,
- pytanie badawcze.

#### 2. Tło teoretyczne

- problem `subset-sum`,
- kryptosystem `Merkle-Hellman`,
- `QUBO`,
- podstawy `annealing`.

#### 3. Metodologia

- model ataku,
- budowa instancji,
- funkcja celu `QUBO`,
- opis solverów,
- metryki.

#### 4. Implementacja

- architektura kodu,
- użyte biblioteki,
- organizacja eksperymentów,
- założenia techniczne.

#### 5. Wyniki

- tabele i wykresy,
- porównanie metod,
- omówienie trendów.

#### 6. Dyskusja

- co działało,
- co nie działało,
- dlaczego wyniki nie oznaczają praktycznego złamania nowoczesnych systemów,
- ograniczenia podejścia.

#### 7. Zakończenie

- odpowiedź na pytanie badawcze,
- najważniejsze wnioski,
- możliwe rozszerzenia.

## 16. Co powinno znaleźć się w raporcie obowiązkowo

Obowiązkowo:

- definicja `subset-sum`,
- opis `Merkle-Hellman`,
- jawne wyprowadzenie lub przynajmniej uzasadnienie funkcji `QUBO`,
- opis użytych solverów,
- eksperymenty na co najmniej kilku rozmiarach instancji,
- wykres skuteczności i czasu,
- krytyczne omówienie ograniczeń.

## 17. Czego nie pisać w raporcie

Nie pisać:

- że projekt „łamie współczesną kryptografię”,
- że `simulated annealing` to to samo co prawdziwy komputer kwantowy,
- że małe wyniki automatycznie skaluje się na duże instancje,
- że `Merkle-Hellman` jest dziś praktycznie używany jako nowoczesny standard.

Trzeba pisać uczciwie:

- to jest model edukacyjny,
- instancje są małe,
- metoda pokazuje ciekawą ścieżkę modelowania problemu, nie realny atak na aktualne systemy produkcyjne.

## 18. Lista artefaktów końcowych

Na koniec projektu powinny istnieć:

1. kod źródłowy,
2. testy,
3. skrypt benchmarkowy,
4. pliki `CSV` z wynikami,
5. wykresy,
6. notebook `Jupyter` do demonstracji i wizualizacji,
7. raport,
8. krótki `README` z instrukcją uruchomienia.

## 19. Definicja ukończenia projektu

Projekt jest ukończony, jeśli:

1. można wygenerować klucze `Merkle-Hellman`,
2. można zaszyfrować i legalnie odszyfrować wiadomość,
3. można zbudować odpowiadający model `QUBO`,
4. można uruchomić co najmniej dwa sposoby rozwiązania instancji,
5. można wykonać benchmark i zapisać wyniki,
6. można wygenerować wykresy,
7. można uruchomić notebook demonstracyjny i obejrzeć wyniki w Jupyterze,
8. można napisać spójny raport na podstawie zebranych danych.

## 20. Zalecany pierwszy prompt do nowej konwersacji

Jeżeli chcesz zacząć implementację w nowej rozmowie, najlepszy pierwszy prompt to:

```text
Na podstawie pliku docs/subset_sum_merkle_hellman_qubo_plan.md utwórz szkielet repozytorium dla projektu w Pythonie. Zacznij od pyproject.toml, struktury src/tests, implementacji klasycznego Merkle-Hellmana oraz testów jednostkowych dla keygen/encrypt/decrypt. Nie przechodź jeszcze do QUBO ani benchmarków.
```

## 21. Zalecana kolejność pracy w nowych rozmowach

1. Szkielet repozytorium i zależności.
2. `Merkle-Hellman`.
3. Testy jednostkowe.
4. `subset-sum` i `brute force`.
5. `QUBO`.
6. `simulated annealing`.
7. Benchmark.
8. Wykresy.
9. Notebook demonstracyjny `Jupyter`.
10. Raport `LaTeX`.

To jest kolejność minimalizująca ryzyko i maksymalizująca szansę dowiezienia projektu.
