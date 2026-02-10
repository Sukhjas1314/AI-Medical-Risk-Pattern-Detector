Explaination_Templates = {
    "Delayed Treatment": (
        "Treatment was initiated {delay} hours later than the recommended "
        "safe window of {threshold} hours. Such delays may increase patient risk."
    ),
    "Missing Follow-up Diagnosis": (
        "An abnormal test result was not followed by a required diagnosis, "
        "which may lead to delayed medical intervention."
    )
}

def generate_explainations(violations):
    explainations = []

    for v in violations:
        rule = v["rule"]
        template = Explaination_Templates.get(
            rule,
            "A deviation from standard care protocol was detected."
        )

        if "delay_hours" in v:
            explainations.append(
                template.format(
                    delay = v["delay_hours"],
                    threshold = v["threshold"]
                )
            )
        else:
            explainations.append(template)

    return explainations