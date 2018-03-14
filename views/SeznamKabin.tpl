<!-- Izpis kabin -->
    <table id="tabele">
        <thead>
        <tr>
            <th scope="col">Ladja</th>
            <th scope="col">Tip kabine</th>
            <th scope="col">Število ležišč</th>
        </tr>
        </thead>
        <tbody>

            %for ladja, tip, stevilo_lezisc in kabine:
            <tr>
                <td>{{ladja}}</td>
                <td>{{tip}}</td>
                <td>{{stevilo_lezisc}}</td>
            </tr>
            % end

        </tbody>
    </table>
