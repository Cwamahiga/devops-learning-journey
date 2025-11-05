#!/usr/bin/env python3
"""
DevOps Learning Journey - Progress Updater
Automatically updates README and XP_TRACKER markdown files with current progress
"""

import json
import os
import re
from datetime import datetime

class ProgressUpdater:
    """Updates markdown files with current progress"""
    
    XP_DATA_FILE = "xp_data.json"
    README_FILE = "../../README.md"
    XP_TRACKER_FILE = "../../Gamification/XP_TRACKER.md"
    
    def __init__(self):
        self.data = self.load_xp_data()
        self.levels = [
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
    
    def load_xp_data(self):
        """Load XP data from JSON"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
    def get_current_level(self):
        """Get current level info"""
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(reversed(self.levels)):
            if xp >= threshold:
                level_num = len(self.levels) - i
                return level_num, name, icon, threshold
        return 1, "Cloud Seedling", "🌱", 0
    
    def get_next_level(self):
        """Get next level info"""
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(self.levels):
            if xp < threshold:
                return i + 1, threshold, name, icon
        return 10, 23000, "DevOps Master", "👑"
    
    def calculate_progress_percentage(self):
        """Calculate progress to next level"""
        level, _, _, current_threshold = self.get_current_level()
        next_level, next_threshold, _, _ = self.get_next_level()
        
        if level == 10:
            return 100
        
        xp_in_level = self.data['total_xp'] - current_threshold
        xp_needed = next_threshold - current_threshold
        
        if xp_needed == 0:
            return 100
        
        return min(100, max(0, (xp_in_level / xp_needed) * 100))
    
    def create_progress_bar(self, percentage, length=20):
        """Create visual progress bar"""
        filled = int(length * percentage / 100)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}] {percentage:.0f}%"
    
    def create_stats_block(self):
        """Create stats block for README"""
        if not self.data:
            return None
        
        level, level_name, icon, _ = self.get_current_level()
        next_level, next_threshold, _, _ = self.get_next_level()
        progress = self.calculate_progress_percentage()
        progress_bar = self.create_progress_bar(progress)
        
        stats = f"""```
█{'░' * 37} Week {self.data['weeks_completed']}/48 ({self.data['weeks_completed']*100//48}%)

Current Phase: {'Phase 1: Foundation' if self.data['weeks_completed'] <= 12 else 'Phase 2: Intermediate' if self.data['weeks_completed'] <= 28 else 'Phase 3: Advanced' if self.data['weeks_completed'] <= 40 else 'Phase 4: Professional'}
Current Week: Week {self.data['weeks_completed'] + 1}
Current Day: Day {(datetime.now() - datetime.fromisoformat(self.data['start_date'])).days + 1}
Hours Invested: {self.data['total_hours']:.1f} / 384 total
Study Sessions Completed: {len([a for a in self.data['activity_log'] if 'session' in a['activity']])} / 192
```"""
        return stats
    
    def create_gamification_stats(self):
        """Create gamification stats block"""
        if not self.data:
            return """```
Level:          [ 1 ] Cloud Seedling 🌱
Total XP:       [   0 / 500 ]
Streak:         [ 0 ] days
Achievements:   [ 0 / 85 ] unlocked
```"""
        
        level, level_name, icon, _ = self.get_current_level()
        next_level, next_threshold, _, _ = self.get_next_level()
        
        return f"""```
Level:          [ {level} ] {level_name} {icon}
Total XP:       [ {self.data['total_xp']:>5} / {next_threshold} ]
Streak:         [ {self.data['current_streak']} ] days 🔥
Achievements:   [ {len(self.data['achievements_unlocked'])} / 85 ] unlocked
```"""
    
    def update_readme(self):
        """Update main README with current stats"""
        if not os.path.exists(self.README_FILE) or not self.data:
            print("README or data not found")
            return

        with open(self.README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update progress tracker section
        stats_block = self.create_stats_block()
        pattern = r'```\n█.*?\n\nCurrent Phase:.*?\n```'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, stats_block, content, flags=re.DOTALL)
            print("Updated Progress Tracker in README")

        # Update gamification stats
        gamif_stats = self.create_gamification_stats()
        pattern2 = r'```\nLevel:.*?\n```'
        if re.search(pattern2, content, re.DOTALL):
            content = re.sub(pattern2, gamif_stats, content, flags=re.DOTALL)
            print("Updated Gamification Stats in README")

        # Save updated README
        with open(self.README_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        print("README.md updated successfully!")
    
    def update_xp_tracker(self):
        """Update XP_TRACKER.md with current progress"""
        if not os.path.exists(self.XP_TRACKER_FILE) or not self.data:
            print("XP_TRACKER or data not found")
            return

        with open(self.XP_TRACKER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        level, level_name, icon, _ = self.get_current_level()
        next_level, next_threshold, _, _ = self.get_next_level()
        progress = self.calculate_progress_percentage()
        progress_bar = self.create_progress_bar(progress)
        
        # Update header stats
        header_pattern = r'\*\*Last Updated:\*\* .*?\n\*\*Current Level:\*\* .*?\n\*\*Total XP:\*\* .*?'
        new_header = f"""**Last Updated:** {datetime.now().strftime('%B %d, %Y')}  
**Current Level:** {level} - {level_name} {icon}  
**Total XP:** {self.data['total_xp']} / {next_threshold} (to Level {next_level})"""
        
        if re.search(header_pattern, content, re.DOTALL):
            content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)
        
        # Update quick stats dashboard
        dashboard_pattern = r'⚡ Experience:.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n'
        
        new_dashboard = f"""⚡ Experience:          {self.data['total_xp']} / {next_threshold} XP
📈 Progress:            {progress_bar}
🔥 Study Streak:        {self.data['current_streak']} days
📅 Week Streak:         {self.data['weeks_completed']} weeks
💻 Commit Streak:       {self.data['current_streak']} days

🏆 Achievements:        {len(self.data['achievements_unlocked'])} / 85 unlocked
📚 Weeks Completed:     {self.data['weeks_completed']} / 48
🎓 Certifications:      {self.data['certifications']} / 4
🎯 Projects Done:       {self.data['projects_completed']} / 12

⏱️  Total Study Time:   {self.data['total_hours']:.1f} / 384 hours
📝 Blog Posts:          {self.data['blog_posts']}
💬 Community Helps:     {self.data['community_helps']}
"""
        
        if re.search(dashboard_pattern, content, re.DOTALL):
            content = re.sub(dashboard_pattern, new_dashboard, content, flags=re.DOTALL)
        
        # Save updated XP_TRACKER
        with open(self.XP_TRACKER_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        print("XP_TRACKER.md updated successfully!")
    
    def update_all(self):
        """Update all markdown files"""
        if not self.data:
            print("No XP data found. Run xp_tracker_v2.py first to create data.")
            return

        print("\nUpdating progress in all files...\n")
        self.update_readme()
        self.update_xp_tracker()
        print("\nAll files updated!\n")

def main():
    """Main function"""
    updater = ProgressUpdater()
    updater.update_all()

if __name__ == "__main__":
    main()
