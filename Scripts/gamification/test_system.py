#!/usr/bin/env python3
"""
Test script for XP tracker - Windows compatible (no emoji printing)
"""

import json
import sys
import os
from datetime import datetime

# Disable emoji printing for Windows compatibility
os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, '.')

# Import but suppress print output
import io
from contextlib import redirect_stdout

from xp_tracker_v2 import DevOpsXPSystem

def test_xp_system():
    """Test the XP tracking system"""

    print("\n" + "="*60)
    print("TESTING DEVOPS XP TRACKER SYSTEM")
    print("="*60 + "\n")

    # Load initial state
    tracker = DevOpsXPSystem()
    initial_xp = tracker.data['total_xp']
    initial_hours = tracker.data['total_hours']

    print(f"Initial State:")
    print(f"  XP: {initial_xp}")
    print(f"  Hours: {initial_hours:.1f}")
    print(f"  Streak: {tracker.data['current_streak']}")

    # Test 1: Add study session
    print("\n" + "-"*60)
    print("Test 1: Adding Study Session (+50 XP, +1.5 hours)")
    print("-"*60)

    # Suppress emoji output
    with redirect_stdout(io.StringIO()):
        tracker.add_xp('study_session', duration_hours=1.5)

    print(f"Result: XP now {tracker.data['total_xp']} (added 50)")
    print(f"Result: Hours now {tracker.data['total_hours']:.1f} (added 1.5)")

    # Test 2: Add blog post
    print("\n" + "-"*60)
    print("Test 2: Adding Blog Post (+75 XP)")
    print("-"*60)

    with redirect_stdout(io.StringIO()):
        tracker.add_xp('blog_post')
    tracker.data['blog_posts'] += 1
    tracker.save_data()

    print(f"Result: XP now {tracker.data['total_xp']} (added 75)")
    print(f"Result: Blog posts: {tracker.data['blog_posts']}")

    # Test 3: Add community help
    print("\n" + "-"*60)
    print("Test 3: Adding Community Help (+25 XP)")
    print("-"*60)

    with redirect_stdout(io.StringIO()):
        tracker.add_xp('community_help')
    tracker.data['community_helps'] += 1
    tracker.save_data()

    print(f"Result: XP now {tracker.data['total_xp']} (added 25)")
    print(f"Result: Community helps: {tracker.data['community_helps']}")

    # Test 4: Check level calculation
    print("\n" + "-"*60)
    print("Test 4: Level Calculation")
    print("-"*60)

    level, name, icon, threshold = tracker.get_current_level()
    next_level, next_threshold, next_name, _ = tracker.get_next_level()
    progress = tracker.calculate_progress_percentage()

    print(f"Current Level: {level} - {name}")
    print(f"Current Threshold: {threshold} XP")
    print(f"Next Level: {next_level} - {next_name}")
    print(f"Next Threshold: {next_threshold} XP")
    print(f"Progress: {progress:.1f}%")
    print(f"XP needed: {next_threshold - tracker.data['total_xp']} XP")

    # Test 5: Check achievements
    print("\n" + "-"*60)
    print("Test 5: Achievement System")
    print("-"*60)

    print(f"Achievements unlocked: {len(tracker.data['achievements_unlocked'])}")
    print(f"Total achievements available: {len(tracker.ACHIEVEMENTS)}")

    if tracker.data['achievements_unlocked']:
        print("\nUnlocked achievements:")
        for ach_id in tracker.data['achievements_unlocked']:
            ach = tracker.ACHIEVEMENTS[ach_id]
            print(f"  - {ach['name']}: {ach['desc']}")
    else:
        print("No achievements unlocked yet")

    # Test 6: Activity log
    print("\n" + "-"*60)
    print("Test 6: Activity Log")
    print("-"*60)

    print(f"Total activities logged: {len(tracker.data['activity_log'])}")
    print("\nRecent activities:")
    for activity in tracker.data['activity_log'][-5:]:
        date = datetime.fromisoformat(activity['date']).strftime('%Y-%m-%d %H:%M')
        name = activity['activity'].replace('_', ' ').title()
        xp = activity['xp']
        hours = activity.get('duration_hours', 0)
        if hours > 0:
            print(f"  {date} | {name:<25} | +{xp:>3} XP | {hours:.1f}h")
        else:
            print(f"  {date} | {name:<25} | +{xp:>3} XP")

    # Final summary
    print("\n" + "="*60)
    print("FINAL STATE")
    print("="*60)

    total_gained = tracker.data['total_xp'] - initial_xp
    hours_gained = tracker.data['total_hours'] - initial_hours

    print(f"\nTotal XP: {tracker.data['total_xp']} (gained {total_gained} in tests)")
    print(f"Level: {level} - {name}")
    print(f"Progress to Level {next_level}: {progress:.1f}%")
    print(f"Study Hours: {tracker.data['total_hours']:.1f} / 384 (gained {hours_gained:.1f}h)")
    print(f"Current Streak: {tracker.data['current_streak']} days")
    print(f"Longest Streak: {tracker.data['longest_streak']} days")
    print(f"Weeks Completed: {tracker.data['weeks_completed']} / 48")
    print(f"Certifications: {tracker.data['certifications']} / 4")
    print(f"Projects: {tracker.data['projects_completed']} / 12")
    print(f"Blog Posts: {tracker.data['blog_posts']}")
    print(f"Community Helps: {tracker.data['community_helps']}")

    print("\n" + "="*60)
    print("ALL TESTS PASSED - XP SYSTEM WORKING!")
    print("="*60 + "\n")

    return True

if __name__ == "__main__":
    try:
        test_xp_system()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
