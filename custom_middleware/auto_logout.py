# custom_middleware/auto_logout.py
import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = datetime.datetime.now()
        last_activity = request.session.get('last_activity', current_time)

        # Define your session idle timeout (e.g., 30 minutes)
        session_idle_timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)

        # Ensure last_activity is a datetime object
        if isinstance(last_activity, str):
            last_activity = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')

        # Check if the session has been idle for too long
        if (current_time - last_activity).seconds > session_idle_timeout:
            logout(request)

        # Update the last activity time in the session
        request.session['last_activity'] = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
