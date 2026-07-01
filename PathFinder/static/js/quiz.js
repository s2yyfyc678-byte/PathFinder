(function(){
    document.addEventListener('DOMContentLoaded', () => {
        const steps = Array.from(document.querySelectorAll('.step'));
        const progressBar = document.getElementById('progress-bar');
        let current = 0;

    function update() {
        steps.forEach((s, i) => s.classList.toggle('active', i === current));
        const pct = Math.round((current) / (steps.length - 1) * 100);
        progressBar.style.width = pct + '%';
        document.getElementById('back-btn').style.visibility = current === 0 ? 'hidden' : 'visible';
        const lang = window.selectedQuizLanguage || 'en';
        const dict = (window.quizI18n && window.quizI18n[lang]) || window.quizI18n.en;
        document.getElementById('next-btn').innerText = current === steps.length -1 ? (dict.finish || 'Finish') : (dict.next || 'Next');
    }

        // Option click handling
        document.querySelectorAll('.question .option').forEach(opt => {
        opt.addEventListener('click', () => {
            const questionEl = opt.closest('.question');
            const qid = questionEl.dataset.q;
            // q13 is personality -> single-select
            if(qid === 'q13'){
                questionEl.querySelectorAll('.option').forEach(el => el.classList.remove('selected'));
                opt.classList.add('selected');
            } else {
                opt.classList.toggle('selected');
            }
        });
    });

        // Internationalization
        window.selectedQuizLanguage = window.selectedQuizLanguage || 'en';
        function applyLanguage(lang){
            const dict = (window.quizI18n && window.quizI18n[lang]) || window.quizI18n.en;
            // header
            const titleEl = document.querySelector('.chat-shell h2');
            if(titleEl) titleEl.innerText = dict.title;
            const subtitleEl = document.querySelector('.chat-shell p');
            if(subtitleEl) subtitleEl.innerText = dict.subtitle;
            // questions
            document.querySelectorAll('.question').forEach(q => {
                const qid = q.dataset.q;
                const label = dict.questions && dict.questions[qid];
                if(label){
                    const h = q.querySelector('h4');
                    if(h) h.innerText = label;
                }
                // options
                q.querySelectorAll('.option').forEach(opt => {
                    const val = opt.dataset.value;
                    if(dict.options && dict.options[val]) opt.innerText = dict.options[val];
                });
            });
            // buttons
            document.getElementById('next-btn').innerText = dict.next;
            document.getElementById('back-btn').innerText = dict.back;
            // mark active lang button
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.language === lang));
            window.selectedQuizLanguage = lang;
        }

        // bind language buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', ()=>{
                applyLanguage(btn.dataset.language);
            });
        });

        // apply initial language
        applyLanguage(window.selectedQuizLanguage);

    function collectAnswers(){
        const answers = {};
        document.querySelectorAll('.question').forEach(q => {
            const qid = q.dataset.q;
            const selected = Array.from(q.querySelectorAll('.option.selected')).map(el => el.dataset.value);
            answers[qid] = selected;
        });
        return answers;
    }

    document.getElementById('next-btn').addEventListener('click', ()=>{
        if(current < steps.length -1){
            current +=1;
            update();
            return;
        }

        const answers = collectAnswers();

        // Build fields from question groups
        const interests = [];
        for(let i=1;i<=6;i++){ if(answers['q'+i]) interests.push(...answers['q'+i]); }
        const skills = [];
        for(let i=7;i<=12;i++){ if(answers['q'+i]) skills.push(...answers['q'+i]); }
        const personality = (answers['q13'] && answers['q13'][0]) ? answers['q13'][0] : '';
        const values = [];
        for(let i=14;i<=20;i++){ if(answers['q'+i]) values.push(...answers['q'+i]); }

        if(!personality){
            alert('Please select the personality question (one option).');
            return;
        }

        fetch('/submit_quiz',{
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                interests: Array.from(new Set(interests)).join(','),
                skills: Array.from(new Set(skills)).join(','),
                personality: personality,
                values: Array.from(new Set(values)).join(','),
                language: window.selectedQuizLanguage
            })
        }).then(()=>{
            window.location = '/results';
        }).catch(()=>{
            alert('Could not submit quiz.');
        });
    });

    document.getElementById('back-btn').addEventListener('click', ()=>{
        if(current>0) current -=1;
        update();
    });

    update();
    });
})();
