    <!-- Izpis ladij -->
    <table id="tabele">
        <thead>
        <tr>
            <th scope="col">Ime</th>
            <th scope="col">Leto izdelave</th>
            <th scope="col">Nosilnost [tone]</th>
        </tr>
        </thead>
        <tbody>

            %for id, ime, leto_izdelave, nosilnost in ladje:
            <tr>
                <td>{{ime}}</td>
                <td>{{leto_izdelave}}</td>
                <td>{{nosilnost}}</td>
            </tr>
            % end

        </tbody>
    </table>