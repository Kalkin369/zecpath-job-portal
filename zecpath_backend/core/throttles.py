from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class InterviewThrottle(UserRateThrottle):

    scope = "interview"

class LoginThrottle(AnonRateThrottle):

    scope = "login"    