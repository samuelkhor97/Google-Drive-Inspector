<!doctype html>
<html>

<head>
    <title>Drive Inspector</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link rel="stylesheet" href="static/common.css" />
    <link rel="stylesheet" href="static/drives.css" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="mobile-web-app-capable" content="yes" />
    <link rel="shortcut icon" sizes="196x196" href="images/icon.png" />
    <link rel="apple-touch-icon-precomposed" href="images/icon.png" />
    
</head>

<body background="static/bg6.jpg">
    <header>
        Make marking easy
    </header>

    

    <div id="allGroups">MY TEAM DRIVES</div>
    <div id="drivesContainer">
        <!-- href='/loading/<team_drive_id>' -->
        % for drive_name in drive_ids:
        <a href='{{drive_ids[drive_name]}}'>
            {{drive_name}}
        </a> 
        % end
    </div>
    
    <div>
        <button id="exitButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
            <i class="material-icons">exit_to_app</i>
        </button>

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