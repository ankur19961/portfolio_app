 
import os
import time
import base64
import html
import re
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
import requests
import streamlit as st
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from streamlit_option_menu import option_menu

# -------------------------------
# 0) PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Portfolio",
    layout="wide",
    page_icon="👧🏻",
)

# Single initialization of commonly used session items
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "bot",
            "content": "Hi! I'm AnkBot, Ankur's AI assistant. Ask me anything about his skills, experience, projects, or visa status! 🚀",
        }
    ]
if "message_counter" not in st.session_state:
    st.session_state.message_counter = 0
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "blocked": 0,
        "faq_prompted": 0,   # when input looked off-topic (questions similarity low)
        "faq_answered": 0,   # answered from curated store `var`
        "llm": 0,
        "too_long": 0,
    }

# -------------------------------
# 1) DATA: BLOCK LIST, QUESTIONS, VAR (curated)
# -------------------------------
# Import the large dicts/lists as in the original app
from stored_questions import var  # expected dict (q->answer) or list of prompts

# ---- Blocked prompts (unchanged content, truncated example) ----
# NOTE: For brevity in this refactor, we assume `blocked_prompts`, `questions` are
# imported from the original module or defined below. Replace `...` with the full content.
# To stay self-contained, we include the original definitions by referencing prior codebase.
# You should paste the full original `blocked_prompts` and `questions` content here.

blocked_prompts = {
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

questions = [
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

]

# -------------------------------
# 2) CSS HELPERS
# -------------------------------

def inject_global_css():
    st.markdown(
        """
        <style>
            /* Global tokens derived from Streamlit theme when possible */
            :root {
                --primary-color: #1a1a1a;
                --secondary-color: #333333;
                --text-color: #ffffff;
                --accent-color: #aaaaaa;
            }
            /* Chat container */
            .chatbot-container {{
                background: #1a1a1a;
                border-radius: 14px;
                border: 1px solid #333;
                display: flex; flex-direction: column;
                position: relative; overflow: hidden;
                height: 420px;
            }}
            .chatbot-header {{
                background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
                color: #fff;
                padding: 12px 15px;
                border-radius: 14px 14px 0 0;
                position: sticky; top: 0; z-index: 100;
                flex-shrink: 0;
            }}
            .chatbot-messages {{
                overflow-y: auto; padding: 16px;
                display: flex; flex-direction: column;
                gap: 12px; flex-grow: 1; height: 380px;
                scroll-behavior: smooth;
            }}
            .message-row {{ display: flex; width: 100%; }}
            .user-row   {{ justify-content: flex-end; }}
            .bot-row    {{ justify-content: flex-start; }}
            .user-message, .bot-message {{
                word-wrap: break-word; white-space: pre-wrap; overflow-wrap: break-word;
                max-width: 75%; padding: 12px 16px; border-radius: 12px; line-height: 1.4;
            }}
            .user-message {{ background: #2a2a2a; color: white; border-radius: 12px 12px 0 12px; }}
            .bot-message  {{ background: #2a2a2a; color: white; border-radius: 12px 12px 12px 0; }}
            .scroll-to {{ height: 1px; }}
            /* Form styling */
            .stForm {{ background: #1a1a1a; border-radius: 0 0 14px 14px; border: 1px solid #333; border-top: none; margin-top: -16px !important; padding: 1rem; }}
            .stTextInput input {{ background: #2a2a2a !important; color: white !important; border-radius: 20px !important; padding: 8px 16px !important; border: none !important; }}
            .stButton button {{ background: #2a2a2a !important; color: white !important; border-radius: 20px !important; padding: 5px 15px !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_message(role: str, text: str) -> str:
    """Safely format a chat bubble for 'user' or 'bot'."""
    safe = html.escape(text or "")
    if role == "bot":
        safe = safe.replace("\n", "<br>")
    cls = "user-message" if role == "user" else "bot-message"
    row = "user-row" if role == "user" else "bot-row"
    return f'<div class="message-row {row}"><div class="{cls}">{safe}</div></div>'


# -------------------------------
# 3) TEXT UTILS & TF-IDF CACHING
# -------------------------------

def preprocess_text(text: str) -> str:
    text = (text or "").lower()
    # keep word and whitespace characters
    text = re.sub(r"[^\w\s]", "", text)
    return text

@st.cache_resource(show_spinner=False)
def _build_tfidf_model(corpus: Tuple[str, ...]):
    preprocessed = [preprocess_text(t) for t in corpus]
    vectorizer = TfidfVectorizer(min_df=1, analyzer="char_wb", ngram_range=(2, 4))
    matrix = vectorizer.fit_transform(preprocessed)
    return vectorizer, matrix

@st.cache_resource(show_spinner=False)
def get_blocked_model():
    corpus = tuple(blocked_prompts.keys())
    vec, mat = _build_tfidf_model(corpus)
    return vec, mat, list(corpus)

@st.cache_resource(show_spinner=False)
def get_questions_model():
    corpus = tuple(questions)
    vec, mat = _build_tfidf_model(corpus)
    return vec, mat, list(corpus)

@st.cache_resource(show_spinner=False)
def get_var_model():
    # support both dict and list for `var`
    mapping = None
    if isinstance(var, dict):
        corpus = list(var.keys())
        mapping = var
    elif isinstance(var, list):
        corpus = var
    else:
        corpus = []
    vec, mat = _build_tfidf_model(tuple(corpus)) if corpus else (None, None)
    return vec, mat, corpus, mapping


def match_similarity(user_input: str, vec, mat, corpus: List[str], threshold: float):
    if not user_input or vec is None or mat is None or not corpus:
        return False, None, 0.0, -1
    processed = preprocess_text(user_input).strip()
    if not processed:
        return False, None, 0.0, -1
    uvec = vec.transform([processed])
    sims = cosine_similarity(uvec, mat).flatten()
    idx = int(np.argmax(sims))
    score = float(np.max(sims)) if sims.size else 0.0
    return (score >= threshold), corpus[idx], score, idx

# -------------------------------
# 4) RAG-LITE FOR bio.txt
# -------------------------------

@st.cache_data(show_spinner=False)
def load_bio_text() -> str:
    # Try to read bio.txt safely; if missing, return empty string and warn once
    try:
        with open(Path("assets/bio.txt"), "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def split_paragraphs(text: str) -> List[str]:
    # split on blank lines; keep non-empty trimmed paragraphs
    paras = [p.strip() for p in re.split(r"\n\s*\n", text or "")]
    return [p for p in paras if p]

@st.cache_resource(show_spinner=False)
def build_bio_index(bio_text: str):
    """Build a simple TF-IDF index over bio paragraphs for retrieval."""
    paragraphs = split_paragraphs(bio_text)
    if not paragraphs:
        return None, None, []
    pre = [preprocess_text(p) for p in paragraphs]
    vec = TfidfVectorizer(min_df=1, analyzer="word", ngram_range=(1, 2))
    mat = vec.fit_transform(pre)
    return vec, mat, paragraphs


def retrieve_bio_context(query: str, bio_text: str, k: int = 3, min_chars: int = 400) -> str:
    """Return top-k relevant paragraphs (concatenated) from bio for the query."""
    vec, mat, paras = build_bio_index(bio_text)
    if not paras or vec is None:
        return ""
    q = preprocess_text(query)
    qv = vec.transform([q])
    sims = cosine_similarity(qv, mat).flatten()
    top_idx = np.argsort(-sims)[: max(k, 1)]
    chunks = [paras[i] for i in top_idx]
    # Ensure enough context length
    joined = "\n\n".join(chunks)
    if len(joined) < min_chars and len(paras) > k:
        # add more paragraphs by descending similarity
        extra = [i for i in np.argsort(-sims) if i not in top_idx][: (k * 2)]
        chunks.extend([paras[i] for i in extra])
        joined = "\n\n".join(chunks)
    return joined

# -------------------------------
# 5) MODEL CLIENT & CALL WITH RETRIES
# -------------------------------

# def create_deepseek_client() -> OpenAI:
#     """Create a DeepSeek-compatible client using the OpenAI SDK wrapper.
#     Requires st.secrets["OPENAI_API_KEY"].
#     """
#     api_key = st.secrets.get("OPENAI_API_KEY")
#     if not api_key:
#         raise RuntimeError("OpenAI API Key not found in Streamlit secrets.")
#     # DeepSeek OpenAI-compatible endpoint
#     return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")



def ask_bot(input_text, bio_content):
    # Initialize typing_placeholder first, outside try block
    typing_placeholder = st.empty()
    
    try:
        # Show typing indicator
        typing_placeholder.markdown("🤖 AnkBot is typing...", unsafe_allow_html=True)

        # Debug: Check if API key exists
        if "GEMINI_API_KEY" not in st.secrets:
            typing_placeholder.empty()
            return "❌ GEMINI_API_KEY not found in secrets. Please add it in Streamlit settings."
        
        # Debug: Show partial key (for verification)
        api_key = st.secrets["GEMINI_API_KEY"]
        if len(api_key) < 10:
            typing_placeholder.empty()
            return f"❌ API key seems too short: {len(api_key)} characters"
        
        key_preview = api_key[:10] + "..." + api_key[-5:] if len(api_key) > 15 else "Key too short"
        
        # Try importing google genai
        try:
            from google import genai
        except ImportError as ie:
            typing_placeholder.empty()
            return f"❌ Import error: {str(ie)}. Check if 'google-genai' is in requirements.txt"

        # Combine context and user question
        contents = f"Context:\n{bio_content}\n\nUser question:\n{input_text}"

        # Try to initialize Gemini client
        try:
            client = genai.Client(api_key=api_key)
        except Exception as ce:
            typing_placeholder.empty()
            return f"❌ Client creation failed: {str(ce)}"

        # Try to call Gemini model
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [contents]}],
                config={
                    "system_instruction": (
                        "You are AnkBot, an AI assistant answering questions about Ankur. "
                        "Use only the provided context when possible. If unsure, do NOT make up answers. "
                        "Politely ask users to contact Ankur at ankurshukla19961@gmail.com.\n\n"
                        "Format responses with:\n"
                        "- Plain text (no markdown)\n"
                        "- Hyphens (-) for lists\n"
                        "- Simple line breaks"
                    ),
                    "temperature": 0.4
                }
            )
        except Exception as me:
            typing_placeholder.empty()
            return f"❌ Model call failed: {str(me)}"

        typing_placeholder.empty()
        
        # Try to get response text
        try:
            response_text = getattr(response, "text", None)
            if not response_text:
                return f"❌ No text in response. Response type: {type(response)}"
            return response_text.strip()
        except Exception as re:
            typing_placeholder.empty()
            return f"❌ Response parsing failed: {str(re)}"

    except Exception as e:
        typing_placeholder.empty()
        return f"❌ Unexpected error: {str(e)}"


# -------------------------------
# 6) LEFT PROFILE PANEL (unchanged content, structured)
# -------------------------------

def side_page():
    def get_image_base64(image_path: str) -> str:
        if not os.path.exists(image_path):
            return ""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    img_b64 = get_image_base64("assets/images/photo.png")

    st.markdown(
        """
        <style>
            .main-card { max-width: 500px; margin: 0 auto; padding: 0.5rem; background-color: var(--primary-color); border-radius: 15px; color: var(--text-color); text-align: center; }
            .profile-img { width: 200px; height: 200px; border-radius: 50%; object-fit: cover; margin-bottom: 1rem; border: 3px solid var(--secondary-color); }
            .name { font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem; display:flex; align-items:center; justify-content:center; }
            .title { color: var(--accent-color); background-color: var(--secondary-color); padding: 0.5rem 1rem; border-radius: 20px; display:flex; font-size: 0.9rem; align-items:center; justify-content:center; }
            .contact-item { display:flex; align-items:center; justify-content:center; margin-top: 1.0rem; gap:0.6rem; }
            .contact-word { color: var(--accent-color); }
            .social-icons { display:flex; justify-content:center; gap: 1.5rem; margin-top: 1.2rem; }
            .social-icon { width: 30px; transition: transform 0.3s ease-in-out; }
            .social-icon:hover { transform: scale(1.08); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Photo
    st.markdown(
        f"""
        <div class="main-card">
            <div>
                <img src="data:image/png;base64,{img_b64}" class="profile-img" />
            </div>
            <div class="name">Ankur Shukla</div>
            <div class="title">Senior Data Scientist</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Contact rows
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/email.png" width="20" />
            <div>
                <strong class="contact-word">EMAIL</strong><br>
                ankurshukla19961@gmail.com
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/phone.png" width="20" />
            <div>
                <strong class="contact-word">PHONE</strong><br>
                +91 8097970726
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="contact-item">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/marker.png" width="20" />
            <div>
                <strong class="contact-word">LOCATION</strong><br>
                Mumbai, India
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Social links
    st.markdown(
        """
        <div class="social-icons">
            <a href="https://www.linkedin.com/in/ankurshukla1996/" target="_blank">
                <img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" class="social-icon" />
            </a>
            <a href="https://github.com/ankur19961" target="_blank">
                <img src="https://img.icons8.com/ios-filled/50/ffffff/github.png" class="social-icon" />
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# 7) CHAT RENDERER (ABOUT ME)
# -------------------------------

def render_about_me():
    inject_global_css()

    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page()

    with col3:
        st.title("Hi, I am Ankur! 👋")
        st.write(
            """
            Senior Data Scientist with 6+ years of experience in Machine Learning, NLP, and Generative AI. Skilled in deploying
            production-grade AI systems using LLMs, RAG pipelines, LangChain, and MLOps frameworks. Proven record of building
            scalable inference services using PyTorch, Docker, and AWS to improve CX, automate workflows, and ensure compliance.
            """
        )

        st.header("Meet AnkBot! 🤖")

        # Render chat history using unified HTML renderer
        chat_messages_html = "".join(
            format_message(m["role"], m["content"]) for m in st.session_state.chat_history
        )
        st.markdown(
            f"""
            <div class="chatbot-container">
                <div class="chatbot-header">
                    <h4 style="margin:0; font-weight: 500;">Ask AnkBot anything about me!</h4>
                </div>
                <div class="chatbot-messages" id="chat-messages">
                    {chat_messages_html}
                    <div id="scroll-target" class="scroll-to"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Input form
        with st.form(key=f"chat_form_{st.session_state.message_counter}", clear_on_submit=True):
            user_input = st.text_input("Message", label_visibility="collapsed")
            submitted = st.form_submit_button("➤")

        # Load BIO once (non-fatal if missing)
        bio_text = load_bio_text()
        if not bio_text:
            st.info("bio.txt not found. I'll still try to help, but responses may be limited.")

        if submitted and user_input.strip():
            st.session_state.message_counter += 1
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Heuristic for very long queries → soft guidance, but continue
            if len(user_input.split()) > 80:
                st.session_state.metrics["too_long"] += 1
                st.session_state.chat_history.append(
                    {
                        "role": "bot",
                        "content": "That’s a detailed question! I’ll do my best. If needed, I may ask a quick follow-up to focus the answer.",
                    }
                )

            # 1) Blocked prompts (fast path)
            bvec, bmat, bcorpus = get_blocked_model()
            matched, match_key, score, idx = match_similarity(user_input, bvec, bmat, bcorpus, threshold=0.80)
            if matched:
                st.session_state.metrics["blocked"] += 1
                reply = blocked_prompts.get(match_key, "I understand.")
                st.session_state.chat_history.append({"role": "bot", "content": reply})
                st.rerun()

            # 2) ‘Questions’ gate — if NOT matched, show a gentle nudge but still proceed
            qvec, qmat, qcorpus = get_questions_model()
            matched_q, _, qscore, _ = match_similarity(user_input, qvec, qmat, qcorpus, threshold=0.40)
            if not matched_q:
                st.session_state.metrics["faq_prompted"] += 1
                st.session_state.chat_history.append(
                    {
                        "role": "bot",
                        "content": "Tip: I answer best on portfolio topics (skills, projects, experience).",
                    }
                )

            # 3) Curated answers from `var` (high precision)
            vvec, vmat, vcorpus, vmapping = get_var_model()
            if vcorpus:
                matched_v, vkey, vscore, vidx = match_similarity(user_input, vvec, vmat, vcorpus, threshold=0.90)
            else:
                matched_v, vkey, vscore, vidx = (False, None, 0.0, -1)

            if matched_v and vmapping and isinstance(vmapping, dict):
                st.session_state.metrics["faq_answered"] += 1
                reply = vmapping.get(vkey, "")
                st.session_state.chat_history.append({"role": "bot", "content": reply})
                st.rerun()

            # 4) LLM fallback with RAG-lite context
            focused_context = retrieve_bio_context(user_input, bio_text, k=3)
            typing_placeholder = st.empty()
            typing_placeholder.markdown("🤖 AnkBot is typing…")
            reply = ask_bot(user_input, focused_context)
            typing_placeholder.empty()

            st.session_state.metrics["llm"] += 1
            st.session_state.chat_history.append({"role": "bot", "content": reply})
            st.rerun()

        # Tiny analytics footer
        with st.expander("Chat diagnostics (local)"):
            mt = st.session_state.metrics
            st.write(
                f"Blocked: {mt['blocked']} • Nudge: {mt['faq_prompted']} • Curated: {mt['faq_answered']} • LLM: {mt['llm']} • Long: {mt['too_long']}"
            )

# -------------------------------
# 8) TECHNICAL EXPERIENCE TAB (unchanged logic)
# -------------------------------

def render_research_experience():
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page()

    with col3:
        st.markdown("<h1 style='margin-bottom: 20px;'>Work Experience</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
                .experience-block { display:flex; background-color:black; border-radius:10px; margin-bottom:20px; box-shadow:0px 4px 6px rgba(0,0,0,0.1); overflow:hidden; }
                .experience-left  { background-color:#F7C873; padding:20px; flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; font-weight:bold; color:black; }
                .experience-right { padding:20px; flex:3; }
                .experience-details { font-size:16px; line-height:1.5; }
                ul { padding-left: 20px; } li { margin-bottom: 10px; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        experiences = [
            {
                "title": "Senior Data Scientist",
                "subtitle": "Fractal Analytics",
                "date": "Apr 2025 - Present",
                "details": [
                    "Initiated an AI-based prescription alerting system to flag high-risk PV1 transactions using historical QRE and Near Miss data.",
                    "Designed a LightGBM model with temporal features to detect anomalies in drug, dose, and patient data, reducing manual interventions by 30%.",
                    "Applied LLM-powered semantic clustering on pharmacist notes, improving labeling accuracy by 28%.",
                    "Integrated real-time alerts into IRIS/Prodigy via FastAPI, achieving sub-300ms latency.",
                ],
            },
            {
                "title": "Senior ML Data Analyst",
                "subtitle": "Tata Consultancy Services",
                "date": "Apr 2021 - Apr 2025",
                "details": [
                    "Spearheaded a GenAI chatbot using LangChain, LangGraph, and RAG, automating 80% of customer queries.",
                    "Built modular conversational flows with LangGraph and AI Agents, achieving 92% completion accuracy.",
                    "Fine-tuned LLMs with Lamini on 10K+ documents, boosting precision by 38%.",
                    "Engineered semantic search using OCR, MiniLM, FAISS, and Pinecone; reduced hallucinations by 31% using RAGAS.",
                ],
            },
            {
                "title": "IT Analyst",
                "subtitle": "Tata Consultancy Services",
                "date": "Dec 2018 - Mar 2021",
                "details": [
                    "Developed ML-based credit eligibility scoring engine, lowering default rates by 18%.",
                    "Built data pipelines consolidating 50–64 features and reduced feature count by 60%.",
                    "Applied LightGBM with SMOTE, achieving 89% AUC-ROC and 82% recall.",
                    "Used SHAP for model explainability and monitored post-COVID drift.",
                ],
            },
        ]

        for exp in experiences:
            details_html = "".join(f"<li>{html.escape(d)}</li>" for d in exp["details"])
            st.markdown(
                f"""
                <div class="experience-block">
                    <div class="experience-left">
                        <div>{html.escape(exp['subtitle'])}</div>
                        <div>{html.escape(exp['title'])}</div>
                        <div>{html.escape(exp['date'])}</div>
                    </div>
                    <div class="experience-right">
                        <div class="experience-details">
                            <ul>{details_html}</ul>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# -------------------------------
# 9) PROJECTS TAB (unchanged logic, small safety)
# -------------------------------

def projects():
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page()

    with col3:
        st.markdown("<h1 style='margin-bottom: 20px;'>Projects</h1>", unsafe_allow_html=True)

        project_data = [
            {
                "title": "Redfin Housing Data Pipeline And Visualization",
                "description": "Data Engineering",
                "category": "Data Engineering and Analysis",
                "image": "assets/images/redfin.jpg",
                "github_link": "https://github.com/yourusername/redfin-project",
            },
            {
                "title": "Kafka Data Pipeline With Streamlined Processing",
                "description": "Real Time Analytics",
                "category": "Data Engineering and Analysis",
                "image": "assets/images/kafka.png",
                "github_link": "https://github.com/vijayrampatel/Data-pipeline-Kafka",
            },
            {
                "title": "Layoffs Data Visualization",
                "description": "ETL and Data Visualization",
                "category": "Data Engineering and Analysis",
                "image": "assets/images/Layoffs.png",
                "github_link": "Layoffs.png",
            },
            {
                "title": "Fraud Transaction Detection",
                "description": "Machine Learning",
                "category": "Machine and Deep Learning",
                "image": "assets/images/fraud_transaction.png",
                "github_link": "https://github.com/yourusername/fraud-detection",
            },
            {
                "title": "Movie Recommendation System",
                "description": "NLP",
                "category": "Machine and Deep Learning",
                "image": "assets/images/movie-recommendation-resized.jpeg",
                "github_link": "https://github.com/vijayrampatel/MovieRecommendationSystem/tree/main",
            },
        ]

        tabs = ["All", "Generative and AI Agents", "Machine and Deep Learning", "Data Engineering and Analysis"]
        selected_tab = st.radio("Filter by category:", tabs, horizontal=True)

        if selected_tab == "All":
            filtered = project_data
        else:
            filtered = [p for p in project_data if p["category"] == selected_tab]

        st.markdown(
            """
            <style>
                .project-card { position: relative; overflow: hidden; border-radius: 10px; }
                .project-card img { transition: transform 0.3s ease; width:100%; border-radius:10px; }
                .project-card:hover img { transform: scale(1.06); }
                .project-overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); display:flex; justify-content:center; align-items:center; opacity:0; transition: opacity 0.3s ease; }
                .project-card:hover .project-overlay { opacity:1; }
                .project-overlay-icon { font-size: 50px; color:#fff; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        cols_per_row = 4
        for i in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, project in zip(cols, filtered[i : i + cols_per_row]):
                with col:
                    image_path = project["image"]
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as f:
                            img64 = base64.b64encode(f.read()).decode()
                        st.markdown(
                            f"""
                            <div class="project-card">
                                <a href="{html.escape(project['github_link'])}" target="_blank">
                                    <img src="data:image/jpg;base64,{img64}">
                                    <div class="project-overlay"><span class="project-overlay-icon">👁️</span></div>
                                </a>
                            </div>
                            <h4 style="margin-top:10px;">{html.escape(project['title'])}</h4>
                            <p>{html.escape(project['description'])}</p>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.warning(f"Image not found for {project['title']}")

# -------------------------------
# 10) RESUME TAB — unified approach (no webbrowser on server)
# -------------------------------

def resume_tab():
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page()
    with col3:
        st.markdown("<h1 style='margin-bottom: 20px;'>Resume</h1>", unsafe_allow_html=True)
        resume_url = "https://drive.google.com/file/d/1ZHL_eMg-m4d8EH4rKVMSXNAwmENtFkfi/view"
        st.link_button("Open Resume in New Tab", resume_url, use_container_width=False)
        st.caption("If the link doesn't open, copy & paste: " + resume_url)

# -------------------------------
# 11) CONTACT TAB (unchanged logic)
# -------------------------------

def contact():
    col1, _, col3 = st.columns([7, 1, 20])
    with col1:
        side_page()
    with col3:
        st.markdown("<h1 style='margin-bottom: 20px;'>Contact</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <section class="mapbox">
                <figure>
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d241317.1160983341!2d72.7410992!3d19.0821978!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b63b0f0aaf2f%3A0x3a1f6f6f6f6f6f6f!2sMumbai%2C%20Maharashtra%2C%20India!5e0!3m2!1sen!2sin!4v1717596151210!5m2!1sen!2sin"
                        width="100%" height="300" style="border:0; border-radius:10px;" allowfullscreen="" loading="lazy"></iframe>
                </figure>
            </section>
            """,
            unsafe_allow_html=True,
        )

        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter your email address")
        message = st.text_area("Message", placeholder="Type your message here…")

        if st.button("Send Message"):
            if full_name and email and message:
                formspree_url = "https://formspree.io/f/mnnjezkg"
                data = {"fullname": full_name, "email": email, "message": message}
                try:
                    r = requests.post(formspree_url, data=data, timeout=10)
                    if r.status_code == 200:
                        st.success("Your message has been sent successfully!")
                    else:
                        st.error("Failed to send your message. Please try again later.")
                except Exception as e:
                    st.error(f"Failed to send your message. {e}")
            else:
                st.error("Please fill out all fields before submitting.")

# -------------------------------
# 12) NAVIGATION
# -------------------------------

selected_tab = option_menu(
    menu_title=None,
    options=["About Me", "Technical Experience", "Projects", "Resume", "Contact"],
    icons=["person", "briefcase", "folder", "info", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected_tab == "About Me":
    render_about_me()
elif selected_tab == "Technical Experience":
    render_research_experience()
elif selected_tab == "Projects":
    projects()
elif selected_tab == "Resume":
    resume_tab()
elif selected_tab == "Contact":
    contact()
