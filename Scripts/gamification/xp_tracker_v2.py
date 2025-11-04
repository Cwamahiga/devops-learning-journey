#!/usr/bin/env python3
"""
DevOps Learning Journey - XP Tracker
Fully functional gamification system with persistence
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

class DevOpsXPSystem:
    """Complete XP tracking system with persistence"""
    
    DATA_FILE = "xp_data.json"
    
    # XP Values
    XP_VALUES = {
        'study_session': 50,
        'lab_session': 100,
        'project_session': 100,
        'weekly_project': 200,
        'certification': 1000,
        'blog_post': 75,
        'community_help': 25,
        'open_source_pr': 150,
        'daily_challenge': 30,
        'documentation': 20,
        'bug_fix': 40,
        'diagram': 50,
        'deployment': 200,
    }
    
    # Level thresholds
    LEVELS = [
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
    
    # Achievements
    ACHIEVEMENTS = {
        # Learning achievements
        'first_steps': {'name': 'First Steps', 'desc': 'Complete Day 1', 'xp': 50, 'icon': '🏅'},
        'week_warrior': {'name': 'Week Warrior', 'desc': 'Complete first week', 'xp': 100, 'icon': '📅'},
        'monthly_master': {'name': 'Monthly Master', 'desc': 'Complete first month', 'xp': 200, 'icon': '📆'},
        
        # Streak achievements
        'streak_3': {'name': 'Getting Started', 'desc': '3-day streak', 'xp': 50, 'icon': '🌱'},
        'streak_7': {'name': 'Building Momentum', 'desc': '7-day streak', 'xp': 100, 'icon': '🔥'},
        'streak_14': {'name': 'On Fire', 'desc': '14-day streak', 'xp': 200, 'icon': '🔥🔥'},
        'streak_30': {'name': 'Unstoppable', 'desc': '30-day streak', 'xp': 500, 'icon': '🔥🔥🔥'},
        'streak_60': {'name': 'Legend', 'desc': '60-day streak', 'xp': 1000, 'icon': '⚡'},
        'streak_100': {'name': 'Immortal', 'desc': '100-day streak', 'xp': 2000, 'icon': '👑'},
        
        # Study hour achievements
        'hours_25': {'name': 'Quarter Century', 'desc': '25 hours studied', 'xp': 100, 'icon': '⏱️'},
        'hours_50': {'name': 'Half Century', 'desc': '50 hours studied', 'xp': 200, 'icon': '⏱️⏱️'},
        'hours_100': {'name': 'The Grind', 'desc': '100 hours studied', 'xp': 500, 'icon': '💪'},
        'hours_200': {'name': 'The Marathon', 'desc': '200 hours studied', 'xp': 1000, 'icon': '🏃'},
        'hours_384': {'name': 'The Mountain', 'desc': '384 hours studied', 'xp': 2000, 'icon': '🏔️'},
    }
    
    def __init__(self):
        self.data = self.load_data()
        
    def load_data(self):
        """Load progress data from JSON file"""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Warning: Could not read data file. Starting fresh.")
        
        # Default data structure
        return {
            'total_xp': 0,
            'current_streak': 0,
            'longest_streak': 0,
            'last_study_date': None,
            'achievements_unlocked': [],
            'activity_log': [],
            'total_hours': 0,
            'weeks_completed': 0,
            'certifications': 0,
            'projects_completed': 0,
            'blog_posts': 0,
            'community_helps': 0,
            'start_date': datetime.now().isoformat(),
            'level_history': [],
            'streak_freezes': 0,
        }
    
    def save_data(self):
        """Save progress data to JSON file"""
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
        print("💾 Progress saved!")
    
    def get_current_level(self):
        """Get current level based on XP"""
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(reversed(self.LEVELS)):
            if xp >= threshold:
                level_num = len(self.LEVELS) - i
                return level_num, name, icon, threshold
        return 1, "Cloud Seedling", "🌱", 0
    
    def get_next_level(self):
        """Get next level info"""
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(self.LEVELS):
            if xp < threshold:
                return i + 1, threshold, name, icon
        return 10, 23000, "DevOps Master", "👑"
    
    def calculate_progress_percentage(self):
        """Calculate progress to next level"""
        current_level, _, _, current_threshold = self.get_current_level()
        next_level, next_threshold, _, _ = self.get_next_level()
        
        if current_level == 10:
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
    
    def add_xp(self, activity, amount=None, duration_hours=0):
        """Add XP for an activity"""
        if amount is None:
            amount = self.XP_VALUES.get(activity, 0)
        
        old_level, _, _, _ = self.get_current_level()
        self.data['total_xp'] += amount
        new_level, level_name, icon, _ = self.get_current_level()
        
        # Log activity
        self.data['activity_log'].append({
            'date': datetime.now().isoformat(),
            'activity': activity,
            'xp': amount,
            'duration_hours': duration_hours
        })
        
        # Update hours
        if duration_hours > 0:
            self.data['total_hours'] += duration_hours
            self.check_hour_achievements()
        
        print(f"✅ +{amount} XP for {activity.replace('_', ' ').title()}")
        print(f"📊 Total XP: {self.data['total_xp']}")
        
        # Check level up
        if new_level > old_level:
            self.level_up(new_level, level_name, icon)
            self.data['level_history'].append({
                'level': new_level,
                'date': datetime.now().isoformat(),
                'total_xp': self.data['total_xp']
            })
        
        self.save_data()
        return amount
    
    def level_up(self, level, name, icon):
        """Handle level up event"""
        print("\n" + "="*50)
        print("🎉 LEVEL UP! 🎉".center(50))
        print("="*50)
        print(f"\n   You are now Level {level}: {icon} {name}!\n")
        print("="*50 + "\n")
    
    def update_streak(self, study_date=None):
        """Update study streak"""
        if study_date is None:
            study_date = datetime.now().date()
        else:
            study_date = datetime.fromisoformat(study_date).date() if isinstance(study_date, str) else study_date
        
        last_date = None
        if self.data['last_study_date']:
            last_date = datetime.fromisoformat(self.data['last_study_date']).date()
        
        if last_date is None:
            # First study day
            self.data['current_streak'] = 1
            print("🔥 Streak started: 1 day!")
        elif (study_date - last_date).days == 1:
            # Consecutive day
            self.data['current_streak'] += 1
            streak = self.data['current_streak']
            print(f"🔥 Streak: {streak} days!")
            
            # Update longest streak
            if streak > self.data['longest_streak']:
                self.data['longest_streak'] = streak
            
            # Check streak achievements
            self.check_streak_achievements()
            
        elif (study_date - last_date).days > 1:
            # Streak broken
            print(f"❌ Streak broken! (was {self.data['current_streak']} days)")
            print(f"💡 Starting fresh. You can do it!")
            self.data['current_streak'] = 1
        else:
            # Same day
            print(f"📅 Already studied today! Streak: {self.data['current_streak']} days")
        
        self.data['last_study_date'] = study_date.isoformat()
        self.save_data()
    
    def check_streak_achievements(self):
        """Check and unlock streak achievements"""
        streak = self.data['current_streak']
        
        achievements_to_check = [
            (3, 'streak_3'),
            (7, 'streak_7'),
            (14, 'streak_14'),
            (30, 'streak_30'),
            (60, 'streak_60'),
            (100, 'streak_100'),
        ]
        
        for threshold, achievement_id in achievements_to_check:
            if streak == threshold and achievement_id not in self.data['achievements_unlocked']:
                self.unlock_achievement(achievement_id)
                
                # Award streak bonus XP
                if streak == 7:
                    self.add_xp('streak_bonus', 100)
                elif streak == 30:
                    self.add_xp('streak_bonus', 500)
                    self.data['streak_freezes'] += 1
                    print(f"🧊 Earned a streak freeze! (Total: {self.data['streak_freezes']})")
    
    def check_hour_achievements(self):
        """Check and unlock hour-based achievements"""
        hours = self.data['total_hours']
        
        achievements_to_check = [
            (25, 'hours_25'),
            (50, 'hours_50'),
            (100, 'hours_100'),
            (200, 'hours_200'),
            (384, 'hours_384'),
        ]
        
        for threshold, achievement_id in achievements_to_check:
            if hours >= threshold and achievement_id not in self.data['achievements_unlocked']:
                self.unlock_achievement(achievement_id)
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement"""
        if achievement_id in self.data['achievements_unlocked']:
            return
        
        achievement = self.ACHIEVEMENTS[achievement_id]
        self.data['achievements_unlocked'].append(achievement_id)
        self.data['total_xp'] += achievement['xp']
        
        print("\n" + "🏆" * 25)
        print(f"   ACHIEVEMENT UNLOCKED!   ".center(50))
        print("🏆" * 25)
        print(f"\n   {achievement['icon']} {achievement['name']}")
        print(f"   {achievement['desc']}")
        print(f"   +{achievement['xp']} XP Bonus!\n")
        print("🏆" * 25 + "\n")
    
    def display_status(self):
        """Display current status dashboard"""
        level, level_name, icon, _ = self.get_current_level()
        next_level, next_threshold, next_name, next_icon = self.get_next_level()
        progress = self.calculate_progress_percentage()
        progress_bar = self.create_progress_bar(progress)
        
        xp_needed = next_threshold - self.data['total_xp']
        
        print("\n" + "━"*50)
        print(f"🎖️  LEVEL {level}: {icon} {level_name.upper()}".center(50))
        print("━"*50)
        print(f"⚡ XP:               {self.data['total_xp']} / {next_threshold}")
        print(f"📈 Progress:         {progress_bar}")
        print(f"🔥 Streak:           {self.data['current_streak']} days (best: {self.data['longest_streak']})")
        print(f"⏱️  Hours Studied:    {self.data['total_hours']:.1f} / 384 hours")
        print(f"🏆 Achievements:     {len(self.data['achievements_unlocked'])} / {len(self.ACHIEVEMENTS)}")
        print(f"📅 Weeks Done:       {self.data['weeks_completed']} / 48")
        print(f"🎓 Certifications:   {self.data['certifications']} / 4")
        print(f"🎯 Projects:         {self.data['projects_completed']} / 12")
        print("━"*50)
        if level < 10:
            print(f"🎯 NEXT: Level {next_level} - {next_icon} {next_name}")
            print(f"   Need {xp_needed} more XP")
        else:
            print("👑 MAX LEVEL REACHED! YOU'RE A DEVOPS MASTER! 👑")
        print("━"*50 + "\n")
    
    def get_stats_dict(self):
        """Get stats as dictionary for export"""
        level, level_name, icon, _ = self.get_current_level()
        progress = self.calculate_progress_percentage()
        
        return {
            'level': level,
            'level_name': level_name,
            'icon': icon,
            'total_xp': self.data['total_xp'],
            'progress_percentage': progress,
            'current_streak': self.data['current_streak'],
            'longest_streak': self.data['longest_streak'],
            'total_hours': self.data['total_hours'],
            'achievements_count': len(self.data['achievements_unlocked']),
            'weeks_completed': self.data['weeks_completed'],
            'certifications': self.data['certifications'],
            'projects_completed': self.data['projects_completed'],
        }
    
    def show_recent_activity(self, count=10):
        """Show recent activity log"""
        print(f"\n📝 Recent Activity (Last {count}):\n")
        print("─"*50)
        
        activities = self.data['activity_log'][-count:]
        for activity in reversed(activities):
            date = datetime.fromisoformat(activity['date']).strftime('%Y-%m-%d %H:%M')
            name = activity['activity'].replace('_', ' ').title()
            xp = activity['xp']
            print(f"{date} │ {name:<25} │ +{xp:>4} XP")
        
        print("─"*50 + "\n")
    
    def show_achievements(self):
        """Show all achievements"""
        print("\n🏆 ACHIEVEMENTS\n")
        print("="*60)
        
        unlocked_count = len(self.data['achievements_unlocked'])
        total_count = len(self.ACHIEVEMENTS)
        
        print(f"Unlocked: {unlocked_count} / {total_count}\n")
        
        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            unlocked = achievement_id in self.data['achievements_unlocked']
            status = "✅" if unlocked else "🔒"
            icon = achievement['icon'] if unlocked else "❓"
            name = achievement['name'] if unlocked else "???"
            desc = achievement['desc'] if unlocked else "Locked"
            xp = achievement['xp']
            
            print(f"{status} {icon} {name:<25} │ {desc:<25} │ {xp:>4} XP")
        
        print("="*60 + "\n")

def main_menu():
    """Interactive main menu"""
    tracker = DevOpsXPSystem()
    
    while True:
        print("\n" + "="*50)
        print("🎮 DEVOPS XP TRACKER 🎮".center(50))
        print("="*50)
        print("\n1.  ✅ Log Study Session (50 XP)")
        print("2.  🧪 Log Lab Session (100 XP)")
        print("3.  🎯 Log Project Work (100 XP)")
        print("4.  📝 Log Blog Post (75 XP)")
        print("5.  🤝 Log Community Help (25 XP)")
        print("6.  🏆 Complete Weekly Project (200 XP)")
        print("7.  🎓 Pass Certification (1000 XP)")
        print("8.  💻 Custom Activity & XP")
        print("9.  📊 View Status")
        print("10. 📝 Recent Activity")
        print("11. 🏆 View Achievements")
        print("12. 📈 Export Stats")
        print("13. 🔄 Reset Data (⚠️  DANGER)")
        print("0.  ❌ Exit & Save")
        print("="*50)
        
        choice = input("\nChoice (0-13): ").strip()
        
        if choice == '1':
            hours = float(input("Hours studied (default 1.5): ") or "1.5")
            tracker.add_xp('study_session', duration_hours=hours)
            tracker.update_streak()
            tracker.display_status()
            
        elif choice == '2':
            hours = float(input("Hours in lab (default 3): ") or "3")
            tracker.add_xp('lab_session', duration_hours=hours)
            tracker.display_status()
            
        elif choice == '3':
            hours = float(input("Hours on project (default 3): ") or "3")
            tracker.add_xp('project_session', duration_hours=hours)
            tracker.display_status()
            
        elif choice == '4':
            tracker.add_xp('blog_post')
            tracker.data['blog_posts'] += 1
            tracker.save_data()
            tracker.display_status()
            
        elif choice == '5':
            tracker.add_xp('community_help')
            tracker.data['community_helps'] += 1
            tracker.save_data()
            tracker.display_status()
            
        elif choice == '6':
            tracker.add_xp('weekly_project')
            tracker.data['projects_completed'] += 1
            week = input("Which week completed? (1-48): ").strip()
            if week.isdigit():
                tracker.data['weeks_completed'] = max(tracker.data['weeks_completed'], int(week))
            tracker.save_data()
            tracker.display_status()
            
        elif choice == '7':
            cert_name = input("Certification name: ")
            tracker.add_xp('certification')
            tracker.data['certifications'] += 1
            tracker.save_data()
            print(f"\n🎉🎉🎉 CONGRATULATIONS ON {cert_name.upper()}! 🎉🎉🎉")
            tracker.display_status()
            
        elif choice == '8':
            activity = input("Activity name: ")
            try:
                amount = int(input("XP amount: "))
                hours = float(input("Hours (0 if not applicable): ") or "0")
                tracker.add_xp(activity, amount, hours)
                tracker.display_status()
            except ValueError:
                print("❌ Invalid input")
                
        elif choice == '9':
            tracker.display_status()
            
        elif choice == '10':
            count = int(input("How many activities to show? (default 10): ") or "10")
            tracker.show_recent_activity(count)
            
        elif choice == '11':
            tracker.show_achievements()
            
        elif choice == '12':
            stats = tracker.get_stats_dict()
            print("\n📊 Current Stats:")
            print(json.dumps(stats, indent=2))
            
        elif choice == '13':
            confirm = input("⚠️  Are you SURE? Type 'RESET' to confirm: ")
            if confirm == 'RESET':
                if os.path.exists(tracker.DATA_FILE):
                    os.remove(tracker.DATA_FILE)
                print("✅ Data reset!")
                tracker = DevOpsXPSystem()
            else:
                print("❌ Reset cancelled")
                
        elif choice == '0':
            tracker.save_data()
            print("\n✅ Progress saved!")
            print("🔥 Keep up the great work!")
            print(f"📊 Final XP: {tracker.data['total_xp']}\n")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--status':
            tracker = DevOpsXPSystem()
            tracker.display_status()
        elif sys.argv[1] == '--quick':
            tracker = DevOpsXPSystem()
            tracker.add_xp('study_session', duration_hours=1.5)
            tracker.update_streak()
            tracker.display_status()
        else:
            print("Usage: python3 xp_tracker_v2.py [--status | --quick]")
    else:
        main_menu()
