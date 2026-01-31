# Flywheel Demo: Hub Finder + Backlinks
# Shows graph intelligence features in action

Output demos/flywheel-demo.gif

Set FontSize 14
Set Width 1200
Set Height 600
Set Theme "Catppuccin Mocha"
Set TypingSpeed 50ms
Set PlaybackSpeed 1.5

Type "claude 'What are my most connected notes?'" Sleep 500ms Enter

Sleep 1s

Type@100ms "Finding hub notes in your vault..."
Sleep 500ms
Enter
Sleep 300ms

Type@100ms "📊 Top Hub Notes (by connections):"
Sleep 200ms
Enter
Sleep 200ms

Type@100ms "┌─────────────────────────────┬─────────┐"
Enter
Type@100ms "│ Note                        │ Links   │"
Enter
Type@100ms "├─────────────────────────────┼─────────┤"
Enter
Type@100ms "│ 🌟 Project Overview          │ 47      │"
Enter
Type@100ms "│ 📝 Meeting Notes             │ 32      │"
Enter
Type@100ms "│ 💡 Ideas & Brainstorming     │ 28      │"
Enter
Type@100ms "│ 🔧 Technical Architecture    │ 24      │"
Enter
Type@100ms "└─────────────────────────────┴─────────┘"
Enter

Sleep 1.5s

Type "claude 'What links to Meeting Notes?'" Sleep 500ms Enter

Sleep 1s

Type@100ms "Analyzing backlinks..."
Sleep 500ms
Enter
Sleep 300ms

Type@100ms "📎 Backlinks to 'Meeting Notes':"
Sleep 200ms
Enter
Sleep 200ms

Type@100ms "├─ 2024-01-30 Daily Note"
Enter
Type@100ms "│  └─ Planning discussion"
Enter
Type@100ms "├─ Project Roadmap"
Enter
Type@100ms "│  └─ Sprint planning reference"
Enter
Type@100ms "├─ Team Decisions"
Enter
Type@100ms "│  └─ Action items follow-up"
Enter
Type@100ms "└─ Quarterly Review"
Enter
Type@100ms "   └─ Meeting summary link"
Enter

Sleep 1.5s

Type "claude 'Open that note'" Sleep 500ms Enter

Sleep 800ms

Type@100ms "Opening Meeting Notes..."
Sleep 400ms
Enter
Sleep 200ms

Type@100ms "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Enter
Type@100ms "# 📝 Meeting Notes"
Enter
Type@100ms ""
Enter
Type@100ms "## Recent Meetings"
Enter
Type@100ms "- [[2024-01-30 Team Sync]]"
Enter
Type@100ms "- [[2024-01-29 Client Call]]"
Enter
Type@100ms "- [[2024-01-25 Sprint Planning]]"
Enter
Type@100ms ""
Enter
Type@100ms "## Key Decisions"
Enter
Type@100ms "- Approved new feature roadmap"
Enter
Type@100ms "- Team velocity: 45 points/sprint"
Enter
Type@100ms "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Enter

Sleep 2s
