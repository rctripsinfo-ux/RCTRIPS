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
    return "".join(f'<div class="ba"><div class="b"><span class="lbl">❌ PEHLE</span>{E(b)}</div><div class="a"><span class="lbl">✅ BAAD MEIN</span>{E(a)}</div></div>' for b, a in pairs)


S = []

# 1 cover
S.append(slide('<div style="font:900 300px/0.9 Inter Display;letter-spacing:-12px;margin-top:30px">120<span class="red">+</span></div>'
               '<h1 style="margin-top:0">Viral Hinglish<br>Hooks <span class="red">PRO</span></h1>'
               '<p class="lead">14 asli reels ka teardown · 12 hook types · 20 before/after · pehle 3 second ka system</p>'
               '<div style="position:absolute;right:70px;bottom:120px;display:flex;align-items:center;gap:18px"><div style="text-align:right;font:800 26px Inter">by @freestack.ai<br><span style="font-weight:600;font-size:22px">17,000+ views ke data se bana</span></div><img class="avatar" src="img/pp.jpg"></div>', "y", "Faceless creators ke liye"))

# 2 contents
S.append(slide('<h2>Is PDF mein kya hai</h2><table class="tbl">'
               + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in [
                   ("01", "Asli reels ka teardown: 8 winners vs 6 flops, screenshots ke saath"),
                   ("02", "Instagram reel ko aage kaise bhejta hai (simple bhasha mein)"),
                   ("03", "3-Layer Hook: text + aawaz + visual ek saath"),
                   ("04", "Hook Score: post karne se pehle 10-point test"),
                   ("05", "Hook fail hone ke 10 kaaran"),
                   ("06", "Screen pe hook kaise likhein (typography rules)"),
                   ("07", "12 hook types: psychology + template + examples"),
                   ("08", "20 before → after rewrites"),
                   ("09", "7 niches × 10 ready hooks (bina blank)"),
                   ("10", "Hook ke baad kya bolein: A.R.C.S. formula"),
                   ("11", "Hook testing aur 'double down' system"),
                   ("12", "7-din ka hook practice plan")]) + "</table>", tag="Andar"))

# 3 story + teardowns
S.append(slide('<div style="display:flex;gap:30px;align-items:center;margin-top:24px"><img class="avatar" src="img/pp.jpg"><div><h2 style="margin:0">Ye PDF kaise bani</h2><p class="small">@freestack.ai · faceless AI-tools page</p></div></div>'
    '<p class="lead" style="margin-top:30px">Maine 30 din tak roz ek reel daali. Same design, same voice, same length. <b>Farak sirf hook ka tha.</b></p>'
    '<div class="card"><b>Result:</b> 17,000+ views. Sabse achhi reel <b>1,645</b>, sabse kharab <b>140</b>. Ek hi page pe <b>11× ka farak</b>, sirf pehli line se.</div>'
    '<div class="card">Is PDF mein wahi hai jo maine data se seekha: kaunse hooks chale, kaunse flop hue, aur kyun. Aage ke pages mein asli reels ka teardown hai.</div>'
    '<p class="small" style="margin-top:14px">Sach batau toh ye ek chhota page hai, koi celebrity nahi. Isliye ye seekh aapke kaam ki hai: aap bhi isi stage pe ho.</p>', tag="Meri kahani"))
WIN=[("05","1,645","Google ne apna AI agent free mein de diya, aur bahut kam log jaante hain.",["Badi brand","Secret","Free"],"Google ka naam = bharosa. 'Kam log jaante hain' = andar ki baat. Viewer ko laga wo kuch miss kar raha hai."),
("07","1,611","Ek hafte mein 5 mehenge AI tools ke free versions. Kitne yaad hain?",["Recap","Quiz","List"],"Sabse chhoti reel (28s). Quiz ne khel bana diya, aur list hone se save hui."),
("04","1,593","Coding ke liye Cursor ka subscription? Ruk jao.",["Ruk jao","Paisa","Badi brand"],"Jis tool ke log paise dete hain, uska naam + seedha order. Sabse zyada likes (49) isi pe aaye."),
("28","1,434","Teen hafton mein itne free versions. Kitne yaad hain?",["Recap","Quiz"],"Doosra recap, doosri baar top 5. Ye format luck nahi, pattern hai."),
("11","1,182","Sirf likho, aur AI video bana dega.",["Result pehle","Wow"],"6 shabd, aur result dimaag mein turant dikh gaya. Samajhne ke liye sochna nahi pada."),
("09","1,102","AI voiceover ke liye har mahine paise de rahe ho?",["Dard","Paisa","Sawaal"],"Creators ka asli kharcha pakda. Sawaal pe viewer ne mann mein 'haan' bola."),
("27","1,093","Purani blurry video ko 4K mein badlo, free.",["Result pehle","Emotion"],"Purani family videos = emotion. Before/after dimaag mein bana."),
("29","1,040","Ye 'free' AI tools sach mein free hain? Ek kadwa sach sun lo.",["Kadwa sach","Trust"],"Koi tool nahi, sirf ek imaandaar raay. Audience ko imaandaari pasand aayi.")]
LOSE=[("24","140","AI ko apni files, GitHub aur apps se jodo, ek standard tareeke se.",["Confusing","Jargon"],"Na dard, na result. 'Standard tareeka' kisi ko nahi chahiye."),
("19","144","Manus AI ka waitlist aur credits bhool jao.",["Unknown naam"],"Maan liya ki log Manus jaante hain. Nahi jaante the."),
("22","144","Ek AI employee, jo kabhi chhutti nahi leta.",["Vague","Ghisa-pita"],"Sunne mein achha, par kya karta hai? Kuch saaf nahi."),
("16","151","Koi bhi article, aur do AI hosts uspe podcast karenge.",["Lamba","Low stakes"],"Lambi line, aur jis tool ka alternative tha wo pehle se free hai."),
("18","153","Google se smart search, jo seedha jawab de.",["Feature only"],"Feature bataya, dard nahi. Kyun rukun?"),
("13","175","Midjourney level AI images, zero rupaye mein.",["Purani khabar"],"Free AI images ab har phone mein hain. 'Free' ab news nahi.")]
def tdw(items, cls, sm=False):
    return "".join(f'<div class="td{" sm" if sm else ""}"><img src="img/{c}.jpg"><div><span class="views {cls}">{v} views</span><div class="hq">"{E(h)}"</div>'+"".join(f'<span class="chip">{E(t)}</span>' for t in tags)+f'<p class="why">{E(w)}</p></div></div>' for c,v,h,tags,w in items)
for i in range(0,8,2):
    S.append(slide(f'<h2 style="margin-bottom:6px">Teardown: <span class="good">kyun chali</span> ({i//2+1}/4)</h2>'+tdw(WIN[i:i+2],"g"), tag="01 · Asli reels"))
for i in range(0,6,3):
    S.append(slide(f'<h2 style="margin-bottom:6px">Teardown: <span class="bad">kyun flop hui</span> ({i//3+1}/2)</h2>'+tdw(LOSE[i:i+3],"l",True), tag="01 · Asli reels"))
S.append(slide('<h2>8 winners vs 6 flops: <span class="red">pattern</span></h2>'
    '<div class="card"><b>Jeetne wale hooks ne kiya:</b><br>✅ aisi cheez ka naam liya jiske log paise dete hain<br>✅ viewer ko seedha challenge ya sawaal kiya<br>✅ quiz/recap ka khel banaya<br>✅ result ek line mein dikha diya</div>'
    '<div class="card" style="border-color:#111"><b>Flop hooks ne kiya:</b><br>❌ sirf feature bataya<br>❌ anjaan naam liya<br>❌ jargon ("standard", "protocol")<br>❌ "free" bola jahan free ab normal hai</div>'
    '<p class="lead" style="margin-top:20px">Agle pages mein ye pattern ek system mein badla gaya hai, jo kisi bhi niche mein chalega.</p>', "y", "01 · Pattern"))

# 4 algorithm
S.append(slide('<h2>Instagram reel ko <span class="red">aage kaise bhejta hai</span></h2>'
               '<div class="card"><b>Step 1:</b> Reel pehle thode logon ko dikhti hai (followers + kuch naye log).</div>'
               '<div class="card"><b>Step 2:</b> Wo log ruke? Poori dekhi? Like kiya? Kisi ko bheji? Agar haan, toh reel naye logon tak jaati hai.</div>'
               '<div class="card"><b>Step 3:</b> Naye log bhi wahi karein, toh aur aage. Yahi "viral" hai.</div>'
               '<p style="margin-top:20px">Instagram ke head <b>Adam Mosseri</b> ne publicly bataya hai ki reels ke sabse bade signals hain: <span class="mark">watch time</span>, <span class="mark">likes per reach</span> aur <span class="mark">sends per reach</span> (DM mein share).</p>'
               '<p><b>Matlab:</b> hook ka kaam sirf rokna nahi, <b>sahi insaan ko rokna</b> hai, jo poori dekhe aur bheje. Clickbait se log rukte hain, par jaldi bhaagte hain, aur reel wahin ruk jaati hai.</p>', tag="02 · Algorithm"))

# 5 three layer
S.append(slide('<h2>3-Layer Hook: <span class="red">teeno ek hi baat bolein</span></h2>'
               '<div class="two"><div><h3>1. Text (screen)</h3><p class="small">3–7 bade shabd. Pehle frame pe, 0.0 second se.</p><h3>2. Aawaz (pehli line)</h3><p class="small">Wahi baat, bolne ke andaaz mein. "Hi guys" ya intro nahi.</p><h3>3. Visual</h3><p class="small">Result, chehre ka reaction, ya kuch hota hua (cup ka crush hona type). Khaali screen nahi.</p></div>'
               '<div style="display:flex;gap:16px;justify-content:center"><div class="phone bad2"><p class="small" style="opacity:.5">pastel bg</p><p class="small"><b>khaali mockup</b></p><p class="small" style="opacity:.5">mascot 4 sec baad</p></div></div></div>'
               '<div class="card"><b>Hamari galti (data se):</b> hamare covers bahut achhe the: laal-peela, mascot, "₹0". Par reel ka <b>pehla frame</b> halka pastel aur khaali mockup tha. Feed mein log cover nahi, <b>frame 0</b> dekhte hain. Lesson: cover design ko hi reel ka pehla frame banao.</div>'
               '<div class="card"><b>Doosri galti:</b> har reel ke 2–5 second "Subscription band karo, Day N" bolne mein gaye. Naye viewer ke liye zero value. Series ka naam chhota sa screen pe likho, bolo mat.</div>', tag="03 · Pehle 3 second"))

# 6 hook score
crit = [("Kam shabd", "Magazine headline jaisa. 3 second mein padh lo."), ("Page se juda", "Topic aapke page ka ho, warna clickbait lagega."),
        ("Ulti soch", "Jo sab maante hain, use hilaye."), ("Aasaan", "Sochna na pade ki matlab kya hai."), ("Bilkul flat nahi", "Thoda dimaag lagaye, warna ignore."),
        ("Curiosity", "Jawab video ke andar ho, hook mein nahi."), ("Original", "Har jagah dikhne wala hook kaam nahi karta."),
        ("Jaana-pehchana + naya", "Famous cheez + ek twist (Google + free)."), ("3-second test", "Dost ko 3 second dikhao, wo bata de topic kya hai."),
        ("Dard ka hal", "Viewer ki asli takleef ka ishaara.")]
S.append(slide('<h2>Hook Score: <span class="red">10 mein se 7</span> se kam? Post mat karo.</h2><table class="tbl"><tr><th>#</th><th>Check</th><th>Kaise parkhein</th></tr>'
               + "".join(f"<tr><td class='num'>{i + 1}</td><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for i, (a, b) in enumerate(crit)) + "</table>"
               '<p class="small" style="margin-top:16px">Framework Brendan Kane ki book <i>Hook Point</i> ke principles se adapt kiya, Hinglish reels ke liye.</p>', tag="04 · Test"))

# 7 fail reasons
fails = [("Bahut lamba", "Ek reel jo 60 second ki thi aur hook 2 line ka: median se thoda hi upar."), ("Confusing", "\"MCP: Model Context Protocol\" → viewer ko pata hi nahi kya hai. 140 views."),
         ("Vague", "\"Ye video aapki zindagi badal degi\" → kaise? kyun?"), ("Ghisa-pita", "\"Wait till the end\" sab ne 1,000 baar dekha hai."),
         ("Kisi ke liye nahi", "\"Sabke liye tips\" = kisi ke liye nahi."), ("Purana", "Jo trend 2 saal pehle tha."),
         ("Maan liya ki interest hai", "\"Manus ka waitlist bhool jao\" → Manus kaun? 144 views."), ("Jhootha", "Promise jo video poora na kare."),
         ("Unique nahi", "Competitor jaisa hi."), ("Dikhne mein feeka", "Chhota text, kam contrast, khaali screen.")]
S.append(slide('<h2>Hook <span class="red">fail</span> hone ke 10 kaaran</h2><table class="tbl">'
               + "".join(f"<tr><td class='num bad'>{i + 1}</td><td><b>{E(a)}:</b> {E(b)}</td></tr>" for i, (a, b) in enumerate(fails)) + "</table>", tag="05 · Galtiyan"))

# 8 typography
S.append(slide('<h2>Screen pe hook <span class="red">kaise likhein</span></h2>'
               '<div class="card"><b>Rule 1, poora vichaar highlight karo:</b> "<span class="mark">Paisa bachao</span>, ameer nahi banoge" ✅. Sirf "Paisa" bold karna galat hai, kyunki akela shabd kuch nahi kehta.</div>'
               '<div class="card"><b>Rule 2, line wahan todo jahan saans lete ho:</b><br>"Roz 3 ghante ek reel pe? / Saal ke 1,000 ghante gaye."</div>'
               '<div class="card"><b>Rule 3, ek rang = ek matlab:</b> laal = dard/galti, peela = hal/result. Poori series mein same rakho.</div>'
               '<div class="card"><b>Rule 4, phone safe zone:</b> text upar 15% aur neeche 25% mein mat rakho, wahan Instagram ke buttons aate hain.</div>'
               '<div class="card"><b>Rule 5, 0.0 second:</b> hook text pehle hi frame pe ho. Fade-in, logo ya intro animation mat lagao.</div>', tag="06 · Typography"))

# 9-20 archetypes
TYPES = [
    ("Ruk Jao (Callout)", "Seedha order. Dimaag ko 'brake' lagta hai, aur jisko bola gaya wo khud ko pehchaan leta hai.",
     "[Jo kaam log kar rahe hain] ke liye [paise/time] de rahe ho? Ruk jao.",
     ["Coding ke liye Cursor ka subscription? Ruk jao.", "Roz 3 ghante reel edit karte ho? Ruk jao.", "Salary aate hi EMI pe EMI? Ruk jao, pehle ye suno."],
     "Order do, par turant wajah bhi do. Sirf 'Ruk jao' bolke chup mat ho jao."),
    ("Kam Log Jaante Hain (Secret)", "Andar ki baat sunna sabko pasand hai. 'Mujhe pata hai, tumhe nahi' wali feeling.",
     "[Badi company/insaan] ne [cheez] free de diya, aur bahut kam log jaante hain.",
     ["Google ne apna AI agent free mein de diya, aur bahut kam log jaante hain.", "Toppers revise ek alag tareeke se karte hain. Kam log jaante hain.", "Phone ki ek setting jo aapki battery chupke se kha rahi hai."],
     "Secret sach mein useful ho. Jhoota secret = unfollow."),
    ("Kitne Yaad Hain? (Recap/Quiz)", "Dimaag ko khel pasand hai. List + quiz = poori dekhi jaati hai aur save hoti hai.",
     "[Time] mein [N] [cheezein]. Kitni yaad hain?",
     ["Ek hafte mein 5 mehenge AI tools ke free versions. Kitne yaad hain?", "Is mahine ke 7 money rules. Kitne follow kiye?", "10 English words jo is hafte seekhe. Kitne yaad hain?"],
     "Hamare data mein dono recap reels top 5 mein thi. Har 7 din mein ek recap daalo."),
    ("Kadwa Sach (Contrarian)", "Imaandari trust banati hai, aur ulti baat scroll rokti hai.",
     "Kadwa sach: [jo sab maante hain] galat hai.",
     ["Ye 'free' AI tools sach mein free hain? Ek kadwa sach sun lo.", "Kadwa sach: aap busy nahi ho, distracted ho.", "Kadwa sach: jaldi uthne se koi ameer nahi banta."],
     "Sach ka saboot do (example, number). Sirf shock ke liye mat bolo."),
    ("Paisa/Time ka Nuksaan (Loss)", "Insaan paane se zyada khone se darta hai. Nuksaan dikhao, log rukte hain.",
     "[Kaam] pe [time/paisa]? Saal ka [bada number] gaya.",
     ["Roz 3 ghante ek reel pe? Saal ke 1,000 ghante gaye.", "Har mahine ₹500 ke subscriptions? Saal ke ₹6,000.", "Roz 2 ghante phone pe scroll? Saal ke 30 din."],
     "Number sach ho aur hisaab simple ho, taaki viewer khud check kar sake."),
    ("Result Pehle (Proof first)", "Dekhna yakeen hai. Pehle result dikhao, phir tareeka.",
     "[Result ka visual]. Ye [tareeka] se hua.",
     ["Purani blurry video ko 4K mein badlo, free.", "Ye reel bina camera, bina mic bani hai. Guess karo kaise?", "Ek line likhi, poori website ready."],
     "Visual result frame 0 pe ho. Hamari 4K wali reel (1,093 views) isi wajah se chali."),
    ("Myth Todo", "Jo sab maante hain, use galat dikhana instant contrast deta hai.",
     "Sabse bada jhooth: '[myth]'.",
     ["Sabse bada jhooth: 'pehle editing seekho, phir page shuru karo.'", "Myth: zyada padhoge toh zyada marks.", "Myth: paisa bachane se ameer bante hain."],
     "Myth sach mein log maante hon. Banawati myth mat todo."),
    ("Identity Callout", "Insaan apne baare mein sunna pasand karta hai. Ek group ko naam se bulao.",
     "Agar aap [age/role] ho, toh [ye] abhi suno.",
     ["Agar aap 20s mein ho, toh ye 3 galtiyan abhi rok do.", "Naya page shuru kiya hai? Ye 5 cheezein pehle din karo.", "Hostel mein rehte ho? Ye 4 paise bachane ki tricks."],
     "Group chhota aur saaf ho. 'Sab log' identity nahi hai."),
    ("Comparison", "Do raaste dikhao. Viewer khud ko ek side mein dekhta hai aur aakhir tak rukta hai.",
     "[A] vs [B]: [N] din baad farak dekho.",
     ["Do creators, same talent. Ek roz post karta hai, ek mood pe. 90 din baad kaun aage?", "₹15,000 ka editor vs ₹67 ki reel.", "Topper vs average student: farak padhai mein nahi."],
     "Dono sides imaandari se dikhao. Ek ko bewakoof mat banao."),
    ("Story Drop-in", "Kahani ke beech se shuru karo. Dimaag ko 'aage kya hua' jaanna hai.",
     "[Insaan] ne [ajeeb kaam] kiya. Phir [twist].",
     ["Usne naukri chhodi, sab ne pagal kaha. 6 mahine baad koi nahi hasa.", "Ek chai wale ne mujhe business ka sabse bada lesson diya.", "Ek saal tak zero posts. Phir ek din ye notice kiya."],
     "Kahani ka lesson viewer ke kaam ka ho, sirf entertainment nahi."),
    ("Challenge / Test", "Viewer ko khel mein shamil karo. Jawab comment mein aata hai, aur comments reach badhate hain.",
     "[Test/sawaal]. Sirf [x%] log sahi karte hain.",
     ["Ek aawaz asli hai, ek AI. Pehchaan ke dikhao.", "In 3 mein se aap kaun ho? Comment karo.", "Ye 30-second test karo: aapka focus kitna hai?"],
     "% ya stat jhootha mat banao. 'Zyada log galat karte hain' bhi kaafi hai."),
    ("Naya/Abhi (Newness)", "Naya cheez = 'mujhe pehle pata hona chahiye'.",
     "[Kal/is hafte] [cheez] aaya hai, aur ye [fayda].",
     ["Instagram ne ek naya feature diya hai, creators ke liye kaam ka.", "Is hafte ek naya free AI tool aaya jo [kaam] karta hai.", "UPI ka naya rule, ye aapko pata hona chahiye."],
     "Sach mein naya ho, aur fact check karo. Galat 'news' se trust jaata hai."),
]
for i, (nm, why, tpl, ex, warn) in enumerate(TYPES):
    S.append(slide(f'<h2>{E(nm)}</h2><p class="lead" style="font-size:31px">{E(why)}</p>'
                   f'<div class="card"><b>Template:</b> {E(tpl)}</div>' + exs(ex) +
                   f'<div class="card" style="border-color:#111;margin-top:22px"><b>⚠️ Dhyaan:</b> {E(warn)}</div>', tag=f"07 · Hook type {i + 1}/12"))

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
S.append(slide('<h2>Hook ke baad kya? <span class="red">A.R.C.S.</span></h2>'
               '<div class="card"><b>A, Ask:</b> aisa sawaal jiska jawab "haan" ho. <i>"Roz post karna chahte ho, par time nahi?"</i></div>'
               '<div class="card"><b>R, Reveal:</b> "main bhi wahin tha." <i>"Mujhe bhi ek reel mein 3 ghante lagte the."</i></div>'
               '<div class="card"><b>C, Call out:</b> wo discovery jisne badla. <i>"Phir maine script se reel banane ka system banaya."</i></div>'
               '<div class="card"><b>S, Send:</b> ek saaf action. <i>"Comment karo REEL, system bhej dunga."</i></div>'
               '<p class="small" style="margin-top:18px">Ye copywriter Craig Clemens ka "Impact Arcs" formula hai (Hook Point book mein bataya gaya), yahan 30-second Hinglish reel ke liye. Ek sentence, ek reel, ya poori presentation, teeno mein chalta hai.</p>', tag="10 · Script"))

# testing
S.append(slide('<h2>Testing aur <span class="red">Double Down</span></h2>'
               '<div class="card"><b>1. Har idea ke 3 hooks likho.</b> Best wala post karo, baaki 2 "Trial Reels" mein test karo (Instagram ka feature jo pehle non-followers ko dikhata hai).</div>'
               '<div class="card"><b>2. 48 ghante baad Insights dekho:</b> views, skip rate / 3-second hold, average watch time, shares. Kisi ek reel pe nahi, 5 reels ke average pe faisla lo.</div>'
               '<div class="card"><b>3. Double down rule:</b> koi reel aapke median se <b>2× ya zyada</b> chale, toh agle 7 din mein usi idea ke <b>3 naye versions</b> banao: naya hook, nayi example, naya angle. Hamare data mein recap 2 baar chala, dono baar top 5 mein.</div>'
               '<div class="card"><b>4. Flop ko bhi padho:</b> 3 sabse kam views wali reels ka hook Hook Score pe check karo. Jo point fail hua, wahi agli baar theek karo.</div>', tag="11 · System"))

# practice
plan = [("Din 1", "Ad Library aur top creators se 20 achhe hooks copy karke ek note mein rakho (sirf seekhne ke liye)."),
        ("Din 2", "Har hook ka type pehchano (12 types mein se). Kaunsa type aapke niche mein sabse zyada hai?"),
        ("Din 3", "5 flop reels dhoondho aur Hook Score se fail point likho."),
        ("Din 4", "Apne niche ke 3 topics pe 3-3 hooks likho (9 total)."),
        ("Din 5", "Har hook ko 3-second dost-test karo. Top 3 rakho."),
        ("Din 6", "Top 3 ke saath reels banao. Frame 0 = hook text + visual."),
        ("Din 7", "Insights dekho, winner chuno, double down shuru.")]
S.append(slide('<h2>7 din ka <span class="red">hook practice</span></h2><table class="tbl">'
               + "".join(f"<tr><td class='num'>{a}</td><td>{E(b)}</td></tr>" for a, b in plan) + "</table>"
               '<div class="card" style="margin-top:22px">Pehle copy karke seekho, phir apna banao. Kisi ka hook as-it-is apne naam pe mat chalao: wo kaam nahi karta aur trust bhi todta hai.</div>', "y", "12 · Practice"))

# upsell
S.append(slide('<h2>Hooks ready. <span class="red">Reels banane ka time nahi?</span></h2>'
               '<p class="lead">Aap niche aur script do. Hum <span class="mark">ready-to-post typography reels</span> banate hain: frame 0 pe hook, bold text, animation aur voice ke saath.</p>'
               '<div class="card"><b>5 reels: ₹199.</b> Trial, 72 ghante mein delivery.</div><div class="card"><b>30 reels: ₹1,999.</b> Poore mahine ka content + calendar.</div>'
               '<div class="cta">Instagram pe @freestack.ai ke bio link se order karo.</div>', "k", "Shortcut"))

body = "".join(s.replace("{FOOT}", f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{TITLE} · {i + 1}/{len(S)}</span></div>') for i, s in enumerate(S))
h = OUT / "hook-bank-pro.html"
h.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const f=process.argv[1];await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});await b.close();})();"""
subprocess.run(["node", "-e", js, str(h)], check=True)
print(len(S), "slides")
