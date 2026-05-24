# Intro
As part of the course DLBDSOOFPP01, the task to create a habit tracker is given. In phase 1, the object is to create a technical concept of the program and hand it in.
This document is the technical concept for Phase 1

# Pitch
Imagine working an interesting, challenging job. Every day you give your very best, yet still in the evenings you feel somewhat tired and exausted. You think, it is just the stress, it will go away. 

After some weeks, you figure you are not going to sports anymore, and rarely you take the time to meditate.

You will do it tomorrow.

Another tomorrow, and still, nothing. Feels like you just did it yesterday, but also feels like you never gonna do it again.

Wouldn't it be great, if you could keep track of your habits? Visualizing behaviour can be a first step into recognizing patterns and think of actionable items.

This is where Hábito, your personal habit tracker, is coming to play. Supporting to log your habits, wether they are daily or weekly. But it is not only logging of course, to give you the extra push of motivation, you can also track your streaks. And for the inner monk, you can access all your data via the analytics module to see patterns.

# Technical concept
## Implementation constraints
The course is called 'Object Oriented and Func-
tional Programming with Python' and as such the implementation needs to be based on modern Python. Also the version is specified to be `>=3.7` 

## Acceptance Criteria
- comprehensive documentation
    - installation instruction
    - run instruction
    - test execution instructions
- usage of Python docstrings
- usage of Python class(es) for the implementation
- supporting at least weekly and daily habits
- ship with demo data 
    - containing 5 predefined habits
    - example tracking data for past 4 weeks
- timestamps for habit creation and completion
- data persistence
- analytics module (using functional paradigm)
    - list of all currently tracked habits
    - list of all habits with the same periodicity
    - longest run streak of all defined habits
    - longest run streak for a specific habit
- a user interface that users understand
- unit test suite 

# Design consideration
## User perspective
As a user, I do not really care for the technical implementation. All I want as a user is
- Easy access to my habits anywhere, anytime.
- Easy to use, Touch > Point and click > CLI

## Technical
Following the users desire of an easy to use, always on solution, these decisions need to be made

### User interface
Modern times, modern devices. According to [^1] and [^2], the web is used with mobile, handheld devices. Tablets play only a minor role and the desktop is loosing market share.\
**Conclusion:** The user interface will be mobile first, with support for desktop browser

### Multi device support
According to [^3], almost 2/3 of the users use both laptop and smartphones. The analysis shows, that users expect data to be accessible through both channels.\
**Conclusion**: Support for a device independent backend with persistence is required
 
# Closing note
This document has been created without the use of any AI/ML technologies and all errors are mine.

---

[^1]: Statcounter https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet, accessed May, 24th 2026

[^2]: Similarweb https://www.similarweb.com/platforms/, accessed May, 24th 2026

[^3]: Datareportal https://datareportal.com/reports/digital-2025-sub-section-device-trends?utm_source=chatgpt.com
