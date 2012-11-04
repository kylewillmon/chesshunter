 <!DOCTYPE html>
 <html>
     <head>
         <meta http-equiv="content-type" content="text/html; charset=utf-8" />
         <title>chesshunter</title>
     </head>
     <body>
         <h1 class="title">Welcome to chesshunter</h1>
		 <div>Logged in as: ${user.username}</div>
         <table>
             <tr><th>Username</th></tr>
% for u in all_users:
             <tr><td>${u.username}</td></tr>
% endfor
         </table>
     </body>
 </html>
