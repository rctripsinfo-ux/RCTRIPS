"""30-Day Content System PRO. Reuses the Hook Bank PRO design (CSS + helpers)."""
import pathlib, subprocess
HERE = pathlib.Path(__file__).parent
_src = (HERE / "hooks_pro.py").read_text(encoding="utf-8")
exec(_src[:_src.index("S = []")])  # CSS, slide(), exs(), E, OUT
TITLE = "30-Day Content System PRO"

S = []
S.append(slide('<div style="font:900 300px/0.9 Inter Display;letter-spacing:-12px;margin-top:30px">30<span class="red">.</span></div>'
               '<h1 style="margin-top:0">Day Content<br>System <span class="red">PRO</span></h1>'
               '<p class="lead">30 fully written scripts · weekly format system · 7 reels in one day · caption formula · Insights review</p>'
               '<div style="position:absolute;right:70px;bottom:120px;display:flex;align-items:center;gap:18px"><div style="text-align:right;font:800 26px Inter">by @freestack.ai<br><span style="font-weight:600;font-size:22px">Built from a real 30-day, 30-reel test</span></div><img class="avatar" src="img/pp.jpg"></div>', "y", "For faceless creators"))

S.append(slide('<h2>What\'s inside</h2><table class="tbl">' + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in [
    ("01", "Our 30-day test: what worked, what broke (real numbers)"),
    ("02", "Weekly Format System: a fixed format for every day"),
    ("03", "The 4-part reel structure, second by second"),
    ("04", "30 complete scripts (Motivation niche), ready to use"),
    ("05", "How to convert them to any niche in 3 steps"),
    ("06", "Batch Day: 7 reels in one day"),
    ("07", "Caption formula + search keywords"),
    ("08", "Weekly Sunday Insights review + double down"),
    ("09", "30-day tracker")]) + "</table>", tag="Contents"))

# 01 data
S.append(slide('<h2>Our 30-day test: <span class="red">real lessons</span></h2>'
               '<p class="small">@freestack.ai: 30 days, 1 reel a day, same time (12 noon). 17,000+ views. Median: 353 views per reel.</p>'
               '<table class="tbl"><tr><th>Lesson</th><th>Data</th></tr>'
               "<tr><td><b>Recap reels win</b></td><td>Day 7 recap: <span class='good'>1,611</span> (4.6× median). Day 28 recap: <span class='good'>1,434</span> (4.1×)</td></tr>"
               "<tr><td><b>Same format every day = fatigue</b></td><td>7 of the 8 reels on days 12–19 got under 400 views</td></tr>"
               "<tr><td><b>Opinion reels work</b></td><td>The 'kadwa sach' (hard truth) reel: <span class='good'>1,040</span>, without featuring any tool</td></tr>"
               "<tr><td><b>Shorter is slightly better</b></td><td>Duration vs views: weak negative link (Spearman −0.25). Top 2 reels were 28 seconds</td></tr>"
               "<tr><td><b>Saying the series tag wastes time</b></td><td>Each reel spent 2–5 sec saying 'Day N'. Zero value for new viewers</td></tr>"
               "<tr><td><b>Keyword CTAs work</b></td><td>The best keyword-CTA reel got 8 people commenting the keyword</td></tr></table>"
               '<div class="card">That is why this system: <b>rotate formats every week, recap every Sunday, always include opinion reels, keep reels 25–35 seconds.</b></div>', tag="01 · Proof"))

# 02 weekly system
WK = [("Mon", "LIST", "'5 things that…' Gets saved."), ("Tue", "MYTH", "'The biggest lie…' Gets comments."),
      ("Wed", "STORY", "Story + lesson. Holds attention longest."), ("Thu", "QUICK TIP", "One thing to try today. Gets shared."),
      ("Fri", "PAIN → FIX", "The viewer's problem + a direct fix."), ("Sat", "HARD TRUTH", "An honest opinion. Builds trust."),
      ("Sun", "RECAP / QUIZ", "'6 lessons this week, how many do you remember?' Our best format.")]
S.append(slide('<h2>Weekly Format <span class="red">System</span></h2><table class="tbl"><tr><th>Day</th><th>Format</th><th>Why</th></tr>'
               + "".join(f"<tr><td class='num'>{a}</td><td><b>{b}</b></td><td>{E(c)}</td></tr>" for a, b, c in WK) + "</table>"
               '<div class="card">Benefits: (1) no more "what should I post today?", (2) your audience gets variety, (3) after 4 weeks you know which format wins in your niche.</div>', tag="02 · System"))

# 03 structure
S.append(slide('<h2>The <span class="red">4-part structure</span> of every reel</h2><table class="tbl"><tr><th>Seconds</th><th>Part</th><th>What to do</th></tr>'
               "<tr><td class='num'>0–3</td><td><b>HOOK</b></td><td>Big text on frame 0 + say the same line. No intro or logo.</td></tr>"
               "<tr><td class='num'>3–8</td><td><b>TENSION</b></td><td>Open the problem a little more: 'and that is exactly why…'</td></tr>"
               "<tr><td class='num'>8–25</td><td><b>VALUE</b></td><td>Points or story. Something new on screen every 2–3 seconds.</td></tr>"
               "<tr><td class='num'>25–30</td><td><b>PAYOFF + CTA</b></td><td>One memorable line + one action (save/comment/follow).</td></tr></table>"
               '<div class="card"><b>Word count:</b> we speak about 2.5 words per second in Hinglish, but on-screen text and pauses make reels longer. <b>50–70 words = a 25–35 second reel.</b> Longer scripts lose viewers in the middle.</div>'
               '<div class="card"><b>Ending trick:</b> don\'t say "Bye". Make the last line connect back to the first, so the reel loops and watch time goes up.</div>', tag="03 · Structure"))

# 04 scripts
SC = [
 ("LIST", "Agar aap 20s mein ho, toh ye 3 galtiyan abhi rok do.", "Pehli: sabko khush rakhna. Jo sabko khush rakhta hai, wo khud ko bhool jaata hai. Doosri: paisa bachana, par seekhne pe kharch na karna. Teesri: 'kal se pakka.' Kal kabhi nahi aata.", "Inme se ek bhi aap kar rahe ho? Comment mein number likho."),
 ("MYTH", "Sabse bada jhooth: 'motivation aayegi, tab shuru karunga.'", "Motivation kaam shuru karne se aati hai, pehle nahi. Jo log roz kaam karte hain, unka mood bhi kharab hota hai. Farak ye hai ki wo mood ka intezaar nahi karte.", "Aaj bas 10 minute shuru karo. Motivation khud aa jayegi."),
 ("STORY", "Ek ladka roz library jaata tha, par kuch padhta nahi tha.", "Wo bas baith ke phone chalata tha. Ek din library wale uncle ne kaha: 'Beta, jagah badalne se aadat nahi badalti.' Usne us din phone ghar pe chhoda. 6 mahine baad wo apne batch mein top pe tha.", "Jagah nahi, aadat badlo. Ye kisi ko bhejo jise zaroorat hai."),
 ("QUICK TIP", "Kaam taal dete ho? Ye 2-minute rule try karo.", "Jo kaam 2 minute mein ho sakta hai, wo abhi karo. Jo bada hai, uska sirf pehla 2 minute karo. Shuru karna hi sabse mushkil hissa hai. Ek baar shuru ho gaye, toh dimaag rukne nahi deta.", "Aaj ek kaam pe try karke batao."),
 ("DARD → HAL", "Subah uthte hi thakaan? Problem neend nahi, phone hai.", "Raat ko aakhri cheez phone, subah pehli cheez phone. Dimaag ko aaram milta hi nahi. Hal: sone se 30 minute pehle phone door, aur uthke 30 minute baad tak bhi.", "7 din karke dekho. Farak khud bataoge."),
 ("KADWA SACH", "Kadwa sach: koi aapko bachane nahi aayega.", "Na koi dost, na koi rishtedaar, na koi lucky break. Jo bhi badlega, aapke kaam se badlega. Ye sunke bura lagta hai, par yahi azaadi hai: aapki zindagi ka remote aapke haath mein hai.", "Sehmat ho? Save karo, roz yaad aayega."),
 ("RECAP", "Is hafte ki 6 baatein. Kitni yaad hain?", "20s ki 3 galtiyan. Motivation ka jhooth. Jagah nahi, aadat badlo. 2-minute rule. Phone aur thakaan. Koi bachane nahi aayega.", "Kitni yaad thi? Comment mein number. Agle hafte aur."),
 ("LIST", "Ye 4 aadatein chupke se aapka time kha rahi hain.", "Bina wajah notifications check karna. Har kaam ek saath karna. 'Bas 5 minute' wali reels. Aur bina plan ke din shuru karna. Inme se ek bhi chhodi, toh roz ek ghanta wapas.", "Kaunsi aadat aapki hai? Number likho."),
 ("MYTH", "Myth: zyada mehnat = zyada success.", "Galat direction mein zyada mehnat, aapko aur door le jaati hai. Pehle 10 minute socho ki kya karna hai, phir 10 ghante lagao. Smart kaam pehle, hard kaam baad mein.", "Aaj ka sabse zaroori ek kaam kya hai? Likho."),
 ("STORY", "Ek company ne 100 logon ko interview kiya. Job ek ko mili.", "Sabke paas degree thi. Sabke paas experience tha. Jise mili, usne bas ek sawaal poocha: 'Main pehle 30 din mein aapke liye kya theek kar sakta hoon?' Baaki sab apne baare mein bol rahe the.", "Apne baare mein kam, unke kaam ke baare mein zyada. Save karo."),
 ("QUICK TIP", "Roz ek ghanta bachane ka sabse boring tareeka.", "Raat ko kal ke 3 sabse zaroori kaam likh lo. Bas 3. Subah uthke sochna nahi padega ki kya karna hai. Decision lene mein jo energy jaati hai, wo kaam mein lagegi.", "Aaj raat try karo. Kal batana."),
 ("DARD → HAL", "Sab kuch try kar liya, phir bhi kuch nahi badla?", "Kyunki aapne sab kuch 3 din ke liye try kiya. Koi bhi aadat 3 din mein result nahi deti. Ek cheez chuno, aur 30 din usi pe tikke raho. Result 21ve din ke baad dikhna shuru hota hai.", "Kaunsi ek cheez 30 din karoge? Comment mein likho."),
 ("KADWA SACH", "Kadwa sach: aap busy nahi ho, distracted ho.", "Screen time check karo. Agar 4 ghante phone pe hain, toh time ki kami nahi hai. Busy hona aur bikhra hona alag hai. Busy log 'na' bolna jaante hain.", "Apna screen time comment mein likho. Imaandaari se."),
 ("RECAP", "Do hafte, 12 baatein. Top 3 kaunsi thi?", "Time khane wali aadatein. Smart kaam pehle. Interview wala sawaal. Kal ke 3 kaam. 30 din ka rule. Busy vs distracted.", "Aapki top 3 comment karo. Hum agle hafte unpe aur banayenge."),
 ("LIST", "Paise ke 3 rules jo school mein nahi sikhaye.", "Ek: pehle khud ko pay karo. Salary aate hi bachat alag. Doosra: jo cheez roz use nahi hoti, use EMI pe mat lo. Teesra: seekhne pe kharch, kharch nahi, investment hai.", "Inme se kaunsa rule aaj se shuru? Batao."),
 ("MYTH", "Myth: 'sahi time aane do, phir shuru karunga.'", "Sahi time kabhi nahi aata. Jo log shuru karte hain, wo bhi darr ke saath shuru karte hain. Farak bas itna hai ki wo shuru karte hain. Perfect plan ka intezaar = zero progress.", "Jo kaam taal rahe ho, uska naam comment karo. Aaj shuru."),
 ("STORY", "Ek student 3 baar fail hua. Chauthi baar topper bana.", "Pehli teen baar wo zyada padhta tha. Chauthi baar usne kam padha, par har din revise kiya. Usne samjha ki problem padhna nahi, bhoolna thi.", "Aap padh rahe ho ya revise kar rahe ho? Save karo."),
 ("QUICK TIP", "Ye ek sawaal har faisle se pehle poocho.", "'5 saal baad isse kya farak padega?' Agar farak nahi padega, toh 5 minute se zyada mat socho. Agar padega, toh 5 din socho. Chhoti cheezon pe energy mat jalao.", "Ye sawaal kisi aise dost ko bhejo jo overthink karta hai."),
 ("DARD → HAL", "Log aapki baat beech mein kaat dete hain?", "Shayad aap shuru mein hi lamba bolte ho. Pehle main point bolo, phir detail. Jaise news: headline pehle, kahani baad mein. Log sunte hi rahenge.", "Agli baatcheet mein try karo. Farak dikhega."),
 ("KADWA SACH", "Kadwa sach: jo aapko roz 5 ghante leta hai, wo hobby nahi hai.", "Wo aadat hai. Aur aadat aapko bana bhi sakti hai, bigaad bhi sakti hai. Gaming, scrolling, ya kuch bhi. Sawaal ye nahi ki bura hai ya achha. Sawaal ye hai: kya aap control mein ho?", "Aapki 5-ghante wali cheez kya hai? Sach batao."),
 ("RECAP", "Teen hafte, 18 baatein. Aap kitne aage aaye?", "Paise ke 3 rules. Sahi time kabhi nahi aata. Revise karo, sirf padho mat. 5 saal wala sawaal. Pehle main point. Hobby vs aadat.", "1 se 10 mein apni progress likho. Imaandaari se."),
 ("LIST", "5 cheezein jo strong log kabhi nahi karte.", "Har baat pe sorry nahi bolte. Doosron se apni tulna nahi karte. Har kisi ko jawab nahi dete. Apni galti chhupaate nahi. Aur haar ke baad rukte nahi.", "Inme se kaunsi aapko mushkil lagti hai?"),
 ("MYTH", "Myth: akele rehna = kamzor hona.", "Akele rehna aur akela mehsoos karna alag hai. Jo log akele time bita sakte hain, wo apni soch saaf rakhte hain. Bheed mein shor hai, akele mein jawab.", "Aap hafte mein kitna time khud ke saath bitaate ho?"),
 ("STORY", "Ek boodhe aadmi ne roz ek ped lagaya.", "Log haste the: 'Aap iske phal kabhi nahi khaoge.' Wo muskuraya: 'Main bhi kisi aur ke lagaye ped ke phal kha raha hoon.' Aaj us gaon mein sabse zyada chhaanv hai.", "Aaj aap kaunsa 'ped' laga rahe ho? Batao."),
 ("QUICK TIP", "Gussa aaye toh ye 10-second trick.", "Bolne se pehle 10 tak gino, aur ek lambi saans lo. Gussa ka sabse tez hissa 10 second ka hota hai. Usse nikal gaye, toh jo bologe wo soch ke bologe.", "Kisi ko bhejo jise iski zaroorat hai. 😄"),
 ("DARD → HAL", "Har din ek jaisa lagta hai? Ye karo.", "Roz ek chhoti si nayi cheez karo. Naya raasta, naya gaana, ek naya insaan se baat. Dimaag ko naya pan chahiye. Bade badlaav nahi, chhote experiments.", "Aaj kaunsa chhota naya kaam karoge?"),
 ("KADWA SACH", "Kadwa sach: sab log aapko pasand nahi karenge.", "Aur ye theek hai. Agar sab aapko pasand karte hain, toh shayad aap kisi baat pe khade nahi ho. Sahi log aapko aapki sachai ke liye pasand karenge.", "Sehmat ho? Kisi aise dost ko tag karo."),
 ("RECAP", "4 hafte, 24 baatein. Ye rahi top 5.", "Motivation kaam se aati hai. Kal ke 3 kaam. 30 din ka rule. 5 saal wala sawaal. Sab aapko pasand nahi karenge.", "Is mahine ki aapki sabse badi seekh kya thi?"),
 ("LIST", "Agle 30 din ke liye 3 chhote vaade.", "Roz 10 minute kuch seekhna. Roz 10 minute bina phone ke. Roz ek kaam jo kal pe taal rahe the. Bas itna. Bade sapne nahi, chhote vaade.", "Comment mein 'IN' likho agar aap saath ho."),
 ("KADWA SACH", "30 din pehle aap jo the, aaj bhi wahi ho?", "Agar haan, toh koi baat nahi. Bas ek cheez badlo. Agar nahi, toh khud ko shabaashi do. Badlaav chhota hota hai, isliye dikhta nahi. Par jud ke bada ho jaata hai.", "Follow karo. Agla mahina aur gehra."),
]
for i in range(0, 30, 2):
    blocks = ""
    for d, (fmt, hook, body, cta) in enumerate(SC[i:i + 2], i + 1):
        words = len((hook + " " + body + " " + cta).split())
        blocks += (f'<div class="card" style="margin:12px 0"><span class="chip">DAY {d}</span><span class="chip" style="background:#111;color:#FFD400">{fmt}</span><span class="chip" style="background:#eee">~{round(words / 2)}s · {words} words</span>'
                   f'<p style="margin:8px 0 6px"><b class="red">HOOK:</b> <b>{E(hook)}</b></p><p class="small" style="margin-bottom:6px"><b>BODY:</b> {E(body)}</p><p class="small" style="margin:0"><b>CTA:</b> {E(cta)}</p></div>')
    S.append(slide(f'<h2 style="margin-bottom:8px">Scripts: Day {i + 1}–{i + 2}</h2>' + blocks, tag="04 · 30 Scripts · Motivation"))

# 05 convert
S.append(slide('<h2>Convert to any niche <span class="red">in 3 steps</span></h2>'
               '<div class="card"><b>Step 1, keep the format, change the topic.</b> "5 cheezein jo strong log nahi karte" → Money: "5 cheezein jo ameer log nahi karte" → Study: "5 cheezein jo toppers nahi karte".</div>'
               '<div class="card"><b>Step 2, swap in your niche\'s pain.</b> Motivation: laziness. Money: salary runs out. Study: forgetting. Facts: "I should have known this".</div>'
               '<div class="card"><b>Step 3, match the CTA to the niche.</b> Study → "save karo exam ke liye". Money → "is mahine ka hisaab comment karo". Facts → "kisi ko bhejo jo ye nahi jaanta".</div>'
               '<table class="tbl" style="margin-top:14px"><tr><th>Format</th><th>Money</th><th>Study</th></tr>'
               "<tr><td><b>MYTH</b></td><td>Bachat se ameer bante hain</td><td>Zyada padhoge, zyada marks</td></tr>"
               "<tr><td><b>STORY</b></td><td>Same salary, alag result</td><td>3 baar fail, 4thi baar topper</td></tr>"
               "<tr><td><b>HARD TRUTH</b></td><td>EMI aapki azaadi kha rahi hai</td><td>Aap padh nahi, dekh rahe ho</td></tr></table>", tag="05 · Convert"))

# 06 batch day
S.append(slide('<h2>Batch Day: <span class="red">one day, 7 reels</span></h2><table class="tbl"><tr><th>Time</th><th>Task</th></tr>'
               "<tr><td class='num'>30 min</td><td>Pick the week's 7 topics (from the Weekly Format System)</td></tr>"
               "<tr><td class='num'>60 min</td><td>Write 7 scripts (this PDF's structure, 50–70 words each)</td></tr>"
               "<tr><td class='num'>30 min</td><td>Write 3 hooks per script, pick the best (Hook Score)</td></tr>"
               "<tr><td class='num'>45 min</td><td>Record all voiceovers together, in one place (same sound)</td></tr>"
               "<tr><td class='num'>90 min</td><td>Edit/generate 7 reels (same template, only the text changes)</td></tr>"
               "<tr><td class='num'>30 min</td><td>7 captions + covers + scheduling</td></tr></table>"
               '<div class="card"><b>About 5 hours = the whole week done.</b> Compared to 1 hour every day you save about 2 hours a week, and more importantly, the daily stress is gone.</div>', tag="06 · Batch"))

# 07 caption
S.append(slide('<h2>Caption <span class="red">formula</span></h2>'
               '<div class="card"><b>Line 1:</b> a second version of the hook (this is what shows in the feed).</div>'
               '<div class="card"><b>Lines 2–4:</b> the reel\'s summary in 3 short lines, so people can read what went by fast.</div>'
               '<div class="card"><b>Line 5:</b> a question or CTA ("Aap kaunse ho? 1 ya 2").</div>'
               '<div class="card"><b>Keywords:</b> Instagram search reads captions. Add 2–3 phrases people search for: "motivation hindi", "study tips", "paise kaise bachaye".</div>'
               '<div class="card"><b>Hashtags:</b> 3–5, niche-specific only. 30 hashtags look like spam.</div>'
               '<div class="card" style="border-color:#111"><b>Example:</b> Aap aalsi nahi ho, aapka plan galat hai. 👇<br>Motivation kaam se aati hai, pehle nahi. Aaj sirf 10 minute shuru karo. Baaki dimaag khud karega.<br>Aaj kya shuru kar rahe ho? Comment karo.<br>#motivationhindi #selfimprovement #discipline</div>', tag="07 · Caption"))

# 08 review
S.append(slide('<h2>Every Sunday: <span class="red">15-minute review</span></h2><table class="tbl"><tr><th>Check</th><th>If…</th><th>Then…</th></tr>'
               "<tr><td><b>Views</b></td><td>A reel gets 2× your median or more</td><td>Make 3 new versions of that idea next week</td></tr>"
               "<tr><td><b>Skip rate / 3-sec hold</b></td><td>Many people leave in the first 3 sec</td><td>Change the hook + frame 0 (Hook Bank PRO)</td></tr>"
               "<tr><td><b>Avg watch time</b></td><td>Less than half the reel</td><td>Cut the script to about 50 words</td></tr>"
               "<tr><td><b>Shares/sends</b></td><td>One format gets more shares</td><td>Post that format twice a week</td></tr>"
               "<tr><td><b>Follows</b></td><td>High views, low follows</td><td>Fix your profile, bio and pinned reels</td></tr></table>"
               '<div class="card">Never decide based on one reel. Use the average of the week\'s 7 reels. In our data, the same format ranged from 150 to 1,600 views.</div>', tag="08 · Review"))

# 09 tracker
tr = "".join(f"<tr><td class='num'>{d:02d}</td><td>{WK[(d - 1) % 7][1]}</td><td></td><td></td><td></td><td></td></tr>" for d in range(1, 16))
S.append(slide(f'<h2>Tracker: Day 1–15</h2><table class="tbl"><tr><th>Day</th><th>Format</th><th>Views</th><th>Watch</th><th>Shares</th><th>Follows</th></tr>{tr}</table>', tag="09 · Tracker"))
tr = "".join(f"<tr><td class='num'>{d:02d}</td><td>{WK[(d - 1) % 7][1]}</td><td></td><td></td><td></td><td></td></tr>" for d in range(16, 31))
S.append(slide(f'<h2>Tracker: Day 16–30</h2><table class="tbl"><tr><th>Day</th><th>Format</th><th>Views</th><th>Watch</th><th>Shares</th><th>Follows</th></tr>{tr}</table>', tag="09 · Tracker"))

S.append(slide('<h2>Scripts ready. <span class="red">No time to make the reels?</span></h2>'
               '<p class="lead">Send us these 30 scripts, or your own. We make <span class="mark">ready-to-post typography reels</span>: bold text, animation and voice.</p>'
               '<div class="card"><b>5 reels: ₹199.</b> Trial, delivered in 72 hours.</div><div class="card"><b>30 reels: ₹1,999.</b> A full month of content.</div>'
               '<div class="cta">Order from the link in @freestack.ai\'s Instagram bio.</div>', "k", "Shortcut"))

body = "".join(s.replace("{FOOT}", f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{TITLE} · {i + 1}/{len(S)}</span></div>') for i, s in enumerate(S))
h = OUT / "content-system-pro.html"
h.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const f=process.argv[1];await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});await b.close();})();"""
subprocess.run(["node", "-e", js, str(h)], check=True)
print(len(S), "slides")
