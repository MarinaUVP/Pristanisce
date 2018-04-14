<!-- Izpis načrtov poti -->

<table id="tabele">
    <thead>
        <th scope="coč">Že dodeljeni nazivi potovanj</th>
    </thead>
    <tbody>
        %for (id, naziv_poti) in vsi_nacrti_poti:
            <tr>
                <td>{{naziv_poti}}</td>
            </tr>
        % end
    </tbody>
</table>
