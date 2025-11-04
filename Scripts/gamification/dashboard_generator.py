#!/usr/bin/env python3
"""
DevOps Learning Journey - Dashboard Generator
Creates beautiful HTML dashboard with charts and progress visualization
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class DashboardGenerator:
    """Generate HTML dashboard with progress visualization"""
    
    XP_DATA_FILE = "xp_data.json"
    OUTPUT_FILE = "dashboard.html"
    
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
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """Load XP data"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
    def get_current_level(self):
        """Get current level info"""
        xp = self.data['total_xp']
        for i, (threshold, name, icon) in enumerate(reversed(self.LEVELS)):
            if xp >= threshold:
                level_num = len(self.LEVELS) - i
                return level_num, name, icon, threshold
        return 1, "Cloud Seedling", "🌱", 0
    
    def get_activity_by_day(self):
        """Get XP earned per day for chart"""
        if not self.data or not self.data['activity_log']:
            return []
        
        daily_xp = {}
        for activity in self.data['activity_log']:
            date = datetime.fromisoformat(activity['date']).date()
            date_str = date.strftime('%Y-%m-%d')
            if date_str not in daily_xp:
                daily_xp[date_str] = 0
            daily_xp[date_str] += activity['xp']
        
        # Sort by date and return list
        sorted_dates = sorted(daily_xp.keys())
        return [{'date': d, 'xp': daily_xp[d]} for d in sorted_dates]
    
    def get_weekly_summary(self):
        """Get weekly XP summary"""
        if not self.data or not self.data['activity_log']:
            return []
        
        weekly_xp = {}
        for activity in self.data['activity_log']:
            date = datetime.fromisoformat(activity['date']).date()
            week = date.isocalendar()[1]
            year = date.year
            key = f"{year}-W{week:02d}"
            if key not in weekly_xp:
                weekly_xp[key] = 0
            weekly_xp[key] += activity['xp']
        
        sorted_weeks = sorted(weekly_xp.keys())
        return [{'week': w, 'xp': weekly_xp[w]} for w in sorted_weeks]
    
    def get_level_progress_data(self):
        """Get progress through each level"""
        progress = []
        for i, (threshold, name, icon) in enumerate(self.LEVELS):
            level_num = i + 1
            xp = self.data['total_xp']
            
            if level_num == 1:
                prev_threshold = 0
            else:
                prev_threshold = self.LEVELS[i-1][0]
            
            if xp >= threshold:
                percentage = 100
            elif xp < prev_threshold:
                percentage = 0
            else:
                percentage = ((xp - prev_threshold) / (threshold - prev_threshold)) * 100
            
            progress.append({
                'level': level_num,
                'name': name,
                'icon': icon,
                'percentage': min(100, percentage)
            })
        
        return progress
    
    def generate_html(self):
        """Generate HTML dashboard"""
        if not self.data:
            return self.generate_empty_dashboard()
        
        level, level_name, icon, _ = self.get_current_level()
        daily_data = self.get_activity_by_day()
        weekly_data = self.get_weekly_summary()
        level_progress = self.get_level_progress_data()
        
        # Calculate stats
        total_days = (datetime.now().date() - datetime.fromisoformat(self.data['start_date']).date()).days + 1
        avg_xp_per_day = self.data['total_xp'] / total_days if total_days > 0 else 0
        
        # Generate chart data
        daily_labels = ','.join([f"'{d['date']}'" for d in daily_data[-30:]])  # Last 30 days
        daily_values = ','.join([str(d['xp']) for d in daily_data[-30:]])
        
        weekly_labels = ','.join([f"'{w['week']}'" for w in weekly_data[-12:]])  # Last 12 weeks
        weekly_values = ','.join([str(w['xp']) for w in weekly_data[-12:]])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Learning Journey - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .level-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .stat-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .level-progress {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .level-item {{
            margin-bottom: 20px;
        }}
        
        .level-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .level-name {{
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .level-bar {{
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }}
        
        .level-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
        }}
        
        .achievements-section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .achievement-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .achievement {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .achievement.unlocked {{
            background: linear-gradient(135deg, #ffd89b, #19547b);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 216, 155, 0.5);
        }}
        
        .achievement-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .achievement-name {{
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.9;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 DevOps Learning Dashboard</h1>
            <div class="level-badge">
                Level {level}: {icon} {level_name}
            </div>
            <p style="color: #666; margin-top: 10px;">
                Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-value">{self.data['total_xp']:,}</div>
                <div class="stat-label">Total XP</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-value">{self.data['current_streak']}</div>
                <div class="stat-label">Day Streak</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⏱️</div>
                <div class="stat-value">{self.data['total_hours']:.1f}</div>
                <div class="stat-label">Hours Studied</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-value">{len(self.data['achievements_unlocked'])}</div>
                <div class="stat-label">Achievements</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-value">{self.data['weeks_completed']}</div>
                <div class="stat-label">Weeks Done</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🎓</div>
                <div class="stat-value">{self.data['certifications']}</div>
                <div class="stat-label">Certifications</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">{self.data['projects_completed']}</div>
                <div class="stat-label">Projects</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{avg_xp_per_day:.0f}</div>
                <div class="stat-label">Avg XP/Day</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 class="chart-title">📈 Daily XP Progress (Last 30 Days)</h2>
            <canvas id="dailyChart"></canvas>
        </div>
        
        <div class="chart-container">
            <h2 class="chart-title">📊 Weekly XP Summary</h2>
            <canvas id="weeklyChart"></canvas>
        </div>
        
        <div class="level-progress">
            <h2 class="chart-title">🎖️ Level Progression</h2>
            {''.join([f'''
            <div class="level-item">
                <div class="level-header">
                    <span class="level-name">{lvl['icon']} Level {lvl['level']}: {lvl['name']}</span>
                    <span>{lvl['percentage']:.0f}%</span>
                </div>
                <div class="level-bar">
                    <div class="level-fill" style="width: {lvl['percentage']}%">
                        {f"{lvl['percentage']:.0f}%" if lvl['percentage'] > 20 else ''}
                    </div>
                </div>
            </div>
            ''' for lvl in level_progress])}
        </div>
        
        <div class="footer">
            <p>🚀 Keep going! You're on your way to DevOps Master! 🚀</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Journey started: {datetime.fromisoformat(self.data['start_date']).strftime('%B %d, %Y')}
            </p>
        </div>
    </div>
    
    <script>
        // Daily Chart
        const dailyCtx = document.getElementById('dailyChart').getContext('2d');
        new Chart(dailyCtx, {{
            type: 'line',
            data: {{
                labels: [{daily_labels}],
                datasets: [{{
                    label: 'XP Earned',
                    data: [{daily_values}],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value + ' XP';
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Weekly Chart
        const weeklyCtx = document.getElementById('weeklyChart').getContext('2d');
        new Chart(weeklyCtx, {{
            type: 'bar',
            data: {{
                labels: [{weekly_labels}],
                datasets: [{{
                    label: 'Weekly XP',
                    data: [{weekly_values}],
                    backgroundColor: 'rgba(118, 75, 162, 0.8)',
                    borderColor: '#764ba2',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value + ' XP';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def generate_empty_dashboard(self):
        """Generate dashboard when no data exists"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Learning Journey - Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        
        .message {
            background: white;
            color: #333;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        h1 { color: #667eea; }
        
        .icon { font-size: 5em; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="message">
        <div class="icon">🎮</div>
        <h1>No Data Yet!</h1>
        <p>Start tracking your progress with:</p>
        <code style="background: #f0f0f0; padding: 10px; display: inline-block; margin: 20px 0; border-radius: 5px;">
            ./xp log
        </code>
        <p>Your dashboard will appear here once you start earning XP!</p>
    </div>
</body>
</html>"""
    
    def save_dashboard(self):
        """Generate and save dashboard"""
        html = self.generate_html()
        
        with open(self.OUTPUT_FILE, 'w') as f:
            f.write(html)
        
        print(f"✅ Dashboard generated: {self.OUTPUT_FILE}")
        print(f"🌐 Open in browser: file://{os.path.abspath(self.OUTPUT_FILE)}")
        
        return os.path.abspath(self.OUTPUT_FILE)

def main():
    """Main function"""
    generator = DashboardGenerator()
    
    if not generator.data:
        print("⚠️  No XP data found!")
        print("Start tracking with: ./xp log")
        print("\nGenerating empty dashboard...")
    
    generator.save_dashboard()

if __name__ == "__main__":
    main()
