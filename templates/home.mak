 <!DOCTYPE html>
 <html>
     <head>
         <meta http-equiv="content-type" content="text/html; charset=utf-8" />
         <title>chesshunter</title>
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
                             <li><a href="#">Logged in as: ${user.username}</a></li>
                         </ul>
                     </div>
                 </div>
             </div>
         </div>
         <div class="container">
             <div class="row">
                 <div class="span3">
                 </div>
                 <div class="span9">
                     <div class="page-header"><h1>Current games</h1></div>
                     <table class="table table-hover">
                         <thead>
                             <tr>
                                 <th>White</th>
                                 <th>Black</th>
                                 <th>Turn</th>
                                 <th>Action</th>
                             </tr>
                         </thead>
                         <tbody>
% for g in games:
                             <tr>
                                 <td>${g.white.username}</td>
                                 <td>${g.black.username}</td>
                                 <td>${g.turn_count()}</td>
% if g.active_player().id == user.id:
                                 <td>Your turn</td>
% else:
                                 <td>Not your turn</td>
% endif
                             </tr>
% endfor
                         </tbody>
                     </table>
                     <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
                     <script src="/static/js/bootstrap.min.js"></script>
                 </div>
             </div>
         </div>
     </body>
 </html>
