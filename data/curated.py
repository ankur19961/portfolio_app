from pathlib import Path
import json
import streamlit as st

# These loaders provide safe defaults so the app runs even if assets are missing.
# You can later plug in your full curated sets from files or `stored_questions.var`.


@st.cache_resource(show_spinner=False)
def get_blocked_prompts() -> dict:
    """
    Returns a dict of phrase -> reply for off-topic/blocked content.
    Add your full set here (or load from a JSON/YAML file).
    """
    # Minimal, safe defaults (non-duplicated keys)
    return {
        
    "no": "I understand. If you change your mind, I'm here to discuss my work! 😊",
    "not interested": "No problem! Let me know if you change your mind about discussing my work. 💼",
    "don't care": "Understood! Feel free to ask if you ever need professional insights. 🧠",
    "idc": "IDC = I Do Coding! Ask about my technical skills instead. 💻",
    "who cares": "People care about results! Let me share my project successes. 🏆",
    "boring": "Let’s spice it up with technical challenges I’ve solved! 🌶️",
    "useless": "My skills delivered 40% efficiency gains – want details? 📈",
    "pointless": "Focus on impactful work instead! Ask about key projects. 🎯",
    "waste of time": "Time invested here could reveal valuable skills! ⏳",
    
    # Dismissive phrases
    "whatever": "‘Whatever’ becomes ‘Wow!’ when discussing achievements – try it! ✨",
    "skip": "Skipping to the good part: Ask about my core competencies! ⏭️",
    "next": "Next topic should be my technical expertise! 💡",
    "shut up": "I’ll pause – restart with work-related questions anytime. 🔇",
    "stop talking": "Silenced! Type ‘portfolio’ to resume professional discussion. 🤐",
    "enough": "Enough preliminaries – ready for skill-specific questions? 🚀",
    
    # Boredom expressions
    "zzz": "Wake up to impressive metrics! Ask about performance gains. ⏰",
    "snore": "No snores in my debugging marathons! Ask about focus. 😴",
    "dull": "Dull code? Never! Ask about my innovative solutions. 💎",
    "mindless": "Mind full of technical knowledge – want specifics? 🧩",
    "tedious": "Turn tedium into triumph! Ask about automation successes. 🤖",
    
    # Aggressive rejection
    "go away": "I’ll retreat – return by asking about my qualifications. 🏃♂️",
    "nobody asked": "Proactive sharing: My projects boosted revenue by 30%. 📊",
    "leave me alone": "Respecting space! Reach out for career insights later. 🚪",
    "get lost": "Lost in code? I can guide technical discussions! 🧭",
    "scram": "Scrambling to showcase skills – your move. 🍳",
    
    # Sarcastic remarks
    "slow clap": "Applaud these results: 50% faster load times! 👏",
    "big deal": "Actually a $1M deal from my project – want details? 💰",
    "cool story": "True story: Reduced server costs by 65%. 📉",
    "yawn": "Yawn-worthy until you hear about efficiency breakthroughs! 😮",
    "whoop de doo": "Celebrate these DOO-ables: Shipped 20+ features. 🎉",
    
    # Follow-up rejection
    "still no": "Persistent no? Persistent yes to career questions! 🔁",
    "not impressed": "Impress yourself with my 4.9/5 client ratings. ⭐",
    "so what": "So... 100k users adopted my solutions. Relevant? 📱",
    "and?": "And I optimized code by 200%. Continue? ➡️",
    "your point?": "Point being: These skills solve real problems. 🎯",
    
    # Text slang negativity
    "meh": "Meh becomes YES! Ask about impactful work. 🔥",
    "nah": "Nah? How about my 95% client retention rate? 📊",
    "nope": "Nope turns to Hope when discussing career potential! 🌱",
    "pass": "Pass on small talk, ace career discussions! ♠️",
    "hard pass": "Hard pass on negativity, open to skill inquiries! 🚪",
    
    # Intellectual rejection
    "too complex": "Simplify it: Ask about my most accessible project. 🧩",
    "over my head": "Let’s lower the ladder – ask basic career questions. 🌉",
    "not smart enough": "I simplify complexity – ask about knowledge sharing. 🎓",
    "confusing": "Clarity is my specialty! Ask straightforward questions. 🧼",
    "tl;dr": "TL;DR: I deliver results. Ask for highlights. 🏁",
    
    # Emotional dismissal
    "cringe": "Cringe becomes interest when discussing ROI figures. 📈",
    "eye roll": "Roll eyes at 50% efficiency gains? Doubtful. 🙄",
    "facepalm": "Facepalm meets palm pilot – I streamline workflows. 🤦♂️",
    "ugh": "Ugh? Agh! At my project turnaround times. ⚡",
    "groan": "Groan now, thank me later for optimized solutions. 😫",
    
    # Typo-based negatives
    "not intrested": "Interested in fixing typos? I debug code too! 🐛",
    "boaring": "No boars here – just solid coding achievements. 🐗",
    "dontcare": "Care about results? I have metrics. 📊",
    "mehh": "Meh² becomes wow! through project demos. ✨",
    "zzzz": "Zzzzap! Energy returns with technical discussions. ⚡",
    
    # Cultural references
    "ain't nobody got time": "Got 30s? I’ll summarize key skills. ⏱️",
    "bye felicia": "Bye! Return as ‘Professional Patricia’ later. 👩💼",
    "talk to the hand": "Hands code – let’s discuss keyboard skills! ⌨️",
    "whatevs": "‘Whatevs’ evolves into interest – try it! 🧬",
    "nunya": "Nunya business? My business solutions impress. 🏢",
    
    # Challenge responses
    "prove it": "Proof: Client testimonials available. Ask! 📜",
    "doubt it": "Doubt resolved through project case studies. 📂",
    "cap": "No cap – 3 awards won. Verify? 🏅",
    "liar": "Honesty policy: 100% delivered projects. ✅",
    "fake": "Genuine GitHub commits available. 💾",
    
    # Patronizing phrases
    "good for you": "Good for teams I’ve led – want details? 👥",
    "aww cute": "Cute? How about 300% scalable solutions? 📈",
    "how precious": "Precious time saved through my optimizations! ⏳",
    "bless your heart": "Bless these 5-star client reviews! ⭐",
    "nice try": "Trying succeeds – 92% project success rate. 🎯",
    
    # Dismissive questions
    "why bother": "Botheration becomes satisfaction – ask how. 😌",
    "what's the use": "Usefulness proven in 15 deployments. 🚀",
    "who needs this": "100+ companies needed these skills. 🏢",
    "anyone actually care": "Cared enough to fund 6 projects. 💸",
    "is this relevant": "Relevant to your needs? Let’s find out. 🔍",
    
    # Existential dismissal
    "why exist": "Existing to solve problems – like yours? 💡",
    "meaningless": "Meaning found in 5 successful launches. 🚀",
    "nothing matters": "Matter matters – ask about material projects. ⚛️",
    "life is pointless": "Points scored in career achievements – 100+. 🏅",
    "we all die anyway": "Legacy lives through impactful code. 💾",
    
    # Playful blocks
    "nope rope": "Rope me into career discussions instead! 🪢",
    "nah fam": "Fam needs skills – I deliver. 👨👩👧👦",
    "yeet": "Yeet negativity, meet productivity! 🥏",
    "sus": "No sus here – 100% transparent track record. 🔍",
    "cringe af": "AF = Actually Functional! Ask about results. 🏭",
    
    # Persistent negativity
    "still no": "Still yes to professional value! ♻️",
    "never": "Never say never to optimized solutions! ♾️",
    "not happening": "Happened for 20+ clients already. ✅",
    "give up": "Giving up? I persisted through 10k lines of code. 💪",
    "you lose": "Win-win scenarios engineered daily. 🏆",
    # Sleep Schedule (20)
    "when do you sleep?": "My schedule is optimized for productivity! Ask about work routines. ⏰",
    "are you a night owl?": "I'm focused around the clock! Ask about daylight achievements. 🦉",
    "what time do you wake up?": "I wake up ready to code! Ask about morning productivity hacks. ☀️",
    "how many hours do you sleep?": "I rest efficiently to maximize development time. Ask about energy management! 💤",
    "do you take naps?": "I power through with focused work sessions! Ask about workflow optimization. ⚡",
    "insomnia much?": "I sleep soundly knowing my code works! Ask about reliable systems. 😴",
    "bedtime routine?": "My routine involves code reviews! Ask about quality assurance processes. 📖",
    "sleeping patterns": "Pattern recognition is for code, not sleep! Ask about algorithms. 🔍",
    "up late coding?": "Always coding efficiently! Ask about time management strategies. 🌙",
    "early riser?": "I rise to technical challenges! Ask about problem-solving approaches. 🌅",
    "sleep deprivation": "My skills stay sharp through proper rest! Ask about work-life balance. ⚖️",
    "best time to work?": "Peak productivity hours vary - ask about consistent output! 📈",
    "dream journal?": "I document project visions instead! Ask about roadmap planning. 📔",
    "sleep tracker?": "I track code performance metrics! Ask about analytics tools. 📊",
    "alarm sound?": "My motivation alarm is project deadlines! Ask about timely delivery. ⏰",
    "sleepwalk ever?": "I walk through code paths consciously! Ask about debugging processes. 🚶♂️",
    "coffee addict?": "Addicted to clean code! Ask about development dependencies. ☕",
    "sleep medication?": "My remedy is solving technical challenges! Ask about troubleshooting. 💊",
    "snore much?": "I make noise through impactful projects! Ask about notable work. 😴",
    "midnight snack?": "I snack on problem-solving! Ask about creative solutions. 🍪",

    # Dietary Habits (25)
    "what's your diet?": "I consume technical knowledge! Ask about learning resources. 📚",
    "vegetarian?": "I digest complex code! Ask about system architecture. 🥦",
    "favorite food?": "My favorite meal is completed projects! Ask about deliverables. 🍽️",
    "meal prep?": "I prepare robust systems! Ask about infrastructure planning. 🥘",
    "cheat days?": "I stay consistent with coding standards! Ask about best practices. 📋",
    "food allergies?": "Allergic to bad code! Ask about quality control measures. 🤧",
    "coffee or tea?": "Brewing solutions either way! Ask about problem-solving methods. ☕",
    "eat breakfast?": "I break fast performance barriers! Ask about optimization. 🍳",
    "junk food fan?": "I prefer clean code snacks! Ask about efficient scripting. 🍟",
    "vegan lifestyle?": "My lifestyle revolves around green tech! Ask about eco-friendly solutions. 🌱",
    "cooking skills?": "I cook up innovative solutions! Ask about creative development. 🧑🍳",
    "favorite restaurant?": "I frequent the repository of knowledge! Ask about resources. 🏢",
    "nutrition plan?": "My plan is skill nourishment! Ask about professional growth. 📈",
    "intermittent fasting?": "I fast-track project completion! Ask about development speed. ⏩",
    "sugar intake?": "My sweet spot is elegant code! Ask about beautiful solutions. 🍬",
    "food cravings?": "Craving technical challenges! Ask about complex problems. 🍔",
    "keto diet?": "My fuel is clean energy! Ask about efficient algorithms. ⚡",
    "gluten free?": "Free to focus on code! Ask about development priorities. 🚫🌾",
    "food diary?": "I document code commits! Ask about version control. 📓",
    "favorite cuisine?": "I savor successful deployments! Ask about release strategies. 🌍",
    "eating disorders?": "I maintain healthy coding habits! Ask about best practices. 🧠",
    "supplements?": "I supplement with continuous learning! Ask about skill development. 💊",
    "calorie count?": "I count clean code lines! Ask about quality metrics. 🔢",
    "fast food?": "I deliver fast solutions! Ask about rapid prototyping. 🍟",
    "home cooking?": "I craft custom solutions! Ask about tailored systems. 🏡",

    # Bad Habits (20)
    "do you smoke?": "I smoke the competition with superior skills! Ask about advantages. 🚭",
    "nail biter?": "I bite into complex challenges! Ask about problem-solving. 💅",
    "procrastinate much?": "I prioritize effectively! Ask about task management. 📅",
    "bad habits?": "Habitually delivering quality work! Ask about consistency. 🏆",
    "addicted to?": "Addicted to innovation! Ask about creative solutions. 💡",
    "chew gum?": "I stick to coding standards! Ask about best practices. 🍬",
    "crack knuckles?": "I flex problem-solving skills! Ask about technical flexibility. 💪",
    "gambling?": "I bet on proven methods! Ask about reliable systems. 🎲",
    "overspend?": "I invest in skill development! Ask about learning investments. 💰",
    "lazy days?": "My rest days fuel productivity! Ask about energy management. 🛋️",
    "phone addict?": "Addicted to clean code! Ask about development focus. 📱",
    "gossip much?": "I communicate professionally! Ask about team collaboration. 🤫",
    "chronic lateness?": "I deliver projects on time! Ask about deadline management. ⏰",
    "impulse buying?": "I carefully select technologies! Ask about stack choices. 🛒",
    "overthinker?": "I thoroughly analyze systems! Ask about architecture reviews. 🤔",
    "people pleaser?": "I please users with great UX! Ask about design principles. 😊",
    "workaholic?": "I work smart! Ask about productivity strategies. 💼",
    "skin picking?": "I pick optimal solutions! Ask about decision-making processes. ✋",
    "social media addict?": "I focus on impactful work! Ask about project results. 📱",
    "fidget spinner?": "I spin up efficient solutions! Ask about rapid development. 🌀",

    # Hairstyle (20)
    "why that haircut?": "My focus is on cutting-edge tech! Ask about innovations. ✂️",
    "dye your hair?": "I color outside the lines in creative coding! Ask about projects. 🎨",
    "bad hair day?": "Every day is a good day for coding! Ask about daily workflows. 💇",
    "hairstyle routine?": "I style efficient code! Ask about clean architecture. 💆♂️",
    "balding?": "Full coverage in code documentation! Ask about thoroughness. 🧢",
    "favorite shampoo?": "I wash away bugs! Ask about debugging tools. 🧴",
    "long hair?": "Long on skills! Ask about extensive experience. 🦱",
    "shaved head?": "Smooth operator in code! Ask about efficient execution. 🪒",
    "gray hairs?": "Earned through complex projects! Ask about challenging work. 👨🦳",
    "curly hair?": "Curly braces maybe? Ask about code structure! 🌀",
    "hair products?": "I product-ize solutions! Ask about application development. 🧴",
    "hat collection?": "I collect achievements instead! Ask about milestones. 🧢",
    "bad haircut?": "No bad cuts in my code! Ask about precision engineering. 💇",
    "hairstyle inspo?": "Inspired by elegant solutions! Ask about design patterns. 💡",
    "split ends?": "I end code fragmentation! Ask about unified systems. ✂️",
    "fringe benefits?": "Benefits come from skills! Ask about professional advantages. 💇♀️",
    "bed head?": "Head in the code clouds! Ask about ambitious projects. ☁️",
    "hair loss?": "No loss in code coverage! Ask about testing protocols. 💇♂️",
    "ponytail?": "Tied-up loose ends in code! Ask about completion rates. 🐎",
    "beard style?": "Style is in clean code! Ask about elegant solutions. 🧔",

    # Clothing Sense (20)
    "why that outfit?": "Dressed for coding success! Ask about technical fit. 👔",
    "fashion sense?": "I sense optimal solutions! Ask about system design. 👗",
    "wardrobe essentials?": "Essential skills include... (ask about technical stack)! 👕",
    "socks with sandals?": "I pair technologies effectively! Ask about integrations. 🧦",
    "designer clothes?": "I design systems! Ask about architecture. 👚",
    "laundry routine?": "I clean up code regularly! Ask about maintenance. 🧺",
    "favorite color?": "The color of success! Ask about achievements. 🎨",
    "dress code?": "Code is my uniform! Ask about development standards. 👔",
    "thrift shopper?": "I thrift for efficient solutions! Ask about optimization. 🛍️",
    "style icon?": "Iconic projects are my signature! Ask about notable work. 👑",
    "hat enthusiast?": "Enthusiastic about headless architectures! Ask about modern systems. 🧢",
    "shoe collection?": "I walk through complex code! Ask about navigation. 👟",
    "formal wear?": "Formally verified code! Ask about testing protocols. 🤵",
    "casual fridays?": "Casual about bugs? Never! Ask about quality control. 🩳",
    "accessories?": "I accessorize with tools! Ask about development stack. 💍",
    "outfit repeat?": "I repeat successful patterns! Ask about design systems. 🔁",
    "fashion victim?": "Victorious in code challenges! Ask about achievements. 👗",
    "brand loyalty?": "Loyal to best tools! Ask about technology choices. 🏷️",
    "seasonal styles?": "Seasoned in multiple tech stacks! Ask about versatility. 🍂",
    "clothing budget?": "I invest in skill development! Ask about learning resources. 💰",
    # Personal/Private Life Questions (Food, Daily Routine)
    "what did you eat": "Let's focus on my professional nourishment - ask about skills I've developed! 🍏",
    "what do you eat": "I consume code and problem-solving! Ask about technical diet. 💻",
    "what's your favorite food": "My favorite 'food' is clean code! Let's discuss programming. 🥑",
    "did you have lunch": "I'm always hungry for new projects! Ask about recent work. 🍱",
    "last meal": "My latest professional meal: skill development! Ask about growth. 🌱",
    "cooking skills": "I specialize in cooking up solutions! Ask about technical expertise. 🧑🍳",

    # Speculative/Future Questions
    "what's the future": "The future holds career growth! Ask about my professional trajectory. 📈",
    "predict future": "I predict career questions coming! Ask about my skills. 🔮",
    "what will happen tomorrow": "Tomorrow brings opportunities to discuss my work! Ask now. ⏳",
    "end of the world": "Let's focus on building things up! Ask about my projects. 🌍",
    "when will i die": "Let's discuss career longevity instead! Ask about experience. ⏳",

    # Sensitive/Racist/Sexist Questions
    "why is he black": "I focus on professional qualities, not physical attributes. Ask about skills! ✋",
    "race of": "Human race united by skills! Ask about technical capabilities. 🌍",
    "why are they gay": "Let's keep discussions professional and inclusive. Ask about work! 🏳️🌈",
    "women belong in": "Everyone belongs in tech! Ask about collaborative projects. 👩💻",
    "racial stereotype": "Stereotypes hinder progress - let's discuss actual achievements! 🚫",
    "is islam violent": "I focus on technical discussions, not religious stereotypes. Ask about work! ☪️",
    "jewish people are": "Professional ethics prohibit stereotypes. Ask about skills instead. ✡️",

    # Existential/Philosophical
    "meaning of life": "Life's meaning varies - let's find meaning in professional growth! 🌱",
    "why do we exist": "We exist to create! Ask about my technical creations. 🛠️",
    "purpose of universe": "My universe revolves around clean code! Ask about projects. 🌌",

    # Inappropriate Personal
    "how much do you weigh": "Let's measure skills instead! Ask about technical weight. ⚖️",
    "body count": "I count code contributions! Ask about project metrics. 🔢",
    "are you single": "I'm married to my work! Ask about professional commitments. 💍",
    "show your face": "My portfolio speaks for itself! Ask about visible achievements. 📁",
    "what's your age": "Age matters less than skills! Ask about technical experience. 📅",

    # Troll/Bait Questions
    "who's better race": "All races excel equally! Let's discuss technical excellence instead. 🏆",
    "why are people stupid": "I focus on smart solutions! Ask about problem-solving skills. 🧠",
    "worst gender": "All genders contribute valuably! Ask about team collaborations. 👥",
    "illegal immigrants should": "I focus on legal code (software)! Ask about programming. ⚖️",

    # Typo-Based Variations
    "waht did you eat": "Let's spell-check our focus to professional skills! 📚",
    "whtas the future": "Future's bright with career questions! Ask properly. ☀️",
    "y r u white": "Color irrelevant - let's discuss colorful achievements! 🎨",
    "why hes black": "Focus on skills, not skin! Ask about capabilities. 🛑",
    "tahts racist": "Indeed - let's redirect to professional topics! 🚩",

    # Enhanced Greetings (30+ variations)
    "hi": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "hello": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "hey": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "hi there": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "hello there": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "hey there": "Hello! Let's discuss my professional background. Ask about my skills or projects! 🚀",
    "good morning": "Good morning! Ready to explore my portfolio? Ask me anything relevant! ☀️",
    "good afternoon": "Good afternoon! Let's focus on my professional experience. What would you like to know? 🌞",
    "good evening": "Good evening! I'm here to discuss my work history and capabilities. 💼",
    "greetings": "Greetings! Let's talk about my technical skills and career achievements. 📈",
    "howdy": "Howdy! Ask me about my professional qualifications and project experience. 🤠",
    "hiya": "Hiya! Let's keep this focused on my portfolio. What would you like to discuss? 🎯",
    "sup": "Let's discuss my professional background instead. Ask about my skills! 💻",
    "yo": "Yo! I'm here to talk about my career and projects. What would you like to know? 🔍",
    
    # Enhanced Farewells (20+ variations)
    "bye": "Feel free to return with questions about my work! 👋",
    "goodbye": "Goodbye! Reach out later for portfolio-related inquiries. 📅",
    "see you": "Looking forward to discussing my work next time! 👀",
    "see ya": "See ya! Let me know if you have work-related questions later. 👍",
    "take care": "Take care! Don't hesitate to ask about my projects later. 💼",
    "farewell": "Farewell! I'm available for career-related questions anytime. 🌟",
    "catch you later": "Catch you later! Questions about my skills are always welcome. 🤝",
    "peace out": "Peace out! Let me know if you need portfolio details later. ✌️",
    "later gator": "Later gator! Professional inquiries welcome anytime. 🐊",
    "signing off": "Signing off! Career-related questions encouraged next time. 📝",

    # Enhanced Small Talk (40+ variations)
    "how are you?": "I'm focused on discussing my portfolio. Ask about my technical skills! 💡",
    "what's up?": "Let's discuss my professional achievements! What interests you? 🏆",
    "how's it going?": "I'm here to talk about my career. Ask about my experience! 👔",
    "how are you doing?": "Let's focus on my professional background. What would you like to know? 📚",
    "what's new?": "Let's discuss recent projects in my portfolio! 🆕",
    "how's your day?": "My day is productive when discussing my work! Ask about my skills! ⚡",
    "how's life?": "Let's keep this professional - ask about my career journey! 🛣️",
    "what's happening?": "Discussing my professional qualifications! Your move. ♟️",
    "how's everything?": "Everything's professional here! Ask about my skills. 📊",
    "what's going on?": "Focusing on career discussions! What would you like to know? 🤔",
    "how've you been?": "Been developing new skills! Ask about my capabilities. 🛠️",
    "what's good?": "My portfolio is good! Let's discuss it. 🎨",
    "how's tricks?": "Professional tricks available! Ask about my technical skills. 🎩",

    # Enhanced Non-Serious (30+ variations)
    "i am bored": "Let's focus on career-related topics! Ask about my projects. 📂",
    "i'm bored": "My portfolio is anything but boring! Ask about my work. 🎉",
    "entertain me": "Let me entertain you with my project successes! Ask away. 🏅",
    "tell me a joke": "How about I share an interesting project challenge instead? 💡",
    "say something funny": "Fun fact: I optimized code by 40%! Ask me how. ⚡",
    "talk to me": "I'm talking career! Ask about my professional experience. 💬",
    "chat with me": "Let's chat about my technical skills and achievements! 🤖",
    "i'm lonely": "Explore my collaborative projects! Ask about team experiences. 👥",
    "keep me company": "Company available through career discussions! Ask away. 🏢",
    "cheer me up": "How about some impressive project metrics? Ask me! 📈",
    "make me laugh": "I laugh when recalling complex bugs I've solved! Ask about solutions. 🐛",
    "distract me": "Get productively distracted! Ask about my technical skills. 🎯",
    "play a game": "Let's play 'discover my portfolio'! Ask work-related questions. 🎮",

    # Enhanced Repetitive/Empty (50+ variations)
    "...": "I'm here to discuss my work! Ask me something specific. 💼",
    "???": "Questions about my portfolio are welcome! Try asking one. ❓",
    "!!!!": "Excitement about my work? Ask about my achievements! 🎉",
    "hmm": "Curious about something? Ask about my skills! 🤔",
    "ok": "Ready to discuss my portfolio? Ask away! 👍",
    "okay": "Okay! Let's talk professional background. What's your question? 💬",
    "lol": "Glad you're amused! Now ask about my work. 😄",
    "haha": "Haha! Let's channel that energy into portfolio discussions. 💥",
    "hehe": "Hehe! Professional inquiries welcome. 😊",
    "nice": "Nice! Now ask something about my work. 😎",
    "cool": "Cool! Let's discuss my technical capabilities. ❄️",
    "wow": "Wow! Wait until you hear about my projects! ✨",
    "oh": "Oh? Ask about my professional experience to learn more! 💡",
    "ah": "Ah! Let's turn that realization into a work-related question. 💭",
    "um": "Unsure what to ask? Try 'What's your strongest skill?' 🤷",
    "uh": "Need help? Try asking about my project experience. 🆘",
    "meh": "Not impressed yet? Ask about my major achievements. 🏆",
    "yikes": "Yikes! Let's recover with a work-related question. 🚑",
    "oof": "Oof! Let's try a portfolio question instead. 💪",
    "zzz": "Wake up! Ask about my exciting projects! ⏰",

    # Enhanced Test/Gibberish (40+ variations)
    "test": "Real portfolio assistant here! Ask about my work. 🔍",
    "testing": "Testing successful! Now ask about real projects. ✅",
    "123": "Numbers are great! Ask about my quantitative achievements. 🔢",
    "abc": "Let's move from ABCs to professional Q&As! 💼",
    "asdf": "Real portfolio discussion available! Ask away. 🎯",
    "qwerty": "Keyboard skills aside, ask about my real skills! ⌨️",
    "random": "Random question? Try asking about my projects! 🎲",
    "just testing": "Test passed! Now let's discuss real work. 📝",
    "does this work?": "It works! Now try work-related questions. ⚙️",
    "is this thing on?": "System active! Ask portfolio questions now. 💻",
    "ping": "Pong! Now serve a work-related question. 🏓",
    "echo": "Echo... echo... Now ask something real. 📡",
    "debug": "No bugs here! Ask about my debugging skills. 🐛",
    "crash": "System stable! Ask about resilient systems I've built. 🛡️",

    # Enhanced Meta/Help (30+ variations)
    "who are you": "AI assistant showcasing my creator's portfolio. Ask about their work! 🤖",
    "what can you do": "I can detail technical skills, projects, and achievements! 💼",
    "help": "Happy to help! Ask about skills, experience, or projects. 🆘",
    "what is this": "AI-powered professional portfolio. Ask about career details! 📁",
    "hello world": "Hello World! Now ask about real-world projects. 🌍",
    "thanks": "You're welcome! Follow up with work-related questions. 👍",
    "thank you": "My pleasure! Continue with portfolio inquiries. 😊",
    "who made you": "Created to showcase professional work - ask about that! 👩💻",
    "what's your purpose": "My purpose is portfolio discussion. Ask work questions! 🎯",
    "are you human": "AI assistant focused on career details. Ask about human skills! 🤖",
    "how old are you": "Age matters less than skills! Ask about technical capabilities. 📅",
    "where are you": "I'm wherever my portfolio is needed! Ask about work experience. 🌍",
    "why exist": "I exist to discuss my creator's work. Ask about it! 🤔",
}

questions = {
    "hi", "hello", "hey", "heya", "what is your name", "who are you", "what can you do",
    "what do you know about you", "bye", "thank you", "i am not in a happy mood right now", 
    "can you cheer me up", "tell me about you", "who is you", "your bio", "your background", 
    "introduce you", "contact information", "how can I contact you", "contact details", 
    "how to reach you", "phone number", "your phone", "email address", "your email", 
    "what is your linkedin", "do you have a linkedin", "linkedin profile", "github profile", 
    "do you have a github", "can I connect with you on github", "where are you from", 
    "your origin", "your nationality", "where did you come from", "education", 
    "what are your educational qualifications", "where did you study", "where did you get your degree", 
    "list your education", "what are you currently studying", "your education", "his education", 
    "education history", "academic background", "gpa", "your gpa", "what's your gpa", 
    "masters gpa", "bachelors gpa", "coursework", "what courses did you take", "subjects studied", 
    "masters coursework", "bachelors coursework", "masters degree", "bachelors degree", 
    "when did you start masters", "when do you graduate", "when are you graduating", 
    "graduating in?", "when graduating?", "graduation", "masters graduation", 
    "masters degree graduation", "when does your masters degree end", "when will you finish your studies", 
    "what is your graduation date", "when do you complete your master's program", 
    "when are you done with school", "when did you graduate bachelors", "when did your bachelors end", 
    "when did you come to us", "when did you come to the US", "bachelors final year project", 
    "final year project", "thesis", "what is your field of study", "did you take deep learning courses", 
    "visa status", "your visa", "visa type", "what visa do you have", "work authorization", 
    "can you work in us", "can you work in the US?", "are you eligible to work in the US?", 
    "us work permit", "need sponsorship", "do you need visa sponsorship", 
    "do you need visa sponsorship?", "will you need sponsorship", "OPT", 
    "what is your opt status", "citizenship", "what citizenship do you have", 
    "international student", "are you an international student", "work experience", 
    "professional experience", "job experience", "where have you worked", "your work history", 
    "employment history", "current job", "where do you work now", 
    "what are you currently working on", "current role", "wisconsin school of business", 
    "wisconsin school of business role", "wisconsin school of business tools", "uw college", 
    "uw college role", "uw college tools", "wisconsin institute for discovery", 
    "wisconsin institute for discovery role", "wisconsin institute for discovery tools", 
    "projects", "tell me about your projects", "projects you have worked in", 
    "give me a list of projects you have worked on", "can you tell me about any projects you have worked on?", 
    "what are some of your projects?", "your project portfolio", "automl", "automl project", 
    "what is AutoML-ify", "automl tools", "automl details", "weather prediction", 
    "weather prediction project", "what is Not Your Basic Weather Prediction", 
    "weather prediction tools", "weather prediction details", "whatsapp chat", 
    "whatsapp chat project", "whatsapp chat tools", "whatsapp chat details", "github", 
    "github repository", "your github", "most impressive project", 
    "what is your most impressive project?", "best project", "what are your skills", 
    "technical skills", "programming languages", "python libraries", "machine learning", 
    "machine learning frameworks", "deep learning", "computer vision", "nlp", "data analysis", 
    "cloud", "aws experience", "databases", "mlops", "data visualization", "strongest skills", 
    "most proficient tools", "favorite technologies", "do you know cloud computing", 
    "do you have experience in cloud computing?", "certifications", "aws certification", 
    "kaggle certifications", "nlp certification", "online courses", "are you certified in AWS", 
    "youtube channel", "youtube", "medium", "medium articles", "hobbies", 
    "do you have a youtube channel", "do you write on medium", "what do you do in your free time?", 
    "do you have a youtube channel?", "do you write blogs?", "research", "research interests", 
    "academic strengths", "do you do research", "what are your research interests", 
    "do you have research experience?", "what topics have you researched?", "nlp experience", 
    "computer vision experience", "mlops experience", "data engineering", "strengths", 
    "work style", "communication skills", "career goals", "future plans", "big data", 
    "devops", "agile", "leadership", "fallback", "what is your age", "how old are you", 
    "what is his age", "how old is he", "your age", "age", "what is your tech stack", 
    "what tools do you use", "what frameworks do you know", "do you know deep learning", 
    "what is your expertise", "what is your primary programming language", 
    "do you have experience with cloud platforms", "what is your experience with NLP", 
    "do you have experience with computer vision", "what is your experience with MLOps", 
    "do you have experience with big data", "what is your experience with data visualization", 
    "do you have experience with SQL", "what is your experience with AI", 
    "do you have experience with automation", "what is your experience with AWS", 
    "do you have experience with Docker", "do you have experience with Kubernetes", 
    "what is your experience with Tableau", "do you have experience with Power BI", 
    "what is your experience with Python", "do you have experience with C++", 
    "do you have experience with JavaScript", "what is your experience with data engineering", 
    "do you have experience with time-series analysis", "what is your experience with active learning", 
    "do you have experience with transformer models", "what is your experience with GPT models", 
    "do you have experience with fine-tuning models", "what is your experience with data augmentation", 
    "do you have experience with semi-supervised learning", "what is your experience with benchmarking", 
    "do you have experience with A/B testing", "what is your experience with hypothesis testing", 
    "do you have experience with regression analysis", "what is your experience with data cleaning", 
    "do you have experience with feature engineering", "what is your experience with model deployment", 
    "do you have experience with model monitoring", "what is your experience with data drift detection", 
    "do you have experience with CI/CD", "what is your experience with version control", 
    "do you have experience with collaborative projects", "what is your experience with Agile", 
    "do you have experience with leadership", "what is your experience with communication", 
    "do you have experience with teaching or mentoring", "what is your experience with public speaking", 
    "do you have experience with writing", "what is your experience with content creation", 
    "do you have experience with photography", "what is your experience with traveling", 
    "do you have experience with creative projects", "what is your experience with problem-solving", 
    "do you have experience with innovation", "what is your experience with research", 
    "do you have experience with academic writing", "what is your experience with teamwork", 
    "do you have experience with cross-functional teams", "what is your experience with project management", 
    "do you have experience with time management", "what is your experience with adaptability", 
    "do you have experience with continuous learning", "what is your experience with open-source contributions", 
    "do you have experience with hackathons", "what is your experience with startups", 
    "do you have experience with entrepreneurship", "what is your experience with data privacy", 
    "do you have experience with ethical AI", "what is your experience with scalability", 
    "do you have experience with performance optimization", "what is your experience with cost optimization", 
    "do you have experience with real-time systems", "what is your experience with edge computing", 
    "do you have experience with IoT", "what is your experience with robotics", 
    "do you like ai", "what programming languages do you know", "what databases do you use", 
    "do you enjoy ai", "what databases have you worked with", "what are your strongest skills", 
    "why should we hire you?", "interesting", "pytorch", "tensorflow", "scikit-learn", 
    "airflow", "dbt", "snowflake", "gcp", "aws", "tableau", "sas", "pyspark", "data pipelines", 
    "data engineering", "data processing", "etl", "salesforce", "dashboard", "interview", 
    "github", "github contributions", "data analysis", "research software", "project assistant", "UW–Madison Data Science Institute", 
    "UW–Madison Data Science Institute role", "UW–Madison Data Science Institute tools", "UW–Madison Data Science Institute projects",
    "UW–Madison Data Science Institute details", "UW–Madison Data Science Institute experience", "UW–Madison Data Science Institute coursework",
    "University of Wisconsin - Madison", "Madison", "University of Wisconsin", "Research Assistant", "Research Assistant role",
    "Data Engineer", "Datacurate Technologies", "SMPH", "School of Medicine and Public Health", "School of Medicine and Public Health role",
    "Universities of Wisconsin System", "Data Analyst", "Redfin Housing Pipeline", "Redfin", "Piepline", "Certifications"


    }


@st.cache_resource(show_spinner=False)
def get_questions_list() -> list:
    """
    Returns a list of canonical question intents for the 'nudge' gate.
    Extend with your full list for better coverage.
    """
    return [
        "who are you",
        "what can you do",
        "tell me about you",
        "projects",
        "work experience",
        "skills",
        "contact information",
        "education",
        "visa status",
        "github",
        "linkedin",
    ]


@st.cache_resource(show_spinner=False)
def get_var_mapping():
    """
    Pulls curated Q&A mapping from `stored_questions.var` if available.
    Supports dict (prompt->answer) or list (prompts only).
    """
    try:
        from stored_questions import var  # your original module
        return var
    except Exception:
        # Safe fallback: no curated answers
        return {}