<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>PDF ↔ WORD · Converter</title>
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3VQ15YNST7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-3VQ15YNST7');
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --cream:#F5F0E8;
  --brown:#2C1810;
  --rust:#C4521A;
  --gold:#D4A832;
  --sage:#4A7856;
  --paper:#EDE8DC;
  --shadow:#1a0f0a;
  --mono:'Space Mono',monospace;
  --sans:'DM Sans',sans-serif;
}

body{
  font-family:var(--sans);
  background:var(--cream);
  color:var(--brown);
  min-height:100vh;
  padding:24px 16px;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(196,82,26,0.06) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(212,168,50,0.06) 0%, transparent 50%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%232C1810' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.wrap{max-width:600px;margin:0 auto;}

/* Header */
header{text-align:center;margin-bottom:32px;}
.stamp{
  display:inline-block;
  border:3px solid var(--brown);
  padding:6px 20px;
  font-family:var(--mono);
  font-size:11px;
  letter-spacing:4px;
  text-transform:uppercase;
  color:var(--rust);
  margin-bottom:16px;
  position:relative;
}
.stamp::before,.stamp::after{
  content:'✦';
  position:absolute;
  top:50%;transform:translateY(-50%);
  color:var(--gold);
  font-size:10px;
}
.stamp::before{left:-20px;}
.stamp::after{right:-20px;}

h1{
  font-family:var(--mono);
  font-size:clamp(28px,6vw,42px);
  font-weight:700;
  line-height:1.1;
  letter-spacing:-1px;
}
h1 span{color:var(--rust);}
.tagline{
  font-size:13px;
  color:#7a6a5a;
  margin-top:8px;
  font-style:italic;
}

/* Card */
.card{
  background:var(--paper);
  border:2px solid var(--brown);
  border-radius:4px;
  padding:28px;
  box-shadow:6px 6px 0 var(--brown);
  margin-bottom:20px;
}

.card-label{
  font-family:var(--mono);
  font-size:10px;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--rust);
  margin-bottom:16px;
  display:flex;align-items:center;gap:8px;
}
.card-label::after{content:'';flex:1;height:1px;background:var(--rust);opacity:0.3;}

/* Drop zone */
.drop-zone{
  border:2px dashed #b0a090;
  border-radius:4px;
  padding:36px 20px;
  text-align:center;
  cursor:pointer;
  transition:all 0.2s;
  position:relative;
  background:rgba(255,255,255,0.4);
}
.drop-zone:hover,.drop-zone.drag-over{
  border-color:var(--rust);
  background:rgba(196,82,26,0.04);
}
.drop-zone input[type=file]{
  position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;
}
.drop-icon{font-size:40px;margin-bottom:10px;display:block;}
.drop-title{font-family:var(--mono);font-size:14px;font-weight:700;margin-bottom:6px;}
.drop-sub{font-size:13px;color:#7a6a5a;}
.drop-sub b{color:var(--rust);}

/* File preview */
.file-preview{
  display:none;align-items:center;gap:12px;
  background:rgba(196,82,26,0.06);
  border:1px solid rgba(196,82,26,0.3);
  border-radius:4px;padding:12px 16px;margin-top:14px;
}
.file-preview.show{display:flex;}
.file-icon{font-size:26px;flex-shrink:0;}
.file-info{flex:1;min-width:0;}
.file-name{font-family:var(--mono);font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.file-size{font-size:12px;color:#7a6a5a;margin-top:2px;}
.file-remove{background:none;border:none;cursor:pointer;font-size:16px;color:#b0a090;padding:2px 6px;border-radius:3px;transition:all 0.15s;}
.file-remove:hover{color:var(--rust);background:rgba(196,82,26,0.1);}

/* Buttons */
.btn-convert{
  width:100%;margin-top:16px;padding:14px;
  border:2px solid var(--brown);border-radius:4px;
  font-family:var(--mono);font-size:14px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  cursor:pointer;
  background:var(--brown);color:var(--cream);
  box-shadow:4px 4px 0 var(--rust);
  transition:all 0.15s;
  display:flex;align-items:center;justify-content:center;gap:10px;
}
.btn-convert:hover:not(:disabled){
  transform:translate(-2px,-2px);
  box-shadow:6px 6px 0 var(--rust);
}
.btn-convert:active:not(:disabled){
  transform:translate(2px,2px);
  box-shadow:2px 2px 0 var(--rust);
}
.btn-convert:disabled{opacity:0.4;cursor:not-allowed;transform:none;}

/* Progress */
.progress-wrap{display:none;margin-top:16px;}
.progress-wrap.show{display:block;}
.progress-track{
  background:#d4cfc7;border:1px solid #b0a090;
  border-radius:2px;height:8px;overflow:hidden;
}
.progress-fill{
  height:100%;width:0%;border-radius:2px;
  background:repeating-linear-gradient(
    45deg,var(--rust),var(--rust) 10px,
    #d4652a 10px,#d4652a 20px
  );
  background-size:28px 8px;
  animation:march 0.5s linear infinite;
  transition:width 0.3s;
}
@keyframes march{0%{background-position:0 0;}100%{background-position:28px 0;}}
.progress-label{font-family:var(--mono);font-size:11px;color:#7a6a5a;margin-top:6px;text-align:center;letter-spacing:1px;}

/* Result */
.result{display:none;margin-top:16px;border-radius:4px;padding:16px;text-align:center;}
.result.show{display:block;}
.result.success{background:rgba(74,120,86,0.08);border:2px solid var(--sage);}
.result.error{background:rgba(196,82,26,0.08);border:2px solid var(--rust);}
.result-icon{font-size:28px;margin-bottom:8px;}
.result-msg{font-family:var(--mono);font-size:13px;font-weight:700;margin-bottom:4px;}
.result-sub{font-size:12px;color:#7a6a5a;margin-bottom:14px;}

.btn-download{
  display:inline-flex;align-items:center;gap:6px;
  padding:10px 20px;border-radius:4px;
  border:2px solid var(--sage);
  background:var(--sage);color:white;
  font-family:var(--mono);font-size:12px;font-weight:700;
  letter-spacing:1px;text-decoration:none;
  box-shadow:3px 3px 0 var(--brown);
  transition:all 0.15s;
}
.btn-download:hover{transform:translate(-1px,-1px);box-shadow:4px 4px 0 var(--brown);}

.btn-again{
  display:inline-block;margin-top:10px;
  font-family:var(--mono);font-size:11px;
  color:var(--rust);cursor:pointer;
  background:none;border:none;letter-spacing:1px;
  text-decoration:underline;text-underline-offset:3px;
}

/* History */
.history-card{margin-top:0;}
.history-empty{
  font-family:var(--mono);font-size:12px;
  color:#b0a090;text-align:center;padding:16px 0;
  letter-spacing:1px;
}
.history-list{list-style:none;}
.history-item{
  display:flex;align-items:center;gap:10px;
  padding:10px 0;border-bottom:1px dashed #c8c0b0;
  font-size:13px;
}
.history-item:last-child{border-bottom:none;}
.hi-icon{font-size:18px;flex-shrink:0;}
.hi-info{flex:1;min-width:0;}
.hi-name{font-family:var(--mono);font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.hi-meta{font-size:11px;color:#7a6a5a;margin-top:2px;}
.hi-dl{
  font-family:var(--mono);font-size:11px;
  color:var(--sage);text-decoration:none;
  border:1px solid var(--sage);border-radius:3px;
  padding:3px 8px;white-space:nowrap;
  transition:all 0.15s;flex-shrink:0;
}
.hi-dl:hover{background:var(--sage);color:white;}

/* Footer */
footer{
  text-align:center;margin-top:24px;
  font-family:var(--mono);font-size:10px;
  color:#b0a090;letter-spacing:2px;
  text-transform:uppercase;
}
footer span{color:var(--rust);}

/* Ticker */
.ticker{
  border-top:1px solid #c8c0b0;
  border-bottom:1px solid #c8c0b0;
  overflow:hidden;padding:6px 0;margin-bottom:24px;
  font-family:var(--mono);font-size:11px;
  color:#7a6a5a;letter-spacing:1px;
  white-space:nowrap;
}
.ticker-inner{display:inline-block;animation:tick 18s linear infinite;}
@keyframes tick{0%{transform:translateX(100vw);}100%{transform:translateX(-100%);}}
</style>
</head>
<body>
<div class="wrap">

  <div class="ticker">
    <span class="ticker-inner">✦ PDF TO WORD ✦ WORD TO PDF ✦ MIỄN PHÍ ✦ NHANH CHÓNG ✦ BẢO MẬT ✦ FILE TỰ XÓA SAU 10 PHÚT ✦ HỖ TRỢ .PDF .DOCX .DOC ✦</span>
  </div>

  <header>
    <div class="stamp">Công cụ chuyển đổi</div>
    <h1>PDF <span>↔</span> WORD</h1>
    <p class="tagline">Chuyển đổi tài liệu nhanh chóng · Không cần đăng ký · Miễn phí</p>
  </header>

  <!-- Upload Card -->
  <div class="card">
    <div class="card-label">① Chọn file</div>

    <div class="drop-zone" id="dropZone">
      <input type="file" id="fileInput" accept=".pdf,.docx,.doc"/>
      <span class="drop-icon">📂</span>
      <div class="drop-title">Kéo thả file vào đây</div>
      <div class="drop-sub">hoặc nhấn để chọn &nbsp;·&nbsp; <b>.pdf → .docx</b> &nbsp;|&nbsp; <b>.docx → .pdf</b></div>
      <div class="drop-sub" style="margin-top:4px;font-size:11px;">Tối đa 20MB</div>
    </div>

    <div class="file-preview" id="filePreview">
      <div class="file-icon" id="fileIcon">📄</div>
      <div class="file-info">
        <div class="file-name" id="fileName"></div>
        <div class="file-size" id="fileSize"></div>
      </div>
      <button class="file-remove" id="fileRemove">✕</button>
    </div>

    <button class="btn-convert" id="btnConvert" disabled>
      <span>⚙</span> CHUYỂN ĐỔI NGAY
    </button>

    <div class="progress-wrap" id="progressWrap">
      <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
      <div class="progress-label" id="progressLabel">ĐANG XỬ LÝ...</div>
    </div>

    <div class="result" id="result">
      <div class="result-icon" id="resultIcon"></div>
      <div class="result-msg" id="resultMsg"></div>
      <div class="result-sub" id="resultSub"></div>
      <div id="resultActions"></div>
      <br>
      <button class="btn-again" id="btnAgain">↩ Chuyển file khác</button>
    </div>
  </div>

  <!-- History Card -->
  <div class="card history-card">
    <div class="card-label">② Lịch sử chuyển đổi</div>
    <ul class="history-list" id="historyList">
      <li class="history-empty" id="historyEmpty">— Chưa có file nào được chuyển đổi —</li>
    </ul>
  </div>

  <!-- Stats Card -->
  <div class="card" style="text-align:center;padding:20px 28px;">
    <div class="card-label" style="justify-content:center;">③ Thống kê</div>

    <!-- Giới hạn ngày -->
    <div style="margin-bottom:16px;padding:12px;background:rgba(196,82,26,0.06);border:1px solid rgba(196,82,26,0.2);border-radius:6px;">
      <div style="font-family:var(--mono);font-size:12px;color:#7a6a5a;margin-bottom:6px;">HÔM NAY ĐÃ DÙNG</div>
      <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--rust)" id="statToday">0</div>
      <div style="font-size:12px;color:#7a6a5a;margin-top:2px;">/ <span id="statLimit">8</span> lần · còn <span id="statRemaining" style="color:var(--sage);font-weight:600;">8</span> lần hôm nay</div>
      <div style="margin-top:8px;background:#d4cfc7;border-radius:99px;height:6px;overflow:hidden;">
        <div id="statBar" style="height:100%;border-radius:99px;background:var(--rust);width:0%;transition:width 0.4s;"></div>
      </div>
    </div>

    <div style="display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin-top:8px;">
      <div>
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--rust)" id="statTotal">0</div>
        <div style="font-size:12px;color:#7a6a5a;margin-top:4px;">Tổng lượt convert</div>
      </div>
      <div>
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--sage)" id="statPdf">0</div>
        <div style="font-size:12px;color:#7a6a5a;margin-top:4px;">PDF → Word</div>
      </div>
      <div>
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--gold)" id="statWord">0</div>
        <div style="font-size:12px;color:#7a6a5a;margin-top:4px;">Word → PDF</div>
      </div>
    </div>
  </div>

  <footer>
    Chạy trên ☁️ Render &nbsp;·&nbsp; File tự xóa sau <span>10 phút</span> &nbsp;·&nbsp; Không lưu dữ liệu
  </footer>
</div>

<script>
const dropZone=document.getElementById('dropZone');
const fileInput=document.getElementById('fileInput');
const filePreview=document.getElementById('filePreview');
const fileIcon=document.getElementById('fileIcon');
const fileName=document.getElementById('fileName');
const fileSize=document.getElementById('fileSize');
const fileRemove=document.getElementById('fileRemove');
const btnConvert=document.getElementById('btnConvert');
const progressWrap=document.getElementById('progressWrap');
const progressFill=document.getElementById('progressFill');
const progressLabel=document.getElementById('progressLabel');
const result=document.getElementById('result');
const resultIcon=document.getElementById('resultIcon');
const resultMsg=document.getElementById('resultMsg');
const resultSub=document.getElementById('resultSub');
const resultActions=document.getElementById('resultActions');
const btnAgain=document.getElementById('btnAgain');
const historyList=document.getElementById('historyList');
const historyEmpty=document.getElementById('historyEmpty');

let selectedFile=null;
let history=[];

function fmtSize(b){
  if(b<1024)return b+' B';
  if(b<1048576)return(b/1024).toFixed(1)+' KB';
  return(b/1048576).toFixed(1)+' MB';
}
function fmtTime(){
  const d=new Date();
  return d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');
}

function setFile(file){
  if(!file)return;
  const ext=file.name.split('.').pop().toLowerCase();
  if(!['pdf','docx','doc'].includes(ext)){alert('Chỉ hỗ trợ .pdf hoặc .docx');return;}
  if(file.size>20*1024*1024){alert('File tối đa 20MB');return;}
  selectedFile=file;
  fileIcon.textContent=ext==='pdf'?'📕':'📘';
  fileName.textContent=file.name;
  const outExt=ext==='pdf'?'.docx':'.pdf';
  fileSize.textContent=fmtSize(file.size)+' · sẽ ra '+outExt;
  filePreview.classList.add('show');
  btnConvert.disabled=false;
  result.classList.remove('show');
  progressWrap.classList.remove('show');
}

fileInput.addEventListener('change',()=>setFile(fileInput.files[0]));
dropZone.addEventListener('dragover',e=>{e.preventDefault();dropZone.classList.add('drag-over');});
dropZone.addEventListener('dragleave',()=>dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop',e=>{e.preventDefault();dropZone.classList.remove('drag-over');setFile(e.dataTransfer.files[0]);});
fileRemove.addEventListener('click',reset);

function reset(){
  selectedFile=null;fileInput.value='';
  filePreview.classList.remove('show');
  btnConvert.disabled=true;
  result.classList.remove('show');
  progressWrap.classList.remove('show');
  progressFill.style.width='0%';
}
btnAgain.addEventListener('click',reset);

// Load stats khi mở trang
async function loadStats(){
  try{
    const r=await fetch('/stats');
    const d=await r.json();
    document.getElementById('statTotal').textContent=d.total||0;
    document.getElementById('statPdf').textContent=d.pdf_to_word||0;
    document.getElementById('statWord').textContent=d.word_to_pdf||0;
    const today=d.today_count||0;
    const limit=d.daily_limit||8;
    const remaining=d.remaining||limit;
    document.getElementById('statToday').textContent=today;
    document.getElementById('statLimit').textContent=limit;
    document.getElementById('statRemaining').textContent=remaining;
    document.getElementById('statBar').style.width=(today/limit*100)+'%';
  }catch(e){}
}
loadStats();

function addHistory(name,url,method,success){
  const ext=name.split('.').pop().toUpperCase();
  const icon=ext==='PDF'?'📕':'📘';
  const item={name,url,method,success,time:fmtTime(),icon};
  history.unshift(item);
  if(history.length>10)history.pop();
  renderHistory();
}

function renderHistory(){
  if(history.length===0){
    historyEmpty.style.display='';return;
  }
  historyEmpty.style.display='none';
  const existing=historyList.querySelectorAll('.history-item');
  existing.forEach(e=>e.remove());
  history.forEach(h=>{
    const li=document.createElement('li');
    li.className='history-item';
    li.innerHTML=`
      <span class="hi-icon">${h.icon}</span>
      <div class="hi-info">
        <div class="hi-name">${h.name}</div>
        <div class="hi-meta">${h.time} · ${h.method} · ${h.success?'✓ Thành công':'✗ Thất bại'}</div>
      </div>
      ${h.success?`<a class="hi-dl" href="${h.url}" download="${h.name}">↓ TẢI</a>`:''}
    `;
    historyList.appendChild(li);
  });
}

btnConvert.addEventListener('click',async()=>{
  if(!selectedFile)return;
  btnConvert.disabled=true;
  result.classList.remove('show');
  progressWrap.classList.add('show');
  progressLabel.textContent='ĐANG TẢI LÊN...';

  let pct=0;
  const ticker=setInterval(()=>{
    pct=Math.min(pct+Math.random()*10,88);
    progressFill.style.width=pct+'%';
    if(pct>30)progressLabel.textContent='ĐANG CHUYỂN ĐỔI...';
    if(pct>70)progressLabel.textContent='SẮP XONG...';
  },300);

  const fd=new FormData();
  fd.append('file',selectedFile);

  try{
    const res=await fetch('/convert',{method:'POST',body:fd});
    const data=await res.json();
    clearInterval(ticker);
    progressFill.style.width='100%';
    progressLabel.textContent='HOÀN TẤT!';

    setTimeout(()=>{
      progressWrap.classList.remove('show');
      result.classList.add('show');
      if(data.success){
          // Cập nhật stats
          if(data.stats){
            const s=data.stats;
            document.getElementById('statTotal').textContent=s.total||0;
            document.getElementById('statPdf').textContent=s.pdf_to_word||0;
            document.getElementById('statWord').textContent=s.word_to_pdf||0;
            const today=s.today_count||0;
            const limit=s.daily_limit||8;
            const remaining=s.remaining||0;
            document.getElementById('statToday').textContent=today;
            document.getElementById('statLimit').textContent=limit;
            document.getElementById('statRemaining').textContent=remaining;
            document.getElementById('statBar').style.width=(today/limit*100)+'%';
          } else { loadStats(); }
        result.className='result show success';
        resultIcon.textContent='✅';
        resultMsg.textContent='CHUYỂN ĐỔI THÀNH CÔNG!';
        resultSub.textContent=data.filename+' · '+data.method;
        resultActions.innerHTML=`<a class="btn-download" href="${data.download_url}" download="${data.filename}">↓ TẢI VỀ ${data.filename}</a>`;
        addHistory(data.filename,data.download_url,data.method,true);
      }else{
        result.className='result show error';
        resultIcon.textContent='✗';
        resultMsg.textContent='CHUYỂN ĐỔI THẤT BẠI';
        resultSub.textContent=data.error||'Vui lòng thử lại.';
        resultActions.innerHTML='';
        addHistory(selectedFile.name,'','',false);
        btnConvert.disabled=false;
      }
    },500);
  }catch(e){
    clearInterval(ticker);
    progressWrap.classList.remove('show');
    result.className='result show error';
    result.classList.add('show');
    resultIcon.textContent='✗';
    resultMsg.textContent='LỖI KẾT NỐI';
    resultSub.textContent='Kiểm tra server đang chạy chưa.';
    resultActions.innerHTML='';
    btnConvert.disabled=false;
  }
});
</script>
</body>
</html>
