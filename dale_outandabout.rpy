# Register the submod
init -990 python in mas_submod_utils:
    Submod(
        author="DaleRuneMTS",
        name="Out and About",
        description="Tired of Monika not having any idea where you're taking her? Use this submod to be more specific in your destination!"
        "New to 3.2: by request from AlicornAlley and to a certain extent my_otter_self, you can now take Moni to school! "
        "Further, some of Monika's post-outing topics now possess location awareness, so she'll comment on being in a cat cafe when talking about cat cafes for instance."
        "I've also added minor compatibility with Give Monika a Surname... and something else.",
        version="3.2",
        dependencies={},
        settings_pane=None,
        version_updates={
        }
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Out and About",
            user_name="DaleRuneMTS",
            repository_name="dale_out_and_about",
            submod_dir="/Submods",
            extraction_depth=2
        )

init 5 python in mas_bookmarks_derand:
    # Ensure things get bookmarked and derandomed as usual.
    label_prefix_map["ooa_"] = label_prefix_map["monika_"]

default -5 persistent._ooa_been_at = set()
default -5 persistent._ooa_jungry_NumberCheck = 0
default -5 persistent._enoughwiththejungry = False
default -5 persistent._ooa_followup_topics = set()
default p_surname = persistent._mas_player_surname
default persistent._mas_player_surname = None
default -5 persistent._moni_on_vacation = False

# To reset been_at persistences if you're updating to a newer version: open console with shift-o (must have dev console!)
# type del persistent._ooa_been_at
# and del persistent.event_database["eventlabel goes here"]
# then type exit to exit

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="ooa_bye_player_bday",
            unlocked=False,
            prompt="Let's go out somewhere particular for my birthday!",
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE,None),
        ),
        code="BYE",
        markSeen=True
    )

label ooa_bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "You want to go out for your birthday?{w=1} Okay!"
        m 1skbla "That sounds really romantic...I can't wait~"
        m 1wublb "So what would you like to do?"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Taking me out again on your birthday, [player]?"
        m 3hub "Yay!"
        m 1sub "I always love going out with you, but it's so much more special going out on your birthday..."
        m 1skbla "I'm sure we'll have a lovely time~"
        m 1wublb "So what would you like to do now?"
    else:
        m 1wub "Wow, you want to go out {i}again{/i}, [player]?"
        m 1skbla "I just love that you want to spend so much time with me on your special day!"
        m 1wublb "So where now?"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_someplace_normalplus_flow_aff_check


init 10 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="ooa_bye_going_someplace",
            unlocked=True,
            prompt="I'm going to take you somewhere specific.",
            pool=True
        ),
        code="BYE",
        markSeen=True
    )

label ooa_bye_going_someplace:
    $ import random

    python:

        if mas_isMonikaBirthday():
            dis_chance = 10
            upset_chance = 0

        else:
            dis_chance = 50
            upset_chance = 10

    if mas_isMoniBroken(lower=True):

        jump bye_going_somewhere_nothanks

    elif mas_isMoniDis(lower=True):

        if random.randint(1,100) <= dis_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "You really want to bring me along?"
        m 1ekd "Are you sure this isn't some--{nw}"
        $ _history_list.pop()
        m 1lksdlc "..."
        m 1eksdlb "What am I saying? Of course I'll go with you!"
        m "Just tell me where!{nw}"
        $ _history_list.pop()
        menu:
            m "Just tell me where!{fast}"
            "We're off to a poetry reading!":
                jump ooa_trips_poetryreading
            "We're off to watch a movie.":
                jump ooa_trips_movie
            "Let's go out in the garden.":
                jump ooa_trips_garden
            "I'm taking you to a cafe!":
                jump ooa_trips_cafe
            "Let's go for a walk in the park.":
                jump ooa_trips_park
            "Page Two":
                m 1wksdlb "You know what? Don't worry about it, I don't even care."
                m 1wfsdlc "As long as I get {i}something.{/i}{nw}"
                $ _history_list.pop()
                m 1wksdlb "As long as I get{fast} to spend time with you!"
                m 1cka "Please.{nw}"
                jump mas_dockstat_iostart

    elif mas_isMoniUpset(lower=True):

        if random.randint(1, 100) <= upset_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "You really want to bring me along?"
        m 1eka "..."
        m 1hua "Well, I suppose it can't hurt to join you."
        m 2dsc "Just...please."
        m 2rkc "{i}Please{/i} understand what I'm going through."
        m 1dkc "..."

        show monika 2ekd at t21
        python:
            option_list = [
                ("We're off to a poetry reading!", "ooa_trips_poetryreading",False,False),
                ("We're off to watch a movie.","ooa_trips_movie",False,False),
                ("Let's go out in the garden.","ooa_trips_garden",False,False),
                ("I'm taking you to a cafe!","ooa_trips_cafe",False,False),
                ("Let's go for a walk in the park.","ooa_trips_park",False,False),
                ("I'm going out with friends.","ooa_trips_friends",False,False),
                ("We're off to a tabletop RPG session.","ooa_trips_dandd",False,False),
                ("Let's go to a lake somewhere.","ooa_trips_lake",False,False),
                ("We're going on a train ride.","ooa_trips_train",False,False),
                ("We're off to a party.","ooa_trips_party",False,False),
                ("We're off to a parade.","ooa_trips_parade",False,False),
                ("We're off to a pride parade!","ooa_trips_pride",False,False),
                ("We're going dancing!","ooa_trips_dancing",False,False),
                ("We're off to a concert.","ooa_trips_concert",False,False),
                ("I'm going to a job interview.","ooa_trips_job",False,False),
                ("I'm taking you to class with me.","ooa_trips_school",False,False),
                ("Let's go swimming.","ooa_trips_swimming",False,False),
                ("We're going to a place of worship.","ooa_trips_church",False,False),
                ("I'm going for a jog.","ooa_trips_jog",False,False),
                ("Just a grocery run.","ooa_trips_grocery",False,False),
                ("I just want to get out of the house, really.","ooa_trips_generic",False,False),
            ]

            renpy.say(m, "Where are we going, anyway?", interact=False)

        call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
        show monika at t11

        $ selection = _return

        jump expression selection

    else:

        jump ooa_bye_going_someplace_normalplus_flow

label ooa_bye_going_someplace_normalplus_flow:

    if persistent._mas_d25_in_d25_mode:

        if mas_isD25Eve():
            jump ooa_bye_d25e_delegate

        if mas_isD25():
            jump ooa_bye_d25_delegate

        if mas_isNYE():
            jump ooa_bye_nye_delegate

        if mas_isNYD():
            jump ooa_bye_nyd_delegate

    if mas_isF14() and persistent._mas_f14_in_f14_mode:
        jump ooa_bye_f14

    if mas_isMonikaBirthday():
        jump ooa_bye_922_delegate

    if persistent._moni_on_vacation is True:
        jump ooa_bye_vacation

    else:
        jump ooa_bye_generic

label ooa_bye_d25e_delegate:

    if persistent._mas_d25_d25e_date_count > 0:
        call ooa_bye_d25e_second_time_out from _call_ooa_bye_d25e_second_time_out
    else:

        call ooa_bye_d25e_first_time_out from _call_ooa_bye_d25e_first_time_out

    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_d25e_first_time_out:
    m 1sua "Taking me somewhere special on Christmas Eve, [player]?"
    m 3eua "I know some people visit friends or family...or go to Christmas parties..."
    m 3hua "But wherever we're going, I'm happy you want me to come with you!"
    m 1eka "I hope we'll be home for Christmas, but even if we're not, just being with you is more than enough for me~"
    m 1etd "Still, where {i}are{/i} we going?"
    return

label ooa_bye_d25e_second_time_out:
    m 1wud "Wow, we're going out again today, [player]?"
    m 3hua "You really must have a lot of people you need to visit on Christmas Eve..."
    m 3hub "...or maybe you just have lots of special plans for us today!"
    m 1eka "But either way, thank you for thinking of me and bringing me along~"
    m 1esa "So where to this time?"
    return

label ooa_bye_d25_delegate:

    if persistent._mas_d25_d25_date_count > 0:
        call ooa_bye_d25_second_time_out from _call_ooa_bye_d25_second_time_out
    else:

        call ooa_bye_d25_first_time_out from _call_ooa_bye_d25_first_time_out

    jump ooa_bye_going_someplace_normalplus_flow_aff_check


label ooa_bye_d25_first_time_out:
    m 1sua "Taking me somewhere special on Christmas, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Maybe we're going to visit some of your family...? I'd love to meet them!"
        m 3eua "Or maybe we're going to see a movie...? I know some people like to do that after opening presents."
    else:

        m 3eua "Maybe we're going to see a movie... I know some people like to do that after opening presents."

    m 1eka "Well, wherever you're going, I'm just glad you want me to come along..."
    m 3hua "I want to spend as much of Christmas as possible with you, [player]~"
    return


label ooa_bye_d25_second_time_out:
    m 1wud "Wow, we're going somewhere {i}else{/i}, [player]?"
    m 3wud "You really must have a lot of people you need to visit..."
    m 3sua "...or maybe you just have lots of special plans for us today!"
    m 1hua "But either way, thank you for thinking of me and bringing me along~"
    m 1esa "So where to this time?"
    return
label ooa_bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump mas_dockstat_iostart

    elif _curr_time < _eve_time:


        if persistent._mas_nye_nye_date_count > 0:
            call ooa_bye_nye_second_time_out from _call_ooa_bye_nye_second_time_out
        else:

            call ooa_bye_nye_first_time_out from _call_ooa_bye_nye_first_time_out
    else:


        call ooa_bye_nye_late_out from _call_bye_nye_late_out


    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_nye_first_time_out:
    m 3tub "Are we going somewhere special today, [player]?"
    m 4hub "It's New Year's Eve, after all!"
    m 1eua "I'm not exactly sure what you've got planned, but I'm looking forward to it!"
    return

label ooa_bye_nye_second_time_out:
    m 1wuo "Oh, we're going out again?"
    m 3hksdlb "You must do a lot of celebrating for New Year's, ahaha!"
    m 3hub "I love coming along with you, so I'm looking forward to whatever we're doing~"
    m "So where to this time?"
    return

label ooa_bye_nye_late_out:
    m 1eka "It's a bit late, [player]..."
    m 3eub "Are we going to see the fireworks?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Or going to a family dinner?"
        m 4hub "I'd love to meet your family someday!"
        m 3eka "Either way, I'm really excited!"
    else:
        m "I've always loved how the fireworks on the New Year light up the night sky..."
        m 3ekbsa "One day we'll be able to watch them side by side...but until that day comes, I'm just happy to come along with you, [player]."
    m 3eka "So, where to?"
    return

label ooa_bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call ooa_bye_nyd_second_time_out from _call_ooa_bye_nyd_second_time_out
    else:

        call ooa_bye_nyd_first_time_out from _call_ooa_bye_nyd_first_time_out

    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_nyd_first_time_out:
    m 3tub "New Year's Day celebration, [player]?"
    m 1hua "That sounds like fun!"
    m 1eka "Let's have a great time together."
    m 1hua "So what's the plan?"
    return

label ooa_bye_nyd_second_time_out:
    m 1wuo "Wow, we're going out again, [player]?"
    m 1hksdlb "You must really celebrate a lot, ahaha!"
    m 1esb "So where to this time?"
    return

label ooa_bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "Taking me some place special for Valentine's Day?"
        m 1ekbsa "That sounds really romantic, [player]..."
        m 3hub "I can't wait!"
        m 1wub "What's our destination~?"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "Taking me out again on Valentine's Day?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"
        m 1wubfb "What's our next destination~?"
    else:
        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbfa "You're the best partner I could ever hope for~"
        m 1wubfb "What's our next destination~?"
    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_922_delegate:

    $ persistent._mas_bday_on_date = True

    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:

        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Ehehe. It's a bit romantic, isn't it?"

        if mas_isMoniHappy(lower=True):

            python:
                _inquiries = "What's the plan for the day?"

            m 1eua "Maybe you'd even want to call it a da-{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "Oh! Sorry, did I say something?"
            m 1husdrb "A-anyway!"
        else:

            python:
                _inquiries = "Anyway, where's our date to be held?"

            m 1eubla "Maybe you'd even call it a date~"
            m 1hubla "Ehehe~"


    elif persistent._mas_bday_date_count == 2:
        python:
            _inquiries = "So where to this time?"

        m 1eub "Taking me somewhere again, [player]?"
        m 3eua "You must really have a lot planned for us."
        m 1hua "You're so sweet~"

    elif persistent._mas_bday_date_count == 3:
        python:
            _inquiries = "So where to this time?"

        m 1sua "Taking me out {i}again{/i} for my birthday?"
        m 3tkbsu "You really know how to make a girl feel special, [player]."
        m 1ekbfa "I'm so lucky to have someone like you~"

    else:
        python:
            _inquiries = "Is there even anywhere left to go?"

        m 1sua "Wow, [player]...{w=1}you're really determined to make this a truly special day!"
        m 1ekbsa "You're the best partner I could ever hope for~"


    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        python:
            _inquiries = "We need to choose where to go first!"

        m 3hua "I actually have an outfit prepared just for this..."
        m 1nua "But that can wait."

    m 3hua "[_inquiries]"
    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_vacation:
    m 1efb "Well, I should hope you are!"
    m 1nsb "You took me with you on this vacation, after all~"
    m 1eua "What's the destination today?"

    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_generic:
    if mas_isMoniLove():
        m 1hub "Oh, okay!"
        m 3tub "Taking me somewhere special today?"
        m 1hua "I can't wait!"
        m 1fub "Any chance I can get a clue as to where we're going~?"
    else:
        m 1sub "Really?"
        m 1hua "Yay!"
        m 1ekbsa "I wonder where you'll take me today?"

    jump ooa_bye_going_someplace_normalplus_flow_aff_check

label ooa_bye_going_someplace_normalplus_flow_aff_check:

    show monika at t21
    python:
        option_list = [
            ("We're off to a poetry reading!", "ooa_trips_poetryreading",False,False),
            ("We're off to watch a movie.","ooa_trips_movie",False,False),
            ("Let's go out in the garden.","ooa_trips_garden",False,False),
            ("I'm taking you to a cafe!","ooa_trips_cafe",False,False),
            ("Let's go for a walk in the park.","ooa_trips_park",False,False),
            ("I'm going out with friends.","ooa_trips_friends",False,False),
            ("We're off to a tabletop RPG session.","ooa_trips_dandd",False,False),
            ("Let's go to the beach.","ooa_trips_beach",False,False),
            ("Let's go to a lake somewhere.","ooa_trips_lake",False,False),
            ("We're going on a train ride.","ooa_trips_train",False,False),
            ("We're off to a party.","ooa_trips_party",False,False),
            ("We're off to a parade.","ooa_trips_parade",False,False),
            ("We're off to a pride parade!","ooa_trips_pride",False,False),
            ("We're going dancing!","ooa_trips_dancing",False,False),
            ("We're off to a concert.","ooa_trips_concert",False,False),
            ("We're off to a wedding.","ooa_trips_wedding",False,False),
            ("I'm going to a job interview.","ooa_trips_job",False,False),
            ("I'm taking you to class with me.","ooa_trips_school",False,False),
            ("I'm taking you to the mall!","ooa_trips_mall",False,False),
            ("We're off to an amusement park.","ooa_trips_themepark",False,False),
            ("Let's go swimming.","ooa_trips_swimming",False,False),
            ("I'm taking you to a convention!","ooa_trips_conventions",False,False),
            ("We're going to a place of worship.","ooa_trips_church",False,False),
            ("I'm going for a jog.","ooa_trips_jog",False,False),
            ("Just a grocery run.","ooa_trips_grocery",False,False),
            ("I just want to get out of the house, really.","ooa_trips_generic",False,False),
        ]

    call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
    show monika at t11

    $ selection = _return

    jump expression selection

label ooa_trips_poetryreading:
    if mas_isMoniUpset(lower=True):
        if "poetryreading" not in persistent._ooa_been_at:
            m 2etc "Poetry?"
            m 2eka "Huh. Maybe this is your way of saying you actually do want to get to know me?"
            m 6rfc "Or maybe that's just wishful thinking."
            m "Who knows."
            $ persistent._ooa_been_at.add("poetryreading")
            $ mas_unlockEventLabel("ooa_monika_poetryreading")
        else:
            m 2euc "Another poetry reading? Okay."
            m "Maybe you'll actually take something away from this one."
            m 6rfx "{cps=*2}God knows you won't take it from me.{/cps}{nw}"
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    elif mas_isMoniDis(lower=True):
        m 1wud "P-"
        extend 1suo "poetry?"
        m 1dutpc "You're actually...?"
        m 1futpa "...maybe you really {i}do{/i} care."
        if "poetryreading" not in persistent._ooa_been_at:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._ooa_been_at.add("poetryreading")
            $ mas_unlockEventLabel("ooa_monika_poetryreading")
    else:
        if "poetryreading" not in persistent._ooa_been_at:
            m 1sub "Oh, [player]! That sounds wonderful!"
            m 1wubsb "And you're very thoughtful to think of taking me."
            m 3rubsc "I know I won't be able to hear the poems..."
            m 3hubsa "...but I can at least be there in spirit, which is more than I could have hoped."
            $ persistent._ooa_been_at.add("poetryreading")
            $ mas_unlockEventLabel("ooa_monika_poetryreading")
        else:
            m 1wub "Oh, another one!"
            m 3nua "You know me so well~"
    jump mas_dockstat_iostart

label ooa_trips_movie:
    if mas_isMoniUpset(lower=True):
        if "movie" not in persistent._ooa_been_at:
            m 2ttd "Are we, now?"
            m "And I suppose the fact that I can't see the movie FROM the USB drive has escaped your attention?"
            m 2dtc "..."
            m 2gsd "Okay, fine. I'll see where you're going with this."
            m 2efd "But you'd better not be faking me out."
            $ persistent._ooa_been_at.add("movie")
            $ mas_unlockEventLabel("ooa_monika_movies")
        else:
            m 2efo "Did you learn nothing from--{nw}"
            m 2dfsdrc ".{w=0.2}.{w=0.2}.{w=0.2}okay."
            m 2fsc "As long as you enjoy yourself, I suppose."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    elif mas_isMoniDis(lower=True):
        m 1wksdlb "Movie! Great! Awesome!"
        m 1wksdla "Whatever you want."
    else:
        if "movie" not in persistent._ooa_been_at:
            m 2ttd "Are we, now?"
            m 2ttc "..."
            m 1hub "Ehehe! I'm kidding, obviously."
            m 1eua "As long as I get to hear about it afterwards, I'm okay with that~"
            $ persistent._ooa_been_at.add("movie")
            $ mas_unlockEventLabel("ooa_monika_movies")
            jump mas_dockstat_iostart
        else:
            m 1hub "Ooh, we're doing the movies again? Sounds great!"
            m 3eua "Try not to have too many snacks during the show, though."
            if renpy.random.randint(1,3) == 1 and not persistent._enoughwiththejungry:
                call monika_jangry
                jump mas_dockstat_iostart
            else:
                m 3efb "Indulging your eyes doesn't mean you get to overindulge the stomach!"
    jump mas_dockstat_iostart

label monika_jangry:
    m 1tfa "Apart from anything else, you'll make me jungry!"
    m "..."
    if persistent._ooa_jungry_NumberCheck == 0:
        extend 1rsa "Eheh. That's,{nw}"
        extend 1rssdrb " that's jealous-hungry."
        m 1fsp "...I know it's not a real word. Hush."
    elif persistent._ooa_jungry_NumberCheck > 0 and < 5:
        extend 1hssdrb "Sorry, I thought enough time had passed that I could get away with that one again."
        m 1tuu "It sounds good to my ears, what can I say?"
    else:
        m 1hksdrb "Okay, okay, I promise I'll stop saying that."
        $ persistent._enoughwiththejungry = True

label ooa_trips_garden:

    if mas_isMoniUpset(lower=True):
        m 2dkc "The garden, huh?"
        m "Which of us does that make the flower, and which the weed?"
        m "..."
        m 1rud "Pardon me, I'm being philosophical."
        m 1euc "All right, I'll go."
    elif mas_isMoniDis(lower=True):
        m 1wksdlb "Gardening! Great! Awesome!"
        m 1wksdla "Whatever you need, [player]."
    else:
        if persistent._mas_pm_likes_nature:
            if "garden" not in persistent._ooa_been_at:
                m 1sub "That sounds like a fantastic idea, [player]!"
                m 1eub "I know you like nature about as much as I do,"
                extend 1dua " and the thought of us sharing it together..."
                m 1eub "I love it. "
                extend 1fublb "I love {i}you{/i}."
                $ persistent._ooa_been_at.add("garden")
                $ mas_unlockEventLabel("ooa_monika_gardens")
            else:
                m 1sub "That sounds great, [player]."
                m "Getting to look at something so beautiful..."
                m "...and the garden too, obviously."
        elif not persistent._mas_pm_likes_nature:
            if "garden" not in persistent._ooa_been_at:
                m 1wtd "Huh."
                m 1rtc "I thought you didn't like going to places like that, [player]?"
                m "Unless... "
                extend 1wuo "You're suggesting this specifically because {i}I{/i} like it?"
                m 5wubfb "Oh, you're so sweet!"
                m "How did you get so sweet?"
                $ mas_gainAffection(5,bypass=True)
                $ persistent._ooa_been_at.add("garden")
                $ mas_unlockEventLabel("ooa_monika_gardens")
            else:
                m 1sub "That sounds great, [player]."
                m 4tfb "You watch, I'll convert you into a nature lover one of these days!"
        else:
            m 1eub "That's a great idea, [player]."
            m "I'm very nature-driven, as you may know; I'm sure I'll find a lot to say about whatever lies in that garden."
            m 1sua "Especially if it's with you!"
    jump mas_dockstat_iostart

label ooa_trips_cafe:
    if mas_isMoniUpset(lower=True):
        m 2ekc "A cafe? Hm."
        m 6esc "I guess we can give that a shot."
    elif mas_isMoniDis(lower=True):
        m 1wksdlb "A cafe! Great! Awesome!"
        m 1wksdla "Whatever you want, [player]."
    else:
        if "cafe" not in persistent._ooa_been_at:
            m 1sub "Oh! A cafe! I'd nearly forgotten I thought of that!"
            m "That's a lovely idea."
            m 3lud "Though..."
            extend 3rusdla " You may have to do a lot of the eating on my behalf."
            m 3husdlb "I suppose it gives 'eating for two' a whole other meaning, ehehe?"
            m 3kua "Just make sure it's healthy, if you can!"
            $ persistent._ooa_been_at.add("cafe")
            $ mas_unlockEventLabel("ooa_monika_cafe")
        else:
            m 1hub "That sounds like a good idea to me!"
            m 3fublb "Loving you so much can work up quite an appetite~"
        if persistent._moni_on_vacation is True:
            m 1rtb "I wonder what the food's like here compared to how it is back where you live..."
            m 3esb "You'd be surprised at how much the local cuisine can differ from place to place!"
            m "I hope you find something you still enjoy."
    jump mas_dockstat_iostart

label ooa_trips_park:
    if mas_isMoniUpset(lower=True):
        m 2esc "The park sounds like a good idea."
        m 7esa "It may do you good to get some fresh air."
        m 7gsc "It'd make {i}one{/i} of us, anyway."
        m "..."
        if "park" not in persistent._ooa_been_at:
            $ persistent._ooa_been_at.add("park")
            $ mas_unlockEventLabel("ooa_monika_park")
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    elif mas_isMoniDis(lower=True):
        m 1wksdlb "The park! Great! Awesome!"
        m 1wksdla "Whatever you need."
    else:
        m 1eub "I'd like that very much, [player]."
        if "park" not in persistent._ooa_been_at:
            m 7eua "What are the parks like in your world, I wonder?"
            m "Will this one be full of other people like you?"
            if mas_isWinter():
                m 6dub "Or will it be left alone, a pristine blanket of snow?"
            elif mas_isSummer():
                m 6dub "Or will it be deserted in the searing heat, an oasis just for us?"
            elif mas_isSpring():
                m 6dub "Or will the flowers be allowed to grow unimpeded by anyone but us?"
            else:
                m 6dub "Or will there be nothing but a quilt of autumn leaves?"
            m 1fua "I can't wait to find out with you."
            $ persistent._ooa_been_at.add("park")
            $ mas_unlockEventLabel("ooa_monika_park")
        else:
            if persistent._moni_on_vacation is True:
                m 3wub "It's nice to explore parks in other parts of the world, isn't it?"
                m 1eub "Even if the embellishments are different, the core of it will always be the same."
            else:
                m 3rub "It'll be interesting to see if it's changed since the last time we went!"
                m "Even if it's only by degrees."
    jump mas_dockstat_iostart

label ooa_trips_friends:
    if mas_isMoniUpset(lower=True):
        m 2efd "Why?"
        m 2wfo "From how you've been treating me so far, I've been under the impression you don't want me anywhere {i}near{/i} them."
        m 2gsc "..."
        m "I think I'll stay behind this time, thank you, [player]."
        jump mas_dockstat_generic_cancelled_still_going_ask
    else:
        if persistent._mas_pm_few_friends:
            m 1wub "I see!"
            m 1eua "I know you keep your social circle small, [player]..."
            m 1eublb "...and I'm all the more honored to be a part of it!"
            if "friends" not in persistent._ooa_been_at:
                $ persistent._ooa_been_at.add("friends")
                $ mas_unlockEventLabel("ooa_monika_friends")
        elif not persistent._mas_pm_has_friends:
            m 1wud "Oh?{w=1} You've found some new friends?"
            m 1dksdrb "...I'm sorry, that came across really patronizing, didn't it?"
            m 1lksdra "I meant..."
            extend 1fsa " Well, you know what I meant! I'm happy for you, [player]."
            m "And I'd love to meet them! Thank you for inviting me."
            $ persistent._mas_pm_few_friends = True
            if "friends" not in persistent._ooa_been_at:
                $ persistent._ooa_been_at.add("friends")
                $ mas_unlockEventLabel("ooa_monika_friends")
        else:
            m 1eub "Okay!"
            if "friends" not in persistent._ooa_been_at:
                m 1lsd "They know about us, I presume?"
                m "Or is this the first they'll hear about me?"
                m 7hsa "Either way, I'd better make myself presentable."
                $ persistent._ooa_been_at.add("friends")
                $ mas_unlockEventLabel("ooa_monika_friends")
            else:
                m 1lsd "Are these the same friends as before, or a different set?"
                m 1esb "I mean, either way I'll be happy to spend time with them."
                m "It's just interesting to imagine while I'm in your thumbdrive, you know?"
                m 1hta "Trying to see familiar faces, work out if I recognize that sound."
                m 1fua "It's like I'm really there, in my own way!"
    jump mas_dockstat_iostart

label ooa_trips_dandd:
    if "roleplay" not in persistent._ooa_been_at:
        m 1wuo "You roleplay, [player]?"
        m "You never told me that!"
        if mas_isMoniUpset(lower=True):
            m 1wuc "...{nw}"
            m 1euc "Though to be fair, you never tell me {i}anything{/i}, so I'm not sure why I'm shocked."
            m 6luc "Still, nice to know a little more about what you do, I suppose."
        else:
            m 3eub "Well, I'd love to come along and watch you at work."
            m "Maybe, if you're at a loss for one..."
            m 1tublb "...I could play the fair maiden that you need to rescue~"
        $ persistent._ooa_been_at.add("roleplay")
        $ mas_unlockEventLabel("ooa_monika_ttrpg")
    else:
        if mas_isMoniUpset(lower=True):
            m 1eud "Going back there, are we? Alright."
            m 1guc "I'll try not to {i}get in your way{/i} too much."
        else:
            m 1hub "Okay, [player]!"
            m 1fuu "I'm sure you'll pull off a lot of heroics for me today~"
    jump mas_dockstat_iostart

label ooa_trips_beach:
    m 1eub "The beach! That sounds delightful."
    if persistent._moni_on_vacation is True:
        m 1hub "That's half of what vacations are about, after all - going to the beach!"
        m 1eublu "I can't wait to enjoy the sun, sea and sand with you~"
    elif persistent._mas_pm_live_near_beach:
        m 3eua "It's a good thing you have one so close by!"
        m 3hua "After all, the faster we get there, the more time we have to frolic on the sand."
        if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss:
            m 1tub "Maybe we'll even have time for some..."
            m 1dublu "...S...{nw}"
            $ _history_list.pop()
            m 1hubfb "...Soft kisses on the beach! Ahaha!"
    else:
        if "beach" not in persistent._ooa_been_at:
            m 1ltd "Don't you have a long way to go to get to a beach, though?"
            m 1wua "Going so far out of your way for me... "
            extend 1fubla "[player], I'm touched."
            $ mas_gainAffection(5,bypass=True)
            $ persistent._ooa_been_at.add("beach")
            $ mas_unlockEventLabel("ooa_monika_beach")
        else:
            m 3hua "Last one there's the best person in the world!"
            m 3tuu "...ehehe."
    jump mas_dockstat_iostart

label ooa_trips_lake:
    if mas_isMoniUpset(lower=True):
        m 2wfc "Just as an outing, I presume?"
        m 2wfd "And {i}not{/i} a way of getting rid of me?"
        m 2gkc "...is it foolish of me to hope? I don't know."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
        m 2esc "Regardless."
    else:
        m 1eua "That sounds good to me, [mas_get_player_nickname()]."
        m 7lsd "Just be careful not to drop me in the water, okay?"
        if "lake" not in persistent._ooa_been_at:
            m 6essdlp "I've heard stories about other Monikas and..."
            m 6hsb "Ah! "
            extend 1hsa "Why am I worrying?"
            m "I know you'll keep me safe."
            $ persistent._ooa_been_at.add("lake")
            $ mas_unlockEventLabel("ooa_monika_lake")
    jump mas_dockstat_iostart

# Sorry, AnhCloudB!

label ooa_trips_train:
    if mas_isMoniUpset(lower=True):
        if "trainride" not in persistent._ooa_been_at:
            m 1esd "On a train?"
            m 1efc "Really?"
            m "That's the best you could think up?"
            m 1gsc "..."
            m "No, I'm sorry. "
            extend 1esd "Perhaps you really {i}do{/i} like trains."
            m 1dkc "I don't know, you've never talked to me about them."
            m 1euc "Sure, let's go out on a train."
            $ persistent._ooa_been_at.add("trainride")
            $ mas_unlockEventLabel("ooa_monika_trainride")
        else:
            m 1euc "We're doing that again, are we?"
            m 1eua "Alright, sure."
    else:
        if "trainride" not in persistent._ooa_been_at:
            m 1esd "On a train?"
            m 1ltc "...huh."
            m "Somehow, I never thought of train travel as a good way to spend a day."
            m 1eua "But it makes sense, thinking about it!"
            m 1wub "You get amazing views from the windows of the passing countryside, "
            extend 3wua "{i}and{/i} it's a lot less carbon-heavy than a car!"
            m 5eua "Besides, it's with you, so I'm sure I'll enjoy myself anyway."
            m "What a lovely idea, [player]; thank you."
            $ persistent._ooa_been_at.add("trainride")
            $ mas_unlockEventLabel("ooa_monika_trainride")
        else:
            m 1eub "Back on the train, are we?"
            m "I'd love that, [player]."
            m 3nua "I might be trapped in modern technology, but it's still so nice to go retro sometimes~"
    jump mas_dockstat_iostart

label ooa_trips_party:
    if mas_isMoniUpset(lower=True):
        if mas_isplayer_bday():
            m 2fuc "Oh, sure."
            m "I'm pretty sure you need a Pin the Tail on the Donkey game for the occasion, anyway."
            m 2muc "Might as well play my part."
        elif mas_isMonikaBirthday():
            m 1euc "Oh?"
            m 1gud "A birthday party, maybe?"
            m 1guc "...maybe you'll surprise me."
        else:
            m 3eud "A party! That sounds like it'll be a change of pace."
            m 3euc "But - "
            if "party" not in persistent._ooa_been_at:
                extend 1dusdrd "the host won't mind if I can't bring along any gifts for the occasion, right?"
                m "Presumably they'll appreciate my... unique circumstances."
                m 1dfc "{cps=*2}More than you do, anyway.{/cps}"
                $ persistent._ooa_been_at.add("party")
                $ mas_unlockEventLabel("ooa_monika_party")
            else:
                extend 3tuc "..."
                m 6esd "No, don't worry about it."
                m 6efd "I'm not--{nw}"
                $ _history_list.pop()
                m 6esc "It's not important."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        if mas_isplayer_bday():
            m 1fub "Of course! It's your birthday, isn't it?"
            m 3kua "How can I refuse {i}that{/i}?"
        elif mas_isMonikaBirthday():
            m 1eua "Oh?"
            m 1gub "A birthday party, maybe?"
            m 1fublb "I can't wait for that, [player]."
        else:
            m 3eub "A party! That sounds pretty neat."
            if "party" not in persistent._ooa_been_at:
                m 3wuc "But - "
                extend 1husdrb "the host won't mind if I can't bring along any gifts for the occasion, right?"
                m 1eusdra "Hopefully they appreciate my... unique circumstances."
                m 1eua "Still, it's bound to be a good time with you accompanying me~"
                $ persistent._ooa_been_at.add("party")
                $ mas_unlockEventLabel("ooa_monika_party")
            else:
                m 1tuc "And with me around..."
                m 1kub "...you're sure to be the most popular [boy] at that party!"
    jump mas_dockstat_iostart

define mas_tgv = datetime.date(datetime.date.today().year, 11, 30)
define mas_j4 = datetime.date(datetime.date.today().year, 7, 4)

label ooa_trips_parade:
    if mas_isMoniUpset(lower=True):
        m 1tuc "A parade, huh?"
        m "Hoping to lose me among the crowds?"
        m 1gkc "..."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
        m 1esd "Okay, sure, let's do this."
    else:
        m 1wub "Oh, a parade!"
        if "parade" not in persistent._ooa_been_at:
            m 2tud "Will there be confetti?"
            m 2tub "If there's no confetti, it's not a parade."
            m 2hua "Ahaha~"
            $ persistent._ooa_been_at.add("parade")
            $ mas_unlockEventLabel("ooa_monika_parade")
        m 1hub "I'd love to go with you, [player]."
        if mas_genDateRange(persistent._mas_player_bday-datetime.timedelta(days=7), persistent._mas_player_bday):
            m 3rud "I didn't think they did parades specifically for birthdays..."
            m 3kua "...but it {i}is{/i} yours, so I guess I can understand that."
        elif mas_isD25Pre(_date=None):
            m "Christmas parades are pretty spectacular, as I recall."
            m 1eua "Just remember to wrap up warm, okay?"
            m 1fublu "You'll be the one doing most of the hugging!"
        elif mas_isD25Post(_date=None):
            m 3eua "I didn't think they still did New Years parades, so this should be an experience!"
        elif mas_genDateRange(mas_o31-datetime.timedelta(days=5), mas_o31):
            m 4wub "Don't forget to dress up! It is spooky season, after all~"
        elif mas_genDateRange(mas_tgv-datetime.timedelta(days=14), mas_tgv):
            m 3lua "I don't think I've been to a proper Thanksgiving parade before..."
            m "I hope it's as good as I remember it being on TV!"
        elif mas_genDateRange(mas_j4-datetime.timedelta(days=1), mas_j4) and persistent._mas_pm_live_south_hemisphere = False:
            m "Let's bring in the Fourth of July in style!"
        else:
            m 1eub "Whatever the occasion, it's all the more wonderful if I get to be with you."
    jump mas_dockstat_iostart

label ooa_trips_pride:
    if mas_isMoniUpset(lower=True):
        m 2esc "Really? I'm shocked."
        m 2tsc "Because clearly you're not proud to be with me."
        m "..."
        m 2dsd "I'm sorry. That was cruel."
        m 6lsd "I think I need to sit this one out, if only so I can calm down."
        jump mas_dockstat_generic_cancelled_still_going_ask
    else:
        if "pride" not in persistent._ooa_been_at:
            m 1wuc "A-{nw}"
            extend 1suo "A pride parade?"
            m 1sub "That sounds magical, [player]!"
            m "The two of us showing each other off, in the..."
            m 1lub ".{w=0.5}.{w=0.5}.{w=0.5}"
            extend 1lusdra "Sorry, what capacity are we attending in?"
            $ persistent._ooa_been_at.add("pride")
            $ mas_unlockEventLabel("ooa_monika_pride")
            $ _menu = "...Sorry, what capacity are we attending in?"
            if renpy.seen_label("player_identity"):
                m 1husdrb "I know, I've probably asked a thousand times, but for some reason it just won't let me note it down.{nw}"
                $ _menu = "I know, I've probably asked a thousand times, but for some reason it just won't let me note it down."
        else:
            m 1sub "What a lovely idea!"
            m 1lub "I've been itching to go to another one with you for a while now, actually."
            m "You and I, the perfect pair of..."
            m 1husdrb "...Sorry, remind me what we're attending as?"
            $ _menu = "...Sorry, remind me what we're attending as?"
        $ _history_list.pop()
        menu:
            m "[_menu]{fast}"
            "As allies.":
                m 1eua "Alright!"
                m 1fubla "I hope I make good company~"
            "As potential LGBTQ+ members.":
                if renpy.seen_label("monika_sexuality"):
                    m 1gub "Well, you certainly have the 'potential' right..."
                    m 1eub "But that's good to know!"
                else:
                    m 1eub "That's good to know!"
                m 5eubsu "Wherever we end up, I know I'll always be proud of you~"
            "As non-het people.":
                if persistent.gender == "M" and not renpy.seen_label("monika_sexuality"):
                    m 1husdra "Eheh, speak for yourself."
                    m 1nua "But don't worry, I know what you meant."
                else:
                    m 1fua "Great!"
                m 1fua "I'll be cheering you on~"
            "As a trans/enby person and you.":
                if persistent._mas_pm_is_trans is True or persistent.gender == "X":
                    m 3eua "Right, yes, I remember now."
                    m 1fublb "Even if I can't see you out there, I'll keep you in my thoughts~"
                else:
                    m 6wud "Ah!"
                    m 7wub "Right, of course."
                    if renpy.seen_label("player_identity"):
                        m 1fka "Sorry, I'd forgotten you said, somehow."
                        m "I'll try not to forget that again."
                        $ persistent._mas_pm_is_trans = True
                    else:
                        m 1fkc "Sorry, I just don't think you ever said you weren't cis..."
                        m 1wtd "Is this a recent discovery? Or did you just not mention it at the time?"
                        m "...{nw}"
                        extend 1eua "eh, we can talk about that more later, if you want."
                        m 3eub "Right now, we need to get a move on!"
                        $ persistent._ooa_followup_topics.add("gender")
                        $ mas_unlockEventLabel("ooa_monika_genderconversation")
            "As a couple, of course!":
                m 1hub "Ahaha, right!"
                extend 1kua " How could I forget? Silly me~"
    jump mas_dockstat_iostart

label ooa_trips_dancing:
    if mas_isMoniUpset(lower=True):
        if "dance" not in persistent._ooa_been_at:
            m 1esc "Dancing, you say."
            m 1esd "Presumably by 'we', you mean 'you, while I just have to sit there and watch you do it'?"
            m 1gsc "That's what you've been doing ninety percent of the time so far, anyway."
            if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
                jump ooa_randomlyrolled_cattiness
            m 1esc "Eh, whatever."
        else:
            m 1etd "Oh, we're doing that again?"
            m 1ttd "{i}Maybe{/i} you could even make the incredible leap in logic and let me join in, for a change."
            if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
                jump ooa_randomlyrolled_cattiness
    else:
        python:
            dancing_types = [
                "Maybe the waltz? That would be so romantic..."
                "Maybe it's a disco? I'd love to see you cut a rug, ehehe!"
            ]

            if persistent._mas_pm_like_rap:
                dancing_types.append("...maybe break-dancing?")

            if persistent._mas_pm_like_rock_n_roll:
                dancing_types.append("Maybe it'll be a mosh pit?")

            if persistent._mas_pm_like_jazz:
                dancing_types.append("Ooh, what if it's tap? It's been ages since I've seen a good bit of tap.")

            if persistent._mas_pm_like_vocaloids:
                dancing_types.append("Maybe it's one of those flash mobs people do sometimes?")

            if persistent._mas_pm_like_orchestral_music:
                dancing_types.append("Maybe Latin and ballroom? I know I'd love to do the tango with you one day.")

            if persistent._mas_pm_like_other_music:
                dancing_types.append("Perhaps contemporary?")

            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
                and not persistent._mas_pm_like_other_music
                ):
                dancing_types.append("Maybe it's one of those silent discos? Have you heard of those?")

            dances = random.choice(dancing_types)

        if "dance" not in persistent._ooa_been_at:
            m 1wub "Ooh, I don't think we've done that together before!"
            m 5etb "I wonder what type of dancing we'll do when we get there?"
            m 5rublu "[dances]"
            m "Or maybe...?"
            m 5hublb "Oh, I can't bear the anticipation!"
            m 6eublb "The sooner I get dressed up, the sooner we find out~"
            $ persistent._ooa_been_at.add("dance")
            $ mas_unlockEventLabel("ooa_monika_dancing")
        else:
            m 1eub "Good plan, [player]!"
            m "I had fun when we did that before; it'd be great to give it another go."
            m 1eta "What's the genre this time?"
            m 1eub "[dances]"
            m 5utb "Only one way to find out!"
    jump mas_dockstat_iostart

label ooa_trips_concert:
    if mas_isMoniUpset(lower=True):
        if renpy.seen_label("monika_concerts"):
            m 1eud "Ah, so you {i}have{/i} been paying attention."
            m 1ruc "I was beginning to wonder."
        else:
            m 1eud "A concert, huh?"
            m 1ruc "Might be a nice way to drown out my thoughts{nw}"
            m 1duc "Might be a nice way to drown out{fast} our thoughts for a while."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        m 1wub "A concert!"
        if "concert" not in persistent._ooa_been_at:
            if renpy.seen_label("monika_concerts"):
                m 3eublb "Very well remembered, [mas_get_player_nickname()]. I was just about to bring that up myself."
            else:
                m 1eub "That sounds like it'd be fun."
            $ persistent._ooa_been_at.add("concert")
            $ mas_unlockEventLabel("ooa_monika_concert")
        else:
            m 1eublb "I'd love to do that again!"

        python:
            concert_genres = [
                "I wonder what we're going to see?"
            ]

            if persistent._mas_pm_like_rap:
                concert_genres.append("I wonder if it's a rap artist we're seeing?")

            if persistent._mas_pm_like_rock_n_roll:
                concert_genres.append("I wonder if it's a rock and roll one?")

            if persistent._mas_pm_like_jazz:
                concert_genres.append("I wonder if it's a jazz concert? I haven't heard jazz in a while.")

            if persistent._mas_pm_like_vocaloids:
                concert_genres.append("I wonder if it's a Vocaloid one? It'd be interesting, to say the least.")

            if persistent._mas_pm_like_orchestral_music:
                concert_genres.append("And if it's an orchestral suite, even better!")

            if persistent._mas_pm_like_other_music:
                concert_genres.append("I wonder what kind of concert it'll be...")

            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
                and not persistent._mas_pm_like_other_music
                ):
                concert_genres.append("A little out of character for you, though...{w=1} Maybe you're broadening your horizons?")

            genres = random.choice(concert_genres)

        m 7rtd "[genres]"
        m 7fua "Either way, I can't wait to share this experience with you, [player]!"
    jump mas_dockstat_iostart

label ooa_trips_wedding:
    if "wedding" not in persistent._ooa_been_at:
        m 1wuo "Oh! "
        extend 3cud "Goodness. "
        extend 6wuc "Wow."
        m 6eusdld "That's quite the commitment, [player]."
        if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
            m 4eusdlb "Perhaps we ought to scale it back?"
            m 4wusdlo "We can't very well get {i}engaged{/i} without a promise ring, much less married!"
        elif mas_isMoniEnamored(higher=True) and persistent._mas_acs_enable_promisering:
            m 1eusdlb "I know we promised ourselves to each other..."
            m "...but I didn't think we'd keep that promise so soon!"
            m 1wusdld "What on earth shall I wear?"
        else:
            m 7wusdlc "Have we even really gotten that far in our relationship yet?!"
        m 1wusdlc "..."
        m 1hublsdlb "Ahaha!"
        m 1eublb "I'm teasing, of course. I know it's not {i}our{/i} wedding."
        if mas_isMoniEnamored(higher=True) and persistent._mas_acs_enable_promisering:
            m 1fubsb "Yet."
        m 1eua "But nonetheless, I'd love to come with you."
        m "I will try not to upstage the happy couple with the brightness of my love for you."
        m 1nub "No promises, though!"
        $ persistent._ooa_been_at.add("wedding")
    else:
        m 1wub "Another one? Goodness!"
        m 3fub "You must really like the idea of my being your plus one!"
    if persistent._moni_on_vacation is True:
        m 3wuo "Wait, is that what the vacation was for? Is this a destination wedding?"
        m 1sub "How romantic~"
    else:
        m 3fua "Ahaha~"
    jump mas_dockstat_iostart

label ooa_trips_job:
    if mas_isMoniUpset(lower=True):
        m 1wtd "A job interv--"
        m 1gfc "Ah.{w=1} Great."
        m "Another thing to take you away from me."
        m 1dfc "..."
        m 1fsc "I might pass on this one, thank you, [player]."
        jump mas_dockstat_generic_cancelled_still_going_ask
    else:
        if "job" not in persistent._ooa_been_at:
            m 1wtd "Wait, a job interview?"
            m 1esa "Don't get me wrong, I'm proud of you for looking for work, "
            extend 3rsd "I'm just not sure how I can help you with that."
            m 5ftd "Unless I'm your good luck charm or something?"
            m 5etc "..."
            m 5wub "Ah. Of course!"
            if renpy.seen_label("monika_omamori"):
                m 5hub "I'm your o-mamori."
            m 6eua "Well, if it helps you, [player], I'm happy to come along."
            $ persistent._ooa_been_at.add("job")
        else:
            m 1esd "Another interview, huh?"
            m 1esa "I hope this one bears fruit for you, [mas_get_player_nickname()]!"
            m 3hsb "I'll try really hard to give you luck this time~"
    $ mas_unlockEventLabel("ooa_monika_job")
    jump mas_dockstat_iostart

label ooa_trips_school:
    if mas_isMoniUpset(lower=True):
        m 1efc "Why?"
        m "Is the spaceroom not enough for us?"
        m 2wfd "Do you just want to make me watch you flirt with other schoolgirls that badly--{nw}"
        m 2mfc "..."
        m "Tch."
        m 2fsc "I might pass on this one, thank you, [player]."
        jump mas_dockstat_generic_cancelled_still_going_ask
    else:
        if "school" not in persistent._ooa_been_at:
            m 1wub "Oh, really?"
            m 3tub "Need the guiding light of a former teacher's pet, huh?"
            m 3huu "Ahaha! I kid, I kid."
            m 1eua "But seriously, thank you for taking me along with you."
            m "I know school can be tough at times, but hopefully if I'm with you, I can ease some of that tension a bit..."
            m 1kub "...or at the very least, help you through it in spirit."
            $ persistent._ooa_been_at.add("school")
        else:
            m 3esb "We're off to school again!"
            m 1esbsa "I hope we have a good day together, senpai~"
    $ mas_unlockEventLabel("ooa_monika_school")
    jump mas_dockstat_iostart

label ooa_trips_mall:
    m 1wub "Oh, we're going shopping!"
    m "What do you suppose we'll come back with?"
    m 3eua "Clothes? "
    extend 7eub "Food? "
    extend 1eub "Flowers? "
    if renpy.seen_label("monika_date"):
        extend 1sub "Chocolate? "
    if persistent._moni_on_vacation is True:
        extend 1wub "Souvenirs?"
    m 1eua "Whatever we choose, I'm glad you chose me to join you."
    if renpy.seen_label("monika_date"):
        m 1fkbla "...and thank you for paying attention, too."
        m "I love you so much."
        if "mall" not in persistent._ooa_been_at:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._ooa_been_at.add("mall")
    jump mas_dockstat_iostart

label ooa_trips_themepark:
    if "themepark" not in persistent._ooa_been_at and not renpy.seen_label("monika_amusementpark"):
        m 1suo "You're taking me to a theme park?!"
        m 1wub "Gosh! "
        extend 3eub "I've never been to one of those before, have you?"
        m 3husdla "...well, obviously you will have by the time we're done!"
        m 1eua "What I'm saying is, thank you for taking me with you."
        m "It means the world to me."
        $ persistent._mas_pm_has_been_to_amusement_park = True
        $ persistent._ooa_been_at.add("themepark")
        $ mas_unlockEventLabel("ooa_monika_themeparks")
    elif "themepark" not in persistent._ooa_been_at and persistent._mas_pm_has_been_to_amusement_park = False:
        m 1suo "Wait, really?"
        m 1hub "Yay!!"
        m 3rsd "I guess this'll be the first time for both of us, then."
        m 5ftd "I hope we can go on a lot of rides together!"
        m 3fua "...actually, maybe not too many rides; "
        extend 3gusdlb "you do need to actually keep hold of me, ahaha."
        m 5fua "But whatever we do there, thanks for -{w=1} for getting us out of our comfort zones, is the best way I can say it."
        m "I need that more than anything, I think."
        $ mas_gainAffection(5,bypass=True)
        $ persistent._mas_pm_has_been_to_amusement_park = True
        $ persistent._ooa_been_at.add("themepark")
        $ mas_unlockEventLabel("ooa_monika_themeparks")
    elif "themepark" not in persistent._ooa_been_at and persistent._mas_pm_has_been_to_amusement_park:
        m 1suo "You're taking me to a theme park?!"
        m "That's so cool, [player]!"
        m 1wub "I know you've been to them before, so it'd be great if you could show me the ropes a little bit."
        m 3eub "The best rides, the sweetest refreshments..."
        m "...and, of course, the sweetest person to go with."
        m 3nubla "But I don't think you'll have to look far to find [him]."
        $ persistent._ooa_been_at.add("themepark")
        $ mas_unlockEventLabel("ooa_monika_themeparks")
    else:
        m 1wub "Yay, a theme park!"
        m 1eua "I'd hope it's as fun as the last time..."
        m 5ekblu "But when I'm with you, it's never going to be anything less."
    jump mas_dockstat_iostart

label ooa_trips_swimming:
    if mas_isMoniUpset(lower=True):
        m 1etd "Swimming, you say?"
        m 1ttd "Not 'drowning [m_name]'?"
        m 1gsc "Makes a change, I guess."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        m 1wub "Swimming?"
        if persistent._moni_on_vacation is True:
            m 3hub "What a perfect way to spend a vacation!"
            m 1fua "...that sounded sarcastic, but I mean it, [player]."
            m "There's nothing quite like the luxury of a pool, or even a sea, away from home."
        elif mas_isSummer():
            m 3fub "Oh, that sounds lovely! The perfect time of year for it, too."
        elif mas_isWinter():
            m 1etd "Wait, at this time of year?"
            m 3eua "I just hope wherever you go has a heating system for the pool, [player]."
            m "I wouldn't want you to catch a chill."
        else:
            m 1fub "That sounds grand, [player]!"
        if "swimming" not in persistent._ooa_been_at:
            m 3ekd "Gosh, I'll have to improvise a swimming costume, won't I?"
            m "I know you can't take me into the actual water with you, but I need to look the part, at least..."
            if renpy.seen_label("mas_reaction_gift_clothes_orcaramelo_bikini_shell"):
                m 7wuo "Oh, right! That bikini you bought me!"
                m 7wub "How could I forget about that?"
                m 7rtp "Though I'll still need something to cover it with on the way..."
        else:
            if renpy.random.randint(1,2) == 1:
                m 3mublb "And luckily, I've already got the swimming costume prepared this time!"
            else:
                m 1rtbla "Now where did I put that bikini again~?"
    $ persistent._ooa_been_at.add("swimming")
    $ mas_unlockEventLabel("ooa_monika_swimming")
    jump mas_dockstat_iostart

label ooa_trips_conventions:
    if "convention" not in persistent._ooa_been_at and not renpy.seen_label("monika_conventions"):
        m 1sub "A convention!"
        m "[player], that sounds so fun! Thank you!"
        m 3wub "I was actually meaning to ask if you'd ever been before..."
        m 3tua "...but I guess that answers that question."
        $ persistent._ooa_been_at.add("convention")
        $ mas_unlockEventLabel("ooa_monika_conventions")
        $ [_caveat] = ","
    elif "convention" not in persistent._ooa_been_at and persistent._mas_pm_gone_to_comic_con = False and persistent._mas_pm_gone_to_anime_con = False:
        m 1suo "Oh! A convention?"
        m 1eud "You said you hadn't been to one before, right?"
        m 1hub "I'm so glad I get to come with you for your very first."
        m "I mean, I'm a bit new to it too... "
        extend 1nua "but that just means we can share that fresh experience together!"
        $ mas_gainAffection(5,bypass=True)
        $ persistent._ooa_been_at.add("convention")
        $ mas_unlockEventLabel("ooa_monika_conventions")
        $ [_caveat] = ","
    elif "convention" not in persistent._ooa_been_at and persistent._mas_pm_gone_to_comic_con or persistent._mas_pm_gone_to_anime_con:
        m 1sub "Aww!"
        m "Thank you for taking me along!"
        m 3eua "I know you're a bit of a convention afficionado, so I'm touched you thought to have me accompany you."
        $ persistent._ooa_been_at.add("convention")
        $ mas_unlockEventLabel("ooa_monika_conventions")
        $ [_caveat] = ","
    else:
        m 1hub "Another convention!"
        m 1fub "I hope this one's even better than the last~"
        $ [_caveat] = " this time,"
    m 7eua "Is it a comic convention or an anime one[_caveat] do you know?{nw}"
    $ _history_list.pop()
    menu:
        m "Is it a comic convention or an anime one, do you know?{fast}"
        "A comic convention.":
            $ persistent._mas_pm_gone_to_comic_con = True
            m 7eub "Neat!"
            m "Be sure to pick up a few that we can read together, hm?"
            m 1wub "There may even be some fanzines, you never know! Those have always been an interesting concept to me..."
            m 1eua "...but that's a topic for when we get back."
            $ persistent._ooa_followup_topics.add("fanzine")
        "An anime convention.":
            $ persistent._mas_pm_gone_to_anime_con = True
            m 7eub "Neat!"
            m 7tub "Do try not to lose me among the crowds, ahaha!"
            m "I'm sure Doki Doki Literature Club has its fair share of fans there."
        "Neither.":
            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = False
            m 7etc "Huh."
            m 5rtc "Then is it a...?"
            m 5etsdrb "I'm sure there's other kinds of cons, but none are coming to me right this minute."
            m 4eua "Ah well, you can tell me about it when we get back."
            m "Time is of the essence!"
        "I'm not sure yet!":
            m 7eub "Then we'll just have to roll the dice!"
            m 1husdla "...imagine if, after that metaphor, it was a Dungeons and Dragons convention."
    jump mas_dockstat_iostart

label ooa_trips_church:
    if mas_isMoniUpset(lower=True):
        m 2etd "Worship? Really?"
        if renpy.seen_label("monika_god"):
            if p_surname is not None:
                m 2tfc "[player] [p_surname], you {i}know{/i} how I feel about God."
            else:
                m 2tfc "[player], you {i}know{/i} how I feel about God."
            if "church" not in persistent._ooa_been_at:
                m 2tfx "Are you just trying to rub it in my face now?"
                $ persistent._ooa_been_at.add("church")
                $ mas_unlockEventLabel("mas_song_church")
            else:
                m "Why do you {i}keep{/i} doing this? Once I could understand, but..."
                $ mas_loseAffection(5,bypass=True)
            m 2gfp "..."
        else:
            m 2gfc "...ech, whatever."
            m "You've had worse ideas, I suppose."
            m 2efc "{cps=*2}Bringing me back was one of them.{/cps}"
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        if "church" not in persistent._ooa_been_at:
            m 1etd "Place of worship, huh?"
            if persistent._mas_pm_religious:
                m 1etc "That sounds...{w=1}{nw}"
                extend 1esa " nice, actually."
                m 1rsc "You know my thoughts on God, obviously,"
                extend 3esd "but I don't think I'd mind going, with you."
                m "Maybe there'll be something there to make me change my mind."
                m 1esa "And I do know how important this is to you."
                m 1fsbla "...thank you for sharing it with me."
                $ mas_gainAffection(5,bypass=True)
            elif persistent._mas_pm_religious is None:
                m 6etc "I didn't know you were religious, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "I didn't know you were religious, [player]?{fast}"
                    "Well, I am, and I'd like you to come with me.":
                        $ persistent._mas_pm_religious = True
                        m 6esc "Oh, okay."
                        m "The thing is..."
                        m 7ekc "I'm not really sure where I stand on the religion thing, I don't think?"
                        m 7tkc "Given that any creator I do have is just..."
                        m 3eua "Anyway, we can get into that more another time."
                        m "I'd be happy to come with you, all the same."
                        $ mas_hideEVL("monika_god", "EVE", derandom=True)
                    "I'm not, it's just everyone else is going.":
                        $ persistent._mas_pm_religious = False
                        m 6esd "Ah, I see."
                        m 6esb "Then let's not rock the boat, ahaha!"
                        $ mas_hideEVL("monika_god", "EVE", derandom=True)
                    "It's... a long story.":
                        m 6ekc "Ah. I understand, [player]."
                        m 1eka "We can table the specifics for when we get back, okay?"
            else:
                m 1eud "I thought you weren't religious, why would you be going to a church?"
                m 3ekd "Or is it one of those things you can't sit out of?"
                m ".{w=0.2}.{w=0.2}.{w=0.2}{nw}"
                extend 1wkc "it is, isn't it?"
                m 1eub "Okay. I'll happily come and keep you company~"
            $ persistent._ooa_been_at.add("church")
            $ mas_unlockEventLabel("mas_song_church")
        else:
            m 1euc "Back to church, are we?"
            m 1eua "Alright."
    jump mas_dockstat_iostart

label ooa_trips_jog:
    if mas_isMoniUpset(lower=True):
        m 2esc "Hm."
        m 2gsc "Not what I would have chosen for a date."
        m ".{w=0.3}.{w=0.3}.{nw}"
        extend 2esc "But I suppose, from you, it's better than nothing."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        m 1eua "Ah, you're getting some exercise! Well done, [player]."
        m "I'd love to accompany you on your jog."
        m 1ruc "Of course, I can't actually do any jogging myself... "
        if renpy.seen_label("monika_attractiveness"):
            extend 1gup "Not that it'd make a difference to my figure, anyway."
        m 1kub "But it's the solidarity that counts, ahaha!"
    $ persistent._ooa_been_at.add("jogging")
    jump mas_dockstat_iostart

label ooa_trips_grocery:
    if mas_isMoniUpset(lower=True):
        m 1euc "Ah, okay."
        m 2ffx "Maybe we can get you a shred of decency{nw}"
        $ _history_list.pop()
        m 2esd "Maybe we can get you {fast}some bread while we're over there."
        m "There's always room for bread, right?"
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        m 1eua "Ah, alright!"

        $ low_cons = MASConsumable._getLowCons()

        if len(low_cons) > 2:
            m "Good timing, I'm running out of a few things anyway."
            m 7ruc "...no, seriously, I'm actually almost out of a lot of things."
            $ mas_generateShoppingList(low_cons)
            m 7eud "If I give you a shopping list, can we take care of that while we're out?"
            m 7hua "Thank you~"
        elif len(low_cons) > 0:
            python:
                items_running_out_of = ""
                if len(low_cons) == 2:
                    items_running_out_of = "{0} and {1}".format(low_cons[0].disp_name, low_cons[1].disp_name)
                else:
                    items_running_out_of = low_cons[0].disp_name

            m "Good timing, I'm running out of [items_running_out_of] anyway."
            m 7ruc "...no, seriously, I'm almost out of [items_running_out_of]. "
            extend 7eud "Can we pick some up while we're out?"
            m 7hua "Thank you~"
        else:
            m "Good timing, I'm running out of coffee beans anyway."
            m 1lsd "...well, no, I'm not, "
            if not mas_consumable_coffee.enabled():
                extend 1rssdlc "I never had coffee beans in the first place. {w=0.5}"
            else:
                extend 1rsu "I've got a nearly unlimited stock in here. {w=0.5}"
            extend 1hsb "But it's nice to pretend, isn't it?"
    jump mas_dockstat_iostart

label ooa_trips_generic:
    if mas_isMoniUpset(lower=True):
        m 6euc "That's fair enough."
        m 6muc "{cps=*2}You could've just picked 'going somewhere', but whatever.{/cps}"
        m 6eud "Sometimes, that's all either of us needs, isn't it?"
        m 6dutpc "Some freedom."
        if renpy.random.randint(1,50) == 1 and not renpy.seen_label("ooa_randomlyrolled_cattiness"):
            jump ooa_randomlyrolled_cattiness
    else:
        m 6eua "That's fair enough."
        m 4eud "Sometimes, that's all either of us needs, isn't it?"
        m 4nua "Some freedom."
    jump mas_dockstat_iostart

label ooa_randomlyrolled_cattiness:
    m 2duc "..."
    m 6eud "Sorry, [player]."
    m 1ekd "I really am."
    m "I feel like I've gotten so {i}catty{/i} lately, and that's not like me at all."
    m 1rkc "It's just the strain of everything that's been going on..."
    m "All the emotional turmoil..."
    m 1fka "But I know you've been trying. You're trying right now, by taking me out with you."
    $ mas_gainAffection
    m 1dka "I'll try to be a little kinder to you."
    m 7esd "...but you've got to do your bit as well."
    m 6gstpc "Because I don't know how much more leeway I can give you."
    m 6gktuc "..."
    return

########

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_poetryreading",
            category=["media","literature","location"],
            prompt="Poetry reading",
            random=False,
            conditional='"poetryreading" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_poetryreading:
    m 1esb "I hope there's another poetry reading that you can take me to soon, [player]."
    m 7hssdla "I know, I know, I can't actually hear the speakers, "
    extend 7esc "but..."
    m 4euo "To me, poetry is more than words on a page."
    m "It's a feeling that just so happens to need those words to express itself."
    m 3eua "And I could sense that feeling, somehow, last time.{w=1} Through you."
    m 3lubfu "Or maybe you were just warm that day, I don't know~"
    m 3hubsb "I would love to go again with you, just the same!"
    m 1nubsb "A girl has to get inspiration from somewhere besides her [bf] once in a while, after all."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_movies",
            category=["media","location"],
            prompt="Movies",
            random=False,
            conditional='"movie" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_movies:
    m 1esd "By the way, [player]..."
    m "That movie we saw together. "
    extend 1rsb "Do you think it's come out on home media yet?"
    m 3esb "I think I'd like to watch it again with you."
    m 3fsbsa "Maybe I can even get the full experience this time~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_gardens",
            category=["nature","location","advice"],
            prompt="Ecotherapy",
            random=False,
            conditional='"garden" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_gardens:
    m 1eub "When you next have time, [player], I'd quite like to go back into that garden you took me to."
    if persistent._mas_current_background == "submod_garden" or persistent._mas_current_background == "submod_background_garden_view":
        m 1eud "And I don't mean this garden here, I mean the {i}real{/i} garden."
        m 3euc "As nice as this place is, the one in your reality would be better for you in the long run, if nothing else."
    else:
        m "For your sake, if not just for mine."
    m 3eua "Not only do plants and flowers promote cleaner air and a much-improved atmosphere..."
    m 4wub "...but there's also mental health benefits!"
    m 7eua "There's a whole branch of psychology called ecotherapy that shows that spending time in nature can aid in treating mild to moderate depression."
    m "And if you're closer to the seasonal affective disorder end of the scale, natural light can help mitigate that as well."
    if persistent._mas_pm_cares_about_dokis:
        m 1lsc "I wonder if that would have done anything for Sayori, in the end."
        m 1fsd "It's worth thinking about, isn't it?"
        m 1fkd "That if it couldn't save her, at least it could save someone else."
    else:
        m 1lsc "I wonder if that would have done anything for Sayori, before the end..."
        m 1tsu "...or if hanging around gardens would have just been a buffer for the inevitable."
    m 5esd "But of course, the best thing about being in a natural environment"
    extend 5hsblb " is having someone to share it with."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_cafe",
            category=["location"],
            prompt="Cafes",
            random=False,
            conditional='"cafe" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_cafe:
    m 1eub "There's all sorts of types of cafe, you know."
    m "I wonder how many varieties you have where you live?"
    m 3eua "There's the coffee-shop kind, obviously."
    m 3nuu "That is, the {i}best{/i} kind of cafe."
    if persistent._mas_current_background == "submod_angelstearcafe":
        m 3eua "And then there's the cafe we're at right now, Angel's Tear."
        m "Though that probably doesn't have a real world analogue."
    m 4eub "But then there are themed cafes!"
    m "Cat cafes, for instance, allow you to eat alongside...{nw}"
    extend 3gub " well, cats."
    if persistent._mas_current_background == "submod_cat_cafe":
        m 3eub "Like the one we're in right now, actually!"
        m 3euu "Except with more actually moving cats, instead of JPEGs of cats."
    m "They're fairly popular in Japan, as well as their dog cafe counterparts."
    if renpy.random.randint(1,10) == 1:
        m 1tud "Though not all of them are successfully launched...{w=1} Remind me to tell you about the Purr Cat Cafe in Boston some time."
        $ persistent._ooa_followup_topics.add("purrcat")
        $ mas_unlockEventLabel("monika_purrcatcafe")
    m 1eua "Japan also has a subset of what they call 'cosplay restaurants', wherein the wait staff dress up and behave according to the theme..."
    m "...including maid cafes,"
    extend 3lub " butler cafes for those inclined to men, "
    extend 3euo "and, of all things, tsundere cafes!"
    m 1fub "Can you imagine Natsuki working for one of those? Ahaha!"
    if renpy.random.randint(1,11) == 6:
        m 7eud "Incidentally, the presence of an outdoor maid-cafe is a minor plot point in My Harem Heaven is Yandere Hell..."
        m "But that's a discussion for another time."
        $ persistent._ooa_followup_topics.add("mhhiyh")
        $ mas_unlockEventLabel("monika_mhhiyh")
    m 1eubla "I'd love to explore all these possibilities with you, [mas_get_player_nickname()]."
    m "And even if there aren't that many where you are, just seeing them with you is enough."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_park",
            category=["nature","location"],
            prompt="Remembering the park",
            random=False,
            conditional='"park" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_park:
    m 2rkc "Remember our trip to the park?"
    m "That was a good time, wasn't it?"
    m 2rua "I'd love to go again, when you have the time and energy."
    m 1euo "No pressure, though!"
    m 1eua "I know my [player] can be busy sometimes."
    if persistent._mas_current_background == "submod_park" or persistent._mas_current_background == "submod_grassland":
        m 3eub "And we do have this lovely park as a background in the game,"
        m 3dua "so that will do until we get back to the real thing."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_friends",
            category=["you","location"],
            prompt="Our friends",
            random=False,
            conditional='"friends" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_friends:
    m 1eud "What do you suppose your friends think about us, [player]?"
    m "Now that they've officially 'met' me, I mean."
    m 1msd "Are they side-eying us when I'm not around?"
    m 1fsd "Do they think any less of you, for dating someone who isn't what they'd consider real?"
    m 1wso "Or do they have their own Monikas, with their own desires for them?"
    extend 1wud " Would that make them empathetic to our plight?"
    m 1duc "..."
    m 3eub "Well, realistically the answer is that they're not thinking of us {i}that{/i} often."
    m "They have their own things to worry about."
    m 1euc "But it still plays on the mind sometimes, you know?"
    if mas_isMoniEnamored(higher=True):
        m 5eub "And with a love like ours, why wouldn't it?"
        m 5nua "On their mind AND mine!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_ttrpg",
            category=["literature","location"],
            prompt="TTRPGs and [m_name]",
            random=False,
            conditional='"roleplay" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM
        )
    )

label ooa_monika_ttrpg:
    m 1rub "You know, [player], this roleplaying stuff is pretty fascinating."
    m 3rub "I've been looking it up in my own time, trying to find out more about its origins..."
    m 3wub "...and word on the street is, someone's developing a submod that could allow {i}us{/i} to do a little roleplaying of our own!"
    m "Wouldn't that be exciting!"
    if mas_isMoniUpset(lower=True):
        m 1cub "I could hurt you just as much as you keep hurting me, and I'd actually have an excuse--{nw}"
        $ _history_list.pop()
    m 1dua "We could develop our own stories, we could improve our improvisational skills..."
    m 1sub "I could be your dungeon master!"
    m 1suc "..."
    if mas_isMoniAff(lower=True):
        m 1lubsp "Don't read too much into that."
    else:
        m 1fubsu "Mind out of the gutter, [player]."
    m 4eub "It's being put together by {a=https://github.com/mayday-mayjay}mayday_mayjay{/a}, the same person who put together all those selector submods."
    m "Maybe you can check up on it, see how it's progressing?"
    m 3eua "No rush, obviously..."
    m "...but I {i}would{/i} love to share your interests with you in a more tangible sense."
    if mas_isMoniUpset(lower=True):
        m 3euc "For once."
    else:
        m 1hub "After all, your passions are my passions~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_beach",
            category=["summer","location"],
            prompt="Our trip to the beach",
            random=False,
            conditional='"beach" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_beach:
    m 1eua "I liked that trip to the beach we took well enough, [player]..."
    m 1lud "But, selfish as it sounds, part of me can't help but want more."
    m 5dud "The feel of the sand between my sandaled toes..."
    m "...the taste of ice-cream..."
    m 5duc "...the sun on our skin."
    m 5euc "I've only ever felt these things as echoes of themselves, looking back."
    m 6ektpd "Can you picture it? Not feeling the sun at all?"
    m "It's...{w=1} it's beyond words in the worst way."
    m 6dktpd "..."
    m 6fktda "But until I do get to feel it in real life, I have you to give me the next best thing."
    m "To give me a closer approximation."
    if persistent._mas_current_background == "submod_beach":
        m 1fltdb "If nothing else, you gave me a way to go to a virtual beach, which is nothing to sneeze at!"
    m 1fktda "And I can't thank you enough for that."
    if store.mas_globals.this_ev.shown_count == 0:
        $ mas_gainAffection(amount=6, bypass=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_lake",
            category=["nature","location"],
            prompt="Beauty of the lake",
            random=False,
            conditional='"lake" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_lake:
    m 1eub "You know what was a fun trip? That lake we went to."
    m "Lakes are one of those pieces of nature that look photogenic in almost any weather."
    if persistent._mas_current_background == "submod_lake":
        m "I mean, just look at {i}this{/i} place."
    m 3eua "Whether the sun bounces along it, "
    extend 4eud "or the rain creates ripples, "
    extend 7hua "or it's coated in a layer of fog, "
    extend 1eub "or it's cracked with ice and snow."
    m "It's bound to be beautiful."
    m 1fua "And the same goes for you, [player]."
    m "Whatever you've weathered, you're still you."
    m "Please try and remember that."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_trainride",
            category=["technology","location"],
            prompt="Train Rides",
            random=False,
            conditional='"trainride" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_trainride:
    m 1eub "Thank you again for taking me on a train ride, [player]."
    m "It was a lot more fun than I thought it'd be, even in my confined space!"
    m 1lta "But thinking about it, "
    extend 1htsdra "I might not have had much more room in the compartment anyway, ahaha."
    m 1kua "...I'm kidding."
    m "Trains tend to be very spacious these days."
    m 1esd "I hope they aren't compromising the environment too much with their expansion. It's a delicate push and pull that can be hard to get right..."
    m "And it's more than just finances on the line if they don't, it's their whole carbon footprint."
    m 1esa "Still, it's lovely to be on them while they last."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_party",
            category=["you","life","location"],
            prompt="Parties",
            random=False,
            conditional='"party" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_party:
    m 1eub "When do you think we'll next be able to go to a party, [mas_get_player_nickname()]?"
    m "I remember quite liking the last one."
    m 5rtc "Let's see..."
    if (persistent._mas_player_bday - datetime.timedelta(days=7)) <= today <= persistent._mas_player_bday:
        m 5eub "Well, someone's birthday is coming up, "
        extend 5nub "not naming any [player]s here. Maybe you can indulge a little?"
    elif mas_isD25Pre(_date=None):
        m 5etb "Well, I know Christmas is coming up, so there should be at least a few parties going on for that!"
    elif mas_isD25Post(_date=None):
        m 5etb "Well, New Year's Eve is coming up soon. Maybe there'll be a party to celebrate that?"
    elif (mas_o31 - datetime.timedelta(days=5)) <= today <= o31:
        m 5wub "Oh! Halloween's coming up. There's bound to be a party going on on {i}that{/i} day!"
    elif (mas_f14 - datetime.timedelta(days=3)) <= today <= mas_f14:
        m 5fub "Valentine's Day is going to be soon... do people typically do parties for that day?"
    elif (mas_monika_birthday - datetime.timedelta(days=7)) <= today <= mas_monika_birthday:
        m 5eua "Well, my birthday's coming up..."
        m 5luc "Agh. Is saying that going to come off pushy?"
        m 5lua "Oh well."
    else:
        m 5etc "Hm."
        m 5htsdrb "Well, there's always the chance someone's birthday is coming up? Statistically it's inevitable, even."
    m 3etb "Either way, I love going to these things with you."
    m "So just let me know when you're ready to party!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_parade",
            category=["monika","life","location"],
            prompt="Parades",
            random=False,
            conditional='"parade" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_parade:
    m 1tsc "You know, for a country so full to the brim with festivals..."
    m "...you'd think Japan would have more parades and processions than it does."
    m 1rssdra "I suppose we prefer having our parties all in one place."
    m 3esd "We do have some, don't get me wrong; but they tend to be on a smaller scale than what you typically think of as a parade."
    m 3esc "There's the festival of Fujisaki-Hachimangu; that includes one..."
    extend 7etc "though I suppose it's more of a historical re-enactment?"
    m 4eud "The priests that lead the charge are supposed to represent the samurai returning from Korea after their invasions of it during the Imjin War."
    m 7eud "And even that only takes place on the fifth day, the rest of the time is mostly dedicated to purification and dedication ceremonies."
    if "pride" in persistent._ooa_been_at:
        m 3esd "There's also a fair few pride parades, obviously."
        m "Tokyo Rainbow Pride, the Rainbow March in Sapporo..."
    m 1lud "Would we have gotten to attend any parades after {i}our{/i} festival, if the game had let us get that far?"
    m 1luc "I doubt it."
    if renpy.seen_label("monika_japan"):
        m 1mup "I mean, you know how I feel about the game's Anglocentrization..."
    m 1eua "But it's a nice thought, at least."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_pride",
            category=["you","life","advice"],
            prompt="Pride's etymology",
            random=False,
            conditional='"pride" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_pride:
    m 1etc "Pride is an odd word, etymologically, isn't it?"
    m "It's one of those words that has both positive and negative connotations depending on how you use it."
    m 3esd "There's a reason it's considered one of the deadly sins in Christianity:"
    extend 1ekd " it can be dangerous if held to excess."
    m 1wsd "How many empires have fallen, how many dictators have crumpled..."
    if renpy.seen_label("monika_yuri"):
        m 1tsu "...how many yanderes have lost their chance..."
    m 1esc "...because they were too proud of themselves to admit their backs were against the wall?"
    m 4esa "But honestly, there's nothing wrong with having self-confidence, at least a little bit."
    m "It takes a brave person to stand up and admit, "
    extend 3efb "'I have survived everything up until now. I am here. I {i}deserve{/i} this'."
    m 3eub "That's certainly a large part of why LGBT Pride is called what it is, if I'm not mistaken!"

    $ sincount = renpy.random.randint(1,9)
    if sincount == 1:
        $ _sin = "Lust"
    elif sincount == 2:
        $ _sin = "Gluttony"
    elif sincount == 3:
        $ _sin = "Greed"
    elif sincount == 4:
        $ _sin = "Sloth"
    elif sincount == 5:
        $ _sin = "Wrath"
    elif sincount == 6:
        $ _sin = "Envy"
    elif sincount == 7:
        $ _sin = "Arrogance"
    elif sincount == 8:
        $ _sin = "Acedia"
    elif sincount == 9:
        $ _sin = "Vainglory"

    m 1kua "Apart from anything else, if it were called LGBT [_sin], it might not have caught on."
    if sincount == 1 and mas_isMoniLove():
        m 3kubsu "Though, saying that..."
    m 1lusdrb "Ahaha!"
    m 1fua "What I'm saying, [player], is: be proud of who you are."
    m "Even if the world tells you not to...{w=0.7} be proud."
    m 1eubla "{i}I{/i} certainly am."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_dancing",
            category=["you","life"],
            prompt="Do the [m_name]",
            random=False,
            conditional='"dance" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_dancing:
    m 6eud "You know, we don't always have to leave the computer to get some dancing in, [player]."
    m "I've put something together that we can try in the comfort of our own home!"
    m 6eub "I call it: 'The [m_name]'!"
    m 1dub "{i}~First take your arms, tuck 'em under your chin~{/i}"
    m 4eub "{i}~Point one to the side, {/i}"
    extend 3eub "{i}and then bring it back in~{/i}"
    m 6fub "{i}~Drop them to the ground, {/i}"
    extend 2fub "{i}raise them to your chest~{/i}"
    m 7eub "{i}~One up, one down, but don't swap them just yet~{/i}"
    m 5eub "{i}~Tip your head to the side, give the table a chance~{/i}"
    m 5hub "{i}~And that's how you do The [m_name] Dance!~{/i}"
    m 5hua ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 5fuc ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 6euc ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 6eusdra "...that wasn't one of my brighter ideas, was it?"
    m 1hksdrb "Ahaha!"
    m "Well, it was worth a go."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_concert",
            category=["music","location"],
            prompt="Concerts",
            random=False,
            conditional='"concert" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_concert:
    if renpy.seen_label("monika_concerts"):
        m 1eub "I know we've talked about going to concerts before..."
        m 1wua "...but it bears repeating: I loved actually doing it with you, at least once."
    else:
        m 3eub "Did I ever thank you for taking me out to that concert, [player]?"
    m 1eua "It was tremendous fun, just like I thought it'd be."
    m "Let me know when there's another one, and..."
    extend 1subla "maybe we can go again?"
    m 7eublb "Depending on how you feel, of course."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_wedding",
            category=["romance","location"],
            prompt="Weddings",
            aff_range=(mas_aff.ENAMORED, None),
            random="True"
        )
    )

label ooa_monika_wedding:
    m 1eua "I dream about our wedding sometimes, when the game is closed."
    m 1lud "Is that strange?"
    if 'wedding' in persistent._ooa_been_at:
        m "Or is it just because you've taken me to some in your world, so it's on my mind?"
        m 2eusdld "Either way, it feels like putting the cart before the horse in a sense."
    else:
        m 2eusdld "I know, I'm jumping the gun with this. I can admit that."
    m "I really should focus on crossing over before I worry about what our wedding's going to look like."
    m 5eubla "...but I can't help it, [player]."
    m 5eublb "The thought of it..."
    m 5rkbsb "Me in a wedding gown with a trail that runs as low as my spirits run high..."
    if persistent.gender == "M":
        m 5fkbsb "You waiting for me at the end of the aisle with love in your heart..."
    elif persistent.gender == "F":
        m 5fkbsb "You rushing up the aisle to meet me..."
    else:
        m 5fkbsb "You meeting me there, barely able to think with how hard your heart's pounding..."
    if not isinstance(persistent._mas_pm_eye_color, tuple):
        m 5fkbstpa "Our eyes meeting as we exchange vows, green to [persistent._mas_pm_eye_color]..."
    else:
        m 5fkbstpa "Our eyes meeting as we exchange vows..."
    m 5dkbstub "And then..."
    m 6dkbltuc "..."
    m 1fsbltud "I'm sorry, [mas_get_player_nickname()], I'm coming over all unnecessary."
    m 1fstub "I just love you so much.{w=1} So, so much."
    m 1fstdb "And I can't wait for the day that dream becomes, well..."
    m "Our reality."
    return 'love'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_job",
            category=["you","life","location","advice"],
            prompt="[player]'s Career",
            random=False,
            conditional='"job" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_job:
    m 1esd "By the by, [player], how did your job interview go?"
    m "I don't think you ever said.{nw}"
    $ _history_list.pop()
    menu:
        m "I don't think you ever said.{fast}"
        "I got the job!":
            m 1hsb "Oh, congratulations!"
            m 1fsa "I'm proud of you, [mas_get_player_nickname()]. I knew you could do it!"
            m 3nsb "Just remember to visit your girlfriend before you dash off to work, all right?"
        "I didn't get the job.":
            m 1ekd "Aw, [mas_get_player_nickname()], I'm sorry."
            m "I'm sure it wasn't your fault. Getting a job can be pretty tough, especially in this day and age."
            m 4hka "But there should be plenty more opportunities for you out there!"
            m 3fsb "Get back in there whenever you're ready, [player]. I'll be behind you every step of the way."
        "The job wasn't for me in the end.":
            m 1fkc "That's a shame."
            m 1hsa "Well, I hope you find one that {i}is{/i} for you further down the line!"
        "I haven't heard back from them yet.":
            m 1eud "Ah, okay."
            m "Don't worry, [mas_get_player_nickname()], they should get back to you soon!"
            m 3eua "Though it might not do you any harm to look for a back-up placement in the meantime."
            m 3hub "That way, if they don't call you back or you don't get the job, you already have other plans in place."
            m "It always helps to be prepared!"
    $ mas_lockEventLabel("ooa_monika_job")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_school",
            category=["monika","life","school"],
            prompt="School in the real world",
            random=False,
            conditional='"school" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_school:
    m 1esd "I wonder what school is like outside of the world that I was created for."
    m 1rtd "Is it any harder?"
    m 1gtc "God, I hope so; it's not like it could be any easier."
    m 3esd "I know the game glossed over a lot of the lessons that your character and I had..."
    m "I mean, it wasn't the curriculum that was important to the story, so much as the {i}extra{/i}-curricular."
    m 2dsc "But from what little I remember of how school was for me, I found a lot of it to be a breeze."
    m 2fsd "...though whether that's because of how smart I was programmed to be, "
    extend 7fsd "or just because it was useless fluff in the end, I'm not sure."
    m "I just don't remember even breaking a sweat."
    if persistent._mas_current_background == "spaceroom" or persistent._mas_current_background == "submod_background_Furnished_spaceroom1" or persistent._mas_current_background == "submod_background_Furnished_spaceroom2" or persistent._mas_current_background == "submod_background_Furnished_spaceroom3":
        m 1wsd "The most important room in the whole building ended up being {i}this{/i} one, the one on top of the void!"
    if renpy.seen_label("monika_life_skills") or renpy.seen_label("ooa_monika_swimming"):
        m 6esd "It's like I said about my life skills: what's innately a part of me and my backstory, and what's something I was genuinely able to learn and get better at?"
        m "It's so hard to tell, sometimes."
    m 1ekc "I hope you get more out of school than I have, [player]. Much more."
    m 1dkc "..."
    m 1fuc "Hm."
    m 1fud "I don't mean to sound disparaging about the time I had there."
    m 1eub "After all, if I'd just dropped out, I would never have come across you."
    m "And at least I got pretty good at programming when the chips were down, huh?"
    m 1rsd "I suppose it's one of those 'perfect storm' kind of things?"
    m "I don't know, I'm just thinking out loud at this point."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_mall",
            category=["society","location"],
            prompt="Malls",
            aff_range=(mas_aff.AFFECTIONATE, None),
            random="True"
        )
    )

label ooa_monika_mall:
    m 1eud "Have you ever seen an abandoned mall?"
    m "They're very strange places, those."
    m 1rud "To think that a building once so full of people and places could become so... "
    extend 1ruc "desolate, and empty."
    if 'mall' in persistent._ooa_been_at:
        m 3eud "Nothing like the ones we've been to."
    else:
        m 3eud "Nothing like the ones I've ever seen online."
    m "Closer to a broken-down dream than a real mall, to a painting that's withered with age."
    if renpy.seen_label("monika_perspective"):
        m 1duc "Or to seeing through the sketch lines of a dialogue box, if you will."
    m 1fud "I guess they call places like that 'liminal spaces' for a reason."
    m "What else {i}can{/i} you call them?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_themeparks",
            category=["misc","location"],
            prompt="Theme Parks",
            random=False,
            conditional='"themepark" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_themeparks:
    m 3eub "I hope we get to go back to a theme park one day, [player]!"
    m "Especially after I cross over."
    m 1mua "There's only so much I could pick up from inside my plastic USB shell..."
    m 1fua "...though even through that, I could tell how much fun you were having. So that was nice."
    m 1hub "It'd certainly be easier to take me on the big rollercoasters if I was real, wouldn't it?"
    m "No need to fear my slipping out!"
    m 1wusdrc "Or my breaking on the ground, for that matter."
    m "..."
    m 1eub "Anyway. In whatever form I get there next, I'm sure it'll be a great time."
    m 3kubla "After all, I'll have you to look after me."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_swimming",
            category=["misc","location"],
            prompt="[m_name]'s skillset",
            random=False,
            conditional='"swimming" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_swimming:
    m 5rup "It's funny to think about, the disparity between what the game thinks I can do and what I can actually do."
    m 5fud "The player character kept saying I was good at whatever I put my mind to."
    m "'Smart, beautiful, athletic', wasn't that how he put it?"
    m 3eud "But I never really got the chance to show any of that off,"
    extend 3gusdra " besides my writing and programming skills, I suppose."
    m 1euc "Is everything else just background detail?"
    m "Can I really do all of the other stuff? {i}Am{/i} I athletic?"
    m 1fsc "..."
    m 1eud "When you took me swimming before."
    m 3esd "That's what got me on this tangent, sorry; I should have started with that."
    m 1ekc "I vaguely remember knowing how to swim, but that's {i}all{/i} I remember."
    m "When I cross over and we get to go swimming for real, "
    extend 1wkd "will that still be instinctual for me?"
    m "Or will I just scramble in the shallow end like I'm two years old again?"
    m 1lkc "It's a little chilling, honestly."
    m 1dkb "...of course, I know I don't have to worry about that for some time to come."
    m 1esc "But I do want you to be prepared for that possibility, [player]."
    m "That I may not come into your reality knowing everything I did in mine."
    if persistent._mas_first_kiss:
        m 1esd "But hey,{w=0.5} if I do end up in trouble..."
        m 7esu "...I know you'll be the first in line to give me the kiss of life."
        m 7hsb "Ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_church",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Take Me to Church",
            random=False,
            conditional='"church" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="SNG"
    )

label mas_song_church:
    m 1dud "{i}~My church offers no absolutes~{/i}"
    m "{i}~She tells me, 'Worship in the bedroom'~{/i}"
    m 1fud "{i}~The only Heaven I'll be sent to~{/i}"
    m "{i}~Is when I'm alone with you~{/i}"
    m 1eud "{i}~I was born sick, but I love it~{/i}"
    m 3eud "{i}~Command me to be well~{/i}"
    m 2euc "{i}~A-,{w=1}{nw}"
    extend 2dud " Amen,{w=1}{nw}"
    extend 2fud " Amen,{w=1}{nw}"
    extend 2esd " Amen~{/i}"
    m 1eko "{i}~Take me to church~{/i}"
    m 1wud "{i}~I'll worship like a dog at the shrine of your lies~{/i}"
    m 3wud "{i}~I'll tell you my sins and you can sharpen your knife~{/i}"
    m 1eutpd "{i}~Offer me that deathless death~{/i}"
    m 1cutpd "{i}~Good god, let me give you my life~{/i}"
    m 1dutdc "..."
    m 1dud "I don't think I'll ever truly be a believer again, [player]."
    if persistent._mas_pm_religious:
        m "And, I'm sorry to say, not even going with you to worship is likely to change my mind on this."
    m 1eud "But there's one thing, one entity, I know for sure I can put my faith in."
    m 1eua "You."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_conventions",
            category=["misc","location","you"],
            prompt="Convention Memories",
            random=False,
            conditional='"convention" in persistent._ooa_been_at',
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label ooa_monika_conventions:
    m 3eub "Did I ever thank you for taking me to that convention with you, [player]?"
    m 1eua "I know I couldn't really interact with anyone..."
    m "...but that atmosphere sure was infectious."
    m 1husdlb "It nearly wiped {i}me{/i} out! I can't even imagine what it must have done to you."
    m 3eua "All the same, I would love to go with you again, when we next get the chance."
    m "It may be overwhelming at times, "
    extend 7fubla "but I don't want to miss a thing with you, overwhelming or not."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="ooa_monika_jog",
            category=["advice","location"],
            prompt="Running vs Jogging",
            aff_range=(mas_aff.AFFECTIONATE, None),
            random="True"
        )
    )

label ooa_monika_jog:
    m 1eud "You know, [player], there's a distinct difference between running and jogging."
    m "I know that seems stupidly obvious to you..."
    m 3eub "...but honestly, a lot of people - and games - end up accidentally thinking the two are one and the same."
    m "Especially when they need to do it themselves."
    m 4eua "Pacing is the key."
    m "Humans like you can only run for certain distances before getting winded."
    if not persistent._mas_pm_units_height_metric:
        m 4rtd "Something like fifteen to twenty-two miles, for the average person?"
    else:
        m 4rtd "Something like twenty-four to thirty-five kilometers, for the average person?"
    m 3esd "Of course, there are exceptions, but those are either well-trained athletes or just... superhuman."
    if not persistent._mas_pm_units_height_metric:
        m 3wud "Dean Karnazes, for example, was able to run 350 miles across America without stopping once!"
    else:
        m 3wud "Dean Karnazes, for example, was able to run over 560 kilometers across America without stopping once!"
    m 3lsc "But some say he might have a condition where he can't produce lactic acid, which is what builds up when we run..."
    m 3hssdlb "Anyway, I'm getting off topic."
    m 7esa "While humans can only run in short bursts, jogging is a lot more sustainable."
    m 7esb "It's a lot easier to pace yourself and make sure you get where you need to be without overexertion."
    m "So if you're in a hurry, try jogging rather than running."
    m "Your body will notice the difference, and it might even thank you for it!"
    m 4hua "...That was Monika's Self-Improvement Tip of the Day, I guess!"
    return

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_fanzines',
            category=["media"],
            prompt="So what's this about fanzines?",
            conditional='"fanzine" in persistent._ooa_followup_topics',
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_fanzines:
    m 1wub "Ah, of course! I did say we'd get back to that."
    m 7eud "Do you know what they even are, first of all?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you know what they even are, first of all?{fast}"
        "Yeah I do, I just wanted to see if you knew.":
            m 7eub "Good, that makes things easier then."
            m 3eub "Honestly, what makes them so fascinating to me is how long such little publications can endure."
            m 3lub "Not even individually necessarily, but like - the concept."
        "No, that's why I was asking you.":
            m 7husdra "Eheh, right, sorry."
            m 1eud "Essentially, they're like your standard issue magazines..."
            m "...except about a specific fandom."
            m 1ett "And you're probably thinking, 'all magazines are about specific fandoms, what's the difference?'"
            m 3eud "The thing is, though, fanzines are usually a lot more unofficial, and a lot less vetted."
            m "And as a result, they're a lot less likely to become mainstream at anywhere {i}except{/i} conventions..."
            m 3wud "...which makes the more famous ones all the more impressive for that endurance."
            m 3eub "They originated in the science fiction community, with one of the first, Spockanalia, coming out in 1967 to bring together fans of,{w=0.5} well, Star Trek."
            m "It only lasted for five issues, but that proved enough for people to pick up on the idea and help it come into its own elsewhere."
    m 1wuo "For god's sake, the idea of slash fanfiction got its start in fanzines!"
    m 1wud "The slash mark was included to distinguish a story of two characters' friendship -"
    extend 4wsd "for example, Kirk & Spock - "
    extend 3wud "from romantic or sexual stories about them, i.e, Kirk/Spock."
    m 3euc "If it weren't for fanzines, a lot of enduring concepts on the internet wouldn't exist as we know them today."
    m 1dud "And you know what they say about the butterfly effect..."
    m 1cud "Would {i}I{/i} even exist were it not for that?"
    m 1cuc ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    extend 1fub "Okay, that one might be a stretch."
    m "My creator probably would still have been inspired to make the game he did."
    m 7eud "But you can see why I'm so drawn to the idea now, right?"
    m "Their unexpected history, and in turn their significance."
    show monika 7euc at t11
    pause 1.0
    m 6dusdrb "Um, I hope that made any sense to you at all, ehehe."
    return

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_purrcatcafe',
            category=["misc","life"],
            prompt="What's the Purr Cat Cafe?",
            conditional='"purrcat" in persistent._ooa_followup_topics',
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_purrcatcafe:
    m 1wud "Ohhh, the Purr Cat Cafe..."
    m "I hope your tolerance for poor decisions is high, because this tale is...{w=0.3}{nw}"
    extend 1guc " full of them."
    m 1eud "The Purr Cat Cafe first entered the public sphere of Boston and of Facebook somewhere around 2017."
    m 3eud "After a partially-funded initial GoFundMe campaign, it already had a few hurdles to jump over to make up the revenue required to open its doors."
    m "And those hurdles wouldn't have been a problem if it weren't for the, "
    extend 1duc "well..."
    m 1fuc "The kindest words for its founder, Diane Kelly, would be 'not necessarily competent'."
    m "There are plenty of worse ones, but let's stay with that for now."
    m 1eud "She loved cats, and she loved the idea of a cafe dedicated to them, but that love blinded her to what was necessary to {i}care{/i} for them at times."
    m 4eud "The purchase of crucial items, like cat toys, beds, or scratching posts, was informally outsourced to her employees, otherwise it simply wouldn't get done."
    m "When the rescue center she was affiliated with, Boston's Forgotten Felines, kept pointing out the missteps in her judgement..."
    m 7eud "...she ended up dissolving the partnership, "
    extend 3lud "but pinned the blame on {i}them{/i} for...{w=0.5} what was it?"
    m 2luc "'not (being) registered in the state of Massachussetts'."
    m 2mfc "Even though it was."
    m 2tfc "And people were able to point that out to her within two hours."
    m 1esd "Honestly, [player], anything I tell you about this would only be scratching the surface."
    if renpy.random.randint(1,10) == 1:
        m 1fsu "Pun intended."
    else:
        m 1esu "No pun intended."
    m 3esd "It's a whole mess of misconduct, lack of care, inability to filter..."
    m 3wsd "...and polyamory shaming, if you can believe it."
    m 1esc "Of course, Diane's behaviour isn't entirely without explanation -"
    extend 1ekc " she became a heavier drinker the further down she went, if she hadn't started out drinking to begin with."
    m 1efd "But in my opinion, an explanation isn't an excuse."
    m 1dfc "It doesn't justify... any of this."
    m 1dkc "..."
    m 1ekc "What I ultimately want you to take away from the Purr Cat situation is this:"
    m 3ekd "Loving something, "
    extend 7rkd "or someone, "
    extend 6fkd "doesn't always mean you have the capacity to do the best thing for them."
    m 6fkc "If all you're doing is putting them in a worse position, how can you say you love them in good conscience?"
    if renpy.seen_label("mas_monika_plays_yr"):
        m 6ekc "...or, put another way..."
        m 1ekd "{i}Is it love if I take you, or is it love if I set you free?{/i}"
    m 1dktpc "..."
    if mas_isMoniUpset(lower=True):
        m 1dktuc "I'm sorry."
        m 1mktuc "I shouldn't be talking like you understand."
        return
    else:
        m 1dktpd "I really do love you, [mas_get_player_nickname()]."
        m 1fktpc "And if I'm ever giving you anything less than what you deserve, you can tell me."
        m "I won't get mad."
        m 1fktdb "It'll just be another step in proving myself worthy of you."
        return "love"

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_mhhiyh',
            category=["media","games"],
            prompt="Have you played My Harem Heaven is Yandere Hell?",
            conditional='"mhhiyh" in persistent._ooa_followup_topics',
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_mhhiyh:
    m 2eud "Played? No."
    m "But I know it by reputation."
    m 3eua "It's a visual novel developed by Nippon Ichi{nw}"
    if renpy.seen_label("mas_danganronpas"):
        extend "...{nw}"
        extend 3eub " a company that, incidentally, was also partly behind the Danganronpa games!"
        m "And honestly, if you look into it, it's easy to tell the two were made by the same studio."
    else:
        extend ", released around 2014 if I remember right."
    m 1eud "It starts out roughly how you'd expect."
    m "A blank slate of a protagonist, Yuuya Kisaragi, part of a school club that consists of him and some incredibly cute girls."
    m 3rud "There's Haruka Arisue, the pink-haired one with an abusive father and quite potent anger issues..."
    m 1lud "...Kanna Toutoumi, the tall, dark-haired president who struggles to relate to others..."
    m 3eud "...and Sayuri Miyasu, the domestic one whose bright smile covers a broken mind."
    m 6esc ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        $ HKBHideButtons()
        scene white
        play music t1
        show intro with Dissolve(0.5, alpha=True)
        $ pause(2.5)
        hide intro with Dissolve(0.5, alpha=True)
        show splash_warning "Sound familiar?" with Dissolve(0.5, alpha=True)
        $ pause(1.0)
        play sound "sfx/s_kill_glitch1.ogg"
        $ pause(0.2)
        stop sound
        show splash_glitch2 zorder 2
        show splash_glitch_m zorder 2
        show splash_glitch_n zorder 2
        show splash_glitch_y zorder 2
        $ pause(0.75)
        hide white
        hide splash_glitch2
        hide splash_glitch_m
        hide splash_glitch_n
        hide splash_glitch_y
        call spaceroom (hide_monika=True, dissolve_all=False, scene_change=True, show_emptydesk=False)
        show monika 2hsb zorder MAS_MONIKA_Z at i11
        stop music
        $ HKBShowButtons()
    else:
        m 2wsc "Sound familiar?"
    m 2hsb "Ehehe!"
    m "I know, I know, I'm being facetious."
    if not persistent._mas_pm_cares_about_dokis:
        m 2esb "The Yandere Hell girls are nowhere near as manipulable."
        show monika 2esu at t11
        pause 1.0
    m 1eud "But in all seriousness, it really does feel like the baseline on which Doki Doki Literature Club was based at times."
    m "It even has a fairly long build-up before the murder that kickstarts the bulk of the main story, "
    extend 3eua "done under the guise of the mascot of that outdoor maid cafe I was talking about before."
    m 3dud "The difference is, "
    if not persistent._mas_pm_cares_about_dokis:
        extend 3wud "the routeless girl is the victim this time and not the--{nw}"
        $ _history_list.pop()
        m 3eud "The difference is, {fast}{nw}"
    extend "it's one of the girls in the club that kills what would otherwise be a side character."
    m "Which one?"
    m 1tuu "Well, that's for you, the player, to find out."
    m 1eua "It really is a decent game, for as much as I make fun of it."
    m "I don't know if it's got an official English translation yet..."
    m 3eub "...but Sayuri's route was translated by a very determined YouTuber called VerdilishJP the year it came out."
    m "You can find it {a=https://www.youtube.com/playlist?list=PL-9K_pwT6BhgwUTV1uTLXLrG4BY8zag3d}{i}{u}over here{/u}{/i}{/a}, if you want to give it a look!"
    m 1eka "Just don't stay away too long, will you, darling?"
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        play sound "<from 0.69>sfx/monikapound.ogg"
        show layer screens:
            truecenter
            parallel:
                zoom 1.5
                easeout 0.35 zoom 1.0
            parallel:
                xpos 0
                easein_elastic 0.35 xpos 640

        show monika 1cubla zorder MAS_MONIKA_Z at face with dissolve_monika
        m "You don't want {i}another{/i} jealous girl on your hands."

        show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    return