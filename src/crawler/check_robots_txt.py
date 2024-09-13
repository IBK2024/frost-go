import os
from collections import defaultdict
from typing import Any, Dict, List
from urllib.parse import urlparse


def check_robots_txt(url: str, robot_txt: str, bot_name: str) -> bool:
    """
    Determines if the given url is allowed to be crawled by checking the given robots.txt content

    Args:
        url (str): The URL to check for access permissions.
        robot_txt (str): The content of the robots.txt file to parse.
        bot_name (str): The name of the bot for which to check permissions.

    Returns:
        bool: True if the URL is allowed to be accessed by the bot, False otherwise.
    """
    rules = get_robot_txt_rules(bot_name, robot_txt)
    paths = [path for path in urlparse(url).path.split("/") if path != ""]
    return check_rules(rules, paths)


def get_robot_txt_rules(bot_name: str, robot_txt: str) -> Dict[str, List[str]]:
    """
    Gets the rules of the provided robots.txt file content

    Args:
        bot_name (str): The name of the bot for which to retrieve rules.
        robot_txt (str): The content of the robots.txt file to parse.

    Returns:
        Dict[str, List[str]]: A dictionary with keys for all bot rules and the specific bot's disallowed links, each containing a List of corresponding paths.
    """
    rules = parse_robot_txt_content(robot_txt)

    all_bots_rules = rules.get("*", {})
    bot_rules = rules.get(f"{bot_name}", {}) if bot_name else {}

    return {
        "all_disallowed": all_bots_rules.get("Disallow", []),
        "all_allowed": all_bots_rules.get("Allow", []),
        "bot_disallowed": bot_rules.get("Disallow", []),
        "bot_allowed": bot_rules.get("Allow", []),
    }


def parse_robot_txt_content(robot_txt: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Parses the robots.txt content and returns a dictionary of rules.

    Args:
        robot_txt (str): The content of the robots.txt file to parse.

    Returns:
        Dict[str, Dict[str, List[str]]]: A dictionary with user-agent keys and their corresponding rules.
    """
    rules: defaultdict[Any, Dict[str, List[Any]]] = defaultdict(lambda: {"Disallow": [], "Allow": []})
    current_agent = None

    user_agent_prefix = "User-agent:"
    disallow_prefix = "Disallow:"
    allow_prefix = "Allow:"

    for line in robot_txt.splitlines():
        line = line.strip()
        if line.startswith(user_agent_prefix):
            current_agent = line.removeprefix(user_agent_prefix).strip()
        elif line.startswith(disallow_prefix) and current_agent:
            rules[current_agent]["Disallow"].append(line.removeprefix(disallow_prefix).strip())
        elif line.startswith(allow_prefix) and current_agent:
            rules[current_agent]["Allow"].append(line.removeprefix(allow_prefix).strip())

    return dict(rules)


def get_rules(robot_txt: str, agent: str, type_rule: str) -> List[str]:
    """
    Extracts specific rules for the given type from the given robots.txt content for a given user agent.

    Args:
        robot_txt (str): The content of the robots.txt file to parse.
        agent (str): The user agent for which to retrieve the specified rules.
        type_rule (str): The type of rule to retrieve (e.g., "Disallow" or "Allow").

    Returns:
     List[str]: A List of paths corresponding to the specified rules for the given user agent.
    """
    if not robot_txt:
        return []

    try:
        bots_rules = robot_txt.split(agent, 1)[1].split("User-agent", 1)[0].strip().split("\n")
    except IndexError:
        return []

    return [rule.removeprefix(f"{type_rule}: ") for rule in bots_rules if rule.startswith(f"{type_rule}: ")]


def check_rules(
    rules: dict[str, List[str]],
    paths: List[str],
) -> bool:
    """
    Evaluates access permissions for a given set of paths based on the rules defined for all bots and specific disallowed links.

    Args:
        rules (dict[str, List[str]]): A dictionary containing rules for
            all bots, with keys indicating the type of rule (allowed or
            disallowed) and values as Lists of corresponding paths.
        paths  List[str]): A List of path segments derived from the URL.

    Returns:
        bool: True if the paths are allowed according to the rules, False otherwise.
    """
    result = True

    for key, rule in rules.items():
        is_disallowed = key.endswith("disallowed")
        result = check_path_against_rules(paths, rule, not is_disallowed, result)

    return result


def check_path_against_rules(paths: List[str], rules: List[str], default: bool, previous_default: bool) -> bool:
    """
    Evaluates whether the constructed paths are allowed or disallowed based on the provided rules.

    Args:
        paths  List[str]): A List of path segments to check against the rules.
        rules  List[str]): A List of rules that define allowed or disallowed paths.
        default (bool): The default return value if the rules contain a wildcard.
        previous_default (bool): The previous default return value to consider.

    Returns:
        bool: True if the paths are allowed according to the rules, False if they are disallowed.
    """
    if not rules:
        return previous_default

    if "/" in rules:
        return default

    rules_set = set(rules)
    new_path = "/"
    for path in paths:
        new_path = os.path.join(new_path, path)
        if new_path in rules_set:
            return default

    return previous_default
