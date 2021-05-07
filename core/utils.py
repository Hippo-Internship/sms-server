from django.contrib.auth import get_user_model


User = get_user_model()

def check_if_user_can_procceed(request_user, school_id, branch_id):
    if request_user.groups.role_id is User.SUPER_ADMIN:
        return True
    if request_user.groups.role_id is User.ADMIN:
        if request_user.school.id is not school_id:
            return False
    else:
        if request_user.branch.id is not branch_id:
            return False
    return True

def check_if_branch_can_procceed(request_user, school_id):
    if request_user.groups.role_id is User.SUPER_ADMIN:
        return True
    if request_user.groups.role_id is User.ADMIN:
        if request_user.school.id is not school_id:
            return False
    else:
            return False
    return True
