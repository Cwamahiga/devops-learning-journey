#!/usr/bin/env python3
"""
DevOps Learning Journey - Statistics Analyzer
Comprehensive analytics and insights tool
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class StatsAnalyzer:
    """Analyze learning patterns and provide insights"""
    
    XP_DATA_FILE = "xp_data.json"
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """Load XP data"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
    def get_daily_xp_stats(self):
        """Calculate daily XP statistics"""
        if not self.data or not self.data['activity_log']:
            return None
        
        daily_xp = defaultdict(int)
        for activity in self.data['activity_log']:
            date = datetime.fromisoformat(activity['date']).date()
            daily_xp[date] += activity['xp']
        
        xp_values = list(daily_xp.values())
        
        return {
            'mean': statistics.mean(xp_values),
            'median': statistics.median(xp_values),
            'mode': statistics.mode(xp_values) if len(set(xp_values)) < len(xp_values) else None,
            'stdev': statistics.stdev(xp_values) if len(xp_values) > 1 else 0,
            'min': min(xp_values),
            'max': max(xp_values),
            'total_days': len(daily_xp)
        }
    
    def get_activity_patterns(self):
        """Analyze activity patterns by day of week and time"""
        if not self.data or not self.data['activity_log']:
            return None
        
        by_weekday = defaultdict(int)
        by_hour = defaultdict(int)
        by_activity_type = defaultdict(int)
        
        for activity in self.data['activity_log']:
            dt = datetime.fromisoformat(activity['date'])
            
            # Day of week (0=Monday, 6=Sunday)
            by_weekday[dt.weekday()] += activity['xp']
            
            # Hour of day
            by_hour[dt.hour] += activity['xp']
            
            # Activity type
            by_activity_type[activity['activity']] += activity['xp']
        
        return {
            'by_weekday': dict(by_weekday),
            'by_hour': dict(by_hour),
            'by_type': dict(by_activity_type)
        }
    
    def get_productivity_analysis(self):
        """Analyze productivity trends"""
        if not self.data or not self.data['activity_log']:
            return None
        
        # Group by week
        weekly_xp = defaultdict(int)
        weekly_hours = defaultdict(float)
        
        for activity in self.data['activity_log']:
            dt = datetime.fromisoformat(activity['date'])
            week_key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
            
            weekly_xp[week_key] += activity['xp']
            weekly_hours[week_key] += activity.get('duration_hours', 0)
        
        # Calculate trends
        weeks = sorted(weekly_xp.keys())
        if len(weeks) < 2:
            return None
        
        first_week_xp = weekly_xp[weeks[0]]
        last_week_xp = weekly_xp[weeks[-1]]
        
        xp_trend = "increasing" if last_week_xp > first_week_xp else "decreasing" if last_week_xp < first_week_xp else "stable"
        
        return {
            'weeks_analyzed': len(weeks),
            'avg_weekly_xp': statistics.mean(weekly_xp.values()),
            'avg_weekly_hours': statistics.mean(weekly_hours.values()),
            'trend': xp_trend,
            'best_week_xp': max(weekly_xp.values()),
            'worst_week_xp': min(weekly_xp.values()),
            'consistency_score': (statistics.stdev(list(weekly_xp.values())) / statistics.mean(weekly_xp.values()) * 100) if len(weeks) > 1 else 0
        }
    
    def get_goal_progress(self):
        """Calculate progress towards goals"""
        if not self.data:
            return None
        
        total_days = (datetime.now().date() - datetime.fromisoformat(self.data['start_date']).date()).days + 1
        target_days = 336  # 48 weeks * 7 days
        
        return {
            'time_progress': (total_days / target_days) * 100,
            'xp_progress': (self.data['total_xp'] / 23000) * 100,  # Max level XP
            'hours_progress': (self.data['total_hours'] / 384) * 100,
            'weeks_progress': (self.data['weeks_completed'] / 48) * 100,
            'certs_progress': (self.data['certifications'] / 4) * 100,
            'projects_progress': (self.data['projects_completed'] / 12) * 100,
            'on_track': None
        }
    
    def calculate_projections(self):
        """Project when goals will be achieved"""
        if not self.data or not self.data['activity_log']:
            return None
        
        total_days = (datetime.now().date() - datetime.fromisoformat(self.data['start_date']).date()).days + 1
        
        if total_days == 0:
            return None
        
        avg_xp_per_day = self.data['total_xp'] / total_days
        avg_hours_per_day = self.data['total_hours'] / total_days
        
        # Project completion dates
        projections = {}
        
        if avg_xp_per_day > 0:
            days_to_max_level = (23000 - self.data['total_xp']) / avg_xp_per_day
            projections['max_level_date'] = (datetime.now() + timedelta(days=days_to_max_level)).date()
        
        if avg_hours_per_day > 0:
            days_to_384_hours = (384 - self.data['total_hours']) / avg_hours_per_day
            projections['target_hours_date'] = (datetime.now() + timedelta(days=days_to_384_hours)).date()
        
        return projections
    
    def get_recommendations(self):
        """Generate personalized recommendations"""
        if not self.data:
            return []
        
        recommendations = []
        
        daily_stats = self.get_daily_xp_stats()
        patterns = self.get_activity_patterns()
        productivity = self.get_productivity_analysis()
        
        # Consistency recommendations
        if self.data['current_streak'] < 7:
            recommendations.append({
                'category': 'Consistency',
                'priority': 'high',
                'message': f"Build your streak! You're at {self.data['current_streak']} days. Aim for 7+ days.",
                'action': "Schedule daily study time in your calendar"
            })
        
        # XP recommendations
        if daily_stats and daily_stats['mean'] < 57:  # 400/7
            recommendations.append({
                'category': 'XP Target',
                'priority': 'medium',
                'message': f"Average {daily_stats['mean']:.0f} XP/day. Target is ~57 XP/day for 400/week.",
                'action': "Add one extra study session per week"
            })
        
        # Hours recommendations
        total_days = (datetime.now().date() - datetime.fromisoformat(self.data['start_date']).date()).days + 1
        target_hours_per_day = 384 / 336  # ~1.14 hours/day
        actual_hours_per_day = self.data['total_hours'] / total_days if total_days > 0 else 0
        
        if actual_hours_per_day < target_hours_per_day:
            recommendations.append({
                'category': 'Study Time',
                'priority': 'medium',
                'message': f"Averaging {actual_hours_per_day:.1f} hrs/day. Target is ~1.1 hrs/day.",
                'action': "Add 15-minute study sessions on busy days"
            })
        
        # Productivity recommendations
        if productivity and productivity['consistency_score'] > 50:
            recommendations.append({
                'category': 'Consistency',
                'priority': 'high',
                'message': "Your weekly XP varies significantly. Aim for more consistent effort.",
                'action': "Set a fixed study schedule and stick to it"
            })
        
        # Achievement recommendations
        if len(self.data['achievements_unlocked']) < 3 and self.data['weeks_completed'] > 2:
            recommendations.append({
                'category': 'Achievements',
                'priority': 'low',
                'message': "Unlock more achievements to boost motivation!",
                'action': "Focus on building your study streak"
            })
        
        # Certification recommendations
        weeks_per_cert = 12  # Roughly
        if self.data['weeks_completed'] >= weeks_per_cert * (self.data['certifications'] + 1):
            recommendations.append({
                'category': 'Certifications',
                'priority': 'high',
                'message': "You're ready for your next certification!",
                'action': f"Schedule your exam for {['AWS CCP', 'AWS SAA', 'CKA', 'AWS SAP'][self.data['certifications']]}"
            })
        
        return recommendations
    
    def generate_full_report(self):
        """Generate comprehensive statistics report"""
        if not self.data:
            return "No data available yet. Start tracking with: ./xp log"
        
        daily_stats = self.get_daily_xp_stats()
        patterns = self.get_activity_patterns()
        productivity = self.get_productivity_analysis()
        goals = self.get_goal_progress()
        projections = self.calculate_projections()
        recommendations = self.get_recommendations()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              COMPREHENSIVE STATISTICS REPORT                  ║
║                  {datetime.now().strftime('%B %d, %Y')}                      ║
╚══════════════════════════════════════════════════════════════╝

📊 DAILY XP STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if daily_stats:
            report += f"""
Average XP/Day:           {daily_stats['mean']:.1f} XP
Median XP/Day:            {daily_stats['median']:.1f} XP
Standard Deviation:       {daily_stats['stdev']:.1f} XP
Best Day:                 {daily_stats['max']} XP
Slowest Day:              {daily_stats['min']} XP
Total Active Days:        {daily_stats['total_days']} days
"""
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += "📅 ACTIVITY PATTERNS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if patterns:
            report += "By Day of Week:\n"
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day_num, day_name in enumerate(days):
                xp = patterns['by_weekday'].get(day_num, 0)
                bar = '█' * int(xp / 50)
                report += f"{day_name:.<15} {xp:>5} XP {bar}\n"
            
            report += "\nMost Productive Day:      " + days[max(patterns['by_weekday'], key=patterns['by_weekday'].get)] if patterns['by_weekday'] else "N/A"
            report += "\n\nTop Activity Types:\n"
            for activity, xp in sorted(patterns['by_type'].items(), key=lambda x: x[1], reverse=True)[:5]:
                activity_name = activity.replace('_', ' ').title()
                report += f"{activity_name:.<25} {xp:>5} XP\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += "📈 PRODUCTIVITY ANALYSIS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if productivity:
            report += f"""Weeks Analyzed:           {productivity['weeks_analyzed']} weeks
Average Weekly XP:        {productivity['avg_weekly_xp']:.1f} XP
Target Weekly XP:         400 XP
Performance:              {(productivity['avg_weekly_xp']/400*100):.0f}% of target

Average Weekly Hours:     {productivity['avg_weekly_hours']:.1f} hours
Target Weekly Hours:      8 hours
Performance:              {(productivity['avg_weekly_hours']/8*100):.0f}% of target

Best Week:                {productivity['best_week_xp']:.0f} XP
Worst Week:               {productivity['worst_week_xp']:.0f} XP
Trend:                    {productivity['trend'].title()}
Consistency Score:        {100 - productivity['consistency_score']:.0f}/100
"""
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += "🎯 GOAL PROGRESS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if goals:
            report += f"""Time Elapsed:             {goals['time_progress']:.1f}% of 48 weeks
XP Progress:              {goals['xp_progress']:.1f}% to max level
Hours Progress:           {goals['hours_progress']:.1f}% to 384 hours
Weeks Progress:           {goals['weeks_progress']:.1f}% complete
Certifications:           {goals['certs_progress']:.1f}% complete
Projects:                 {goals['projects_progress']:.1f}% complete

Status: """
            
            # Determine if on track
            avg_progress = (goals['xp_progress'] + goals['hours_progress'] + goals['weeks_progress']) / 3
            if avg_progress >= goals['time_progress']:
                report += "✅ ON TRACK or AHEAD"
            elif avg_progress >= goals['time_progress'] * 0.9:
                report += "⚠️  SLIGHTLY BEHIND (catchable)"
            else:
                report += "❌ BEHIND (needs acceleration)"
        
        report += "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += "🔮 PROJECTIONS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if projections:
            report += "At current pace:\n\n"
            if 'max_level_date' in projections:
                report += f"Reach Max Level:          {projections['max_level_date'].strftime('%B %d, %Y')}\n"
            if 'target_hours_date' in projections:
                report += f"Complete 384 Hours:       {projections['target_hours_date'].strftime('%B %d, %Y')}\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += "💡 PERSONALIZED RECOMMENDATIONS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                emoji = priority_emoji.get(rec['priority'], '⚪')
                
                report += f"{i}. {emoji} {rec['category']} ({rec['priority'].upper()})\n"
                report += f"   {rec['message']}\n"
                report += f"   → Action: {rec['action']}\n\n"
        else:
            report += "Great job! Keep up the excellent work! 🎉\n\n"
        
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        report += f"""Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

╚══════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def save_report(self, filename=None):
        """Save statistics report to file"""
        if filename is None:
            filename = f"stats_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        report = self.generate_full_report()
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Statistics report saved: {filename}")
        return filename

def main():
    """Main function"""
    analyzer = StatsAnalyzer()
    
    if not analyzer.data:
        print("❌ No XP data found!")
        print("Start tracking with: ./xp log")
        return
    
    # Display report
    report = analyzer.generate_full_report()
    print(report)
    
    # Ask to save
    save = input("\nSave report to file? (y/n): ").strip().lower()
    if save == 'y':
        analyzer.save_report()

if __name__ == "__main__":
    main()
