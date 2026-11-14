"""30-Day Content System PRO. Reuses the Hook Bank PRO design (CSS + helpers)."""
import pathlib, subprocess
HERE = pathlib.Path(__file__).parent
_src = (HERE / "hooks_pro.py").read_text(encoding="utf-8")
exec(_src[:_src.index("S = []")])  # CSS, slide(), exs(), E, OUT
TITLE = "30-Day Content System PRO"

S = []
S.append(slide('<div style="font:900 300px/0.9 Inter Display;letter-spacing:-12px;margin-top:30px">30<span class="red">.</span></div>'
               '<h1 style="margin-top:0">Din ka Content<br>System <span class="red">PRO</span></h1>'
               '<p class="lead">30 poori likhi hui scripts · weekly format system · ek din mein 7 reels · caption formula · Insights review</p>'
               '<div style="position:absolute;right:70px;bottom:120px;display:flex;align-items:center;gap:18px"><div style="text-align:right;font:800 26px Inter">by @freestack.ai<br><span style="font-weight:600;font-size:22px">30 din, 30 reels ke asli test se bana</span></div><img class="avatar" src="img/pp.jpg"></div>', "y", "Faceless creators ke liye"))

S.append(slide('<h2>Is PDF mein kya hai</h2><table class="tbl">' + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in [
    ("01", "Hamara 30-din test: kya chala, kya toota (asli numbers)"),
    ("02", "Weekly Format System: har din ka format fix"),
    ("03", "Reel ka 4-part structure: seconds ke hisaab se"),
    ("04", "30 poori scripts (Motivation niche), copy-ready"),
    ("05", "Kisi bhi niche mein badalne ka 3-step tareeka"),
    ("06", "Batch Day: ek din mein 7 reels"),
    ("07", "Caption formula + search keywords"),
    ("08", "Har Sunday ka Insights review + double down"),
    ("09", "30-din tracker")]) + "</table>", tag="Andar"))

# 01 data
S.append(slide('<h2>Hamara 30-din test: <span class="red">asli seekh</span></h2>'
               '<p class="small">@freestack.ai pe 30 din, roz 1 reel, same time (12 baje). 17,000+ views. Median 353 views per reel.</p>'
               '<table class="tbl"><tr><th>Seekh</th><th>Data</th></tr>'
               "<tr><td><b>Recap reels sabse aage</b></td><td>Din 7 recap: <span class='good'>1,611</span> (4.6× median). Din 28 recap: <span class='good'>1,434</span> (4.1×)</td></tr>"
               "<tr><td><b>Ek jaisi reels roz = thakaan</b></td><td>Din 12–19 ki 8 mein se 7 reels 400 se neeche</td></tr>"
               "<tr><td><b>Raay/sach wali reel chali</b></td><td>'Kadwa sach' reel: <span class='good'>1,040</span>, bina kisi tool ke</td></tr>"
               "<tr><td><b>Chhoti reel thodi behtar</b></td><td>Duration vs views: halka ulta rishta (Spearman −0.25). Top 2 reels 28 second ki</td></tr>"
               "<tr><td><b>Bolke series tag dena = waste</b></td><td>Har reel ke 2–5 sec 'Day N' bolne mein gaye. Naye viewer ke liye zero value</td></tr>"
               "<tr><td><b>Keyword CTA kaam karta hai</b></td><td>Sabse zyada 'comment keyword' wali reel pe 8 log ne keyword likha</td></tr></table>"
               '<div class="card">Isliye ye system: <b>har hafte formats badlo, har Sunday recap, raay wali reels zaroor, 25–35 second.</b></div>', tag="01 · Proof"))

# 02 weekly system
WK = [("Somvaar", "LIST", "'5 cheezein jo…' Save hoti hai."), ("Mangal", "MYTH", "'Sabse bada jhooth…' Comment aate hain."),
      ("Budh", "STORY", "Kahani + lesson. Sabse lamba rokti hai."), ("Guru", "QUICK TIP", "Ek cheez, aaj hi try karo. Share hoti hai."),
      ("Shukra", "DARD → HAL", "Viewer ki takleef + seedha hal."), ("Shani", "KADWA SACH", "Imaandaar raay. Trust banata hai."),
      ("Ravi", "RECAP / QUIZ", "'Is hafte ki 6 baatein, kitni yaad?' Hamara best format.")]
S.append(slide('<h2>Weekly Format <span class="red">System</span></h2><table class="tbl"><tr><th>Din</th><th>Format</th><th>Kyun</th></tr>'
               + "".join(f"<tr><td class='num'>{a}</td><td><b>{b}</b></td><td>{E(c)}</td></tr>" for a, b, c in WK) + "</table>"
               '<div class="card">Fayde: (1) roz "kya post karu" ka sawaal khatam, (2) audience ko variety milti hai, (3) 4 hafte baad pata chal jaata hai ki aapke niche mein kaunsa format jeetta hai.</div>', tag="02 · System"))

# 03 structure
S.append(slide('<h2>Har reel ka <span class="red">4-part structure</span></h2><table class="tbl"><tr><th>Second</th><th>Part</th><th>Kya karna hai</th></tr>'
               "<tr><td class='num'>0–3</td><td><b>HOOK</b></td><td>Frame 0 pe bada text + wahi line bolo. Intro/logo nahi.</td></tr>"
               "<tr><td class='num'>3–8</td><td><b>TENSION</b></td><td>Problem ko thoda aur khol do: 'aur isi wajah se…'</td></tr>"
               "<tr><td class='num'>8–25</td><td><b>VALUE</b></td><td>Points/kahani. Har 2–3 second mein screen pe kuch naya.</td></tr>"
               "<tr><td class='num'>25–30</td><td><b>PAYOFF + CTA</b></td><td>Ek yaad rehne wali line + ek action (save/comment/follow).</td></tr></table>"
               '<div class="card"><b>Shabd ginti:</b> Hinglish mein hum ~2.5 shabd/second bolte hain, par screen text aur pauses ke saath reel lambi ho jaati hai. <b>50–70 shabd = 25–35 second ki reel.</b> Isse lambi script = beech mein log chhodenge.</div>'
               '<div class="card"><b>Ending trick:</b> "Bye" mat bolo. Aakhri line aisi ho jo pehli line se jud jaaye, taaki reel loop ho aur watch time badhe.</div>', tag="03 · Structure"))

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
        blocks += (f'<div class="card" style="margin:12px 0"><span class="chip">DIN {d}</span><span class="chip" style="background:#111;color:#FFD400">{fmt}</span><span class="chip" style="background:#eee">~{round(words / 2)}s · {words} shabd</span>'
                   f'<p style="margin:8px 0 6px"><b class="red">HOOK:</b> <b>{E(hook)}</b></p><p class="small" style="margin-bottom:6px"><b>BODY:</b> {E(body)}</p><p class="small" style="margin:0"><b>CTA:</b> {E(cta)}</p></div>')
    S.append(slide(f'<h2 style="margin-bottom:8px">Scripts: Din {i + 1}–{i + 2}</h2>' + blocks, tag="04 · 30 Scripts · Motivation"))

# 05 convert
S.append(slide('<h2>Kisi bhi niche mein <span class="red">badlo: 3 step</span></h2>'
               '<div class="card"><b>Step 1, format rakho, topic badlo.</b> "5 cheezein jo strong log nahi karte" → Money: "5 cheezein jo ameer log nahi karte" → Study: "5 cheezein jo toppers nahi karte".</div>'
               '<div class="card"><b>Step 2, apne niche ka dard daalo.</b> Motivation ka dard: aalas. Money ka: salary khatam. Study ka: bhoolna. Facts ka: "ye mujhe pata hona chahiye tha".</div>'
               '<div class="card"><b>Step 3, CTA niche ke hisaab se.</b> Study → "save karo exam ke liye". Money → "is mahine ka hisaab comment karo". Facts → "kisi ko bhejo jo ye nahi jaanta".</div>'
               '<table class="tbl" style="margin-top:14px"><tr><th>Format</th><th>Money</th><th>Study</th></tr>'
               "<tr><td><b>MYTH</b></td><td>Bachat se ameer bante hain</td><td>Zyada padhoge, zyada marks</td></tr>"
               "<tr><td><b>STORY</b></td><td>Same salary, alag result</td><td>3 baar fail, 4thi baar topper</td></tr>"
               "<tr><td><b>KADWA SACH</b></td><td>EMI aapki azaadi kha rahi hai</td><td>Aap padh nahi, dekh rahe ho</td></tr></table>", tag="05 · Convert"))

# 06 batch day
S.append(slide('<h2>Batch Day: <span class="red">ek din, 7 reels</span></h2><table class="tbl"><tr><th>Time</th><th>Kaam</th></tr>'
               "<tr><td class='num'>30 min</td><td>Hafte ke 7 topics chuno (Weekly Format System se)</td></tr>"
               "<tr><td class='num'>60 min</td><td>7 scripts likho (is PDF ka structure, 50–70 shabd each)</td></tr>"
               "<tr><td class='num'>30 min</td><td>Har script ke 3 hooks, best chuno (Hook Score)</td></tr>"
               "<tr><td class='num'>45 min</td><td>Voice record karo, ek saath, ek hi jagah (same sound)</td></tr>"
               "<tr><td class='num'>90 min</td><td>7 reels edit/generate karo (same template, sirf text badlo)</td></tr>"
               "<tr><td class='num'>30 min</td><td>7 captions + cover + schedule</td></tr></table>"
               '<div class="card"><b>Total ~5 ghante = poora hafta free.</b> Roz 1 ghanta dene se bachat: hafte ke 2 ghante, aur sabse badi baat, roz ki tension khatam.</div>', tag="06 · Batch"))

# 07 caption
S.append(slide('<h2>Caption <span class="red">formula</span></h2>'
               '<div class="card"><b>Line 1:</b> hook ka doosra version (feed mein ye dikhta hai).</div>'
               '<div class="card"><b>Line 2–4:</b> reel ka saar, 3 short lines. Jo reel mein jaldi nikal gaya, wo yahan padh lein.</div>'
               '<div class="card"><b>Line 5:</b> ek sawaal ya CTA ("Aap kaunse ho? 1 ya 2").</div>'
               '<div class="card"><b>Keywords:</b> Instagram search caption padhta hai. 2–3 shabd daalo jo log search karte hain: "motivation hindi", "study tips", "paise kaise bachaye".</div>'
               '<div class="card"><b>Hashtags:</b> 3–5, sirf niche wale. 30 hashtags spam lagte hain.</div>'
               '<div class="card" style="border-color:#111"><b>Example:</b> Aap aalsi nahi ho, aapka plan galat hai. 👇<br>Motivation kaam se aati hai, pehle nahi. Aaj sirf 10 minute shuru karo. Baaki dimaag khud karega.<br>Aaj kya shuru kar rahe ho? Comment karo.<br>#motivationhindi #selfimprovement #discipline</div>', tag="07 · Caption"))

# 08 review
S.append(slide('<h2>Har Sunday: <span class="red">15-minute review</span></h2><table class="tbl"><tr><th>Dekho</th><th>Agar…</th><th>Toh…</th></tr>'
               "<tr><td><b>Views</b></td><td>Koi reel median ka 2× ya zyada</td><td>Usi idea ke 3 naye versions agle hafte</td></tr>"
               "<tr><td><b>Skip rate / 3-sec hold</b></td><td>Zyada log pehle 3 sec mein gaye</td><td>Hook + frame 0 badlo (Hook Bank PRO)</td></tr>"
               "<tr><td><b>Avg watch time</b></td><td>Reel ke aadhe se kam</td><td>Script chhoti karo, 50 shabd ke aas-paas</td></tr>"
               "<tr><td><b>Shares/sends</b></td><td>Kisi format pe zyada</td><td>Wo format hafte mein 2 baar</td></tr>"
               "<tr><td><b>Follows</b></td><td>Views zyada, follows kam</td><td>Profile, bio aur pinned reels theek karo</td></tr></table>"
               '<div class="card">Ek reel pe faisla mat lo. Hafte ke 7 reels ka average dekho. Hamare data mein bhi ek hi format ke views 150 se 1,600 tak gaye.</div>', tag="08 · Review"))

# 09 tracker
tr = "".join(f"<tr><td class='num'>{d:02d}</td><td>{WK[(d - 1) % 7][1]}</td><td></td><td></td><td></td><td></td></tr>" for d in range(1, 16))
S.append(slide(f'<h2>Tracker: Din 1–15</h2><table class="tbl"><tr><th>Din</th><th>Format</th><th>Views</th><th>Watch</th><th>Shares</th><th>Follows</th></tr>{tr}</table>', tag="09 · Tracker"))
tr = "".join(f"<tr><td class='num'>{d:02d}</td><td>{WK[(d - 1) % 7][1]}</td><td></td><td></td><td></td><td></td></tr>" for d in range(16, 31))
S.append(slide(f'<h2>Tracker: Din 16–30</h2><table class="tbl"><tr><th>Din</th><th>Format</th><th>Views</th><th>Watch</th><th>Shares</th><th>Follows</th></tr>{tr}</table>', tag="09 · Tracker"))

S.append(slide('<h2>Scripts ready. <span class="red">Reels banane ka time nahi?</span></h2>'
               '<p class="lead">Ye 30 scripts bhejo, ya apni. Hum <span class="mark">ready-to-post typography reels</span> banate hain: bold text, animation aur voice ke saath.</p>'
               '<div class="card"><b>5 reels: ₹199.</b> Trial, 72 ghante mein delivery.</div><div class="card"><b>30 reels: ₹1,999.</b> Poore mahine ka content.</div>'
               '<div class="cta">Instagram pe @freestack.ai ke bio link se order karo.</div>', "k", "Shortcut"))

body = "".join(s.replace("{FOOT}", f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{TITLE} · {i + 1}/{len(S)}</span></div>') for i, s in enumerate(S))
h = OUT / "content-system-pro.html"
h.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const f=process.argv[1];await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});await b.close();})();"""
subprocess.run(["node", "-e", js, str(h)], check=True)
print(len(S), "slides")
