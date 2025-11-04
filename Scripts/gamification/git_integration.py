#!/usr/bin/env python3
"""
DevOps Learning Journey - Git Integration
Automatically commit with XP stats and maintain streak
"""

import json
import os
import subprocess
from datetime import datetime

class GitIntegration:
    """Git integration for automatic commits with XP tracking"""
    
    XP_DATA_FILE = "xp_data.json"
    
    def __init__(self):
        self.data = self.load_xp_data()
    
    def load_xp_data(self):
        """Load XP data"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
    def get_commit_message(self, activity, custom_msg=None):
        """Generate commit message with XP stats"""
        if not self.data:
            return f"📝 {activity}"
        
        level, level_name, icon = self.get_current_level()
        xp = self.data['total_xp']
        streak = self.data['current_streak']
        day = (datetime.now() - datetime.fromisoformat(self.data['start_date'])).days + 1
        
        if custom_msg:
            base_msg = custom_msg
        else:
            base_msg = f"Day {day}: {activity}"
        
        commit_msg = f"""📝 {base_msg}

Level: {level} - {level_name} {icon}
XP: {xp}
Streak: {streak} days 🔥"""
        
        return commit_msg
    
    def get_current_level(self):
        """Get current level"""
        xp = self.data['total_xp']
        levels = [
            (0, "Cloud Seedling", "🌱"),
            (500, "Cloud Apprentice", "☁️"),
            (1500, "DevOps Initiate", "🔧"),
            (3000, "Infrastructure Builder", "🛠️"),
            (5000, "Container Captain", "🐳"),
            (7500, "Automation Engineer", "⚙️"),
            (10500, "Kubernetes Commander", "☸️"),
            (14000, "Cloud Architect", "🏗️"),
            (18000, "DevOps Professional", "🚀"),
            (23000, "DevOps Master", "👑"),
        ]
        
        for i, (threshold, name, icon) in enumerate(reversed(levels)):
            if xp >= threshold:
                level_num = len(levels) - i
                return level_num, name, icon
        return 1, "Cloud Seedling", "🌱"
    
    def git_commit(self, activity, custom_msg=None, files=None):
        """Commit with XP stats"""
        try:
            # Check if in git repo
            subprocess.run(['git', 'status'], check=True, capture_output=True)
            
            # Add files
            if files:
                for file in files:
                    subprocess.run(['git', 'add', file], check=True)
            else:
                subprocess.run(['git', 'add', '.'], check=True)
            
            # Create commit message
            commit_msg = self.get_commit_message(activity, custom_msg)
            
            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                check=True,
                capture_output=True,
                text=True
            )
            
            print("✅ Git commit successful!")
            print(f"\n{commit_msg}\n")
            
            # Ask to push
            push = input("Push to remote? (y/n): ").strip().lower()
            if push == 'y':
                subprocess.run(['git', 'push'], check=True)
                print("✅ Pushed to remote!")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def main():
    """Main function"""
    git = GitIntegration()
    
    print("\n🔗 Git Integration\n")
    print("="*50)
    
    activity = input("What did you do? (e.g., 'Completed Week 1'): ").strip()
    
    if not activity:
        activity = "Updated progress"
    
    custom = input("Custom commit message? (leave empty for auto): ").strip()
    
    git.git_commit(activity, custom if custom else None)

if __name__ == "__main__":
    main()
