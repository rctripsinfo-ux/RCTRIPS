"""Hook Bank PRO: 1080x1350 slide-deck PDF. Frameworks adapted (not copied) from Hook Point
(Brendan Kane) and creator guides, combined with @freestack.ai's own 30-reel performance data."""
import html, pathlib, subprocess

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
E = html.escape
TITLE = "Hook Bank PRO"

CSS = """
@page { size: 1080px 1350px; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: 'Inter', sans-serif; color: #111 }
.s { width: 1080px; height: 1350px; padding: 84px 80px 110px; position: relative; overflow: hidden; page-break-after: always; background: #fff }
.y { background: #FFD400 } .k { background: #111; color: #fff } .r { background: #E10600; color: #fff }
.tag { display: inline-block; background: #111; color: #FFD400; font: 800 24px 'Inter'; letter-spacing: 1px; padding: 9px 18px; text-transform: uppercase }
.k .tag, .r .tag { background: #FFD400; color: #111 }
h1 { font: 900 118px/0.98 'Inter Display'; letter-spacing: -3px; margin: 34px 0 26px }
h2 { font: 900 64px/1.05 'Inter Display'; letter-spacing: -1px; margin: 22px 0 26px }
h3 { font: 800 34px/1.2 'Inter'; margin: 0 0 10px }
p { font: 500 31px/1.45 'Inter'; margin-bottom: 14px }
.lead { font: 600 38px/1.35 'Inter' }
.red { color: #E10600 } .k .red, .r .red { color: #FFD400 }
.mark { background: #FFD400; padding: 0 8px; color: #111 }
.foot { position: absolute; left: 80px; right: 80px; bottom: 44px; display: flex; justify-content: space-between; font: 700 21px 'Inter'; opacity: .5 }
.card { background: #F3F3F3; border-left: 12px solid #E10600; padding: 22px 28px; margin: 14px 0; font: 500 29px/1.42 'Inter' }
.k .card { background: #1E1E1E } .y .card { background: #fff }
.card b { font-weight: 800 }
.tbl { width: 100%; border-collapse: collapse; font: 500 25px/1.32 'Inter' }
.tbl th { background: #111; color: #FFD400; text-align: left; padding: 12px; font-weight: 800 }
.tbl td { padding: 11px 12px; border-bottom: 2px solid #e6e6e6; vertical-align: top }
.num { font-weight: 900 }
.good { color: #0a8a3a; font-weight: 900 } .bad { color: #E10600; font-weight: 900 }
.ex { font: 600 31px/1.38 'Inter'; padding: 14px 0 14px 54px; position: relative; border-bottom: 2px solid #eee }
.ex .n { position: absolute; left: 0; top: 13px; font: 900 28px 'Inter Display'; color: #E10600 }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 18px }
.ba { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 10px 0 }
.ba div { padding: 16px 18px; font: 600 26px/1.35 'Inter'; border-radius: 8px }
.ba .b { background: #FFE5E3 } .ba .a { background: #E3F7EA }
.lbl { font: 900 20px 'Inter'; letter-spacing: 1px; display: block; margin-bottom: 6px; opacity: .7 }
.phone { width: 300px; height: 533px; border: 12px solid #111; border-radius: 34px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px; background: #fff }
.phone.bad2 { background: #F3EFF7 }
.cta { background: #E10600; color: #fff; padding: 26px 30px; font: 800 33px/1.3 'Inter'; margin-top: 26px }
.small { font-size: 26px !important }
.td { display: grid; grid-template-columns: 250px 1fr; gap: 28px; padding: 20px 0; border-bottom: 3px solid #eee; align-items: start }
.td img { width: 250px; height: 444px; object-fit: cover; border-radius: 14px; border: 5px solid #111 }
.td.sm { grid-template-columns: 170px 1fr } .td.sm img { width: 170px; height: 302px }
.views { display: inline-block; font: 900 40px 'Inter Display'; padding: 4px 16px; border-radius: 8px; margin-bottom: 12px }
.views.g { background: #0a8a3a; color: #fff } .views.l { background: #E10600; color: #fff }
.chip { display: inline-block; font: 800 21px 'Inter'; background: #FFD400; padding: 5px 12px; margin: 0 8px 8px 0; border-radius: 6px }
.hq { font: 800 30px/1.3 'Inter'; margin: 6px 0 10px } .why { font: 500 25px/1.4 'Inter' }
.avatar { width: 150px; height: 150px; border-radius: 50%; border: 6px solid #111 }
"""


def slide(inner, cls="", tag=""):
    t = f'<div class="tag">{E(tag)}</div>' if tag else ""
    return f'<div class="s {cls}">{t}{inner}{{FOOT}}</div>'


def exs(items, start=1):
    return "".join(f'<div class="ex"><span class="n">{start + i}</span>{E(x)}</div>' for i, x in enumerate(items))



def ba(pairs):
    return "".join(f'<div class="ba"><div class="b"><span class="lbl">❌ BEFORE</span>{E(b)}</div><div class="a"><span class="lbl">✅ AFTER</span>{E(a)}</div></div>' for b, a in pairs)


S = []

# 1 cover
S.append(slide('<div style="font:900 300px/0.9 Inter Display;letter-spacing:-12px;margin-top:30px">120<span class="red">+</span></div>'
               '<h1 style="margin-top:0">Viral Hinglish<br>Hooks <span class="red">PRO</span></h1>'
               '<p class="lead">14 real reel teardowns · 12 hook types · 20 before/after rewrites · the first-3-seconds system</p>'
               '<div style="position:absolute;right:70px;bottom:120px;display:flex;align-items:center;gap:18px"><div style="text-align:right;font:800 26px Inter">by @freestack.ai<br><span style="font-weight:600;font-size:22px">Built from 17,000+ views of real data</span></div><img class="avatar" src="img/pp.jpg"></div>', "y", "For faceless creators"))

# 2 contents
S.append(slide('<h2>What\'s inside</h2><table class="tbl">'
               + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in [
                   ("01", "Real reel teardowns: 8 winners vs 6 flops, with screenshots"),
                   ("02", "How Instagram decides who sees your reel (in plain words)"),
                   ("03", "The 3-Layer Hook: text + voice + visual together"),
                   ("04", "Hook Score: a 10-point test before you post"),
                   ("05", "10 reasons hooks fail"),
                   ("06", "How to put a hook on screen (typography rules)"),
                   ("07", "12 hook types: psychology + template + examples"),
                   ("08", "20 before → after rewrites"),
                   ("09", "7 niches × 10 ready-to-use hooks (no blanks)"),
                   ("10", "What to say after the hook: the A.R.C.S. formula"),
                   ("11", "Hook testing and the 'double down' system"),
                   ("12", "7-day hook practice plan")]) + "</table>", tag="Contents"))

# 3 story + teardowns
S.append(slide('<div style="display:flex;gap:30px;align-items:center;margin-top:24px"><img class="avatar" src="img/pp.jpg"><div><h2 style="margin:0">How this PDF was made</h2><p class="small">@freestack.ai · faceless AI-tools page</p></div></div>'
    '<p class="lead" style="margin-top:30px">I posted one reel every day for 30 days. Same design, same voice, same length. <b>The only thing that changed was the hook.</b></p>'
    '<div class="card"><b>Result:</b> 17,000+ views. Best reel: <b>1,645</b> views. Worst: <b>140</b>. An <b>11× gap</b> on the same page, from the first line alone.</div>'
    '<div class="card">This PDF is what that data taught me: which hooks worked, which flopped, and why. The next pages break down the actual reels.</div>'
    '<p class="small" style="margin-top:14px">To be honest, this is a small page, not a celebrity. That is exactly why these lessons are useful to you: you are at the same stage.</p>', tag="My story"))
WIN=[("05","1,645","Google ne apna AI agent free mein de diya, aur bahut kam log jaante hain.",["Big brand","Secret","Free"],"Google's name = instant trust. 'Few people know' = insider info. Viewers felt they were missing out."),
("07","1,611","Ek hafte mein 5 mehenge AI tools ke free versions. Kitne yaad hain?",["Recap","Quiz","List"],"The shortest reel (28s). The quiz turned it into a game, and the list format made people save it."),
("04","1,593","Coding ke liye Cursor ka subscription? Ruk jao.",["Stop command","Money","Big brand"],"Named a tool people actually pay for, plus a direct command. Got the most likes of the series (49)."),
("28","1,434","Teen hafton mein itne free versions. Kitne yaad hain?",["Recap","Quiz"],"Second recap, second time in the top 5. This format is a pattern, not luck."),
("11","1,182","Sirf likho, aur AI video bana dega.",["Result first","Wow"],"Six words, and the result appears in your head instantly. No thinking needed."),
("09","1,102","AI voiceover ke liye har mahine paise de rahe ho?",["Pain","Money","Question"],"Hit a real monthly cost creators pay. The question made viewers silently answer 'yes'."),
("27","1,093","Purani blurry video ko 4K mein badlo, free.",["Result first","Emotion"],"Old family videos = emotion. The before/after formed in the viewer's mind."),
("29","1,040","Ye 'free' AI tools sach mein free hain? Ek kadwa sach sun lo.",["Hard truth","Trust"],"No tool at all, just an honest opinion. The audience rewarded honesty.")]
LOSE=[("24","140","AI ko apni files, GitHub aur apps se jodo, ek standard tareeke se.",["Confusing","Jargon"],"No pain, no result. Nobody wants 'a standard way'."),
("19","144","Manus AI ka waitlist aur credits bhool jao.",["Unknown name"],"Assumed people knew what Manus was. They didn't."),
("22","144","Ek AI employee, jo kabhi chhutti nahi leta.",["Vague","Overused"],"Sounds nice, but what does it actually do? Not clear."),
("16","151","Koi bhi article, aur do AI hosts uspe podcast karenge.",["Too long","Low stakes"],"Long line, and the 'paid' tool it replaced is already free."),
("18","153","Google se smart search, jo seedha jawab de.",["Feature only"],"Described a feature, not a pain. Why would anyone stop?"),
("13","175","Midjourney level AI images, zero rupaye mein.",["Old news"],"Free AI images are on every phone now. 'Free' is no longer news.")]
def tdw(items, cls, sm=False):
    return "".join(f'<div class="td{" sm" if sm else ""}"><img src="img/{c}.jpg"><div><span class="views {cls}">{v} views</span><div class="hq">"{E(h)}"</div>'+"".join(f'<span class="chip">{E(t)}</span>' for t in tags)+f'<p class="why">{E(w)}</p></div></div>' for c,v,h,tags,w in items)
for i in range(0,8,2):
    S.append(slide(f'<h2 style="margin-bottom:6px">Teardown: <span class="good">why it worked</span> ({i//2+1}/4)</h2>'+tdw(WIN[i:i+2],"g"), tag="01 · Real reels"))
for i in range(0,6,3):
    S.append(slide(f'<h2 style="margin-bottom:6px">Teardown: <span class="bad">why it flopped</span> ({i//3+1}/2)</h2>'+tdw(LOSE[i:i+3],"l",True), tag="01 · Real reels"))
S.append(slide('<h2>8 winners vs 6 flops: <span class="red">the pattern</span></h2>'
    '<div class="card"><b>Winning hooks:</b><br>✅ named something people already pay for<br>✅ challenged or questioned the viewer directly<br>✅ turned the reel into a quiz or recap<br>✅ showed the result in one line</div>'
    '<div class="card" style="border-color:#111"><b>Flop hooks:</b><br>❌ only described a feature<br>❌ used a name nobody knew<br>❌ used jargon ("standard", "protocol")<br>❌ said "free" where free is already normal</div>'
    '<p class="lead" style="margin-top:20px">The next pages turn this pattern into a system that works in any niche.</p>', "y", "01 · Pattern"))

# 4 algorithm
S.append(slide('<h2>How Instagram <span class="red">pushes a reel</span></h2>'
               '<div class="card"><b>Step 1:</b> Your reel is first shown to a small group (some followers + some new people).</div>'
               '<div class="card"><b>Step 2:</b> Did they stop? Watch to the end? Like it? Send it to someone? If yes, it goes to more new people.</div>'
               '<div class="card"><b>Step 3:</b> If new people react the same way, it keeps going. That is "going viral".</div>'
               '<p style="margin-top:20px">Instagram head <b>Adam Mosseri</b> has said publicly that the biggest signals for reels are <span class="mark">watch time</span>, <span class="mark">likes per reach</span> and <span class="mark">sends per reach</span> (shares by DM).</p>'
               '<p><b>So:</b> a hook\'s job is not just to stop people. It must stop the <b>right</b> people, who watch to the end and share. Clickbait stops people, but they leave fast, and the reel dies there.</p>', tag="02 · Algorithm"))

# 5 three layer
S.append(slide('<h2>The 3-Layer Hook: <span class="red">all three say the same thing</span></h2>'
               '<div class="two"><div><h3>1. Text (on screen)</h3><p class="small">3–7 big words. On the very first frame, from 0.0 seconds.</p><h3>2. Voice (first line)</h3><p class="small">The same message, said naturally. No "Hi guys", no intro.</p><h3>3. Visual</h3><p class="small">A result, a face reacting, or something happening. Never an empty screen.</p></div>'
               '<div style="display:flex;gap:16px;justify-content:center"><div class="phone bad2"><p class="small" style="opacity:.5">pastel background</p><p class="small"><b>empty mockup</b></p><p class="small" style="opacity:.5">mascot after 4 sec</p></div></div></div>'
               '<div class="card"><b>Our mistake (from the data):</b> our covers were strong: red-yellow, mascot, "₹0". But the reel\'s <b>first frame</b> was a pale pastel screen with an empty mockup. In the feed, people see <b>frame 0</b>, not your cover. Lesson: make your cover design the first frame of the reel.</div>'
               '<div class="card"><b>Second mistake:</b> every reel spent 2–5 seconds saying "Subscription band karo, Day N". Zero value for a new viewer. Put the series name small on screen, don\'t say it.</div>', tag="03 · First 3 seconds"))

# 6 hook score
crit = [("Few words", "Like a magazine headline. Readable in 3 seconds."), ("On-brand", "Matches your page's topic, or it feels like clickbait."),
        ("Flips a belief", "Challenges something people assume."), ("Easy", "No effort needed to understand it."), ("Not too flat", "Makes people think a little, or they ignore it."),
        ("Curiosity", "The answer is inside the video, not in the hook."), ("Original", "A hook seen everywhere stops working."),
        ("Familiar + new", "Something known + a twist (Google + free)."), ("3-second test", "Show a friend for 3 seconds. Can they tell the topic?"),
        ("Solves a pain", "Points at the viewer's real problem.")]
S.append(slide('<h2>Hook Score: below <span class="red">7 out of 10</span>? Don\'t post.</h2><table class="tbl"><tr><th>#</th><th>Check</th><th>How to judge</th></tr>'
               + "".join(f"<tr><td class='num'>{i + 1}</td><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for i, (a, b) in enumerate(crit)) + "</table>"
               '<p class="small" style="margin-top:16px">Adapted from the principles in Brendan Kane\'s book <i>Hook Point</i>, for Hinglish reels.</p>', tag="04 · Test"))

# 7 fail reasons
fails = [("Too long", "A 60-second reel with a 2-line hook: barely above median."), ("Confusing", "\"MCP: Model Context Protocol\" → viewers had no idea what it was. 140 views."),
         ("Vague", "\"Ye video aapki zindagi badal degi\" → how? why?"), ("Overused", "\"Wait till the end\" has been seen 1,000 times."),
         ("For no one", "\"Tips for everyone\" = tips for no one."), ("Outdated", "A trend from two years ago."),
         ("Assumes interest", "\"Manus ka waitlist bhool jao\" → who is Manus? 144 views."), ("Dishonest", "A promise the video doesn't keep."),
         ("Not unique", "Same as every competitor."), ("Looks dull", "Small text, low contrast, empty screen.")]
S.append(slide('<h2>10 reasons hooks <span class="red">fail</span></h2><table class="tbl">'
               + "".join(f"<tr><td class='num bad'>{i + 1}</td><td><b>{E(a)}:</b> {E(b)}</td></tr>" for i, (a, b) in enumerate(fails)) + "</table>", tag="05 · Mistakes"))

# 8 typography
S.append(slide('<h2>How to put a hook <span class="red">on screen</span></h2>'
               '<div class="card"><b>Rule 1, highlight a complete thought:</b> "<span class="mark">Paisa bachao</span>, ameer nahi banoge" ✅. Highlighting only "Paisa" is wrong, because one word alone says nothing.</div>'
               '<div class="card"><b>Rule 2, break lines where you would breathe:</b><br>"Roz 3 ghante ek reel pe? / Saal ke 1,000 ghante gaye."</div>'
               '<div class="card"><b>Rule 3, one colour = one meaning:</b> red = pain/mistake, yellow = solution/result. Keep it the same across the series.</div>'
               '<div class="card"><b>Rule 4, phone safe zone:</b> keep text out of the top 15% and bottom 25%, where Instagram\'s buttons sit.</div>'
               '<div class="card"><b>Rule 5, 0.0 seconds:</b> the hook text must be on the first frame. No fade-in, logo or intro animation.</div>', tag="06 · Typography"))

# 9-20 archetypes
TYPES = [
    ("Stop Command (Callout)", "A direct order hits the brain's brakes, and the person being called out recognises themselves.",
     "[Paying money/time] for [task]? Ruk jao.",
     ["Coding ke liye Cursor ka subscription? Ruk jao.", "Roz 3 ghante reel edit karte ho? Ruk jao.", "Salary aate hi EMI pe EMI? Ruk jao, pehle ye suno."],
     "Give the order, then give the reason immediately. Don't just say 'Ruk jao' and stop."),
    ("Insider Secret", "Everyone loves insider info: the 'I know something you don't' feeling.",
     "[Big company/person] gave [thing] away free, and very few people know.",
     ["Google ne apna AI agent free mein de diya, aur bahut kam log jaante hain.", "Toppers revise ek alag tareeke se karte hain. Kam log jaante hain.", "Phone ki ek setting jo aapki battery chupke se kha rahi hai."],
     "The secret must be genuinely useful. A fake secret = an unfollow."),
    ("Recap / Quiz", "The brain loves games. List + quiz = watched to the end and saved.",
     "[N] [things] in [time]. How many do you remember?",
     ["Ek hafte mein 5 mehenge AI tools ke free versions. Kitne yaad hain?", "Is mahine ke 7 money rules. Kitne follow kiye?", "10 English words jo is hafte seekhe. Kitne yaad hain?"],
     "In our data both recap reels made the top 5. Post one recap every 7 days."),
    ("Hard Truth (Contrarian)", "Honesty builds trust, and an unexpected opinion stops the scroll.",
     "Hard truth: [what everyone believes] is wrong.",
     ["Ye 'free' AI tools sach mein free hain? Ek kadwa sach sun lo.", "Kadwa sach: aap busy nahi ho, distracted ho.", "Kadwa sach: jaldi uthne se koi ameer nahi banta."],
     "Back it up with an example or a number. Don't say it just for shock."),
    ("Loss (Money / Time)", "People fear losing more than they enjoy gaining. Show the loss and they stop.",
     "[Time/money] on [task]? That's [big yearly number] gone.",
     ["Roz 3 ghante ek reel pe? Saal ke 1,000 ghante gaye.", "Har mahine ₹500 ke subscriptions? Saal ke ₹6,000.", "Roz 2 ghante phone pe scroll? Saal ke 30 din."],
     "The number must be true and the maths simple enough for viewers to check."),
    ("Result First (Proof)", "Seeing is believing. Show the result first, the method after.",
     "[Visual of the result]. Here's how it happened.",
     ["Purani blurry video ko 4K mein badlo, free.", "Ye reel bina camera, bina mic bani hai. Guess karo kaise?", "Ek line likhi, poori website ready."],
     "The visual result must be on frame 0. Our 4K reel (1,093 views) worked for exactly this reason."),
    ("Myth Buster", "Proving a common belief wrong creates instant contrast.",
     "The biggest lie: '[myth]'.",
     ["Sabse bada jhooth: 'pehle editing seekho, phir page shuru karo.'", "Myth: zyada padhoge toh zyada marks.", "Myth: paisa bachane se ameer bante hain."],
     "People must actually believe the myth. Don't bust a made-up one."),
    ("Identity Callout", "People love hearing about themselves. Call one group by name.",
     "If you are [age/role], listen to this now.",
     ["Agar aap 20s mein ho, toh ye 3 galtiyan abhi rok do.", "Naya page shuru kiya hai? Ye 5 cheezein pehle din karo.", "Hostel mein rehte ho? Ye 4 paise bachane ki tricks."],
     "Keep the group small and specific. 'Everyone' is not an identity."),
    ("Comparison", "Show two paths. Viewers place themselves on one side and watch to the end.",
     "[A] vs [B]: see the difference after [N] days.",
     ["Do creators, same talent. Ek roz post karta hai, ek mood pe. 90 din baad kaun aage?", "₹15,000 ka editor vs ₹67 ki reel.", "Topper vs average student: farak padhai mein nahi."],
     "Show both sides fairly. Don't make one side look stupid."),
    ("Story Drop-in", "Start in the middle of the story. The brain needs to know what happens next.",
     "[Person] did [unusual thing]. Then [twist].",
     ["Usne naukri chhodi, sab ne pagal kaha. 6 mahine baad koi nahi hasa.", "Ek chai wale ne mujhe business ka sabse bada lesson diya.", "Ek saal tak zero posts. Phir ek din ye notice kiya."],
     "The lesson must be useful to the viewer, not just entertaining."),
    ("Challenge / Test", "Pull the viewer into a game. Answers go in the comments, and comments boost reach.",
     "[A test or question]. Most people get it wrong.",
     ["Ek aawaz asli hai, ek AI. Pehchaan ke dikhao.", "In 3 mein se aap kaun ho? Comment karo.", "Ye 30-second test karo: aapka focus kitna hai?"],
     "Never invent a % or a statistic. 'Most people get this wrong' is enough."),
    ("Newness", "Something new = 'I should have known this first'.",
     "[Thing] just launched [this week], and it [benefit].",
     ["Instagram ne ek naya feature diya hai, creators ke liye kaam ka.", "Is hafte ek naya free AI tool aaya jo [kaam] karta hai.", "UPI ka naya rule, ye aapko pata hona chahiye."],
     "It must really be new, and fact-checked. Fake 'news' destroys trust."),
]
for i, (nm, why, tpl, ex, warn) in enumerate(TYPES):
    S.append(slide(f'<h2>{E(nm)}</h2><p class="lead" style="font-size:31px">{E(why)}</p>'
                   f'<div class="card"><b>Template:</b> {E(tpl)}</div>' + exs(ex) +
                   f'<div class="card" style="border-color:#111;margin-top:22px"><b>⚠️ Watch out:</b> {E(warn)}</div>', tag=f"07 · Hook type {i + 1}/12"))

# rewrites
RW = [("Aaj main aapko ek AI tool ke baare mein bataunga.", "Ye free AI tool aapke 3 ghante bachata hai. Roz."),
      ("MCP ek open standard hai.", "AI ko apne phone ke apps chalane do. Ek setting se."),
      ("Ek AI employee jo kabhi chhutti nahi leta.", "Email padhna, reply likhna, sheet bharna. Ab AI karega, free."),
      ("Hello guys, welcome back!", "Ruko! Ye galti aap roz karte ho."),
      ("Motivation chahiye?", "Aap aalsi nahi ho. Aapka plan galat hai."),
      ("5 tips for students", "Exam mein sab bhool jaate ho? Ye 1 tareeka badlo."),
      ("Paise bachane ke tips", "Salary 20 tareekh tak khatam? Galti yahan hai."),
      ("Ye video zaroor dekhna", "Agar aap 20s mein ho, toh ye 3 cheezein abhi rok do."),
      ("Interesting facts", "Aapki aankh har din ek cheez nahi dekh paati. Kya?"),
      ("Shayari part 12", "Jo log chup rehte hain, wo sabse zyada sochte hain."),
      ("English improve karo", "Ye 5 English lines bolte hi log aapko smart samjhenge."),
      ("Business ideas 2026", "₹5,000 se shuru hone wale 3 kaam, jo ghar se ho sakte hain."),
      ("Health tips", "Subah uthte hi thakaan? Ye 1 aadat check karo."),
      ("Ek kahani suniye", "Sab hans rahe the. 6 mahine baad koi nahi hasa."),
      ("Productivity hacks", "Roz 2 ghante bachane ka ek boring sa tareeka."),
      ("Career advice", "Resume mein ye 1 line hai? Isliye call nahi aa rahi."),
      ("New AI update", "Google ne chupke se ek naya free tool diya hai."),
      ("Cricket facts", "Ye record shayad kabhi nahi tootega. Kaunsa?"),
      ("Relationship tips", "Ye 3 baatein bolte hi ladai khatam."),
      ("Psychology facts", "Jo insaan ye karta hai, wo jhooth bol raha hai.")]
for i in range(0, 20, 7):
    S.append(slide(f'<h2>Before → After <span class="red">{i + 1}–{min(i + 7, 20)}</span></h2>' + ba(RW[i:i + 7]), tag="08 · Rewrites"))

# niche banks
NB = [("Motivation", ["Aap aalsi nahi ho. Aapka plan galat hai.", "Kadwa sach: koi aapko bachane nahi aayega.", "Jo aaj kar rahe ho, wahi 5 saal baad ban jaoge.", "Mood ka intezaar karoge toh kabhi shuru nahi hoga.", "Log aapko judge nahi kar rahe. Wo apne mein busy hain.", "20s mein ye 3 galtiyan zindagi bhar ka nuksaan hain.", "Har din 1% better. 1 saal baad hisaab dekho.", "Jis din haarne ka darr gaya, us din jeet shuru.", "Aapki comfort zone ek sundar si jail hai.", "Discipline ka sabse aasaan tareeka, jo koi nahi batata."]),
      ("Facts", ["Aapka dimaag raat ko ek ajeeb kaam karta hai.", "Ye cheez aap roz khaate ho, par asal mein phal nahi hai.", "Duniya ka ek desh jahan suraj 2 mahine nahi doobta.", "Aapki aankh ek rang kabhi nahi dekh sakti.", "Ye record shayad kabhi nahi tootega.", "Shahad kabhi kharab nahi hota. Kyun?", "Aap roz itna paani peete ho bina jaane.", "Ek ghanti jisne poora itihaas badal diya.", "Sach ya jhooth: insaan ka DNA kele se milta hai?", "Ye shabd aap roz bolte ho, par matlab nahi pata."]),
      ("Money tips", ["Salary 20 tareekh tak khatam? Galti yahan hai.", "Har mahine ₹500 ke subscriptions = saal ke ₹6,000.", "Credit card ki ye 1 galti, aur interest ka jaal.", "Paisa bachao, ameer nahi banoge. Ye bhi karo.", "Pehli salary pe ye 3 kaam karo.", "Ameer log chupke se ye 1 cheez karte hain.", "UPI pe ye setting abhi on karo.", "Do log, same salary. 10 saal baad ek ameer kyun?", "₹100 roz = saal ke ₹36,500. Kahan ja rahe hain?", "Bank ye baat aapse kabhi nahi kahega."]),
      ("Study tips", ["Padhte ho, par exam mein bhool jaate ho? Ye badlo.", "Toppers revise ek alag tareeke se karte hain.", "Raat ko padhna galat hai? Sach sun lo.", "1 ghante ki padhai 20 minute mein.", "Exam se 1 din pehle ye galti mat karna.", "Phone saath rakh ke padhte ho? Ye suno.", "Ye 3 sawaal har chapter ke baad khud se poocho.", "Yaad karne ka nahi, bhoolne ka system samjho.", "Topper vs average: farak ghanton mein nahi hai.", "Notes banana time waste hai? Kadwa sach."]),
      ("AI tools", ["Google ne chupke se ek naya free tool diya hai.", "ChatGPT ki ye setting 90% log on nahi karte.", "Ye free AI tool aapke 3 ghante bachata hai.", "Paid AI tool ka free version, phone pe.", "Ek photo do, aur wo bolne lagegi.", "Ye 'free' AI tools sach mein free hain?", "AI se ye kaam karwao, boss khush.", "Ek prompt, aur poori presentation ready.", "AI jo aapka phone khud chalata hai.", "Ye AI tool students ke liye cheat code hai."]),
      ("Shayari / quotes", ["Jo log chup rehte hain, wo sabse zyada sochte hain.", "Kuch log yaadein nahi, sabak ban jaate hain.", "Maa ki ek baat jo ab samajh aayi.", "Dosti ki ek line, jo dil pe lagegi.", "Raat ke 2 baje wali soch.", "Jise khona nahi chahte, use ye kabhi mat kehna.", "Waqt sab badal deta hai. Ye bhi.", "Kuch rishte shor nahi karte, bas nibhaate hain.", "Akela hona aur tanha hona alag hai.", "Ek line jo aapke kisi khaas ko bhejni chahiye."]),
      ("Stories", ["Usne naukri chhodi, sab ne pagal kaha. Phir ye hua.", "Ek chai wale ne mujhe business sikhaya.", "Ek message ne uska poora saal badal diya.", "100 baar haara. 101vi baar kya hua?", "Teacher ka ek sawaal, jiska jawab koi nahi de paya.", "Ek ghadi ki kahani jo 50 saal se ruki hai.", "Raja ne ek ajeeb hukm diya.", "Ek galti jisne company dooba di.", "Ek ladka, ek sapna, aur ek bus ticket.", "Sab hans rahe the. 6 mahine baad koi nahi hasa."])]
n = 1
for nm, hs in NB:
    S.append(slide(f'<h2>{E(nm)}: <span class="red">10 ready hooks</span></h2>' + exs(hs, n), tag="09 · Niche bank"))
    n += 10

# ARCS
S.append(slide('<h2>After the hook: <span class="red">A.R.C.S.</span></h2>'
               '<div class="card"><b>A, Ask:</b> a question your viewer answers "yes" to. <i>"Roz post karna chahte ho, par time nahi?"</i></div>'
               '<div class="card"><b>R, Reveal:</b> show you were in the same spot. <i>"Mujhe bhi ek reel mein 3 ghante lagte the."</i></div>'
               '<div class="card"><b>C, Call out:</b> the discovery that changed things. <i>"Phir maine script se reel banane ka system banaya."</i></div>'
               '<div class="card"><b>S, Send:</b> one clear action. <i>"Comment karo REEL, system bhej dunga."</i></div>'
               '<p class="small" style="margin-top:18px">This is copywriter Craig Clemens\' "Impact Arcs" formula (described in the book Hook Point), adapted for 30-second Hinglish reels. It works for one sentence, one reel, or a full presentation.</p>', tag="10 · Script"))

# testing
S.append(slide('<h2>Testing and the <span class="red">Double Down</span></h2>'
               '<div class="card"><b>1. Write 3 hooks for every idea.</b> Post the best one, test the other two as "Trial Reels" (Instagram\'s feature that shows a reel to non-followers first).</div>'
               '<div class="card"><b>2. Check Insights after 48 hours:</b> views, skip rate / 3-second hold, average watch time, shares. Decide on the average of 5 reels, never on one.</div>'
               '<div class="card"><b>3. Double down rule:</b> if a reel gets <b>2× your median</b> or more, make <b>3 new versions</b> of the same idea within 7 days: new hook, new example, new angle. In our data the recap worked twice, both times in the top 5.</div>'
               '<div class="card"><b>4. Study your flops too:</b> run the hooks of your 3 lowest reels through the Hook Score. Fix whichever point failed next time.</div>', tag="11 · System"))

# practice
plan = [("Day 1", "Collect 20 strong hooks from the Ad Library and top creators in one note (for learning only)."),
        ("Day 2", "Label each hook with one of the 12 types. Which type dominates your niche?"),
        ("Day 3", "Find 5 flop reels and note which Hook Score point they fail."),
        ("Day 4", "Write 3 hooks each for 3 topics in your niche (9 total)."),
        ("Day 5", "Run the 3-second friend test on each. Keep the top 3."),
        ("Day 6", "Make reels with the top 3. Frame 0 = hook text + visual."),
        ("Day 7", "Check Insights, pick the winner, start doubling down.")]
S.append(slide('<h2>7-day <span class="red">hook practice</span></h2><table class="tbl">'
               + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in plan) + "</table>"
               '<div class="card" style="margin-top:22px">Learn by studying others, then write your own. Never post someone else\'s hook as-is under your name: it rarely works and it breaks trust.</div>', "y", "12 · Practice"))

# upsell
S.append(slide('<h2>Hooks ready. <span class="red">No time to make the reels?</span></h2>'
               '<p class="lead">Send us your niche and script. We make <span class="mark">ready-to-post typography reels</span>: hook on frame 0, bold text, animation and voice.</p>'
               '<div class="card"><b>5 reels: ₹199.</b> Trial, delivered in 72 hours.</div><div class="card"><b>30 reels: ₹1,999.</b> A full month of content + calendar.</div>'
               '<div class="cta">Order from the link in @freestack.ai\'s Instagram bio.</div>', "k", "Shortcut"))

body = "".join(s.replace("{FOOT}", f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{TITLE} · {i + 1}/{len(S)}</span></div>') for i, s in enumerate(S))
h = OUT / "hook-bank-pro.html"
h.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const f=process.argv[1];await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});await b.close();})();"""
subprocess.run(["node", "-e", js, str(h)], check=True)
print(len(S), "slides")
