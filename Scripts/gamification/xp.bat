@echo off
REM DevOps XP Tracker - Windows Batch Wrapper
REM Quick access to all gamification tools

setlocal
cd /d "%~dp0"

if "%1"=="" goto :help
if "%1"=="help" goto :help
if "%1"=="h" goto :help
if "%1"=="-h" goto :help
if "%1"=="--help" goto :help

if "%1"=="log" goto :log
if "%1"=="l" goto :log

if "%1"=="track" goto :track
if "%1"=="t" goto :track

if "%1"=="status" goto :status
if "%1"=="s" goto :status

if "%1"=="quick" goto :quick
if "%1"=="q" goto :quick

if "%1"=="update" goto :update
if "%1"=="u" goto :update

if "%1"=="commit" goto :commit
if "%1"=="c" goto :commit

if "%1"=="dashboard" goto :dashboard
if "%1"=="dash" goto :dashboard
if "%1"=="d" goto :dashboard

if "%1"=="report" goto :report
if "%1"=="weekly" goto :report
if "%1"=="w" goto :report

if "%1"=="stats" goto :stats
if "%1"=="analytics" goto :stats

if "%1"=="share" goto :share
if "%1"=="social" goto :share

if "%1"=="achievements" goto :achievements
if "%1"=="a" goto :achievements

if "%1"=="history" goto :history
if "%1"=="hist" goto :history

goto :unknown

:help
echo.
echo 🎮 DevOps XP Tracker - Command Reference
echo ========================================
echo.
echo Usage: xp [command]
echo.
echo Commands:
echo   log, l         Quick daily log (easiest way!)
echo   track, t       Full XP tracker menu
echo   status, s      Show current status
echo   quick, q       Quick study session log
echo   update, u      Update markdown files
echo   commit, c      Git commit with XP stats
echo   dashboard, d   Generate HTML dashboard
echo   report, w      Generate weekly report
echo   stats          Comprehensive statistics
echo   share          Social media posts
echo   achievements   Show all achievements
echo   history        Show recent activity
echo   help, h        Show this help
echo.
echo Examples:
echo   xp log         # Quick log today's activity
echo   xp status      # Show your current stats
echo   xp dashboard   # Generate visual dashboard
echo   xp report      # Get weekly report
echo.
goto :eof

:log
echo 📝 Quick Daily Log
python quick_log.py
goto :eof

:track
echo 🎮 Full XP Tracker
python xp_tracker_v2.py
goto :eof

:status
echo 📊 Current Status
chcp 65001 >nul 2>&1
python -c "import sys; sys.path.insert(0, '.'); from xp_tracker_v2 import DevOpsXPSystem; tracker = DevOpsXPSystem(); level, name, icon, _ = tracker.get_current_level(); next_level, next_threshold, _, _ = tracker.get_next_level(); print('\n' + '='*50); print(f'Level {level}: {icon} {name}'.center(50)); print('='*50); print(f'\nXP: {tracker.data[\"total_xp\"]} / {next_threshold}'); print(f'Progress: {tracker.calculate_progress_percentage():.0f}%%'); print(f'Streak: {tracker.data[\"current_streak\"]} days'); print(f'Hours: {tracker.data[\"total_hours\"]:.1f} / 384'); print(f'Achievements: {len(tracker.data[\"achievements_unlocked\"])} / {len(tracker.ACHIEVEMENTS)}'); print(f'Weeks: {tracker.data[\"weeks_completed\"]} / 48'); print(f'Certifications: {tracker.data[\"certifications\"]} / 4'); print(f'Projects: {tracker.data[\"projects_completed\"]} / 12'); print('\n' + '='*50 + '\n')"
goto :eof

:quick
echo ⚡ Quick Study Log
python -c "import sys; sys.path.insert(0, '.'); from xp_tracker_v2 import DevOpsXPSystem; tracker = DevOpsXPSystem(); tracker.add_xp('study_session', duration_hours=1.5); tracker.update_streak(); tracker.display_status()"
goto :eof

:update
echo 🔄 Updating Files
echo NOTE: Manual update required on Windows due to encoding issues.
echo Please manually update README.md and XP_TRACKER.md with your current stats.
echo Your current XP:
python -c "import sys; sys.path.insert(0, '.'); from xp_tracker_v2 import DevOpsXPSystem; tracker = DevOpsXPSystem(); print(f'XP: {tracker.data[\"total_xp\"]}, Streak: {tracker.data[\"current_streak\"]}, Hours: {tracker.data[\"total_hours\"]:.1f}')"
goto :eof

:commit
echo 🔗 Git Commit
python git_integration.py
goto :eof

:dashboard
echo 📊 Generate Dashboard
python dashboard_generator.py
goto :eof

:report
echo 📈 Weekly Report
python weekly_report.py
goto :eof

:stats
echo 📊 Statistics Analysis
python stats_analyzer.py
goto :eof

:share
echo 📱 Social Media Share
python social_share.py
goto :eof

:achievements
echo 🏆 Achievements
python -c "import sys; sys.path.insert(0, '.'); from xp_tracker_v2 import DevOpsXPSystem; tracker = DevOpsXPSystem(); tracker.show_achievements()"
goto :eof

:history
echo 📜 Recent Activity
python -c "import sys; sys.path.insert(0, '.'); from xp_tracker_v2 import DevOpsXPSystem; tracker = DevOpsXPSystem(); tracker.show_recent_activity(20)"
goto :eof

:unknown
echo ❌ Unknown command: %1
echo.
echo Run 'xp help' for a list of available commands
goto :eof

:eof
endlocal
