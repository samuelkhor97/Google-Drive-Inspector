<!doctype html>
<html>

<head>
    <title>{{drive_name}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link rel="stylesheet" href="../static/Assignment1CSS.css" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="mobile-web-app-capable" content="yes" />

</head>

<body id="mainPageBackground" background="../static/Background_for_all.jpg">
    <div>
        <header>
            <div id="mainPageHeader">
                Make marking easy
            </div>
            <div id="projectName">
                {{drive_name}}
            </div>
        </header>

        <label for="DrawerMenuTrigger" class="OpenMenuButton">CLICK FOR MENU</label>
        <input type="checkbox" id="DrawerMenuTrigger" hidden>
        <aside class="DrawerMenu">

            <div class="MenuContainer">
                <nav class="Menu">
                    <h2 class="Menu__Title">M E N U</h2>
                    <a href="#">File 1</a>
                    <a href="#">File 2</a>
                    <a href="#">File 3</a>
                    <a href="#">Date</a>

                </nav>
            </div>

            <label for="DrawerMenuTrigger" class="MenuOverlay"></label>
        </aside>

        <div>

            <button id="homeButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()">
                <i class="material-icons">home</i>
            </button>

            <button id="uploadButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
                <i class="material-icons">arrow_back</i>
            </button>

            <div id="mainpiechart"></div>

            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

            <script type="text/javascript">
                // Load google charts
                google.charts.load('current', {
                    'packages': ['corechart']
                });
                google.charts.setOnLoadCallback(drawChart);

                let contributionsArray = [
                    ['Author', 'Revision Commits']
                ];
                chartData = {{!contributions}};
                for (user in chartData) {
                    contributionsArray.push([user, chartData[user]]);
                }

                // Draw the chart and set the chart values
                function drawChart() {
                    var data = google.visualization.arrayToDataTable(contributionsArray);

                    // Optional; add a title and set the width and height of the chart
                    var options = {
                        'title': 'Total overall contribution, by author, in {{drive_name}}',
                        'width': 550,
                        'height': 300
                    };

                    // Display the chart inside the <div> element with id="piechart"
                    var chart = new google.visualization.PieChart(document.getElementById('mainpiechart'));
                    chart.draw(data, options);
                }
            </script>

            <table class="maintable">
                <tr>
                    <th>Author</th>
                    <th>Revision Commits</th>
                    <th>% of Contributions</th>
                </tr>
                % for (user, contribution), (user, percent) in zip(contributions.items(), contributions_percent.items()):
                <tr>
                    <td>{{user}}</td>
                    <td>{{contribution}}</td>
                    <td>{{percent}}</td>
                <tr>
                % end
            </table>

        </div>
    </div>

    <!-- Javascript files below: -->
    <script>
        function returnHome() {
            window.location.href = "/team_drives"
        }

        function logoutPrompt() {
            if (confirm("Logout?")) {
                window.location.href = "/logout";
            }
        }
    </script>
</body>

</html>