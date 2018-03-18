-- ZA NAČRT POTI

-- Načrt poti, sestavljen iz odsekov
SELECT naziv_potovanja, odhod, cas_potovanja, x.pristanisce, y.pristanisce FROM Ima_odsek
JOIN Nacrt_poti ON (Ima_odsek.id_nacrta_poti = Nacrt_poti.id)
JOIN Odsek ON (Ima_odsek.id_odseka_poti = Odsek.id)
JOIN Pristanisce AS x ON (Odsek.id_zacetnega_pristanisca = x.id)
JOIN Pristanisce AS y ON (Odsek.id_koncnega_pristanisca = y.id)
ORDER BY naziv_potovanja, odhod;

-- Iz katerega pristanišča se posamezno potovanje začne - MIN relativnega datuma
SELECT naziv_potovanja, odhod, id_zacetnega_pristanisca, Pristanisce.pristanisce
FROM Nacrt_poti as nacrt
JOIN Ima_odsek ON (Ima_odsek.id_nacrta_poti = nacrt.id)
JOIN Odsek ON (Odsek.id = Ima_odsek.id_odseka_poti)
JOIN Pristanisce ON (Pristanisce.id = Odsek.id_zacetnega_pristanisca)
WHERE odhod = (SELECT MIN(odhod) FROM Ima_odsek WHERE id_nacrta_poti = nacrt.id);

-- V katerem pristanišču se posamezno potovanje konča - MAX relativnega datuma
SELECT naziv_potovanja, odhod, id_koncnega_pristanisca, Pristanisce.pristanisce
FROM Nacrt_poti as nacrt
JOIN Ima_odsek ON (Ima_odsek.id_nacrta_poti = nacrt.id)
JOIN Odsek ON (Odsek.id = Ima_odsek.id_odseka_poti)
JOIN Pristanisce ON (Pristanisce.id = Odsek.id_koncnega_pristanisca)
WHERE odhod = (SELECT MAX(odhod) FROM Ima_odsek WHERE id_nacrta_poti = nacrt.id);


-- Izberemo le pristanišča, do katerih lahko pridemo iz določenega pristanišča, npr. iz Kopra
SELECT x.pristanisce, y.pristanisce, cas_potovanja FROM Odsek
JOIN Pristanisce AS x ON (Odsek.id_zacetnega_pristanisca = x.id)
JOIN Pristanisce AS y ON (Odsek.id_koncnega_pristanisca = y.id)
WHERE x.pristanisce = "Koper"
ORDER BY cas_potovanja DESC;


-- VOZOVNICA

-- Podatki, vezani na posamezno vozovnico
SELECT Potnik.ime, Potnik.priimek, Tip_kabine.tip, cena, Nacrt_poti.naziv_potovanja, Izvedba_potovanja.datum_zacetka
FROM Ima_vozovnico
JOIN Potnik ON (Potnik.emso = Ima_vozovnico.emso_potnika)
JOIN Vozovnica ON (Vozovnica.id = Ima_vozovnico.id_vozovnice)
JOIN Izvedba_potovanja ON (Vozovnica.id_izvedbe_potovanja = Izvedba_potovanja.id)
JOIN Nacrt_poti ON (Nacrt_poti.id = Izvedba_potovanja.id_nacrta_poti)
JOIN Ladja ON (Izvedba_potovanja.id_ladje = Ladja.id)
JOIN Kabina ON (Vozovnica.id_kabine = Kabina.id) --pridružiš kabino, ki je vezana na vozovnico
JOIN Tip_kabine ON (Kabina.tip = Tip_kabine.id)
LEFT JOIN Cena_kabine ON (Cena_kabine.id_nacrt_poti = Nacrt_poti.id)
WHERE Cena_kabine.id_tip_kabine = Tip_kabine.id;


-- IZPIS kombinacij, za katere še NISMO DOLOČILI CENE KABIN
SELECT naziv_potovanja, tip FROM Nacrt_poti
JOIN Tip_kabine
WHERE (Nacrt_poti.id, Tip_kabine.id) NOT IN (SELECT Cena_kabine.id_nacrt_poti, Cena_kabine.id_tip_kabine FROM Cena_kabine);


-- Izpišemo ladje, ki nimajo kabin. Tem ladjam jih moramo dodati. 
SELECT ime FROM Ladja 
WHERE ime NOT IN (
    SELECT ime
    FROM Ladja 
    JOIN Kabina ON (Kabina.id_ladje = Ladja.id)
    GROUP BY id_ladje
    )
;

-- POTOVANJE

-- Izpišemo, katera potovanja so dostopna in za katere datume
SELECT naziv_potovanja, datum_zacetka, Ladja.ime, Tip_kabine.tip, cena, Kabina.stevilo_lezisc
FROM Izvedba_potovanja
JOIN Ladja ON (Ladja.id = Izvedba_potovanja.id_ladje)
JOIN Nacrt_poti ON (Nacrt_poti.id = Izvedba_potovanja.id_nacrta_poti)
JOIN Kabina ON (Kabina.id_ladje = Ladja.id)
JOIN Tip_kabine ON (Tip_kabine.id = Kabina.tip)
JOIN Cena_kabine ON (Cena_kabine.id_nacrt_poti = Nacrt_poti.id)
WHERE Cena_kabine.id_tip_kabine = Tip_kabine.id -- Zakaj tu ne dela, če damo Kabina.tip??? Bi moralo, ker sta vrednosti enaki...
;
