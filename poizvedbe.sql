SELECT ime, priimek, Kabina.tip, cena
FROM Vozovnica JOIN Potnik ON (Vozovnica.emso_potnika = Potnik.emso)
JOIN Kabina ON (Vozovnica.id_kabine = Kabina.id)
JOIN Cena_kabine ON (Vozovnica.id_izvedbe_potovanja = Cena_kabine.id_nacrt_poti)
WHERE Cena_kabine.id_tip_kabine = Tip_kabine.id;

-- Izriše načrt potovanja za posamezen odsek 
-- Sprogramiraj tako, da se bo končno pristanišče ujemalo z naslednjim začetnim in da odhod iz naslednjega začetnega ne bo prehiteval prihoda v končno
SELECT naziv_potovanja, odhod, cas_potovanja, x.pristanisce, y.pristanisce FROM Ima_odsek
JOIN Nacrt_poti ON (Ima_odsek.id_nacrta_poti = Nacrt_poti.id)
JOIN Odsek ON (Ima_odsek.id_odseka_poti = Odsek.id)
JOIN Pristanisce AS x ON (Odsek.id_zacetnega_pristanisca = x.id)
JOIN Pristanisce AS y ON (Odsek.id_koncnega_pristanisca = y.id)
ORDER BY naziv_potovanja, odhod;




-- Izberemo le pristanišča, do katerih lahko pridemo iz določenega pristanišča
SELECT x.pristanisce, y.pristanisce, cas_potovanja FROM Odsek
JOIN Pristanisce AS x ON (Odsek.id_zacetnega_pristanisca = x.id)
JOIN Pristanisce AS y ON (Odsek.id_koncnega_pristanisca = y.id)
WHERE x.pristanisce IN ("Koper", "Izola")
ORDER BY cas_potovanja DESC;

-- 



