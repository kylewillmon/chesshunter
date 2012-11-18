<%inherit file="base.mak"/>
<div class="container">
    <div class="row">
        <div class="span12">
            % if message != '':
            <div class="alert">
                <button type="button" class="close" data-dismiss="alert">x</button>
                ${message}
            </div>
            % endif
            % if error != '':
            <div class="alert alert-error">
                <button type="button" class="close" data-dismiss="alert">x</button>
                ${error}
            </div>
            % endif
            <h1 class="title">User Registration</h1>
            <form class="form-horizontal" method="POST" action="#">
                <div class="control-group">
                    <label class="control-label" for="inputUsername">Username</label>
                    <div class="controls">
                        <input type="text" name="username" id="inputUsername" placeholder="Username">
                    </div>
                </div>
                <div class="control-group">
                    <label class="control-label" for="inputPassword">Password</label>
                    <div class="controls">
                        <input type="password" name="password" id="inputPassword" placeholder="Password">
                    </div>
                </div>
                <div class="control-group">
                    <div class="controls">
                        <button type="submit" name="submit" class="btn">Sign in</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
