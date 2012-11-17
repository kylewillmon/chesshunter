<%inherit file="base.mak"/>
<div class="container">
    <div class="row">
        <div class="span3">
        </div>
        <div class="span9">
            % if games:
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
            % else:
            <div class="hero-unit">
                <h1>You have no current games :(</h1>
                <p>You should challenge someone to a game.</p>
            </div>
            % endif
        </div>
    </div>
</div>
