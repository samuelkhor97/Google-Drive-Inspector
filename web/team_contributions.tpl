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

        <div id="MenuButton">
            <label for="DrawerMenuTrigger">
                <img src="../static/new-tab.png">
            </label>
        </div>

        <input type="checkbox" id="DrawerMenuTrigger" hidden>
        <aside class="DrawerMenu">

            <div class="MenuContainer">
                <nav class="Menu">
                    <h2 class="Menu__Title">F I L E S</h2> 
                    % for name in file_names_ids:
                        <a href={{file_names_ids[name]}}>File: {{name}}</a> 
                    % end
                    <div>
                        Enter timeframe to check work commits:
                    </div>
                    <div>
                        <label for="start">Start</label>
                        <input type="date" id="start" name="start" value="yyyy-mm-dd" min="2016-01-01" />
                    </div>

                    <div>
                        <label for="end">End</label>
                        <input type="date" id="end" name="end" value="yyyy-mm-dd" min="2016-01-01" />
                    </div>
                    <button class="mdl-button mdl-button--raised" onclick='submitDate()'>Submit</button>
                </nav>
            </div>

            <label for="DrawerMenuTrigger" class="MenuOverlay"></label>
        </aside>

        <div>

            <button id="homeButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()">
                <i class="material-icons">home</i>
            </button>

            <button id="exitButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
                <i class="material-icons">exit_to_app</i>
            </button>

            <div id="mainpiechart"></div>
            <div id="maintimeline"></div>

            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

            <script type="text/javascript">
                // Check if the obj is empty
                function isEmpty(obj) {
                    for (var key in obj) {
                        if (obj.hasOwnProperty(key)) {
                            return false;
                        }
                    }
                    return true;
                }
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
                    chartData = {{!contributions}};
                    if (isEmpty(chartData)) {
                        setTimeout(function() {
                            alert("No data to be showned.");
                        }, 2000);
                    }
                    for (user in chartData) {
                        contributionsArray.push([user, chartData[user]]);
                    }
                    var data = google.visualization.arrayToDataTable(contributionsArray);

                    var options = {
                        'title': 'Overall contribution, by author, in {{drive_name}}',
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

                    if (isEmpty(chartData)) {
                        setTimeout(function() {
                            alert("No data to be showned.");
                        }, 2000);
                    }
  
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
                        'title': 'Contribution Timeline in {{drive_name}}',
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
        drive = '{{drive_name}}';

        function returnHome() {
            window.location.href = "/team_drives";
        }

        function logoutPrompt() {
            if (confirm("Logout?")) {
                window.location.href = "/logout";
            }
        }

        // Take in dates submitted by user and redirect to contribution page
        function submitDate() {
            startDateObj = document.getElementById('start')
            endDateObj = document.getElementById('end')
            startDate = startDateObj.value;
            endDate = endDateObj.value;

            if (startDate > endDate) {
                alert("End date must be later than Start date!")
            } else if ((startDate < startDateObj.min) || (endDate < endDateObj.min)) {
                alert("Invalid date earlier than " + startDateObj.min)
            } else {
                window.location.href = "/timeContribution/" + startDate + "/" + endDate + "/" + drive;
            }

        }
    </script>
</body>

</html>