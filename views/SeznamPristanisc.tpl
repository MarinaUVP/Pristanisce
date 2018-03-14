    <table id="tabele">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Pristanišče</th>
        </tr>
        </thead>
        <tbody>

            %for id, pristanisce in pristanisca:
            <tr>
                <td scope="row">{{id}}</td>
                <td>{{pristanisce}}</td>
            </tr>
            % end

        </tbody>
    </table>


