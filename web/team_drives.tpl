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
        <link rel="shortcut icon" sizes="196x196" href="images/icon.png"/>
        <link rel="apple-touch-icon-precomposed" href="images/icon.png"/>
    </head>
    
    <body   id="mainPageBackground" background="static/Background_for_all.jpg">
        <div>
            <header>
                <div id="mainPageHeader" >
                    Make marking easy
                </div>

            </div>

            </header>

            <div id="allGroups">ALL GROUPS</div>

                <a href="page3.html">
                    <button class="Group1">Team GitRekt</button>
                    <button class="Group2">Team RandomName</button>
                </a>

                <button id="uploadButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()"> 
                    <i class="material-icons">add_box</i> 
                </button>  
                
                <a href="LogInPage.html">
                    <button id="backButton3" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored"> 
                        <i class="material-icons">arrow_back</i> 
                    </button>  
                </a>

                <button id="deleteButton" class="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored" onclick="returnHome()"> 
                    <i class="material-icons">delete_sweep</i> 
                </button>  

            </div>
            <div>
            
            </div>
            
            
        </div>
        
        <!-- Javascript files below: -->
    </body>
</html>