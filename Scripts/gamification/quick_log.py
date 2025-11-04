#!/usr/bin/env python3
"""
DevOps Learning Journey - Quick Daily Log
Simple one-command logging for daily progress
"""

import json
import os
import sys
from datetime import datetime

# Import from xp_tracker (assuming it's in same directory)
sys.path.insert(0, os.path.dirname(__file__))

try:
    from xp_tracker_v2 import DevOpsXPSystem
except ImportError:
    print("❌ Error: xp_tracker_v2.py not found!")
    print("Make sure both files are in the same directory.")
    sys.exit(1)

def quick_log():
    """Quick logging interface"""
    tracker = DevOpsXPSystem()
    
    print("\n" + "="*50)
    print("⚡ QUICK LOG ⚡".center(50))
    print("="*50 + "\n")
    
    # Quick options
    print("What did you do today?\n")
    print("1. 📚 Evening study session (1.5h)")
    print("2. 🧪 Weekend lab (3h)")
    print("3. 🎯 Project work (3h)")
    print("4. ✍️  Wrote blog post")
    print("5. 🤝 Helped someone")
    print("6. 🏆 Completed week/project")
    print("7. 📝 Custom entry")
    print("0. ❌ Cancel\n")
    
    choice = input("Choice (0-7): ").strip()
    
    if choice == '1':
        tracker.add_xp('study_session', duration_hours=1.5)
        tracker.update_streak()
        print("\n✅ Study session logged!")
        
    elif choice == '2':
        tracker.add_xp('lab_session', duration_hours=3)
        tracker.update_streak()
        print("\n✅ Lab session logged!")
        
    elif choice == '3':
        tracker.add_xp('project_session', duration_hours=3)
        tracker.update_streak()
        print("\n✅ Project work logged!")
        
    elif choice == '4':
        tracker.add_xp('blog_post')
        tracker.data['blog_posts'] += 1
        tracker.save_data()
        print("\n✅ Blog post logged!")
        
    elif choice == '5':
        count = int(input("How many people helped? ") or "1")
        for _ in range(count):
            tracker.add_xp('community_help')
        tracker.data['community_helps'] += count
        tracker.save_data()
        print(f"\n✅ {count} community help(s) logged!")
        
    elif choice == '6':
        tracker.add_xp('weekly_project')
        week = input("Week number completed? ")
        if week.isdigit():
            tracker.data['weeks_completed'] = max(tracker.data['weeks_completed'], int(week))
            tracker.data['projects_completed'] += 1
            tracker.save_data()
        print("\n✅ Week/project completed!")
        
    elif choice == '7':
        activity = input("Activity: ")
        xp = int(input("XP: "))
        hours = float(input("Hours (0 if none): ") or "0")
        tracker.add_xp(activity, xp, hours)
        print("\n✅ Custom entry logged!")
        
    elif choice == '0':
        print("\n❌ Cancelled")
        return
    
    else:
        print("\n❌ Invalid choice")
        return
    
    # Show updated stats
    tracker.display_status()
    
    # Offer to update markdown files
    update = input("\nUpdate README & tracker files? (y/n): ").strip().lower()
    if update == 'y':
        try:
            from progress_updater import ProgressUpdater
            updater = ProgressUpdater()
            updater.update_all()
        except ImportError:
            print("⚠️  progress_updater.py not found. Skipping file updates.")
    
    # Offer to commit
    commit = input("\nCommit to Git? (y/n): ").strip().lower()
    if commit == 'y':
        try:
            from git_integration import GitIntegration
            git = GitIntegration()
            activity_name = {
                '1': 'Study session',
                '2': 'Lab session',
                '3': 'Project work',
                '4': 'Blog post',
                '5': 'Community help',
                '6': 'Week completed',
                '7': 'Progress update'
            }.get(choice, 'Progress update')
            git.git_commit(activity_name)
        except ImportError:
            print("⚠️  git_integration.py not found. Skipping git commit.")

if __name__ == "__main__":
    quick_log()
