#!/usr/bin/env python3
"""
DevOps Learning Journey - Weekly Report Generator
Creates detailed weekly progress reports
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class WeeklyReportGenerator:
    """Generate comprehensive weekly progress reports"""
    
    XP_DATA_FILE = "xp_data.json"
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """Load XP data"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
    def get_this_week_activities(self):
        """Get activities from this week"""
        if not self.data or not self.data['activity_log']:
            return []
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        this_week = []
        for activity in self.data['activity_log']:
            activity_date = datetime.fromisoformat(activity['date']).date()
            if activity_date >= week_start:
                this_week.append(activity)
        
        return this_week
    
    def get_last_week_activities(self):
        """Get activities from last week"""
        if not self.data or not self.data['activity_log']:
            return []
        
        today = datetime.now().date()
        this_week_start = today - timedelta(days=today.weekday())
        last_week_start = this_week_start - timedelta(days=7)
        
        last_week = []
        for activity in self.data['activity_log']:
            activity_date = datetime.fromisoformat(activity['date']).date()
            if last_week_start <= activity_date < this_week_start:
                last_week.append(activity)
        
        return last_week
    
    def calculate_week_stats(self, activities):
        """Calculate stats for a week"""
        total_xp = sum(a['xp'] for a in activities)
        total_hours = sum(a.get('duration_hours', 0) for a in activities)
        
        # Group by activity type
        by_type = defaultdict(int)
        by_type_hours = defaultdict(float)
        
        for activity in activities:
            activity_type = activity['activity']
            by_type[activity_type] += activity['xp']
            by_type_hours[activity_type] += activity.get('duration_hours', 0)
        
        # Count days with activity
        unique_days = set()
        for activity in activities:
            date = datetime.fromisoformat(activity['date']).date()
            unique_days.add(date)
        
        return {
            'total_xp': total_xp,
            'total_hours': total_hours,
            'activity_days': len(unique_days),
            'by_type': dict(by_type),
            'by_type_hours': dict(by_type_hours),
            'activity_count': len(activities)
        }
    
    def generate_report(self):
        """Generate weekly report"""
        if not self.data:
            return "No data available yet. Start tracking with: ./xp log"
        
        this_week = self.get_this_week_activities()
        last_week = self.get_last_week_activities()
        
        this_week_stats = self.calculate_week_stats(this_week)
        last_week_stats = self.calculate_week_stats(last_week)
        
        # Calculate changes
        xp_change = this_week_stats['total_xp'] - last_week_stats['total_xp']
        xp_change_pct = (xp_change / last_week_stats['total_xp'] * 100) if last_week_stats['total_xp'] > 0 else 0
        
        hours_change = this_week_stats['total_hours'] - last_week_stats['total_hours']
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    WEEKLY PROGRESS REPORT                     ║
║              {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}                  ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total XP This Week:       {this_week_stats['total_xp']:>6} XP
Last Week:                {last_week_stats['total_xp']:>6} XP
Change:                   {xp_change:>+6} XP ({xp_change_pct:+.1f}%)

Hours Studied This Week:  {this_week_stats['total_hours']:>6.1f} hrs
Last Week:                {last_week_stats['total_hours']:>6.1f} hrs
Change:                   {hours_change:>+6.1f} hrs

Active Days This Week:    {this_week_stats['activity_days']:>6} / 7 days
Activities Logged:        {this_week_stats['activity_count']:>6}

Current Level:            Level {self.get_current_level()[0]} - {self.get_current_level()[1]} {self.get_current_level()[2]}
Current XP:               {self.data['total_xp']:,} XP
Current Streak:           {self.data['current_streak']} days 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 ACTIVITY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Activity breakdown
        for activity_type, xp in sorted(this_week_stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            hours = this_week_stats['by_type_hours'].get(activity_type, 0)
            activity_name = activity_type.replace('_', ' ').title()
            report += f"{activity_name:<25} {xp:>6} XP"
            if hours > 0:
                report += f"  ({hours:.1f} hrs)"
            report += "\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Overall progress
        completion = (self.data['weeks_completed'] / 48) * 100
        hours_completion = (self.data['total_hours'] / 384) * 100
        
        report += f"""🎯 OVERALL PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Weeks Completed:          {self.data['weeks_completed']} / 48  ({completion:.1f}%)
Hours Completed:          {self.data['total_hours']:.1f} / 384  ({hours_completion:.1f}%)
Certifications:           {self.data['certifications']} / 4
Projects Completed:       {self.data['projects_completed']} / 12
Blog Posts Written:       {self.data['blog_posts']}
Community Helps:          {self.data['community_helps']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 ACHIEVEMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Unlocked:           {len(self.data['achievements_unlocked'])} / 14

Recent Unlocks:
"""
        
        # Show recent achievements (last 5)
        recent_achievements = self.data['achievements_unlocked'][-5:] if self.data['achievements_unlocked'] else []
        
        achievement_names = {
            'first_steps': '🏅 First Steps',
            'week_warrior': '📅 Week Warrior',
            'monthly_master': '📆 Monthly Master',
            'streak_3': '🌱 Getting Started',
            'streak_7': '🔥 Building Momentum',
            'streak_14': '🔥🔥 On Fire',
            'streak_30': '🔥🔥🔥 Unstoppable',
            'streak_60': '⚡ Legend',
            'streak_100': '👑 Immortal',
            'hours_25': '⏱️ Quarter Century',
            'hours_50': '⏱️⏱️ Half Century',
            'hours_100': '💪 The Grind',
            'hours_200': '🏃 The Marathon',
            'hours_384': '🏔️ The Mountain',
        }
        
        if recent_achievements:
            for ach in recent_achievements:
                report += f"  ✓ {achievement_names.get(ach, ach)}\n"
        else:
            report += "  No achievements unlocked yet\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Performance metrics
        avg_xp_per_day = self.data['total_xp'] / ((datetime.now().date() - datetime.fromisoformat(self.data['start_date']).date()).days + 1)
        avg_hours_per_week = self.data['total_hours'] / max(1, self.data['weeks_completed'])
        
        report += f"""📊 PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Average XP/Day:           {avg_xp_per_day:.1f} XP
Target XP/Week:           400 XP
This Week's Performance:  {(this_week_stats['total_xp']/400*100):.0f}% of target

Average Hours/Week:       {avg_hours_per_week:.1f} hrs
Target Hours/Week:        8 hrs
This Week's Performance:  {(this_week_stats['total_hours']/8*100):.0f}% of target

Longest Streak:           {self.data['longest_streak']} days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS & RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Generate insights
        insights = []
        
        if this_week_stats['total_xp'] >= 400:
            insights.append("✅ Great job! You hit your weekly XP target!")
        elif this_week_stats['total_xp'] >= 300:
            insights.append("👍 Good progress! You're close to your weekly goal.")
        else:
            insights.append("💪 Keep pushing! Try to hit 400 XP this week.")
        
        if this_week_stats['activity_days'] >= 5:
            insights.append("🔥 Excellent consistency! You studied most days this week.")
        elif this_week_stats['activity_days'] >= 3:
            insights.append("👌 Good consistency. Try to study at least 5 days per week.")
        else:
            insights.append("📅 Aim for more consistent study days throughout the week.")
        
        if self.data['current_streak'] >= 7:
            insights.append(f"🏆 Amazing streak! {self.data['current_streak']} days strong!")
        elif self.data['current_streak'] >= 3:
            insights.append("🌱 Building momentum! Keep your streak going!")
        
        if xp_change > 0:
            insights.append(f"📈 You earned {xp_change} more XP than last week!")
        elif xp_change < 0:
            insights.append("📉 Try to match or exceed last week's XP!")
        
        for insight in insights:
            report += f"\n{insight}"
        
        report += "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Next week goals
        report += f"""🎯 GOALS FOR NEXT WEEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Earn at least 400 XP
□ Study 8+ hours
□ Maintain {self.data['current_streak'] + 7}-day streak
□ Complete week {self.data['weeks_completed'] + 1} curriculum
□ Log activity at least 5 days
□ Write a blog post (if scheduled)
□ Help someone in the community

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Keep up the great work! 🚀

╚══════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def get_current_level(self):
        """Get current level"""
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
        
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(reversed(levels)):
            if xp >= threshold:
                return len(levels) - i, name, icon
        return 1, "Cloud Seedling", "🌱"
    
    def save_report(self, filename=None):
        """Save report to file"""
        if filename is None:
            filename = f"weekly_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Weekly report saved: {filename}")
        return filename

def main():
    """Main function"""
    generator = WeeklyReportGenerator()
    
    if not generator.data:
        print("❌ No XP data found!")
        print("Start tracking with: ./xp log")
        return
    
    # Print report to console
    report = generator.generate_report()
    print(report)
    
    # Ask to save
    save = input("\nSave report to file? (y/n): ").strip().lower()
    if save == 'y':
        generator.save_report()

if __name__ == "__main__":
    main()
