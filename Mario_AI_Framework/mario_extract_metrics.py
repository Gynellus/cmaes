import re

def extract_results(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    
    # Extract the results using regular expressions
    level_pattern = re.compile(r"Level: (.+)")
    result_pattern = re.compile(r"Results: (.+)")
    
    levels = level_pattern.findall(data)
    results = result_pattern.findall(data)
    
    return levels, results

def calculate_metrics(levels, results):
    from collections import defaultdict
    import json
    
    level_metrics = defaultdict(lambda: {"wins": 0, "completionPercentages": []})
    
    for level, result in zip(levels, results):
        result_dict = json.loads(result.replace("'", '"'))  # Convert string to dictionary
        game_status = result_dict['gameStatus']
        completion_percentage = result_dict['completionPercentage']
        
        if game_status == 'WIN':
            level_metrics[level]["wins"] += 1
        level_metrics[level]["completionPercentages"].append(completion_percentage)
    
    metrics = {}
    for level, metrics_data in level_metrics.items():
        total_games = len(metrics_data["completionPercentages"])
        win_percentage = (metrics_data["wins"] / total_games) * 100
        avg_completion_percentage = sum(metrics_data["completionPercentages"]) / total_games
        
        metrics[level] = {
            "win_percentage": win_percentage,
            "avg_completion_percentage": avg_completion_percentage
        }
    
    return metrics

if __name__ == "__main__":
    levels, results = extract_results("game_results.txt")
    metrics = calculate_metrics(levels, results)
    
    for level, metric in metrics.items():
        print(f"Level: {level}")
        print(f"Win Percentage: {metric['win_percentage']}%")
        print(f"Average Completion Percentage: {metric['avg_completion_percentage']}\n")
