from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class InterviewThrottle(UserRateThrottle):

    scope = "interview"


class LoginThrottle(AnonRateThrottle):

    scope = "login"


class PremiumRecruiterThrottle(UserRateThrottle):

    scope = "premium_recruiter"
