from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED      = "Applied"
    HR_SCREENING = "HR Screening"
    INTERVIEW    = "Interview"
    OFFER        = "Offer"
    ON_HOLD      = "On Hold"
    REJECTED     = "Rejected"
