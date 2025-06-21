import os
import shutil
import datetime
import json

class SimpleVC:
    def __init__(self):
        self.repo_dir = ".myvc"
        self.commits_file = os.path.join(self.repo_dir, "commits.json")
        
    def init(self):
        """Initialize version control"""
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            os.makedirs(os.path.join(self.repo_dir, "snapshots"))
            
            # Create commits file
            with open(self.commits_file, 'w') as f:
                json.dump([], f)
            
            print("✅ Version control initialized!")
            return True
        else:
            print("✅ Version control already exists!")
            return False
    
    def add_and_commit(self, filename, message):
        """Add file and create commit"""
        if not os.path.exists(filename):
            print(f"❌ File {filename} not found!")
            return
        
        # Load existing commits
        with open(self.commits_file, 'r') as f:
            commits = json.load(f)
        
        # Create new commit
        commit_id = len(commits) + 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Copy file to snapshots
        snapshot_name = f"commit_{commit_id}_{filename}"
        snapshot_path = os.path.join(self.repo_dir, "snapshots", snapshot_name)
        shutil.copy2(filename, snapshot_path)
        
        # Record commit
        commit_info = {
            "id": commit_id,
            "timestamp": timestamp,
            "message": message,
            "file": filename,
            "snapshot": snapshot_name
        }
        
        commits.append(commit_info)
        
        # Save commits
        with open(self.commits_file, 'w') as f:
            json.dump(commits, f, indent=2)
        
        print(f"✅ Commit {commit_id} created: {message}")
        print(f"📁 File: {filename}")
        print(f"🕒 Time: {timestamp}")
    
    def log(self):
        """Show commit history"""
        with open(self.commits_file, 'r') as f:
            commits = json.load(f)
        
        if not commits:
            print("No commits yet!")
            return
        
        print("\n📜 Commit History:")
        print("-" * 50)
        for commit in reversed(commits):  # Show newest first
            print(f"Commit {commit['id']}: {commit['message']}")
            print(f"  File: {commit['file']}")
            print(f"  Date: {commit['timestamp']}")
            print()

# Main execution
vc = SimpleVC()

print("🚀 Simple Version Control for Pyto")
print("=" * 40)

# Initialize
vc.init()

# Commit our calculator
vc.add_and_commit("calculator.py", "Initial commit: Add simple calculator")

# Show history
vc.log()

print("\n🎉 Your calculator is now version controlled!")
print("You can modify calculator.py and run this script again to create new commits!")
