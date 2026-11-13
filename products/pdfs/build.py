"""Build FreeStack AI PDF products as 1080x1350 slide decks (HTML -> PDF via Playwright)."""
import html, json, subprocess, sys, pathlib

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

CSS = """
@page { size: 1080px 1350px; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: 'Inter', sans-serif; color: #111 }
.s { width: 1080px; height: 1350px; padding: 90px 84px; position: relative; overflow: hidden; page-break-after: always; background: #fff }
.y { background: #FFD400 } .k { background: #111; color: #fff } .r { background: #E10600; color: #fff }
.tag { display: inline-block; background: #111; color: #FFD400; font: 800 26px 'Inter'; letter-spacing: 1px; padding: 10px 20px; text-transform: uppercase }
.k .tag { background: #FFD400; color: #111 }
h1 { font: 900 112px/1.0 'Inter Display', 'Inter'; letter-spacing: -2px; margin: 36px 0 24px }
h2 { font: 900 72px/1.05 'Inter Display', 'Inter'; letter-spacing: -1px; margin: 28px 0 30px }
h3 { font: 800 38px/1.2 'Inter'; margin: 0 0 14px }
p, li { font: 500 34px/1.45 'Inter' }
.big { font: 600 44px/1.35 'Inter' }
.mark { background: #FFD400; padding: 0 8px } .red { color: #E10600 }
.k .red, .r .red { color: #FFD400 }
.bg { position: absolute; right: -30px; bottom: -60px; font: 900 420px/1 'Inter Display'; opacity: .07; letter-spacing: -10px }
.foot { position: absolute; left: 84px; right: 84px; bottom: 50px; display: flex; justify-content: space-between; font: 700 22px 'Inter'; opacity: .55 }
.list { list-style: none } .list li { padding: 18px 0 18px 64px; position: relative; border-bottom: 2px solid #eee }
.k .list li { border-color: #333 }
.list li .n { position: absolute; left: 0; top: 16px; font: 900 34px 'Inter Display'; color: #E10600 }
.k .list li .n { color: #FFD400 }
.card { background: #F4F4F4; border-left: 12px solid #E10600; padding: 26px 30px; margin: 18px 0; font: 500 31px/1.45 'Inter' }
.k .box { background: #222 } .k .box h3 { color: #FFD400 }
.card b { font-weight: 800 }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 22px }
.box { background: #F4F4F4; padding: 26px; border-radius: 10px }
.box h3 { font-size: 34px } .box p { font-size: 28px; line-height: 1.4 }
.small li, .small p { font-size: 29px; line-height: 1.4 }
.hook { font: 600 40px/1.35 'Inter'; padding: 26px 0 26px 72px; position: relative; border-bottom: 2px solid #eee }
.hook .n { position: absolute; left: 0; top: 26px; font: 900 38px 'Inter Display'; color: #E10600 }
.tbl { width: 100%; border-collapse: collapse; font: 500 26px/1.35 'Inter' }
.tbl th { background: #111; color: #FFD400; text-align: left; padding: 14px 12px; font-weight: 800 }
.tbl td { padding: 12px; border-bottom: 2px solid #eee; vertical-align: top }
.tbl td:first-child { font-weight: 900; color: #E10600; width: 70px }
.cta { background: #E10600; color: #fff; padding: 30px 34px; font: 800 36px/1.3 'Inter'; margin-top: 30px }
"""

E = html.escape


def foot(title, i):
    return f'<div class="foot"><span>FreeStack AI · @freestack.ai</span><span>{E(title)} · {i}</span></div>'


def deck(name, title, slides):
    body = "".join(s.replace("{{FOOT}}", foot(title, i + 1)) for i, s in enumerate(slides))
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    h = OUT / f"{name}.html"
    h.write_text(doc, encoding="utf-8")
    return h


def cover(tag, t1, t2, sub, bgword):
    return f"""<div class="s y"><div class="bg">{E(bgword)}</div>
<div class="tag">{E(tag)}</div><h1>{t1}</h1><p class="big">{t2}</p>
<p style="margin-top:40px;font-weight:700">{E(sub)}</p>{{{{FOOT}}}}</div>"""


def section(tag, title, inner, cls=""):
    return f'<div class="s {cls}"><div class="tag">{E(tag)}</div><h2>{title}</h2>{inner}{{{{FOOT}}}}</div>'


def ol(items, start=1):
    return '<ul class="list">' + "".join(
        f'<li><span class="n">{start + i:02d}</span>{x}</li>' for i, x in enumerate(items)) + "</ul>"


def hooks(items, start):
    return "".join(f'<div class="hook"><span class="n">{start + i}</span>{E(x)}</div>' for i, x in enumerate(items))


UPSELL = section("Shortcut", "Reels banane ka time nahi?",
    '<p class="big">Aap sirf niche aur script do. Hum aapke liye <span class="mark">ready-to-post typography reels</span> banate hain: bold text, animation aur voice ke saath.</p>'
    '<div class="grid" style="margin-top:40px"><div class="box"><h3>5 reels</h3><p><b>₹199</b>, trial. 72 ghante mein delivery.</p></div>'
    '<div class="box"><h3>30 reels</h3><p><b>₹1,999</b>, poore mahine ka content + calendar.</p></div></div>'
    '<div class="cta">Instagram pe @freestack.ai ke bio link se order karo.</div>', "k")

# ---------------------------------------------------------------- PDF 1: Hook Bank
HOOK_GROUPS = [
    ("Curiosity", "Dimaag ko adhoori baat bardasht nahi hoti. Jawab aakhir mein do.", [
        "Ye cheez 99% log galat karte hain, aur unhe pata bhi nahi.",
        "Is video ke end tak aap [topic] ko alag nazar se dekhoge.",
        "[Famous cheez] ke peeche ka asli sach kisi ne nahi bataya.",
        "Ek aadat jo chupke se aapka [paisa/time/growth] kha rahi hai.",
        "Ye trick maine 2 saal pehle seekhi hoti toh aaj kahin aage hota.",
        "Number 3 sunke aap rukoge.",
        "Iska naam aapne suna hai, par iska kaam kisi ko nahi pata.",
        "Main ye video delete karne wala tha. Phir socha aapko pata hona chahiye.",
        "Sabse simple cheez, sabse bada farak. Aakhir tak dekho.",
        "Ye sunke aapko gussa aayega, par baat sach hai."]),
    ("Pain point", "Viewer ki asli takleef ek line mein bolo. Wo khud ko pehchaan lega.", [
        "Roz mehnat karte ho, phir bhi result zero? Problem mehnat nahi hai.",
        "[Kaam] mein 3 ghante lagte hain? Ye video aapke liye hai.",
        "Har mahine salary aati hai aur 20 tareekh tak khatam?",
        "Padhte ho, par exam mein sab bhool jaate ho?",
        "Post karte ho, views 200 pe atak jaate hain?",
        "Subah uthte hi thakaan? Ye 1 galti check karo.",
        "Sab kuch try kar liya, phir bhi kuch nahi badla?",
        "Log aapki baat beech mein kaat dete hain? Iski wajah sun lo.",
        "Kaam shuru karte ho, phir 4 din mein chhod dete ho?",
        "Mehnat aap karte ho, credit koi aur le jaata hai?"]),
    ("Myth tod do", "Jo sab maante hain, use galat sabit karo. Contrast scroll rokta hai.", [
        "Sabse bada jhooth: '[popular belief]'.",
        "Nahi, [popular advice] se kuch nahi hoga. Ye karo.",
        "Aapko jo sikhaya gaya, wo aadha sach tha.",
        "[Cheez] bura nahi hai. Bura hai ise galat tareeke se karna.",
        "Talent ki zaroorat nahi. Bas ye ek cheez chahiye.",
        "Jaldi uthne se aap successful nahi banoge. Ye sach hai.",
        "Zyada mehnat answer nahi hai. Sahi direction hai.",
        "Motivation ka intezaar mat karo. Wo kabhi nahi aata.",
        "Paisa bachane se ameer nahi bante. Ye bhi chahiye.",
        "Pehle perfect banoge, phir shuru karoge? Aisa kabhi nahi hota."]),
    ("Number / list", "Number dimaag ko bata deta hai video kitni lambi hai. Log list poori dekhte hain.", [
        "3 cheezein jo har [role] ko 25 se pehle pata honi chahiye.",
        "5 [topic] jo aapki zindagi aasaan kar denge.",
        "Sirf 2 minute, aur aapko [result] ka tareeka pata hoga.",
        "7 din, 1 aadat, aur farak khud dekh lena.",
        "Ye 4 galtiyan aapka [goal] rok rahi hain.",
        "1 rule jo maine kabhi nahi toda, aur isliye yahan hoon.",
        "10 second mein samjho [mushkil topic].",
        "3 signs ki aap sahi raaste pe ho, chahe result abhi na dikhe.",
        "5 cheezein jo amir log chupke se karte hain.",
        "Bas 3 sawaal, aur aapko pata chal jayega [answer]."]),
    ("Story", "Ek insaan, ek problem, ek mod. Kahani sabse lamba rokti hai.", [
        "Ek ladka tha, jiske paas kuch nahi tha. Bas ek aadat thi.",
        "2019 mein ek aadmi ne ek galti ki. Aaj wahi galti aap kar rahe ho.",
        "Meri dost ne ek din ye kaha, aur meri soch badal gayi.",
        "Ek chai wale ne mujhe business ka sabse bada lesson diya.",
        "Usne 100 baar haar maani. 101vi baar kya hua?",
        "Ek message ne mera poora saal badal diya.",
        "Sab hans rahe the. 6 mahine baad koi nahi hasa.",
        "Ye kahani 1 minute ki hai, par yaad zindagi bhar rahegi.",
        "Ek teacher ne class mein ek sawaal poocha. Koi jawab nahi de paya.",
        "Usne naukri chhodi, sab ne pagal kaha. Phir ye hua."]),
    ("Challenge / quiz", "Viewer ko khel mein shamil karo. Jawab comment mein aata hai.", [
        "Sirf 1% log isko pehli baar mein solve karte hain.",
        "Aap in 3 mein se kaunse ho? Comment mein batao.",
        "Agar aapne ye galti nahi ki, toh aap rare ho.",
        "Ek aawaz asli hai, ek AI. Pehchaan ke dikhao.",
        "Guess karo, iski keemat kitni hai?",
        "Ye test karo, 30 second lagenge.",
        "Kitne yaad hain? Comment mein number likho.",
        "Sach ya jhooth? Video ke end mein jawab.",
        "Agar ye 5 baatein aap mein hain, toh aap aage jaoge.",
        "Rukna mat. Aakhir mein ek twist hai."]),
    ("Secret / kam log jaante hain", "Andar ki baat sunna sabko pasand hai. Exclusive feel do.", [
        "Ye feature 90% log use hi nahi karte.",
        "[Famous company] ye baat aapko kabhi nahi batayegi.",
        "Kam log jaante hain, par [cheez] free mein milta hai.",
        "Toppers ye trick chupke se use karte hain.",
        "Bank ye baat aapse kabhi nahi kahega.",
        "Is setting ko abhi on karo. Shukriya baad mein bolna.",
        "Ye shortcut jaan ke aap hairaan ho jaoge.",
        "Insta pe log ye trick share nahi karte. Main kar raha hoon.",
        "Ek chhupa hua tareeka jo seedha kaam karta hai.",
        "Ye maine ek expert se seekha, ab aapko bata raha hoon."]),
    ("Kadwa sach", "Seedhi, thodi kadwi baat. Imaandari trust banati hai.", [
        "Kadwa sach: koi aapko bachane nahi aayega.",
        "Sach sun lo, aapka phone aapki zindagi chala raha hai.",
        "Aap busy nahi ho. Aap distracted ho.",
        "Log aapko judge nahi kar rahe. Wo apne mein busy hain.",
        "'Kal se pakka' kabhi nahi aata.",
        "Free cheez sach mein free nahi hoti. Ye samjho.",
        "Aapki comfort zone hi aapki sabse badi dushman hai.",
        "Kisi ko farak nahi padta ki aap kitne thake ho. Result chahiye.",
        "Jo aapko roz 5 ghante leta hai, wo hobby nahi, aadat hai.",
        "Sach ye hai: shuruat hamesha kharab hoti hai. Phir bhi karo."]),
    ("Comparison", "Do raaste dikhao. Log khud ko ek side mein dekhte hain.", [
        "Do log, same salary. 10 saal baad ek ameer, ek nahi. Kyun?",
        "Gareeb soch vs ameer soch: ek line ka farak.",
        "Aap vs aap 1 saal baad, agar aaj ye shuru karo.",
        "₹100 ka [product] vs ₹1,000 ka: asli farak kya hai?",
        "Topper vs average student: farak padhai mein nahi hai.",
        "Roz 1% better vs roz 1% worse, 1 saal baad.",
        "Jo ye karta hai vs jo nahi karta, 6 mahine baad dekho.",
        "Naukri vs side hustle: sach kya hai?",
        "Sasta vs mehenga: kab kya lena chahiye.",
        "Pehle vs ab: maine kya badla."]),
    ("Urgency / stop scroll", "Seedha order do. Pehla shabd hi brake ho.", [
        "Ruko! Ye video skip mat karna.",
        "Agar aap [age] ke ho, toh abhi suno.",
        "Ye video dobara nahi milegi. Save kar lo.",
        "Scroll karne se pehle ye ek baat sun lo.",
        "Abhi ke abhi ye setting badlo.",
        "Iske baad aap pehle jaise nahi rahoge.",
        "Agar aaj ye nahi kiya, toh kal pachtaoge.",
        "Bas 20 second do, baaki zindagi aasaan.",
        "Ye pehle pata hota, toh paisa bach jaata.",
        "Is video ko [kisi dost] ko bhejo jo ye galti karta hai."]),
]

p1 = [cover("Hook Bank · Hinglish", "100 <span class='red'>Viral</span><br>Hooks", "Faceless reels ke liye ready-to-use Hinglish hooks, 10 types mein.", "Copy karo · [blank] bharo · post karo", "HOOK")]
p1.append(section("Pehle ye samjho", "Hook = pehle <span class='red'>3 second</span>",
    '<p class="big">Reel ka 80% kaam pehli line karti hai. Viewer 1–2 second mein decide karta hai ki rukna hai ya scroll karna hai.</p>'
    '<div class="card"><b>Achha hook teen kaam karta hai:</b><br>1. Kisi ek insaan ko target karta hai<br>2. Ek sawaal ya takleef kholta hai<br>3. Jawab video ke andar chhupata hai</div>'
    '<div class="card"><b>Is PDF ka use kaise karo:</b> apne niche ka hook chuno, [blank] bharo, aur screen pe pehle frame mein bada likho. Wahi line voice mein bhi bolo.</div>'))
p1.append(section("Formula", "Har hook ka <span class='red'>formula</span>",
    ol(["<b>Kaun?</b> Kisse baat kar rahe ho: student, creator, naukri wale…",
        "<b>Kya dard?</b> Unki ek takleef ya chahat",
        "<b>Kya twist?</b> Ek ulti baat, number, ya raaz",
        "<b>Kab tak?</b> Jawab aakhir mein, taaki video poori dekhi jaaye"]) +
    '<div class="card"><b>Example:</b> "Padhte ho, par exam mein sab bhool jaate ho? (dard) Problem yaad karne mein nahi, revise karne ke tareeke mein hai. (twist)"</div>'))
n = 1
for i, (name, why, hs) in enumerate(HOOK_GROUPS):
    for half in (0, 5):
        p1.append(section(f"Type {i + 1} of 10" + (" · contd." if half else ""), E(name),
            (f'<p style="font-weight:700;margin-bottom:16px">{E(why)}</p>' if not half else '') + hooks(hs[half:half + 5], n + half)))
    n += len(hs)
p1.append(section("Bonus", "Hook ko <span class='red'>screen</span> pe kaise likho",
    ol(["Pehle frame mein hook ke <b>3–6 bade shabd</b>, poori line nahi",
        "Ek <b>keyword</b> alag rang mein (laal ya peela)",
        "Pehle second mein hi text aa jaaye. Intro, logo ya 'Hi guys' nahi",
        "Hook ke turant baad <b>payoff ka ishaara</b>: 'number 3 sabse zaroori hai'",
        "Hook jo bola, video wahi de. Clickbait se follow nahi milta"]), "y"))
p1.append(section("Bonus", "Niche ke hisaab se <span class='red'>best types</span>",
    '<table class="tbl"><tr><th>Niche</th><th>Sabse achhe hook types</th></tr>'
    '<tr><td>💪</td><td><b>Motivation:</b> Kadwa sach, Story, Myth tod do</td></tr>'
    '<tr><td>🧠</td><td><b>Facts:</b> Curiosity, Secret, Challenge</td></tr>'
    '<tr><td>💰</td><td><b>Money tips:</b> Comparison, Pain point, Secret</td></tr>'
    '<tr><td>📚</td><td><b>Study tips:</b> Pain point, Number/list, Myth</td></tr>'
    '<tr><td>🤖</td><td><b>AI tools:</b> Secret, Urgency, Comparison</td></tr>'
    '<tr><td>✍️</td><td><b>Shayari/quotes:</b> Story, Kadwa sach, Curiosity</td></tr>'
    '<tr><td>📖</td><td><b>Stories:</b> Story, Curiosity, Challenge</td></tr></table>'
    '<div class="card" style="margin-top:30px"><b>Test karo:</b> ek hi reel 2 alag hooks ke saath banao. Jiska 3-second hold zyada ho (Insights mein), wahi type aapke niche ka winner hai.</div>'))
p1.append(UPSELL)

# ---------------------------------------------------------------- PDF 2: 30-Day plan
DAYS = [
    ("Intro", "Main kaun hoon / ye page kis baare mein hai"), ("List", "Apne niche ki 5 basic cheezein"),
    ("Myth", "Niche ka sabse bada myth tod do"), ("Story", "Ek kahani jo lesson deti hai"),
    ("Tip", "Ek tip jo aaj hi kaam aaye"), ("Question", "Audience se ek sawaal (comment mein jawab)"),
    ("Recap", "Hafte ki best 3 baatein"), ("Pain", "Viewer ki sabse badi takleef + hal"),
    ("Comparison", "Do raaste: kaunsa sahi?"), ("List", "3 galtiyan jo log karte hain"),
    ("Secret", "Ek kam-jaani baat"), ("Story", "Kisi ki asli/inspired kahani"),
    ("Kadwa sach", "Ek seedhi, imaandaar baat"), ("Recap", "Hafte ka recap + 'kitne yaad hain?'"),
    ("Tip", "5 second ki aadat/trick"), ("Challenge", "7 din ka chhota challenge do"),
    ("List", "Beginners ke liye 3 steps"), ("Myth", "Doosra myth, doosra sach"),
    ("Question", "'Aap kis type ke ho?' quiz"), ("Story", "Haar se jeet tak"),
    ("Recap", "Teen hafton ki best tips"), ("Pain", "'Sab kiya, phir bhi kuch nahi hua?'"),
    ("Comparison", "Pehle vs ab"), ("List", "Mere favourite 5 resources"),
    ("Secret", "Experts ka chhupa tareeka"), ("Kadwa sach", "Jo koi nahi bolta"),
    ("Challenge", "Comment mein apna goal likho"), ("Tip", "Ek mistake se kaise bacho"),
    ("Recap", "30 din ki 10 best seekh"), ("Thank you", "Safar ka recap + agla plan"),
]

TEMPLATES = {
    "Intro": "HOOK: Agar aap [niche] mein [problem] se pareshaan ho, toh ye page aapke liye hai.\nBODY: Yahan roz milega: [1], [2], [3].\nCTA: Follow karo, kal se shuru.",
    "List": "HOOK: [N] [cheezein] jo har [audience] ko pata honi chahiye.\nBODY: 1… 2… 3… (har point 1 line + 1 example)\nCTA: Save karo, kaam aayega.",
    "Myth": "HOOK: Sabse bada jhooth: '[myth]'.\nBODY: Log kyun maante hain → asli sach → kya karna chahiye.\nCTA: Agree karte ho? Comment karo.",
    "Story": "HOOK: Ek [insaan] tha jo [problem] se pareshaan tha.\nBODY: Kya hua → mod kya aaya → kya seekha.\nCTA: Ye lesson kisi ko bhejo.",
    "Tip": "HOOK: Bas 1 cheez badlo, [result] khud dikhega.\nBODY: Tip → kaise karna hai (2 steps) → kyun kaam karta hai.\nCTA: Aaj try karke batao.",
    "Question": "HOOK: Sach batao, aap [A] ho ya [B]?\nBODY: A wale aisa karte hain… B wale aisa…\nCTA: Comment mein A ya B likho.",
    "Recap": "HOOK: Is hafte [N] baatein seekhi. Kitni yaad hain?\nBODY: 1 line mein har ek.\nCTA: Save karo + follow, agla hafta aur bhi.",
    "Pain": "HOOK: [Pain] ho raha hai? Galti aapki nahi, tareeke ki hai.\nBODY: Asli wajah → seedha hal → chhota example.\nCTA: Agar ye aap ho, toh comment mein 'haan'.",
    "Comparison": "HOOK: [A] vs [B]: farak sunke hairaan ho jaoge.\nBODY: A ka result… B ka result… asli farak.\nCTA: Aap kaunse ho? Batao.",
    "Secret": "HOOK: Ye baat bahut kam log jaante hain.\nBODY: Raaz → kaise use karein → ek example.\nCTA: Save karo, dobara nahi milega.",
    "Kadwa sach": "HOOK: Kadwa sach: [statement].\nBODY: Kyun ye sach hai → kya karna chahiye.\nCTA: Sehmat ho? Share karo.",
    "Challenge": "HOOK: 7 din ka challenge, karoge?\nBODY: Roz kya karna hai → kya farak aayega.\nCTA: Comment mein 'IN' likho.",
    "Thank you": "HOOK: 30 din, 30 reels. Thank you.\nBODY: Kya seekha, kya aage aayega.\nCTA: Follow karo, agla mahina aur bada.",
}

p2 = [cover("30-Day Plan · Faceless Page", "30 Din ka<br><span class='red'>Content</span> Plan", "Calendar + 13 fill-in script templates. Har din kya post karna hai, decide ho chuka hai.", "Kisi bhi faceless niche ke liye", "30")]
p2.append(section("Kaise use karein", "Plan ka <span class='red'>logic</span>",
    '<p class="big">Har din ek <b>format</b> hai (List, Myth, Story…). Aap bas apne niche ka topic bharte ho.</p>'
    '<div class="card"><b>Kyun formats?</b> Ek jaisi reels roz daalne se audience bore hoti hai. Formats badalne se har din kuch naya lagta hai, aur aapko pata chalta hai kaunsa format aapke niche mein chalta hai.</div>'
    '<div class="card"><b>Har hafte ek Recap</b> (din 7, 14, 21, 29). List aur recap reels sabse zyada save hoti hain.</div>'))
cal_rows = "".join(f"<tr><td>{d:02d}</td><td><b>{E(f)}</b></td><td>{E(t)}</td></tr>" for d, (f, t) in enumerate(DAYS[:15], 1))
p2.append(section("Calendar", "Din 1–15", f'<table class="tbl"><tr><th>Din</th><th>Format</th><th>Topic idea</th></tr>{cal_rows}</table>'))
cal_rows = "".join(f"<tr><td>{d:02d}</td><td><b>{E(f)}</b></td><td>{E(t)}</td></tr>" for d, (f, t) in enumerate(DAYS[15:], 16))
p2.append(section("Calendar", "Din 16–30", f'<table class="tbl"><tr><th>Din</th><th>Format</th><th>Topic idea</th></tr>{cal_rows}</table>'))
tpl = list(TEMPLATES.items())
for i in range(0, len(tpl), 4):
    inner = "".join(f'<div class="card small"><b>{E(k)}</b><p style="white-space:pre-line;margin-top:8px">{E(v)}</p></div>' for k, v in tpl[i:i + 4])
    p2.append(section("Script templates", f"Templates {i + 1}–{min(i + 4, len(tpl))}", inner))
p2.append(section("Example", "Template se <span class='red'>poori script</span>",
    '<p style="font-weight:700">Niche: Money tips · Format: Myth</p>'
    '<div class="card"><b>HOOK:</b> Sabse bada jhooth: "paisa bachane se ameer bante hain."</div>'
    '<div class="card"><b>BODY:</b> Bachat zaroori hai, par sirf bachat se paisa nahi badhta. Mehngai har saal uski value kam karti hai. Isliye bachat ke saath seekho ki paisa kaam pe kaise lagta hai: skill, side income, aur samajhdaari se invest.</div>'
    '<div class="card"><b>CTA:</b> Agree karte ho? Comment mein "haan" likho.</div>'
    '<p style="margin-top:24px">Total: ~25 second. Screen pe har line ke 3–5 bade shabd.</p>'))
p2.append(section("Checklist", "Post karne se <span class='red'>pehle</span>",
    ol(["Pehle frame mein hook bada likha hai?", "Hook ke turant baad value shuru?", "Reel 20–40 second ke beech?",
        "Captions/text phone pe padhne layak bade?", "Ending pe ek clear CTA (save/comment/follow)?",
        "Caption mein 1 line hook + 3–5 hashtags?", "Roz ek hi time pe post?"]), "y"))
track = "".join(f"<tr><td>{d:02d}</td><td></td><td></td><td></td><td></td></tr>" for d in range(1, 16))
p2.append(section("Tracker", "Kya chala, <span class='red'>likh lo</span>",
    f'<table class="tbl"><tr><th>Din</th><th>Views</th><th>Likes</th><th>Saves</th><th>Follows</th></tr>{track}</table>'
    '<p class="small" style="margin-top:20px">Print karo ya screenshot pe likho. 2 hafte baad dekho: kaunsa format sabse aage hai, wahi zyada banao.</p>'))
p2.append(UPSELL)

# ---------------------------------------------------------------- PDF 3: Niche ideas
NICHES = [
    ("Motivation", "Ek line, bold text, gehri aawaz", ["Kadwa sach series", "'Agar aap 20s mein ho' tips", "Haar se jeet ki kahaniyan", "Subah ki 1 aadat"]),
    ("Amazing facts", "Har reel ek 'wow'", ["Body ke ajeeb facts", "Itihaas ke anjaane sach", "Desh-duniya ke record", "Sach ya jhooth quiz"]),
    ("Money tips", "Chhote paise, badi samajh", ["Salary ka 50-30-20 rule", "Faltu kharche pakdo", "UPI/credit card galtiyan", "Pehli bachat kaise shuru karein"]),
    ("Study tips", "Students sabse zyada save karte hain", ["Revise karne ka tareeka", "Exam se 1 din pehle kya karein", "Focus ki 3 tricks", "Topper ki aadatein"]),
    ("AI tools", "Har hafte naya tool", ["Free AI tools ki list", "Paid tool ka free version", "Phone pe AI tricks", "AI se ghante bachao"]),
    ("Shayari / quotes", "Emotion bikta hai", ["Dosti shayari", "Breakup lines", "Maa-baap pe lines", "Raat ki soch"]),
    ("Short stories", "Aakhir tak roke", ["1 minute moral story", "Twist ending kahani", "Itihaas ki kahani", "Real-life inspired"]),
    ("Psychology facts", "Log khud ko samajhna chahte hain", ["Body language signs", "Log jhooth kaise bolte hain", "Dimaag ke shortcuts", "Aadatein kaise banti hain"]),
    ("Relationship tips", "Comments sabse zyada", ["Red flags / green flags", "Dosti ke rules", "Baat karne ka tareeka", "Ladai ke baad kya karein"]),
    ("Health habits", "Simple aur safe tips (doctor ki salah nahi)", ["Paani, neend, walk", "Phone aur aankhein", "Subah ki routine", "Chhoti healthy swaps"]),
    ("Tech tips", "Phone/laptop tricks", ["Hidden phone settings", "Battery bachao", "Shortcuts jo time bachayein", "Privacy settings"]),
    ("Business ideas", "Sapne dikhao, sach bolo", ["Kam paise ke business", "Business ke kadwe sach", "Famous brand ki kahani", "Side hustle ideas"]),
    ("Spiritual / gyaan", "Shanti aur seekh", ["Gita/granth se ek line", "Dhyaan ke 2 minute", "Karma ki kahaniyan", "Subah ke vichaar"]),
    ("English learning", "Har Indian ki chahat", ["Roz 1 word", "Common galtiyan", "Interview lines", "Hindi se English"]),
    ("Career tips", "Freshers ke liye", ["Resume galtiyan", "Interview sawaal", "Skills jo demand mein hain", "Pehli job ke rules"]),
    ("Productivity", "Kam samay, zyada kaam", ["To-do list ka sahi tareeka", "Phone addiction todo", "2-minute rule", "Deep work"]),
    ("Book summaries", "1 kitaab, 1 reel", ["Ek kitaab ki 3 seekh", "Must-read list", "Ek quote, ek kahani", "Kitaab vs zindagi"]),
    ("Life hacks", "Roz kaam aaye", ["Kitchen hacks", "Ghar ki safai tricks", "Travel packing tips", "Paise bachane ke hacks"]),
    ("Cricket / sports facts", "Fans ka pyaar", ["Record jo koi nahi todega", "Player ki kahani", "Sports trivia quiz", "Iconic moments"]),
    ("Bollywood facts", "Nostalgia + gossip-free facts", ["Film ke peeche ki kahani", "Dialogue jo amar ho gaye", "Flop se hit tak", "Kya aapko pata tha?"]),
    ("Parenting tips", "Naye maa-baap", ["Bachchon se baat ka tareeka", "Screen time rules", "Achhi aadatein", "Padhai mein madad"]),
    ("Cooking (text-only)", "Recipe text mein", ["5 minute nashta", "Hostel recipes", "Healthy snacks", "Masale ka gyaan"]),
    ("Travel facts", "Ghoomne ke sapne", ["Kam budget jagahein", "Desh ki anjaani jagahein", "Travel galtiyan", "Mausam ke hisaab se trip"]),
    ("Law / rights awareness", "Har citizen ke kaam ka (sirf general jaankari)", ["Aapke basic adhikaar", "Online fraud se bacho", "Consumer rights", "Police complaint kaise"]),
    ("History stories", "Kahani + gyaan", ["Raja-maharaja ki kahani", "Aazadi ki anjaani kahaniyan", "Itihaas ke mysteries", "Ek din, ek ghatna"]),
]
p3 = [cover("Niche Guide · Faceless", "25 Faceless<br><span class='red'>Page</span> Ideas", "Har niche ke saath 4 ready reel ideas: 100 ideas total. Bina chehra, bina camera.", "Kaunsa page banau? Ab confusion khatam.", "25")]
p3.append(section("Pehle ye", "Niche kaise <span class='red'>chunein</span>",
    ol(["<b>Aapko pasand ho:</b> 30 din tak roz bana sako", "<b>Content khatam na ho:</b> kam se kam 100 topics nikal sako",
        "<b>Text mein samjhe:</b> typography reels mein kaam kare, video footage na chahiye",
        "<b>Log save/share karein:</b> tips, facts, lists, emotions", "<b>Ek audience:</b> 'sabke liye' nahi, ek insaan ke liye"])))
for i in range(0, len(NICHES), 4):
    boxes = "".join(f'<div class="box"><h3>{i + j + 1}. {E(nm)}</h3><p style="font-weight:700;margin-bottom:8px">{E(why)}</p><p>' +
                    "<br>".join("• " + E(x) for x in ideas) + "</p></div>" for j, (nm, why, ideas) in enumerate(NICHES[i:i + 4]))
    p3.append(section("Niches", f"Ideas {i + 1}–{min(i + 4, len(NICHES))}", f'<div class="grid">{boxes}</div>'))
p3.append(section("Dhyaan rakho", "Safe <span class='red'>rehna</span>",
    ol(["Health, law, finance mein <b>general jaankari</b> do, personal salah nahi", "Doosron ki video/gaane bina permission mat use karo",
        "Fake facts mat daalo. Ek galti se trust jaata hai", "Bollywood/sports mein gossip nahi, facts"]), "y"))
p3.append(UPSELL)

decks = [("100-viral-hooks", "100 Viral Hooks", p1), ("30-day-content-plan", "30-Day Content Plan", p2), ("25-faceless-page-ideas", "25 Faceless Page Ideas", p3)]
files = [str(deck(n, t, s)) for n, t, s in decks]
print(json.dumps({n: len(s) for n, _, s in decks}))
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:f.replace(/\\.html$/,'.pdf'),width:'1080px',height:'1350px',printBackground:true});}await b.close();})();"""
subprocess.run(["node", "-e", js, *files], check=True)
