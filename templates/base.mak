 <!DOCTYPE html>
 <html>
     <head>
         <meta http-equiv="content-type" content="text/html; charset=utf-8" />
         <title><%block name="title">chesshunter</%block></title>
         <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
         <style type="text/css">
             body {
                 padding-top: 60px;
             }
         </style>
     </head>
     <body>
         <div class="navbar navbar-inverse navbar-fixed-top">
             <div class="navbar-inner">
                 <div class="container">
                     <a class="brand" href="/">chesshunter</a>
                     <div class="nav-collapse collapse">
                         <ul class="nav">
                             <li class="active"><a href="#">Home</a></li>
                             <li><a href="#about">About</a></li>
                             <li><a href="#contact">Contact</a></li>
                         </ul>
                         <ul class="nav pull-right">
                             % if logged_in:
                             <li><a href="#">Logged in as: ${user.username}</a></li>
                             % else:
                             <li><a href="/login">Login</a></li>
                             % endif
                         </ul>
                     </div>
                 </div>
             </div>
         </div>
         ${next.body()}
         <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
         <script src="/static/js/bootstrap.min.js"></script>
     </body>
 </html>
