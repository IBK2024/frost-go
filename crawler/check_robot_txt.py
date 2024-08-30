from typing import Dict, List
import urllib.parse as _urlparse


def check_robot_txt(url: str, robot_txt: str, bot_name: str) -> bool:
    """Parses the provided robots.txt and checks if the provided url is allowed"""

    # !Parse robot.txt file
    parsed_robot_txt_data = parse_robot_txt(bot_name, robot_txt)

    # !Get needed rules
    all_bots_rules = parsed_robot_txt_data["all bot rules"]
    bot_rules_allowed_links = parsed_robot_txt_data[f"{bot_name}_allow"]
    bot_rules_disallowed_links = parsed_robot_txt_data[f"{bot_name}_disallow"]

    # !Get the paths
    paths = _urlparse.urlparse(url).path.split("/")
    paths.remove("")

    allowed: bool = True

    if "/" in all_bots_rules:
        allowed = False
    else:
        new_path = ""
        for path in paths:
            new_path = f"{new_path}/{path}"
            if new_path in all_bots_rules:
                allowed = False
                break

    if len(bot_rules_disallowed_links) > 0:
        if "/" in bot_rules_disallowed_links:
            allowed = False
        else:
            new_path = ""
            for path in paths:
                new_path = f"{new_path}/{path}"
                if new_path in bot_rules_disallowed_links:
                    allowed = False
                    break

    if len(bot_rules_allowed_links) > 0:
        if "/" in bot_rules_allowed_links:
            allowed = True
        else:
            new_path = ""
            for path in paths:
                new_path = f"{new_path}/{path}"
                if new_path in bot_rules_allowed_links:
                    allowed = True
                    break

    return allowed


def parse_robot_txt(bot_name: str, robot_txt: str) -> Dict[str, List[str]]:
    """Parse provided robot.txt file content"""
    # !Get the rules for all bots
    all_bots_rules: List[str] = robot_txt.split("User-agent: *")
    if len(all_bots_rules) > 1:
        all_bots_rules = all_bots_rules[1].split("\n\n")[0].split("\n")
        all_bots_rules.remove("")  # *Removes unnecessary spaces
    else:
        all_bots_rules = []

    all_bots_rules_disallowed_links: List[str] = [
        rule.removeprefix("Disallow: ") for rule in all_bots_rules if "Disallow" in rule
    ]

    # !Get the rules for the provided bot name
    bot_rules: List[str] = robot_txt.split("User-agent: FrostBot")
    if len(bot_rules) > 1:
        bot_rules = bot_rules[1].split("\n\n")[0].split("\n")
        bot_rules.remove("")
    else:
        bot_rules = []

    # !Separate rules for provided bot name into allowed and disallowed
    bot_rules_allowed_links: List[str] = [rule.removeprefix("Allow: ") for rule in bot_rules if "Allow:" in rule]
    bot_rules_disallowed_links: List[str] = [
        rule.removeprefix("Disallow: ") for rule in bot_rules if "Disallow:" in rule
    ]

    return {
        "all bot rules": all_bots_rules_disallowed_links,
        f"{bot_name}_allow": bot_rules_allowed_links,
        f"{bot_name}_disallow": bot_rules_disallowed_links,
    }
