<!doctype html>
<html>

<head>
    <title>{{drive_name}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link rel="stylesheet" href="../../../static/Assignment1CSS.css" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="mobile-web-app-capable" content="yes" />

</head>

<body id="mainPageBackground" background="../../../static/Background_for_all.jpg">
    <div>
        <header>
            <div id="mainPageHeader">
                Make marking easy
            </div>
            <div id="projectName">
                {{drive_name}} 
            </div>
            <div id="projectName1">
                Contribution breakdown from {{start_date}} to {{end_date}}
            </div>
        </header>

        <div id="MenuButton">
            <label for="DrawerMenuTrigger">
                <img src="../../../static/new-tab.png" style="cursor: pointer;">
            </label>
        </div>
        
        <input type="checkbox" id="DrawerMenuTrigger" hidden>
        <aside class="DrawerMenu">

            <div class="MenuContainer">
                <nav class="Menu">
                    <div>
                        Enter timeframe to check work commits:
                    </div>
                    <div>
                        <label for="start">Start</label>
                        <input type="date" id="start" name="start"
                        value="yyyy-mm-dd"
                        min="2016-01-01" />
                    </div>

                    <div>
                        <label for="end">End</label>
                        <input type="date" id="end" name="end"
                        value="yyyy-mm-dd"
                        min="2016-01-01"/>
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

            <button id="backButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnTeamDrive()">
                <i class="material-icons">arrow_back</i>
            </button>

            <button id="exitButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
                <i class="material-icons">exit_to_app</i>
            </button>

        </div>

        <div id="charts-container">

            <div id="mainpiechart"></div>


            <div id="maintable">
                <table class="maintable">
                    <tr>
                        <th>Author</th>
                        <th>Revision Commits</th>
                        <th>% of Contributions</th>
                    <!-- Add table elements dynamically -->
                    </tr>
                    % for (user, contribution), (user, percent) in zip(contributions.items(), contributions_percent.items()):
                    <tr>
                        <td>{{user}}</td>
                        <td>{{contribution}}</td>
                        <td>{{percent}}</td>
                    </tr>
                    % end
                </table>
            </div>

        </div>
    </div>

    <!-- Javascript files below: -->
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

            <script type="text/javascript">
                // Check if the obj is empty
                function isEmpty(obj) {
                    for(var key in obj) {
                        if(obj.hasOwnProperty(key)) {
                            return false;
                        }
                    }
                    return true;
                }
                // Load google charts
                google.charts.load('current', {
                    'packages': ['corechart']
                });
                google.charts.setOnLoadCallback(drawChart);

                let contributionsArray = [
                    ['Author', 'Revision Commits']
                ];
                //  Load the contribution data passed into template
                chartData = {{!contributions}};
                if (isEmpty(chartData)) {
                    setTimeout(function() {alert("No data to be showned.");},1500);
                }
                for (user in chartData) {
                    contributionsArray.push([user, chartData[user]]);
                }

                // Draw the Pie chart and set the chart values
                function drawChart() {
                    var data = google.visualization.arrayToDataTable(contributionsArray);

                    var options = {
                        'title': 'Time-framed contribution, by author, in {{drive_name}}',
                        'width': 600,
                        'height': 350,
                        'backgroundColor':'transparent'
                    };

                    // Display the chart inside the <div> element with id="mainpiechart"
                    var chart = new google.visualization.PieChart(document.getElementById('mainpiechart'));
                    chart.draw(data, options);
                }
            </script>

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

        function returnTeamDrive() {
            window.location.href = "/team_drive_contributions/{{drive_id}}";
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