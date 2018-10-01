<!doctype html>
<html>

<head>
    <title>{{file_name}}</title>
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
                {{file_name}}
            </div>
        </header>


        <div id="MenuButton">
            <label for="DrawerMenuTrigger">
                <img src="../static/tab.png">
            </label>
        </div>
        
        <input type="checkbox" id="DrawerMenuTrigger" hidden>
        <aside class="DrawerMenu">

            <div class="MenuContainer">
                <nav class="Menu">
                    <h2 class="Menu__Title">M E N U</h2>
                    % for name in file_names_ids:
                        <a href={{file_names_ids[name]}}>File: {{name}}</a>
                    % end
                </nav>
            </div>

            <label for="DrawerMenuTrigger" class="MenuOverlay"></label>
        </aside>

        <div>

            <button id="homeButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()">
                <i class="material-icons">home</i>
            </button>

            <button id="backButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnTeamDrive()">
                <i class="material-icons">arrow_back</i>
            </button>

            <button id="exitButton2" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
                <i class="material-icons">exit_to_app</i>
            </button>

            <div id="mainpiechart"></div>
            <div id="maintimeline"></div>

            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

            <script type="text/javascript">
                // Load google charts
                google.charts.load('current', {
                    'packages': ['corechart']
                });
                // Draw the Pie chart of contributions onLoad
                google.charts.setOnLoadCallback(drawChart);
                // Draw the Timeline of contributions onLoad
                google.charts.setOnLoadCallback(drawTimeline);

                // Draw the Pie chart and set the chart values
                function drawChart() {
                    let contributionsArray = [
                    ['Author', 'Revision Commits']
                    ];
                    // Load contributions data passed into template
                    chartData = {{!contribution}};
                    for (user in chartData) {
                        contributionsArray.push([user, chartData[user]]);
                    }
                    var data = google.visualization.arrayToDataTable(contributionsArray);

                    var options = {
                        'title': 'Overall contribution, by author, in {{file_name}}',
                        'width': 550,
                        'height': 300,
                        'backgroundColor': {
                            'fill': '#FFFAF0',
                            'fillopacity': 0.5
                        }
                    };

                    // Display the chart inside the <div> element with id="mainpiechart"
                    var chart = new google.visualization.PieChart(document.getElementById('mainpiechart'));
                    chart.draw(data, options);
                }

                // Draw the Timeline and set the values
                function drawTimeline() {
                    // Load contributions data passed into template
                    let chartData = {{!weekly_contributions}};
                    let usersList = {{!users_list}};
                    let contributionsArray = [];
  
                    contributionsArray.push(['Users'].concat(usersList));
                    // Pushing contributions data
                    for (week in chartData) {
                        dataArray = [week];
                        for (user in chartData[week]) {
                            dataArray.push(
                                chartData[week][user]);
                        }
                        contributionsArray.push(
                                dataArray);
                    }
                    var data = google.visualization.arrayToDataTable(contributionsArray);

                    var options = {
                        'title': 'File Contribution Timeline in {{file_name}}',
                        'height': 350,
                        'backgroundColor': {
                            'fill': '#FFFAF0',
                            'fillopacity': 0.5
                        },
                        'legend': { 
                            'position': 'top', 
                            'maxLines': 2 
                        },
                        'bar': { 
                            'groupWidth': '75%' 
                        },
                        'isStacked': true,
                        'vAxis': {
                            'minValue': 0
                        }
                    };

                    // Display the chart inside the <div> element with id="maintimeline"
                    var chart = new google.visualization.ColumnChart(document.getElementById('maintimeline'));
                    chart.draw(data, options);
                }
            </script>

            <table class="maintable">
                <tr>
                    <th>Author</th>
                    <th>Revision Commits</th>
                    <th>% of Contributions</th>
                <!-- Adding table elements dynamically -->
                </tr>
                % for (user, file_contribution), (user, percent) in zip(contribution.items(), contribution_percent.items()):
                <tr>
                    <td>{{user}}</td>
                    <td>{{file_contribution}}</td>
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

        function returnTeamDrive() {
            window.location.href = "/team_drive_contributions/{{current_drive}}"
        }
        function logoutPrompt() {
            if (confirm("Logout?")) {
                window.location.href = "/logout";
            }
        }
    </script>
</body>

</html>