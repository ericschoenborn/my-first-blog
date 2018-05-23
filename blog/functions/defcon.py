from datetime import datetime


def calculate_defcon(idle, status, estimate, dpl, name, due, now, unverifiable):

    defcon_score = 0

    # Idle score
    if status == "In Progress":
        defcon_score -= 10 * (idle / 3)
    elif status == "Code Review":
        defcon_score -= 10 * idle
    elif status == "Test Deployable":
        defcon_score -= 10 * idle
    elif status == "Staging Deployable":
        defcon_score -= 10 * (idle / 2)
    elif status == "QA":
        defcon_score -= 10 * (idle / 3)
    elif status == "Production Deployable":
        defcon_score -= 10 * (idle / 7)
    elif status == "UAT":
        defcon_score -= 10 * (idle / 14)

    # Estimate score
    if estimate == "NA":
        defcon_score -= 100

    elif estimate < 0:
        defcon_score -= 10 * abs(estimate)

    # Dpl score
    if dpl == "N":
        # exclude meta projects
        if not ("KA-" in name or "PMM-" in name or "HR-" in name or "ISD-" in name):
            defcon_score -= 100

    # pass due score
    if due != "NA":
        due = datetime.strptime(due, "%Y-%m-%d").date()

        if due < now:
            defcon_score -= 500

    # Unverifiable score
    if unverifiable == "Y":
        defcon_score -= 500

    # get defcon level from defcon score
    if defcon_score == 0:
        return 5
    elif defcon_score <= -500:
        return 1
    elif defcon_score <= -250:
        return 2
    elif defcon_score <= -100:
        return 3
    elif defcon_score > -100:
        return 4

    else:
        return "error"
