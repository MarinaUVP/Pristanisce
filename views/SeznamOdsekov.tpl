<!-- Izpis kabin -->

<table id="tabele">
    <thead>
        <th scope="col">Prvo pristanišče</th>
        <th scope="col">Drugo pristanišče</th>
        <th scope="col">Čas potovanja med njima</th>
    </thead>
    <tbody>
        %for (id, x_pristanisce, y_pristanisce, cas_potovanja) in odseki:
            <tr>
                <td>{{x_pristanisce}}</td>
                <td>{{y_pristanisce}}</td>
                <td>{{cas_potovanja}}</td>
            </tr>
        %end
    </tbody>
</table>
