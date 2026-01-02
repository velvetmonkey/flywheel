---
type: daily
date: (% tp.date.now("YYYY-MM-DD") %)
tags:
  - "#daily"
---
# [[Habits]]
- [ ] [[Walk]] #[[Habit]]
- [ ] [[Stretch]] #habit
- [ ] [[Vitamins]] #habit
---
# Today
## Tasks
```dataviewjs
const tasks = dv.pages().file.tasks
  .where(task => !task.tags?.includes("#habit") && !task.completed && task.due <= dv.date("today"))
  .sort(task => task.due, 'asc');

if (tasks.length === 0) {
  dv.paragraph("- No tasks");
} else {
  dv.taskList(tasks, false);
}
```
## [[Log]]

- (% tp.file.cursor() %)
