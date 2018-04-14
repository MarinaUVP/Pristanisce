<!-- Izpis cen kabin -->
    <table id="tabele">
        <thead>
            <th scope="col">Naziv potovanja</th>
            <th scope="col">Tip potovanja</th>
            <th scope="col">Cena kabine</th>
        </thead>
        <body>
            %for (naziv_potovanja, tip_kabine, cena_kabine) in cene_kabin:
                <tr>
                    <td>{{naziv_potovanja}}</td>
                    <td>{{tip_kabine}}</td>
                    <td>{{cena_kabine}}</td>
                </tr>
            %end
        </body>
    </table>


