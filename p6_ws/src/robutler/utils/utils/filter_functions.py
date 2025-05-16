from typing import Dict, List

def filter_function_call(function_call: Dict, keys_to_remove: Dict[str, List[str]]) -> Dict:
    """
    Filters specific argument keys and removes return values from a function call.
    
    Args:
        function_call (Dict): The function call dictionary to filter.
        keys_to_remove (Dict[str, List[str]]): Mapping of function_name to a list of argument keys to remove.
        
    Returns:
        Dict: Filtered function call with specified keys removed and return_values omitted.
    """
    function_name = function_call.get("function_name")
    args = function_call.get("args", {}).copy()  # Prevent modifying the original

    # Remove specified keys if function_name matches
    keys_to_exclude = keys_to_remove.get(function_name, [])
    for key in keys_to_exclude:
        args.pop(key, None)  # Safely remove if exists

    # Build the filtered function call without return_values
    filtered_call = {
        "function_name": function_name,
        "args": args
    }

    return filtered_call

