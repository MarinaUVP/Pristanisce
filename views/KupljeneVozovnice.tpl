<!--Izpis že kupljenih vozovnic-->

    <table id="tabele">
        <thread>
            <tr>
                <th scope="col">Ime potnika</th>
                <th scope="col">Priimek potnika</th>
                <th scope="col">Tip kabine</th>
                <th scope="col">Cena kabine</th>
                <th scope="col">Število vozovnic</th>
                <th scope="col">Naziv potovanja</th>
                <th scope="col">Datum odhoda</th>
            </tr>
        </thread>

        <tbody>

            %for ime, priimek, tip, cena, stevilo_lezisc, naziv_potovanja, datum_zacetka in vozovnice:
            <tr>
                <td>{{ime}}</td>
                <td>{{priimek}}</td>
                <td>{{tip}}</td>
                <td>{{cena}}</td>
                <td>{{stevilo_lezisc}}</td>
                <td>{{naziv_potovanja}}</td>
                <td>{{datum_zacetka}}</td>
            </tr>
            %end


        </tbody>

    </tabele>

