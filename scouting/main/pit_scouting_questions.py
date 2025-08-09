from django.utils.translation import gettext_lazy as _

# ----------
# 2024
# ----------
crescendo = [
    {
        "text": _("What is your drivetrain?"),
        "simple_name": "drivetrain",
        "type": "choice",
        "choices": ["Swerve", "Tank", "Mecanum", "Octocanum", "Other"],
        "answers": [],
    },
    {
        "text": _("Can your robot score in the amp?"),
        "simple_name": "amp",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot score in the trap?"),
        "simple_name": "trap",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot score in the speaker?"),
        "simple_name": "speaker",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Does your robot climb?"),
        "simple_name": "climb",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("How does your robot score in the trap?"),
        "simple_name": "how_trap",
        "type": "text",
        "answers": [],
    },
    {
        "text": _("Does your robot have a variable angle launcher?"),
        "simple_name": "variable_angle_launcher",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Where does your robot usually shoot from?"),
        "simple_name": "shoot_position",
        "type": "text",
        "answers": [],
    },
    {
        "text": _("Do you have autons?"),
        "simple_name": "auton",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("If so, how many pieces can you score in auton?"),
        "simple_name": "auton_pieces",
        "type": "number",
        "answers": [],
    },
    {
        "text": _("Do you go to the midfield during auton?"),
        "simple_name": "auton_midfield",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("What are your start positions in auton? (A, B, C, or D)"),
        "simple_name": "auton_start_positions",
        "type": "text",
        "answers": [],
    },
    {
        "text": _("How often do you meet in build season?"),
        "simple_name": "meeting_frequency",
        "type": "text",
        "answers": [],
    },
]

# ----------
# 2025
# ----------
reefscape = [
    {
        "text": _("What is your drivetrain?"),
        "simple_name": "drivetrain",
        "type": "choice",
        "choices": ["Swerve", "Tank", "Other"],
        "answers": [],
    },
    {
        "text": _("Can your robot score coral in the reef?"),
        "simple_name": "reef",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot remove algae from the reef?"),
        "simple_name": "remove_algae",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot score algae in the net?"),
        "simple_name": "net",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot score algae in the processor?"),
        "simple_name": "processor",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("Can your robot climb?"),
        "simple_name": "climb",
        "type": "choice",
        "choices": ["No", "Shallow Cage", "Deep Cage"],
        "answers": [],
    },
    {
        "text": _("Do you have autos?"),
        "simple_name": "auton",
        "type": "boolean",
        "answers": [],
    },
    {
        "text": _("If so, how many pieces can you score in auto?"),
        "simple_name": "auton_pieces",
        "type": "number",
        "answers": [],
    },
    {
        "text": _("How often do you meet in build season?"),
        "simple_name": "meeting_frequency",
        "type": "text",
        "answers": [],
    },
    {
        "text": _("Which CAD software do you use?"),
        "simple_name": "cad",
        "type": "text",
        "answers": [],
    },
    {
        "text": _("How long does your team strategize for?"),
        "simple_name": "strategize_time",
        "type": "text",
        "answers": [],
    },
    {
        "text": _(
            "How long does it take before you're building and assembling your robot?"
        ),
        "simple_name": "build_time",
        "type": "text",
        "answers": [],
    },
]
