<!doctype html>
<html>

<head>
    <title>Drive Inspector</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link rel="stylesheet" href="static/Assignment1CSS.css" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="mobile-web-app-capable" content="yes" />
    <link rel="shortcut icon" sizes="196x196" href="images/icon.png" />
    <link rel="apple-touch-icon-precomposed" href="images/icon.png" />
</head>

<body id="mainPageBackground" background="static/Background_for_all.jpg">
    <div>
        <header>
            <div id="mainPageHeader">
                Make marking easy
            </div>

    </div>

    </header>

    <div id="allGroups">ALL TEAM DRIVES</div>

    <!-- <button class="Group1">Team GitRekt</button>
                <button class="Group2">Team RandomName</button> -->
    % for drive_name in drive_ids:
    <a href={{drive_ids[drive_name]}} style="
                            position:relative;
                            text-align: center;
                            top:250px;
                            left:300px;
                            width:200px;
                            height:200px;

                            font: bold 11px Arial;
                              text-decoration: none;
                              background-color: #EEEEEE;
                              color: #333333;
                              padding: 2px 6px 2px 6px;
                              border-top: 1px solid #CCCCCC;
                              border-right: 1px solid #333333;
                              border-bottom: 1px solid #333333;
                              border-left: 1px solid #CCCCCC;">{{drive_name}}</a> 
    % end

    </div>
    <button id="uploadButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="logoutPrompt()">
        <i class="material-icons">arrow_back</i>
    </button>
    <div>
        <button id="backButton3" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()">
            <i class="material-icons">home</i>
        </button>

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