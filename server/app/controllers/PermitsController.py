def buy():

    from flask import request

    if request.method == 'POST':
        from flask_login import current_user
        current_user.add_permit(request.form['permit'])
        current_user.update()
        from flask import redirect, url_for
        return redirect(url_for('permits.buy'))

    else:
        from app.server.models import PERMIT_LIST
        from flask_login import current_user
        print(current_user.permits)
        print(PERMIT_LIST)

        user_permits = {key:value for (key, value) in PERMIT_LIST.items() if key in current_user.permits}
        missing_permits = {key:value for (key, value) in PERMIT_LIST.items() if key not in current_user.permits}

        from flask import render_template
        return render_template('permits.html', missing_permits=missing_permits, user_permits=user_permits)
