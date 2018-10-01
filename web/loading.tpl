<!doctype html>
<html>

<head>
    <title>Loading Team Drive</title>
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
                loading team drive insight... 
            </div>
        </header>

        <div id="catgif">
            <img src="../static/runcat2.gif">
        </div>

        <div class="loading">
            <div class="loading-bar"></div>
            <div class="loading-bar"></div>
            <div class="loading-bar"></div>
            <div class="loading-bar"></div>
        </div>

        <!-- Javascript files below: -->
        <script>
            poll = function() {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/isready');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        if (xhr.responseText == 1) {

                            window.location.href = "{{redirect_link}}";
                        } else {
                            setTimeout(poll, 1000);
                        }
                    }
                }
                xhr.send(null);
            }

            setTimeout(poll, 1000);
        </script>
</body>

</html>