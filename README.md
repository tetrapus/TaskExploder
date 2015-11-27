# TaskExploder
[![Build Status](https://travis-ci.org/tetrapus/TaskExploder.svg?branch=master)](https://travis-ci.org/tetrapus/TaskExploder)

A nested agile-inspired todo list with story points.

## UI controls

Tasks:

    Up/down to navigate
        -> Shift+up/down reorders
    Left/right sets/resets progress (task)
        -> Shift+left/right edits total points
    Enter explodes a task or stops amend
        -> Shift+enter explode instead? or unexplode
    Backspace goes up
        -> Bad idea if input focused?
    Delete marks done (task)
        -> Shift+delete deletes task
    Delete deletes element (done task)
        -> Shift+delete marks undone
    Enter undos delete (undo)
        -> Delete confirms delete
        -> Shift+delete marks undone          
    Start typing to amend, or tab to set field

Hold shift to re-order.


TODO:
- [x] Story points
- [ ] Animations
- [ ] Deleting tasks
- [ ] Task undo and retry pseudotasks
- [ ] Toasts
- [ ] Filters and sort
- [ ] Re-ordering
- [ ] Main tasks & Subtasks
- [ ] Explode event
- [ ] Colours
- [ ] Markdown'd descriptions
- [ ] Making sure tasks stay visible
- [ ] URLs
- [ ] Mobile users
- [ ] Offline mode
- [ ] Rebase

Feature checklist:
- Syncstate updated
- Toasts created
- Rollback created
- Element animated
- Responsive
x Local updates updated

Others:
- Recurring Tasks
- Inline task groups
- Your plate
- Burndown
- Task sharing
