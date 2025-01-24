import re
import csv
import sys
import os
import argparse
from datetime import datetime
import subprocess
import shutil

def select_log_file(log_dir):
    log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
    
    if not log_files:
        print("No log files found in the specified directory.")
        sys.exit(1)
    
    print("Available log files:")
    for idx, file in enumerate(log_files, 1):
        print(f"{idx}. {file}")
    
    while True:
        try:
            file_choice = int(input("Select a file by number: "))
            if 1 <= file_choice <= len(log_files):
                return os.path.join(log_dir, log_files[file_choice - 1])
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def parse_nginx_log(log_file, final_output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{timestamp}_output.csv"
    output_path = os.path.normpath(os.path.join(final_output_dir, output_filename))
    
    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)

    log_pattern = re.compile(
        r'(?P<remote_addr>\d+\.\d+\.\d+\.\d+)\s-\s-\s'
        r'\[(?P<time_local>.+?)\]\s'
        r'"(?P<request>.*?)"\s'
        r'(?P<status>\d+)\s'
        r'(?P<body_bytes_sent>\d+)\s'
        r'"(?P<http_referer>.*?)"\s'
        r'"(?P<http_user_agent>.*?)"'
    )

    with open(log_file, 'r') as f, open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['remote_addr', 'time_local', 'request', 'status', 'body_bytes_sent', 'http_referer', 'http_user_agent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in f:
            match = log_pattern.match(line)
            if match:
                writer.writerow(match.groupdict())

    print(f"Log has been parsed and saved to final directory: {output_path}")
    push_to_github(final_output_dir, timestamp)

def push_to_github(output_dir, timestamp):
    git_repo_url = "YOUR_GIT_REPO_URL"
    
    if not git_repo_url:
        print("No GitHub repository URL provided.")
        return

    try:
        subprocess.run(['git', 'init'], check=True)

        existing_remotes = subprocess.run(['git', 'remote'], capture_output=True, text=True, check=True)
        if 'origin' not in existing_remotes.stdout:
            subprocess.run(['git', 'remote', 'add', 'origin', git_repo_url], check=True)
        else:
            subprocess.run(['git', 'remote', 'set-url', 'origin', git_repo_url], check=True)

        subprocess.run(['git', 'fetch', 'origin'], check=True)
        subprocess.run(['git', 'reset', '--hard', 'origin/main'], check=True)

        subprocess.run(['git', 'add', output_dir], check=True)
        commit_message = f"Add parsed log files with timestamp {timestamp}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)

        print("Files pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pushing to GitHub: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse NGINX log files and upload results to GitHub.")
    parser.add_argument(
        '--log-dir',
        type=str,
        default="./logs",
        help="Directory containing log files (default: ./logs)"
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default="./output",
        help="Directory to save output files (default: ./output)"
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help="Automatically process the first log file (default: False)"
    )

    args = parser.parse_args()

    log_dir = args.log_dir
    final_output_dir = args.output_dir
    auto_mode = args.auto

    if not os.path.exists(log_dir):
        print(f"The log directory '{log_dir}' does not exist.")
        sys.exit(1)

    log_file = select_log_file(log_dir) if not auto_mode else os.path.join(log_dir, os.listdir(log_dir)[0])
    parse_nginx_log(log_file, final_output_dir)
