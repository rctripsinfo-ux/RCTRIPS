"""Faceless Page Blueprint PRO. Reuses Hook Bank PRO design. Methods summarised (not copied) from creator
tutorials the owner supplied, combined with @freestack.ai's own 30-reel data. English explanations, Hinglish examples."""
import pathlib, subprocess
HERE = pathlib.Path(__file__).parent
_src = (HERE / "hooks_pro.py").read_text(encoding="utf-8")
exec(_src[:_src.index("S = []")])
TITLE = "Faceless Page Blueprint PRO"


def bullets(items):
    return "".join(f'<div class="ex"><span class="n">{i + 1}</span>{x}</div>' for i, x in enumerate(items))


S = []
S.append(slide('<div style="font:900 230px/0.9 Inter Display;letter-spacing:-10px;margin-top:30px">0→1K</div>'
               '<h1 style="margin-top:10px">Faceless Page<br>Blueprint <span class="red">PRO</span></h1>'
               '<p class="lead">Niche → branding → research → content → growth → money. The full system, without showing your face.</p>'
               '<div style="position:absolute;right:70px;bottom:120px;display:flex;align-items:center;gap:18px"><div style="text-align:right;font:800 26px Inter">by @freestack.ai<br><span style="font-weight:600;font-size:22px">With our real mistakes and data</span></div><img class="avatar" src="img/pp.jpg"></div>', "y", "For faceless creators"))

S.append(slide('<h2>What\'s inside</h2><table class="tbl">' + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in [
    ("01", "What our own page taught us (honest numbers)"),
    ("02", "The 5-question Niche Checklist"),
    ("03", "8 faceless niches, broken down in depth"),
    ("04", "Branding: name, profile picture, bio that converts"),
    ("05", "The first 7 days: warming up your page"),
    ("06", "Viral research: where to look + the outlier rule"),
    ("07", "Remodel, don't copy: the safe way to use what works"),
    ("08", "Your signature style (why people remember you)"),
    ("09", "The 30-day launch roadmap"),
    ("10", "Organic growth tactics + the viral window"),
    ("11", "Views → followers: the conversion problem"),
    ("12", "The money ladder: from 0 to your first sale")]) + "</table>", tag="Contents"))

# 01 our lessons
S.append(slide('<div style="display:flex;gap:30px;align-items:center;margin-top:20px"><img class="avatar" src="img/pp.jpg"><div><h2 style="margin:0">What our page taught us</h2><p class="small">@freestack.ai · 30 reels in 30 days</p></div></div>'
               '<table class="tbl" style="margin-top:24px"><tr><th>What happened</th><th>The lesson</th></tr>'
               "<tr><td>17,000+ views but only 116 followers (0.7%)</td><td><b>Views are not growth.</b> The profile must give a reason to follow.</td></tr>"
               "<tr><td>Bio said '👇 free list' but had no link</td><td><b>A broken promise kills trust</b> at the exact moment someone is interested.</td></tr>"
               "<tr><td>Category was set to 'Marketing Agency'</td><td>Small details decide whether you look like a creator or a business.</td></tr>"
               "<tr><td>Same template every day → 7 of 8 reels on days 12–19 under 400 views</td><td><b>Repetition = 'views stuck'.</b> Rotate formats.</td></tr>"
               "<tr><td>Recap + opinion reels were 3–4.6× the median</td><td>Find your winning formats early, then double down.</td></tr></table>"
               '<p class="small" style="margin-top:16px">This PDF is the system we wish we had on day 1.</p>', tag="01 · Proof"))

# 02 checklist
S.append(slide('<h2>The 5-question <span class="red">Niche Checklist</span></h2>'
               + bullets(["<b>Interest:</b> could I make 100 reels on this without getting bored?",
                          "<b>Proof of concept:</b> can I find 3+ faceless pages in this niche growing right now?",
                          "<b>Money:</b> will this audience pay for something later (PDF, course, product, brand deals)?",
                          "<b>Audience quality:</b> do people here want to learn or improve, not just laugh and scroll?",
                          "<b>Feasibility:</b> can I make this content with text, voice and simple visuals, without complex animation?"])
               + '<div class="card"><b>Rule:</b> all 5 must be "yes". Missing proof of concept is the most common mistake: an interesting topic with no successful pages usually means no audience on Instagram.</div>'
               '<div class="card"><b>How to check proof:</b> search the niche keyword on Instagram, open 3 pages, and check whether their recent reels (last 30 days) are getting views far above their follower count.</div>', tag="02 · Niche"))

# 03 niches
NICHES = [
    ("Motivation / Self-improvement", "18–25, students and young workers who feel stuck", "Laziness, no discipline, comparing themselves to others",
     ["Hard truths", "Discipline systems", "Short stories with a lesson"], "Habit tracker PDF, 30-day challenge, journal",
     ["Kadwa sach: aap busy nahi ho, distracted ho.", "20s mein ye 3 galtiyan abhi rok do.", "Usne naukri chhodi, sab ne pagal kaha. Phir ye hua."], "Easy"),
    ("Money tips (Personal finance)", "First-job earners, 21–30", "Salary runs out by the 20th, EMI traps, no savings",
     ["Spending traps", "Simple saving rules", "Rich vs poor habits"], "Budget sheet, salary-planning PDF, affiliate (only trusted products)",
     ["Salary 20 tareekh tak khatam? Galti yahan hai.", "Credit card ki ye 1 galti, aur interest ka jaal.", "Do log, same salary. 10 saal baad ek ameer kyun?"], "Easy · keep it general, no investment advice"),
    ("Study tips", "Class 10–college students, exam aspirants", "Forgetting, no focus, phone addiction",
     ["Revision methods", "Exam-week plans", "Topper habits"], "Study planner, notes templates, revision system PDF",
     ["Padhte ho, par exam mein bhool jaate ho? Ye badlo.", "Toppers revise ek alag tareeke se karte hain.", "Exam se 1 din pehle ye galti mat karna."], "Easy"),
    ("AI tools", "Students, creators, freelancers", "Paying for tools, wasting time, fear of falling behind",
     ["Free alternatives", "Phone AI tricks", "Honest tool tests"], "Prompt packs, tool guides, services (like done-for-you reels)",
     ["Google ne chupke se ek naya free tool diya hai.", "ChatGPT ki ye setting 90% log on nahi karte.", "Ye 'free' AI tools sach mein free hain?"], "Medium · fast-changing, verify facts"),
    ("Amazing facts", "Broad, 16–30", "Boredom, curiosity",
     ["Body & mind facts", "History mysteries", "True/false quizzes"], "Hard to sell products; better for promos and shoutouts",
     ["Aapka dimaag raat ko ek ajeeb kaam karta hai.", "Shahad kabhi kharab nahi hota. Kyun?", "Sach ya jhooth: insaan ka DNA kele se milta hai?"], "Easy · facts must be verified"),
    ("Psychology", "18–30, people curious about others and themselves", "Overthinking, relationships, confidence",
     ["Body language", "Dark psychology (ethical)", "Self-understanding"], "Ebooks, guides, journals",
     ["Jo insaan ye karta hai, wo jhooth bol raha hai.", "Log aapko judge nahi kar rahe. Ye suno.", "Overthinking band karne ka 1 tareeka."], "Medium · avoid fake 'science'"),
    ("Shayari / quotes", "Emotional, 16–28", "Loneliness, heartbreak, nostalgia",
     ["Love/breakup", "Dosti", "Life lessons"], "Promos, custom shayari, wallpaper packs",
     ["Jo log chup rehte hain, wo sabse zyada sochte hain.", "Kuch rishte shor nahi karte, bas nibhaate hain.", "Raat ke 2 baje wali soch."], "Easy · very competitive"),
    ("Short stories", "Broad", "Wants to feel something in 60 seconds",
     ["Moral stories", "Twist endings", "Historical stories"], "Story ebooks, promos",
     ["Ek chai wale ne mujhe business sikhaya.", "Raja ne ek ajeeb hukm diya.", "100 baar haara. 101vi baar kya hua?"], "Medium · needs good writing"),
]
for i, (nm, who, pain, pillars, money, hooks, diff) in enumerate(NICHES):
    S.append(slide(f'<h2 style="margin-bottom:12px">{E(nm)}</h2>'
                   f'<table class="tbl"><tr><td style="width:240px"><b>Target viewer</b></td><td>{E(who)}</td></tr>'
                   f'<tr><td><b>Their pain</b></td><td>{E(pain)}</td></tr>'
                   f'<tr><td><b>3 content pillars</b></td><td>{E(" · ".join(pillars))}</td></tr>'
                   f'<tr><td><b>How it makes money</b></td><td>{E(money)}</td></tr>'
                   f'<tr><td><b>Difficulty</b></td><td>{E(diff)}</td></tr></table>'
                   '<h3 style="margin-top:24px">First 3 reels (ready hooks)</h3>' + exs(hooks), tag=f"03 · Niche {i + 1}/8"))

# 04 branding
S.append(slide('<h2>Branding that <span class="red">converts</span></h2>'
               '<div class="card"><b>Name:</b> short, easy to spell, says the niche. "@paisa.rules" beats "@the_real_finance_guy_2026".</div>'
               '<div class="card"><b>Profile picture:</b> faceless is fine, but it must be recognisable at tiny size: a mascot, a bold logo letter, or one icon on a strong colour. Our red-yellow mascot works because it is the same everywhere.</div>'
               '<div class="card"><b>Bio formula:</b> who it\'s for + what they get + proof/journey + one action.</div>'
               '<div class="card"><b>Never beg:</b> "Follow me for more" gives no reason. Give a reason instead: "Roz 1 money rule jo school ne nahi sikhaya."</div>'
               '<div class="card"><b>Highlights:</b> 3–5 covers in your brand colours: Start here · Best reels · Free stuff · Results.</div>'
               '<div class="card"><b>Category:</b> pick "Digital creator" or "Education", not a random business category.</div>', tag="04 · Branding"))
S.append(slide('<h2>Bio: <span class="bad">bad</span> vs <span class="good">good</span></h2>'
               + ba([("Motivation | Quotes | Follow for more 🔥", "Discipline > motivation 💪\nRoz 1 kadwa sach jo aapko aage le jaaye\n👇 Free 30-day habit tracker"),
                     ("Finance tips daily", "Salary 20 tareekh tak khatam? 💸\nPaise bachane ke simple rules, Hinglish mein\n👇 Free salary planner"),
                     ("Study motivation page", "Kam padho, zyada yaad rakho 📚\nToppers ke revision systems\n👇 Free exam-week plan"),
                     ("AI tools | Tech | Free", "Paid AI tool ka free version 🔓\nHonest tests, catch ke saath\n👇 30 free AI tools list")]).replace("\n", "<br>")
               + '<div class="card" style="margin-top:16px"><b>Check:</b> the 👇 must point to a real, working link. Ours didn\'t, and people who wanted the list had nowhere to go.</div>', tag="04 · Bio"))

# 05 warm-up
S.append(slide('<h2>The first 7 days: <span class="red">warm up</span></h2>'
               + bullets(["<b>Act like a normal user.</b> No mass liking, mass following or copy-paste comments. Bot-like behaviour can limit a new page.",
                          "<b>Train your feed.</b> Watch, like and save only reels from your niche for 15–20 minutes a day, so Instagram learns what your page is about and shows you research material.",
                          "<b>Finish your profile</b> (name, picture, bio, link, category) before the first post.",
                          "<b>Make 5 reels before posting the first one.</b> A buffer protects your consistency when life gets busy.",
                          "<b>Switch to a Creator account</b> so you get Insights. Instagram shows more detailed professional insights once you reach 100 followers."])
               , tag="05 · Warm-up"))

# 06 research
S.append(slide('<h2>Viral research: <span class="red">where to look</span></h2>'
               + bullets(["<b>Fastest-growing pages:</b> list 10 pages in your niche in a sheet. Sort by how fast they are growing, not by total followers.",
                          "<b>Their following list:</b> big pages usually follow other strong pages in the same niche. Free research.",
                          "<b>Intentional scrolling:</b> after the warm-up, your Reels feed shows niche content. Scroll with a notebook, not for fun.",
                          "<b>Meta Ad Library:</b> ads running for months are messages that are proven to work."])
               + '<div class="card"><b>The outlier rule:</b> a reel is worth studying only if it got <b>3× or more</b> that page\'s usual views. A page with 10K average views and one reel at 200K = an outlier. That reel shows what the audience really wants.</div>'
               '<div class="card"><b>Quality filter:</b> likes around 2–5% of views, real comments (not just emojis), and posted <b>recently</b> (ideally within the last week). Old viral reels show what worked then, not now.</div>', tag="06 · Research"))

# 07 remodel
S.append(slide('<h2>Remodel, <span class="red">don\'t copy</span></h2>'
               '<p class="lead" style="font-size:32px">Taking the <b>idea</b> that works is learning. Re-uploading someone\'s reel is theft, and it gets pages removed.</p>'
               '<table class="tbl"><tr><th>Keep</th><th>Change</th></tr>'
               "<tr><td>The concept / topic</td><td>The hook wording (write 3 new ones)</td></tr>"
               "<tr><td>The structure (list, story, myth…)</td><td>Examples, numbers and language (make it Hinglish, make it Indian)</td></tr>"
               "<tr><td>The length and pace</td><td>Design, font, colours: your signature style</td></tr>"
               "<tr><td></td><td>Voice: your own recording or your own AI voice, never their audio</td></tr></table>"
               '<div class="card"><b>Mix sources:</b> take ideas from many creators, never only one. A page that copies one creator gets called out, and its audience never trusts it.</div>'
               '<div class="card"><b>Music:</b> use Instagram\'s licensed library or royalty-free tracks. Copyrighted songs added in an editor can get your reel muted.</div>', tag="07 · Remodel"))

# 08 signature style
S.append(slide('<h2>Your <span class="red">signature style</span></h2>'
               '<p class="lead" style="font-size:32px">If someone sees your reel twice, would they know it is yours? If not, every view is a stranger again.</p>'
               + bullets(["<b>Same visual identity:</b> 1 font, 2 colours, same layout for hook text.",
                          "<b>A signature opening or closing line</b> (example: ending every reel with \"Ab jao, kaam karo.\").",
                          "<b>A recurring series:</b> \"Kadwa Sach Monday\", \"Sunday Recap\".",
                          "<b>Same mascot / logo position</b> in every reel."])
               + '<div class="card"><b>Give it 3–6 months.</b> Style forms slowly. Experiment in month 1, pick what works, then keep it fixed. Don\'t copy another creator\'s style: people will say you copied them.</div>', tag="08 · Recall"))

# 09 roadmap
S.append(slide('<h2>30-day <span class="red">launch roadmap</span></h2><table class="tbl"><tr><th>Week</th><th>Focus</th><th>Do this</th></tr>'
               "<tr><td class='num'>0</td><td><b>Setup</b></td><td>Niche checklist, branding, warm-up, 5 reels in the bank</td></tr>"
               "<tr><td class='num'>1</td><td><b>Test formats</b></td><td>1 reel/day, a different format each day (Weekly Format System)</td></tr>"
               "<tr><td class='num'>2</td><td><b>Find winners</b></td><td>Check Insights: which 2 formats beat your median?</td></tr>"
               "<tr><td class='num'>3</td><td><b>Double down</b></td><td>60% winning formats, 40% new tests. Start a recurring series.</td></tr>"
               "<tr><td class='num'>4</td><td><b>Convert</b></td><td>Fix bio + highlights, add a free lead magnet + comment-keyword DM</td></tr></table>"
               '<div class="card"><b>Realistic expectation:</b> most new pages see slow numbers for weeks before one reel breaks out. That flat period is where most people quit. Plan for 90 days, not 9.</div>', tag="09 · Roadmap"))

# 10 growth tactics
S.append(slide('<h2>Organic growth <span class="red">tactics</span></h2>'
               + bullets(["<b>Early valuable comments:</b> turn on notifications for 2–3 bigger pages (100K–500K) in your niche and leave a genuinely useful first comment. Good comments get seen by thousands. No spam, no fake accounts.",
                          "<b>Collabs:</b> use Instagram's Collab feature with a similar-size page in your niche. Both audiences see the reel.",
                          "<b>Trial Reels:</b> post variations (different hook or font) of the same reel to non-followers first and keep the winner.",
                          "<b>Reply to every comment in the first hour.</b> Conversation signals the reel is worth pushing.",
                          "<b>Ride trends that fit your niche:</b> budget day, exam season, New Year, a viral event, with your niche's angle."])
               + '<div class="card"><b>The viral window:</b> creators commonly see that after a reel goes viral, the next 3–14 days give new posts extra reach. Don\'t go quiet. Post more often (if possible 2/day) and post follow-ups on the same topic.</div>', tag="10 · Growth"))

# 11 conversion
S.append(slide('<h2>Views → followers: <span class="red">the real game</span></h2>'
               '<div class="card"><b>The example:</b> a creator who grew from 1K to 800K followers in 150 days shared that two of his reels got almost the same views (2.1M and 2.2M), but one brought <b>40,000</b> followers and the other only <b>16,000</b>. The difference: how much real value the reel gave.</div>'
               '<div class="card"><b>Our case:</b> 17,000 views → 116 followers (0.7%). Mostly tool lists people could save without needing us again.</div>'
               '<h3 style="margin-top:20px">How to raise conversion</h3>'
               + bullets(["Give value that makes people want the <b>next</b> reel too (series, part 1/2/3).",
                          "Talk to one person, like a friend, not to an audience.",
                          "End with a line that hits the viewer personally, so they feel 'this page gets me'.",
                          "Make the profile instantly explain what they'll get by following."]), tag="11 · Conversion"))

# 12 views stuck
S.append(slide('<h2>"Views stuck"? <span class="red">Diagnose it</span></h2><table class="tbl"><tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr>'
               "<tr><td>Low views on every reel</td><td>Weak hook / frame 0</td><td>Hook Score + 3 hooks per idea</td></tr>"
               "<tr><td>Views drop week after week</td><td>Same format repeated</td><td>Rotate formats, new series</td></tr>"
               "<tr><td>Good views, no follows</td><td>Profile doesn't sell the page</td><td>Bio formula, highlights, pinned reels</td></tr>"
               "<tr><td>Good watch time, no shares</td><td>Nothing 'sendable'</td><td>Relatable or useful-to-a-friend angles</td></tr>"
               "<tr><td>One viral reel, then silence</td><td>Missed the viral window</td><td>Post follow-ups within 3–14 days</td></tr></table>", tag="11 · Diagnose"))

# 13 money ladder
S.append(slide('<h2>The money <span class="red">ladder</span></h2><table class="tbl"><tr><th>Step</th><th>What</th><th>When</th></tr>'
               "<tr><td class='num'>1</td><td><b>Free lead magnet</b> (checklist, PDF) via comment-keyword DM</td><td>From day 1</td></tr>"
               "<tr><td class='num'>2</td><td><b>Email list / broadcast channel</b> of people who took the freebie</td><td>From a few hundred followers</td></tr>"
               "<tr><td class='num'>3</td><td><b>Low-ticket digital product</b> (₹99–₹499)</td><td>Once people ask for more</td></tr>"
               "<tr><td class='num'>4</td><td><b>Paid promos / shoutouts</b> for brands in your niche</td><td>Once you have a steady audience</td></tr>"
               "<tr><td class='num'>5</td><td><b>Services or bigger products</b></td><td>When trust is built</td></tr></table>"
               '<div class="card"><b>Rule:</b> build the product from what your comments and DMs ask for. In our case, viewers literally asked for "clipping with captions" and "truly free video tools". That is product research for free.</div>'
               '<div class="card"><b>Trust first:</b> no fake testimonials, no income promises. One broken promise can cost you the whole audience.</div>', tag="12 · Money"))

# 14 mindset
S.append(slide('<h2>Why most pages <span class="red">quit</span></h2>'
               '<div class="card"><b>The valley of disappointment:</b> results always come slower than expected. Effort goes in, numbers stay flat, and that gap is where people quit. Results compound later, which is why most people never see them.</div>'
               '<div class="card"><b>Shiny object syndrome:</b> switching niche every 2 weeks resets everything. Give one niche 90 days of consistent posting before judging it.</div>'
               '<div class="card"><b>Measure inputs, not just outputs:</b> "Did I post today and study 3 outliers?" is in your control. Views are not.</div>'
               '<p class="lead" style="margin-top:24px">Consistency with quality beats talent. Every time.</p>', "y", "Mindset"))

S.append(slide('<h2>Page planned. <span class="red">No time to make the reels?</span></h2>'
               '<p class="lead">Send us your niche. We make <span class="mark">ready-to-post typography reels</span> in your signature style: hook on frame 0, bold text, animation and voice.</p>'
               '<div class="card"><b>5 reels: ₹199.</b> Trial, delivered in 72 hours.</div><div class="card"><b>30 reels: ₹1,999.</b> A full month of content.</div>'
               '<div class="cta">Order from the link in @freestack.ai\'s Instagram bio.</div>', "k", "Shortcut"))

body = "".join(s.replace("{FOOT}", f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{TITLE} · {i + 1}/{len(S)}</span></div>') for i, s in enumerate(S))
h = OUT / "faceless-blueprint-pro.html"
h.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const f=process.argv[1];await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});await b.close();})();"""
subprocess.run(["node", "-e", js, str(h)], check=True)
print(len(S), "slides")
