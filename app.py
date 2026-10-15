from flask import Flask, render_template_string

app = Flask(__name__)

QUESTIONS = [
 {"q":"He likes math, ____ he practices it every day.","options":["However","So","Otherwise","But"],"answer":"So","meaning":"Cậu ấy thích Toán, vì vậy cậu ấy luyện tập mỗi ngày.","explain":"'So' diễn tả kết quả."},
 {"q":"It was raining. ____, we still went outside.","options":["Therefore","However","So","Because"],"answer":"However","meaning":"Trời đang mưa. Tuy nhiên, chúng tôi vẫn ra ngoài.","explain":"'However' diễn tả sự tương phản."},
 {"q":"She was sick, ____ she went to school.","options":["so","because","but","therefore"],"answer":"but","meaning":"Cô ấy bị ốm, nhưng vẫn đi học.","explain":"'But' có nghĩa là 'nhưng'."},
 {"q":"You should leave now; ____, you will be late.","options":["otherwise","however","therefore","and"],"answer":"otherwise","meaning":"Bạn nên đi ngay; nếu không, bạn sẽ bị trễ.","explain":"'Otherwise' có nghĩa là 'nếu không thì'."},
 {"q":"Tom studied very hard. ____, he passed the exam.","options":["Although","Therefore","But","Or"],"answer":"Therefore","meaning":"Tom học rất chăm chỉ. Vì vậy, cậu ấy đã vượt qua kỳ thi.","explain":"'Therefore' nêu kết quả."},
 {"q":"I stayed at home ____ I was tired.","options":["so","but","because","however"],"answer":"because","meaning":"Tôi ở nhà vì tôi mệt.","explain":"'Because' nêu nguyên nhân."},
 {"q":"Would you like tea ____ coffee?","options":["and","or","so","although"],"answer":"or","meaning":"Bạn muốn trà hay cà phê?","explain":"'Or' đưa ra lựa chọn."},
 {"q":"Lan likes English ____ she also likes science.","options":["and","otherwise","however","because"],"answer":"and","meaning":"Lan thích tiếng Anh và cũng thích khoa học.","explain":"'And' dùng để thêm thông tin."},
 {"q":"____ it was cold, they went swimming.","options":["Because","Although","So","Therefore"],"answer":"Although","meaning":"Mặc dù trời lạnh, họ vẫn đi bơi.","explain":"'Although' có nghĩa là 'mặc dù'."},
 {"q":"The bus was late, ____ we arrived after 8 o'clock.","options":["so","although","however","otherwise"],"answer":"so","meaning":"Xe buýt đến muộn, vì vậy chúng tôi đến sau 8 giờ.","explain":"'So' nêu kết quả."},
 {"q":"He is young, ____ he is very responsible.","options":["because","however","but","therefore"],"answer":"but","meaning":"Cậu ấy còn trẻ, nhưng rất có trách nhiệm.","explain":"'But' nối hai ý tương phản."},
 {"q":"Hurry up, ____ you will miss the train.","options":["and","otherwise","because","although"],"answer":"otherwise","meaning":"Nhanh lên, nếu không bạn sẽ lỡ chuyến tàu.","explain":"'Otherwise' nêu điều có thể xảy ra nếu không làm theo lời nhắc."}
]

CONNECTORS = [
 ("However","tuy nhiên","Diễn tả sự tương phản; thường đứng đầu câu và theo sau bởi dấu phẩy."),
 ("Therefore","do đó / vì vậy","Nêu kết quả hoặc kết luận."),
 ("Otherwise","nếu không thì","Nêu kết quả có thể xảy ra nếu không làm điều được nhắc đến."),
 ("But","nhưng","Nối hai ý tương phản trong cùng câu."),
 ("So","vì vậy / nên","Nêu kết quả."),
 ("Because","bởi vì","Nêu nguyên nhân."),
 ("Although","mặc dù","Nêu sự tương phản; thường mở đầu mệnh đề phụ."),
 ("And","và","Thêm thông tin hoặc nối các ý tương tự."),
 ("Or","hoặc / hay","Đưa ra lựa chọn.")
]

PAGE = r'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>English Connectors</title>
<style>
:root{--bg:#0b1020;--panel:#151d33;--panel2:#1c2945;--text:#eef3ff;--muted:#aab8d4;--accent:#7c9cff;--good:#48d6a0;--bad:#ff7b8b}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(140deg,#0b1020,#182544);font-family:system-ui,Arial,sans-serif;color:var(--text);min-height:100vh}
.wrap{max-width:900px;margin:auto;padding:22px 15px 50px}.hero{padding:24px 4px 14px}.tag{color:#a9bcff;font-weight:700;letter-spacing:1.5px;font-size:12px}
h1{font-size:clamp(27px,6vw,42px);margin:8px 0}.sub,.muted{color:var(--muted)}p{line-height:1.55}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.tab{border:1px solid #344365;background:#121a2d;color:var(--text);padding:10px 15px;border-radius:12px;cursor:pointer;font-weight:700}.tab.active{background:var(--accent);color:#0b1020}
.panel{background:rgba(21,29,51,.95);border:1px solid #2b3958;border-radius:18px;padding:20px;margin-top:12px;box-shadow:0 12px 35px #0002}.hidden{display:none}
.question-top{display:flex;justify-content:space-between;gap:10px;color:var(--muted);font-size:14px}.q{font-size:22px;font-weight:750;margin:18px 0}
.options{display:grid;grid-template-columns:1fr 1fr;gap:10px}.opt{background:var(--panel2);color:var(--text);border:1px solid #354568;border-radius:12px;padding:13px;text-align:left;font-size:16px;cursor:pointer}.opt.selected{border-color:var(--accent);outline:2px solid #7c9cff33}.opt.correct{border-color:var(--good);background:#123a35}.opt.wrong{border-color:var(--bad);background:#412331}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.btn{background:var(--accent);color:#0b1020;border:0;border-radius:12px;padding:12px 17px;font-weight:800;cursor:pointer}.btn.secondary{background:#273654;color:var(--text)}.btn:disabled{opacity:.4;cursor:not-allowed}
.feedback{padding:13px;border-radius:12px;margin-top:14px;line-height:1.55}.feedback.good{background:#123a35}.feedback.bad{background:#412331}.score{font-size:27px;font-weight:850}.progress{height:7px;background:#2a3651;border-radius:99px;overflow:hidden;margin-top:12px}.bar{height:100%;width:0;background:var(--accent);transition:width .2s}
.connector{display:grid;grid-template-columns:140px 1fr;gap:12px;padding:13px 0;border-bottom:1px solid #2c3855}.connector:last-child{border-bottom:0}.word{font-size:18px;font-weight:800;color:#a9bcff}.translation{font-weight:700}.small{font-size:14px;color:var(--muted)}
@media(max-width:560px){.options{grid-template-columns:1fr}.connector{grid-template-columns:1fr;gap:4px}.panel{padding:16px}.q{font-size:20px}}
</style></head><body><main class="wrap">
<header class="hero"><div class="tag">ENGLISH • GRADE 8</div><h1>English Connectors</h1><p class="sub">Luyện cách dùng However, Therefore, Otherwise, But, So và các từ nối thường gặp.</p></header>
<nav class="tabs"><button class="tab active" onclick="showTab('practice',this)">📝 Làm bài</button><button class="tab" onclick="showTab('learn',this)">📚 Học từ nối</button></nav>
<section id="practice" class="panel"><div class="question-top"><span id="counter"></span><span id="liveScore">Điểm: 0</span></div><div class="progress"><div class="bar" id="bar"></div></div>
<div id="quizArea"><div class="q" id="question"></div><div class="options" id="options"></div><div id="feedback"></div>
<div class="controls"><button class="btn" id="checkBtn" onclick="checkAnswer()">Kiểm tra</button><button class="btn secondary" id="nextBtn" onclick="nextQuestion()" disabled>Câu tiếp theo →</button></div></div>
<div id="resultArea" class="hidden"><div class="score" id="finalScore"></div><p id="finalText"></p><button class="btn" onclick="restart()">Làm lại từ đầu ↻</button></div></section>
<section id="learn" class="panel hidden"><h2>Các từ nối cần nhớ</h2><p class="muted">Đọc nghĩa và cách dùng trước khi làm bài.</p>
{% for word, meaning, explain in connectors %}<div class="connector"><div class="word">{{ word }}</div><div><div class="translation">{{ meaning }}</div><div class="small">{{ explain }}</div></div></div>{% endfor %}
</section><p class="small">Mẹo: Đọc cả hai vế câu để xác định quan hệ: kết quả, nguyên nhân, tương phản hay lựa chọn.</p></main>
<script>
const questions = {{ questions|tojson }};let index=0,score=0,selected=null,checked=false;
function showTab(id,btn){document.querySelectorAll('section.panel').forEach(x=>x.classList.add('hidden'));document.getElementById(id).classList.remove('hidden');document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));btn.classList.add('active')}
function render(){if(index>=questions.length){finish();return}selected=null;checked=false;const q=questions[index];document.getElementById('counter').textContent=`Câu ${index+1} / ${questions.length}`;document.getElementById('liveScore').textContent=`Điểm: ${score}`;document.getElementById('bar').style.width=`${index/questions.length*100}%`;document.getElementById('question').textContent=q.q;document.getElementById('feedback').innerHTML='';document.getElementById('checkBtn').disabled=false;document.getElementById('nextBtn').disabled=true;const box=document.getElementById('options');box.innerHTML='';q.options.forEach((o,i)=>{const b=document.createElement('button');b.className='opt';b.textContent=String.fromCharCode(65+i)+'. '+o;b.onclick=()=>choose(o,b);box.appendChild(b)})}
function choose(value,btn){if(checked)return;selected=value;document.querySelectorAll('.opt').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected')}
function checkAnswer(){if(!selected){document.getElementById('feedback').innerHTML='<div class="feedback bad">Bạn hãy chọn một đáp án trước nhé.</div>';return}if(checked)return;checked=true;const q=questions[index],good=selected.toLowerCase()===q.answer.toLowerCase();if(good)score++;document.querySelectorAll('.opt').forEach(b=>{const val=b.textContent.slice(3);if(val.toLowerCase()===q.answer.toLowerCase())b.classList.add('correct');else if(val===selected)b.classList.add('wrong')});document.getElementById('feedback').innerHTML=`<div class="feedback ${good?'good':'bad'}"><b>${good?'✓ Chính xác!':'✗ Chưa đúng.'}</b><br>Đáp án: <b>${q.answer}</b><br>${q.meaning}<br><span class="small">${q.explain}</span></div>`;document.getElementById('liveScore').textContent=`Điểm: ${score}`;document.getElementById('checkBtn').disabled=true;document.getElementById('nextBtn').disabled=false}
function nextQuestion(){index++;render()}
function finish(){document.getElementById('quizArea').classList.add('hidden');document.getElementById('resultArea').classList.remove('hidden');document.getElementById('bar').style.width='100%';document.getElementById('finalScore').textContent=`${score} / ${questions.length} câu đúng`;document.getElementById('finalText').textContent=score>=10?'Xuất sắc! Bạn đã nắm khá vững các từ nối.':score>=7?'Tốt lắm! Hãy xem lại các câu sai để nhớ lâu hơn.':'Cố lên! Hãy xem mục “Học từ nối” rồi thử lại nhé.'}
function restart(){index=0;score=0;document.getElementById('quizArea').classList.remove('hidden');document.getElementById('resultArea').classList.add('hidden');render()}render();
</script></body></html>'''

@app.route("/")
def home():
    return render_template_string(PAGE, questions=QUESTIONS, connectors=CONNECTORS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
 
