#!/usr/bin/env python3
"""
DevOps Learning Journey - Social Media Share Generator
Generate shareable content for Twitter, LinkedIn, etc.
"""

import json
import os
from datetime import datetime

class SocialShareGenerator:
    """Generate social media shareable content"""
    
    XP_DATA_FILE = "xp_data.json"
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """Load XP data"""
        if os.path.exists(self.XP_DATA_FILE):
            with open(self.XP_DATA_FILE, 'r') as f:
                return json.load(f)
        return None
    
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
    
    def generate_level_up_post(self):
        """Generate level-up announcement"""
        level, name, icon = self.get_current_level()
        
        tweets = [
            f"🎉 LEVEL UP! 🎉\n\nJust reached Level {level}: {icon} {name} on my #DevOps learning journey!\n\n⚡ {self.data['total_xp']:,} XP earned\n🔥 {self.data['current_streak']} day streak\n⏱️ {self.data['total_hours']:.0f} hours studied\n\n#100DaysOfCode #CloudComputing #DevOpsJourney",
            
            f"Level {level} unlocked! {icon}\n\nProud to announce I'm now a {name} in my DevOps journey!\n\nProgress:\n✅ {self.data['total_xp']:,} XP\n✅ {self.data['weeks_completed']}/48 weeks\n✅ {self.data['certifications']}/4 certs\n\n#DevOps #Learning #CloudSkills",
            
            f"🚀 Achievement Unlocked! 🚀\n\n{icon} {name}\n\nMy DevOps learning stats:\n• Level {level}\n• {self.data['total_hours']:.0f} hours invested\n• {self.data['current_streak']} day streak 🔥\n• {self.data['projects_completed']} projects built\n\nThe grind continues! 💪\n\n#DevOps #TechCareer"
        ]
        
        return tweets
    
    def generate_streak_post(self):
        """Generate streak milestone post"""
        streak = self.data['current_streak']
        
        if streak >= 100:
            milestone = "100-DAY"
            emoji = "👑"
        elif streak >= 60:
            milestone = "60-DAY"
            emoji = "⚡"
        elif streak >= 30:
            milestone = "30-DAY"
            emoji = "🔥🔥🔥"
        elif streak >= 14:
            milestone = "14-DAY"
            emoji = "🔥🔥"
        elif streak >= 7:
            milestone = "7-DAY"
            emoji = "🔥"
        else:
            milestone = f"{streak}-DAY"
            emoji = "🌱"
        
        posts = [
            f"{emoji} {milestone} STREAK! {emoji}\n\nConsistency is key! {streak} consecutive days of DevOps learning.\n\n📊 Stats:\n• {self.data['total_xp']:,} XP earned\n• {self.data['total_hours']:.0f} hours invested\n• Level {self.get_current_level()[0]}\n\n#DevOps #Consistency #LearningInPublic",
            
            f"Day {streak} of learning DevOps! 🎯\n\nNever breaking the chain! Here's what {streak} days of consistency looks like:\n\n✅ {self.data['total_hours']:.0f} hours studied\n✅ {self.data['projects_completed']} projects\n✅ {len(self.data['achievements_unlocked'])} achievements\n\n#100DaysOfCode #DevOps",
            
            f"{streak} days and counting! {emoji}\n\nMy DevOps journey update:\n• Study streak: {streak} days\n• Current level: {self.get_current_level()[0]}\n• XP earned: {self.data['total_xp']:,}\n• Hours invested: {self.data['total_hours']:.0f}\n\nConsistency beats intensity! 💪\n\n#DevOps #TechLearning"
        ]
        
        return posts
    
    def generate_certification_post(self, cert_name):
        """Generate certification announcement"""
        posts = [
            f"🎓 CERTIFIED! 🎓\n\nJust passed {cert_name}!\n\nThis marks certification #{self.data['certifications']} in my DevOps journey.\n\n📊 Journey stats:\n• Level {self.get_current_level()[0]}\n• {self.data['total_hours']:.0f} hours studied\n• {self.data['weeks_completed']} weeks completed\n\n#AWS #Kubernetes #DevOps #Certified",
            
            f"✅ {cert_name} - PASSED! ✅\n\nAnother milestone in my cloud journey!\n\nStudy approach:\n• Consistent daily practice\n• Hands-on projects\n• {self.data['total_hours']:.0f} total hours\n• {self.data['current_streak']} day streak\n\nOnto the next one! 🚀\n\n#CloudCertification #DevOps",
            
            f"New certification unlocked! 🏆\n\n{cert_name}\n\nCertification {self.data['certifications']}/4 complete!\n\nWhat's working:\n✅ Consistent study schedule\n✅ Hands-on practice\n✅ Building real projects\n✅ Community engagement\n\n#DevOpsCertified #CloudSkills"
        ]
        
        return posts
    
    def generate_weekly_update(self):
        """Generate weekly progress update"""
        completion = (self.data['weeks_completed'] / 48) * 100
        level, name, icon = self.get_current_level()
        
        posts = [
            f"📅 Week {self.data['weeks_completed']} Complete!\n\nDevOps learning journey update:\n\n🎖️ Level {level}: {icon} {name}\n⚡ {self.data['total_xp']:,} XP\n🔥 {self.data['current_streak']} day streak\n📊 {completion:.0f}% complete\n\nFeeling unstoppable! 💪\n\n#DevOps #WeeklyProgress #LearningInPublic",
            
            f"Week {self.data['weeks_completed']}/48 ✅\n\nProgress update on my DevOps certification path:\n\n• Current: {icon} {name}\n• XP earned: {self.data['total_xp']:,}\n• Hours: {self.data['total_hours']:.0f}\n• Projects: {self.data['projects_completed']}\n• Streak: {self.data['current_streak']} days 🔥\n\nThe journey continues! 🚀\n\n#DevOps #CloudComputing",
            
            f"🎯 Week {self.data['weeks_completed']} in the books!\n\nMy DevOps stats:\n→ Level {level}\n→ {self.data['total_hours']:.0f} hours invested\n→ {len(self.data['achievements_unlocked'])} achievements\n→ {self.data['certifications']} certifications\n\n{48 - self.data['weeks_completed']} weeks to go!\n\n#DevOps #TechCareer #ConsistencyIsKey"
        ]
        
        return posts
    
    def generate_project_post(self, project_name):
        """Generate project completion post"""
        posts = [
            f"🎯 Project Complete! 🎯\n\n{project_name}\n\nJust shipped project #{self.data['projects_completed']} in my DevOps journey!\n\nTech stack & learnings in thread... 🧵👇\n\n#DevOps #ProjectBased #BuildInPublic",
            
            f"✅ {project_name}\n\nAnother project in the bag! This one taught me:\n• [Key learning 1]\n• [Key learning 2]\n• [Key learning 3]\n\nCode: [GitHub link]\n\nProject {self.data['projects_completed']}/12 ✓\n\n#DevOps #Kubernetes #Docker #AWS",
            
            f"Built and deployed: {project_name} 🚀\n\nThis project covered:\n→ Infrastructure as Code\n→ CI/CD pipelines\n→ Container orchestration\n\nProgress: {self.data['projects_completed']}/12 projects\n\nGitHub: [link]\n\n#DevOps #CloudNative #InfraAsCode"
        ]
        
        return posts
    
    def generate_achievement_post(self, achievement_name):
        """Generate achievement unlock post"""
        achievement_emojis = {
            'first_steps': '🏅',
            'week_warrior': '📅',
            'streak_7': '🔥',
            'streak_30': '🔥🔥🔥',
            'streak_100': '👑',
            'hours_100': '💪',
            'hours_384': '🏔️',
        }
        
        emoji = achievement_emojis.get(achievement_name, '🏆')
        
        posts = [
            f"{emoji} Achievement Unlocked! {emoji}\n\n{achievement_name.replace('_', ' ').title()}\n\nDevOps journey update:\n• Level {self.get_current_level()[0]}\n• {self.data['total_xp']:,} XP\n• {len(self.data['achievements_unlocked'])} achievements\n• {self.data['current_streak']} day streak\n\n#DevOps #Achievement #Milestone",
            
            f"🎉 New Achievement! 🎉\n\n{achievement_name.replace('_', ' ').title()} {emoji}\n\nProgress stats:\n→ XP: {self.data['total_xp']:,}\n→ Hours: {self.data['total_hours']:.0f}\n→ Achievements: {len(self.data['achievements_unlocked'])}\n\nFeeling motivated! 💪\n\n#DevOps #Gamification"
        ]
        
        return posts
    
    def generate_linkedin_post(self):
        """Generate LinkedIn post format"""
        level, name, icon = self.get_current_level()
        completion = (self.data['weeks_completed'] / 48) * 100
        
        post = f"""🚀 DevOps Learning Journey Update 🚀

I'm excited to share my progress on my structured 12-month DevOps and Cloud Solutions Architecture certification path!

📊 Current Status:
• Level {level}: {icon} {name}
• {self.data['total_xp']:,} XP earned through consistent practice
• {self.data['total_hours']:.0f} hours of hands-on learning
• {self.data['current_streak']} day learning streak 🔥
• {self.data['weeks_completed']}/48 weeks completed ({completion:.0f}%)

🎓 Certifications:
{"✅" if self.data['certifications'] >= 1 else "🎯"} AWS Cloud Practitioner
{"✅" if self.data['certifications'] >= 2 else "🎯"} AWS Solutions Architect Associate
{"✅" if self.data['certifications'] >= 3 else "🎯"} Certified Kubernetes Administrator
{"✅" if self.data['certifications'] >= 4 else "🎯"} AWS Solutions Architect Professional

💻 Projects Completed: {self.data['projects_completed']}/12
📝 Blog Posts Written: {self.data['blog_posts']}
🤝 Community Contributions: {self.data['community_helps']}

Key Learnings:
• Consistency beats intensity - daily practice builds real skills
• Hands-on projects cement theoretical knowledge
• Community engagement accelerates learning
• Gamification makes the journey enjoyable

What's been your biggest learning from your tech journey? Share in the comments! 👇

#DevOps #CloudComputing #AWS #Kubernetes #ContinuousLearning #TechCareers #CloudArchitecture #SRE
"""
        
        return post
    
    def display_all_options(self):
        """Display all shareable content options"""
        if not self.data:
            print("❌ No data available yet!")
            return
        
        print("\n" + "="*60)
        print("📱 SOCIAL MEDIA SHARE GENERATOR 📱".center(60))
        print("="*60 + "\n")
        
        print("Choose content type:\n")
        print("1. 🎉 Level-Up Announcement")
        print("2. 🔥 Streak Milestone")
        print("3. 🎓 Certification Post")
        print("4. 📅 Weekly Update")
        print("5. 🎯 Project Completion")
        print("6. 🏆 Achievement Unlock")
        print("7. 💼 LinkedIn Long-form Post")
        print("8. 📊 Generate All")
        print("0. ❌ Exit\n")
        
        choice = input("Choice (0-8): ").strip()
        
        if choice == '1':
            posts = self.generate_level_up_post()
            self.display_posts("Level-Up Announcement", posts)
        elif choice == '2':
            posts = self.generate_streak_post()
            self.display_posts("Streak Milestone", posts)
        elif choice == '3':
            cert = input("Certification name: ")
            posts = self.generate_certification_post(cert)
            self.display_posts("Certification Announcement", posts)
        elif choice == '4':
            posts = self.generate_weekly_update()
            self.display_posts("Weekly Update", posts)
        elif choice == '5':
            project = input("Project name: ")
            posts = self.generate_project_post(project)
            self.display_posts("Project Post", posts)
        elif choice == '6':
            ach = input("Achievement name: ")
            posts = self.generate_achievement_post(ach)
            self.display_posts("Achievement Post", posts)
        elif choice == '7':
            post = self.generate_linkedin_post()
            print("\n" + "="*60)
            print("💼 LINKEDIN POST".center(60))
            print("="*60 + "\n")
            print(post)
            print("\n" + "="*60 + "\n")
        elif choice == '8':
            self.generate_all()
        elif choice == '0':
            return
    
    def display_posts(self, title, posts):
        """Display post options"""
        print("\n" + "="*60)
        print(f"{title}".center(60))
        print("="*60 + "\n")
        
        for i, post in enumerate(posts, 1):
            print(f"Option {i}:")
            print("─"*60)
            print(post)
            print("\n")
        
        # Copy option
        choice = input("Copy which option? (1-{}, 0 to skip): ".format(len(posts)))
        if choice.isdigit() and 1 <= int(choice) <= len(posts):
            selected = posts[int(choice) - 1]
            try:
                import pyperclip
                pyperclip.copy(selected)
                print("✅ Copied to clipboard!")
            except ImportError:
                print("\n📋 Copy this text:")
                print("="*60)
                print(selected)
                print("="*60)
    
    def generate_all(self):
        """Generate and save all post types"""
        output = []
        
        output.append("="*60)
        output.append("SOCIAL MEDIA CONTENT - ALL OPTIONS")
        output.append("="*60 + "\n")
        
        # Level up
        output.append("\n🎉 LEVEL-UP POSTS:\n")
        for i, post in enumerate(self.generate_level_up_post(), 1):
            output.append(f"Option {i}:\n{post}\n")
        
        # Streak
        output.append("\n🔥 STREAK POSTS:\n")
        for i, post in enumerate(self.generate_streak_post(), 1):
            output.append(f"Option {i}:\n{post}\n")
        
        # Weekly
        output.append("\n📅 WEEKLY UPDATE POSTS:\n")
        for i, post in enumerate(self.generate_weekly_update(), 1):
            output.append(f"Option {i}:\n{post}\n")
        
        # LinkedIn
        output.append("\n💼 LINKEDIN POST:\n")
        output.append(self.generate_linkedin_post())
        
        content = "\n".join(output)
        
        filename = f"social_posts_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"\n✅ All posts saved to: {filename}")
        print("📋 Open the file to copy any post you want to share!")

def main():
    """Main function"""
    generator = SocialShareGenerator()
    
    if not generator.data:
        print("❌ No XP data found!")
        print("Start tracking with: ./xp log")
        return
    
    generator.display_all_options()

if __name__ == "__main__":
    main()
