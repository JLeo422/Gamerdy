
import streamlit as st

# ------------------- SESSION STATE INIT -------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'start'
if 'num_players' not in st.session_state:
    st.session_state.num_players = 0
if 'player_names' not in st.session_state:
    st.session_state.player_names = {}
if 'used_questions' not in st.session_state:
    st.session_state.used_questions = set()
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = None
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'reveal_answer' not in st.session_state:
    st.session_state.reveal_answer = False
if 'last_award' not in st.session_state:
    st.session_state.last_award = None
if 'gambles_locked' not in st.session_state:
    st.session_state.gambles_locked = False
if 'random_reveal' not in st.session_state:
    st.session_state.random_reveal = False


# ------------------- CATEGORY DATA -------------------
CATEGORIES = {
            "FPS": {
                100: {"question": "This iconic Fortnite location is known for chaotic landings, high-rise battles, and being the unofficial capital of early eliminations.", "answer": "Tilted Towers"},
                200: {"question": "Set in a quaint mid-century neighborhood with a dark atomic secret, this Call of Duty map looks like Fallout’s vacation home… until the countdown hits zero.", "answer": "Nuke Town"},
                300: {"question": "In Halo, this four-wheeled vehicle comes equipped with a mounted gun, poor steering, and a strong tendency to flip when you breathe on it wrong.", "answer": "Warthog"},
                400: {"question": "This bolt-action sniper rifle in CS:GO costs $4750, one-shots enemies, and is responsible for more eco rounds than actual mismanagement.", "answer": "AWP"},
                500: {"question": "This 3-foot menace from GoldenEye 007 on the N64 was notoriously hard to hit due to his small hitbox and immunity to auto-aim.", "answer": "Oddjob"}
            },
            "MOBA": {
                100: {"question": "This popular MOBA from Valve features Radiant vs. Dire and over 100 unique heroes.", "answer": "Dota 2"},
                200: {"question": "This glowing blue item is often built to upgrade a hero’s ultimate ability and is named after a powerful wizard.", "answer": "Aghanim’s Scepter"},
                300: {"question": "This high-energy League streamer who resembles a jacked Geodude was banned in 2016 for toxicity, only to return reformed and break Twitch records.", "answer": "Tyler1"},
                400: {"question": "Which champion in League of Legends says, 'A True Master Is An Eternal Student'?", "answer": "Master Yi"},
                500: {"question": "In League of Legends, this legendary base backdoor by a Kassadin player became the blueprint for every bold Nexus steal attempt.", "answer": "xPeke"}
            },
            "RPG": {
                100: {"question": "This white-haired monster hunter is the main protagonist in The Witcher series.", "answer": "Geralt of Rivia"},
                200: {"question": "In Elden Ring, this currency is used to level up, buy items, and is dropped on death.", "answer": "Runes"},
                300: {"question": "This Fallout companion is loyal, fluffy, and somehow able to tank a Super Mutant with nothing but vibes and teeth.", "answer": "Dogmeat"},
                400: {"question": "In Skyrim, these massive enemies are peaceful — until you poke one — then they send you flying into space with a single swing.", "answer": "Giants"},
                500: {"question": "This blue, four-armed Pokémon is built like a tank, wears a championship belt, and still faints to a level 5 Pidgey using Gust.", "answer": "Machamp"}
            },
            "MMO": {
                100: {"question": "In MapleStory, this area is where players gather to sell goods and flex their cosmetic drip.", "answer": "Free Market"},
                200: {"question": "In LOTRO, new players often begin their journey in this peaceful hobbit-filled zone with pies to deliver and zero XP from killing wolves.", "answer": "The Shire"},
                300: {"question": "This classic MMO, released in 1999, was one of the first 3D MMORPGs and helped inspire World of Warcraft.", "answer": "EverQuest"},
                400: {"question": "This raid legend screamed his name and ran into a room full of dragon eggs, wiping his team and becoming a WoW meme icon.", "answer": "Leeroy Jenkins"},
                500: {"question": "This god-tier sword in RuneScape can freeze enemies and is dropped by the infamous god boss K’ril Tsutsaroth.", "answer": "Zamorak Godsword"}
            },
            "FlashG": {
                100: {"question": "In this Flash game, a baby in sunglasses defends treasure by launching tennis balls at pirates from a floating platform.", "answer": "Raft Wars"},
                200: {"question": "In Pandemic, what must happen for you to win the game?", "answer": "Everyone dies / Global extinction"},
                300: {"question": "In Interactive Buddy, how do you earn money to unlock new weapons and items?", "answer": "By interacting with or hurting the buddy"},
                400: {"question": "Which type of Bloons from Bloons Tower Defense can only be popped by specific upgraded towers, often sneaking through undetected?", "answer": "Camo Bloons"},
                500: {"question": "In Stick RPG, if you've maxed your stats and avoided dying in traffic, you can land this stressful high-paying job complete with a tie and a midlife crisis.", "answer": "CEO"}
            }
        }

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="GAMERDY Jeopardy", layout="centered")
st.title("🎮 GAMERDY: Jeopardy Game")

# ------------------- STAGE: START -------------------
if st.session_state.stage == 'start':
    st.markdown("Welcome to **GAMERDY**, the ultimate gamer-themed Jeopardy showdown!")
    if st.button("Start Game"):
        st.session_state.stage = 'choose_players'
        st.rerun()

# ------------------- STAGE: SELECT NUMBER OF PLAYERS -------------------
elif st.session_state.stage == 'choose_players':
    st.subheader("Select Number of Players")
    num = st.slider("How many players?", min_value=1, max_value=6, step=1)
    st.session_state.num_players = num

    if st.button("Next"):
        st.session_state.stage = 'enter_names'
        st.rerun()

# ------------------- STAGE: ENTER PLAYER NAMES -------------------
elif st.session_state.stage == 'enter_names':
    st.subheader("Enter Player Names")

    for i in range(st.session_state.num_players):
        name = st.text_input(f"Player {i+1} Name", key=f"name_{i}")
        st.session_state.player_names[f"Player {i+1}"] = name if name else f"Player {i+1}"

    if st.button("Continue to Game Board"):
        st.session_state.scores = {k: 0 for k in st.session_state.player_names.keys()}
        st.session_state.stage = 'game_board'
        st.rerun()

# ------------------- STAGE: GAME BOARD -------------------
elif st.session_state.stage == 'game_board':
    st.subheader("🧠 Jeopardy Board")

    if not st.session_state.selected_question:
        cols = st.columns(len(CATEGORIES))
        for col_idx, (category, questions) in enumerate(CATEGORIES.items()):
            with cols[col_idx]:
                st.markdown(f"### {category}")
                for points, qa in questions.items():
                    q_id = f"{category}_{points}"
                    disabled = q_id in st.session_state.used_questions

                    if st.button(f"{points}", key=q_id, disabled=disabled):
                        st.session_state.selected_question = (category, points)
                        st.session_state.reveal_answer = False
                        st.session_state.used_questions.add(q_id)
                        st.session_state.random_reveal = False
                        st.rerun()
    else:
        cat, pts = st.session_state.selected_question
        question_data = CATEGORIES[cat][pts]
        question = question_data["question"]
        answer = question_data["answer"]

        st.markdown(f"### {cat} - {pts} Points")
        st.info(question)

        if not st.session_state.reveal_answer:
            if st.button("Reveal Answer"):
                st.session_state.reveal_answer = True
                st.session_state.random_reveal = False
                st.rerun()
        else:
            st.success(f"**Answer:** {answer}")

        st.markdown("#### Who answered correctly?")
        correct_players = {}
        for key, name in st.session_state.player_names.items():
            correct_players[key] = st.checkbox(name, key=f"correct_{key}")

        if st.button("Award Points"):
            awarded = [key for key, val in correct_players.items() if val]
            st.session_state.last_award = {
                "players": awarded,
                "points": pts,
                "question_id": f"{cat}_{pts}"
            }
            for key in awarded:
                st.session_state.scores[key] += pts
            st.session_state.selected_question = None
            st.session_state.reveal_answer = False
            st.session_state.random_reveal = False
            st.rerun()

    st.markdown("---")
    st.markdown("### Scores:")
    for key, score in st.session_state.scores.items():
        st.write(f"{st.session_state.player_names[key]}: {score} pts")

    # Show Undo and Random Event buttons ONLY when no question is selected
    if not st.session_state.selected_question:
        if st.session_state.last_award:
            if st.button("Undo Last Points Awarded"):
                for key in st.session_state.last_award["players"]:
                    st.session_state.scores[key] -= st.session_state.last_award["points"]
                qid = st.session_state.last_award["question_id"]
                st.session_state.used_questions.discard(qid)
                st.session_state.last_award = None
                st.session_state.random_reveal = False
                st.rerun()

        total_questions = sum(len(qset) for qset in CATEGORIES.values())
        if len(st.session_state.used_questions) == total_questions:
            if st.button("🔥 Start Random Event Round"):
                st.session_state.stage = "random_event"
                st.session_state.random_index = 0
                st.session_state.multipliers = {k: 1.0 for k in st.session_state.player_names}
                st.session_state.gambles = {}
                st.session_state.gambles_locked = False
                st.session_state.random_reveal = False
                st.rerun()

# ------------------- STAGE: RANDOM EVENT ROUND -------------------
elif st.session_state.stage == "random_event":
    RANDOM_QUESTIONS = [
        {"question": "What MMO is known for unexpected random events?", "answer": "Runescape"},
        {"question": "What’s the Fallout beverage that glows and stayed carbonated?", "answer": "Nuka-Cola"},
        {"question": "What flash game features prehistoric battles evolving through the ages?", "answer": "Age of War"},
        {"question": "What Call of Duty game introduced Zombies mode?", "answer": "World at War"},
        {"question": "What blue League item boosts ultimates?", "answer": "Aghanim's Scepter"},
    ]

    idx = st.session_state.random_index

    if idx == 0 and not st.session_state.gambles_locked:
        st.header("🎲 Gamble Time!")
        st.markdown("Each player: How many points do you want to gamble?")

        for pid in st.session_state.player_names:
            st.number_input(
                f"{st.session_state.player_names[pid]}'s Gamble", min_value=0,
                max_value=st.session_state.scores[pid], key=f"gamble_{pid}"
            )

        if st.button("Lock In Gambles"):
            for pid in st.session_state.player_names:
                st.session_state.gambles[pid] = st.session_state[f"gamble_{pid}"]
            st.session_state.gambles_locked = True
            st.session_state.random_index += 1
            st.session_state.random_reveal = False
            st.rerun()

    elif idx <= len(RANDOM_QUESTIONS):
        q = RANDOM_QUESTIONS[idx - 1]
        st.subheader(f"🧠 Random Question {idx}")
        st.info(q["question"])

        if not st.session_state.random_reveal:
            if st.button("Reveal Answer"):
                st.session_state.random_reveal = True
                st.rerun()
        else:
            st.success(f"**Answer:** {q['answer']}")

        st.markdown("Who got it right?")
        answers = {}
        for pid in st.session_state.player_names:
            answers[pid] = st.checkbox(st.session_state.player_names[pid], key=f"rand_q{idx}_{pid}")

        if st.button("Submit Answers"):
            for pid, correct in answers.items():
                if correct:
                    st.session_state.multipliers[pid] += 1
                else:
                    st.session_state.multipliers[pid] *= 0.5
            st.session_state.random_index += 1
            st.session_state.random_reveal = False
            st.rerun()

    else:
        st.header("🏁 Final Scores After Random Event!")

        for pid in st.session_state.player_names:
            gamble = st.session_state.gambles[pid]
            multiplier = st.session_state.multipliers[pid]
            gain = int(gamble * multiplier)
            st.session_state.scores[pid] += gain

            st.success(f"{st.session_state.player_names[pid]} gambled {gamble}, multiplier ×{multiplier:.2f}, gained {gain} pts")

        if st.button("Show Final Rankings"):
            st.session_state.stage = "final_ranking"
            st.session_state.random_reveal = False
            st.rerun()

# ------------------- STAGE: FINAL RANKING -------------------
elif st.session_state.stage == "final_ranking":
    st.header("🏆 Final Rankings")

    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)

    for i, (pid, score) in enumerate(sorted_scores):
        st.markdown(f"**{i+1}. {st.session_state.player_names[pid]}** — {score} pts")

    winner = st.session_state.player_names[sorted_scores[0][0]]
    st.success(f"🏅 Winner: {winner}!")

    if st.button("Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
