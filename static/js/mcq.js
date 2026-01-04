// Variables are initialized in mcq.html template

const questionTextEl = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const feedback = document.getElementById('feedback');
const feedbackTitle = document.getElementById('feedback-title');
const feedbackAnswer = document.getElementById('feedback-answer');
const feedbackExplanation = document.getElementById('feedback-explanation');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');
const reportIcon = document.getElementById('report-icon');
const progressText = document.getElementById('progress-text');
const questionCounter = document.getElementById('question-counter');
const testTitle = document.getElementById('test-title');

let answered = false;
let userAttempts = {}; // Store user attempts

// Initialize userAttempts from questionData
questionData.forEach(q => {
    if (q.selected) {
        userAttempts[q.id] = {
            selected_text: q.selected,
            is_correct: q.is_correct
        };
    }
});

// Find the first unattempted question, or start from beginning if all are attempted
let currentIndex = 0;
const firstUnattemptedIndex = questionData.findIndex(q => !q.selected || q.selected === '');
if (firstUnattemptedIndex !== -1) {
    currentIndex = firstUnattemptedIndex;
}

testTitle.textContent = title;

function updateNavigationState() {
    prevBtn.disabled = currentIndex === 0;
    // Next/Finish button is only enabled after answering
    if (!answered) {
        nextBtn.disabled = true;
    }
}

function renderQuestion() {
    const q = questionData[currentIndex];
    questionTextEl.innerHTML = q.question;
    questionCounter.textContent = `Question ${currentIndex + 1}`;
    progressText.innerHTML = `${currentIndex + 1}<span>/${questionData.length}</span>`;
    optionsContainer.innerHTML = '';

    // Check if user has a previous attempt for this question
    const previousAttempt = userAttempts[q.id] || (q.selected ? {
        selected_text: q.selected,
        is_correct: q.is_correct
    } : null);

    if (previousAttempt) {
        answered = true;
        feedback.style.display = 'block';
        nextBtn.disabled = false;
        nextBtn.textContent = (currentIndex === questionData.length - 1) ? 'Finish' : 'Next Question →';
    } else {
        answered = false;
        feedback.style.display = 'none';
        nextBtn.disabled = true;
    }

    q.options.forEach((opt) => {
        const div = document.createElement('div');
        div.className = 'option';
        div.dataset.key = opt.key;
        div.innerHTML = `<span>${opt.label}</span>`;
        
        // Check if this option was previously selected
        const wasSelected = previousAttempt && previousAttempt.selected_text === opt.label;
        const isCorrect = opt.key === q.correct;
        
        if (previousAttempt) {
            div.classList.add('disabled');
            if (isCorrect) {
                div.classList.add('correct');
                const pill = document.createElement('span');
                pill.className = 'pill correct';
                pill.textContent = '✓';
                div.appendChild(pill);
            }
            if (wasSelected && !isCorrect) {
                div.classList.add('incorrect');
                const pill = document.createElement('span');
                pill.className = 'pill incorrect';
                pill.textContent = '✕';
                div.appendChild(pill);
            }
        } else {
            div.addEventListener('click', () => handleSelect(opt.key, opt.label));
        }
        
        optionsContainer.appendChild(div);
    });

    // Show feedback if there's a previous attempt
    if (previousAttempt) {
        if (previousAttempt.is_correct) {
            feedbackTitle.textContent = 'Correct!';
            feedbackAnswer.innerHTML = `You selected the right answer: ${q.options.find(o => o.key === q.correct).label}`;
        } else {
            feedbackTitle.textContent = 'Wrong answer!';
            const correctLabel = q.options.find(o => o.key === q.correct).label;
            feedbackAnswer.innerHTML = `Correct Answer: ${correctLabel}`;
        }
        feedbackExplanation.innerHTML = q.explanation || 'Explanation not available.';
    }
    
    updateNavigationState();
    typesetMath();
}

function handleSelect(selectedKey, selectedText) {
    if (answered) return;
    answered = true;
    const q = questionData[currentIndex];
    const correctKey = q.correct;
    const isCorrect = selectedKey === correctKey;

    // Save attempt to database
    saveAttemptToDB(q.id, selectedText, isCorrect);

    // Store in local memory
    userAttempts[q.id] = {
        selected_text: selectedText,
        is_correct: isCorrect
    };

    optionsContainer.querySelectorAll('.option').forEach(opt => {
        const key = opt.dataset.key;
        opt.classList.add('disabled');
        if (key === correctKey) {
            opt.classList.add('correct');
            const pill = document.createElement('span');
            pill.className = 'pill correct';
            pill.textContent = '✓';
            opt.appendChild(pill);
        }
        if (key === selectedKey && key !== correctKey) {
            opt.classList.add('incorrect');
            const pill = document.createElement('span');
            pill.className = 'pill incorrect';
            pill.textContent = '✕';
            opt.appendChild(pill);
        }
    });

    if (isCorrect) {
        feedbackTitle.textContent = 'Correct!';
        feedbackAnswer.innerHTML = `You selected the right answer: ${q.options.find(o => o.key === correctKey).label}`;
    } else {
        feedbackTitle.textContent = 'Wrong answer!';
        const correctLabel = q.options.find(o => o.key === correctKey).label;
        feedbackAnswer.innerHTML = `Correct Answer: ${correctLabel}`;
    }
    feedbackExplanation.innerHTML = q.explanation || 'Explanation not available.';
    feedback.style.display = 'block';
    nextBtn.disabled = false;
    nextBtn.textContent = (currentIndex === questionData.length - 1) ? 'Finish' : 'Next Question →';
    updateNavigationState();
    typesetMath();
}

function saveAttemptToDB(questionId, selectedText, isCorrect) {
    if (typeof isAuthenticated !== 'undefined' && isAuthenticated) {
        const formData = new FormData();
        formData.append('question_id', questionId);
        formData.append('selected_text', selectedText);
        if (typeof csrfToken !== 'undefined') {
            formData.append('csrfmiddlewaretoken', csrfToken);
        }

        // Use correct endpoint based on question type
        const endpoint = (typeof isPastPaper !== 'undefined' && isPastPaper) 
            ? '/api/save-past-paper-attempt/' 
            : '/api/save-attempt/';

        fetch(endpoint, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Failed to save attempt:', data.error);
            }
        })
        .catch(error => {
            console.error('Error saving attempt:', error);
        });
    } else {
        // User not authenticated, just store locally
        console.log('User not authenticated, attempt not saved to database');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function goToNext() {
    if (currentIndex < questionData.length - 1) {
        currentIndex += 1;
        renderQuestion();
    } else {
        // If on last question, redirect to dashboard
        window.location.href = '/dashboard/';
    }
}

function goToPrev() {
    if (currentIndex > 0) {
        currentIndex -= 1;
        renderQuestion();
    }
}

nextBtn.addEventListener('click', goToNext);
prevBtn.addEventListener('click', goToPrev);

// Report icon click handler
const reportIconEl = document.getElementById('report-icon');
if (reportIconEl) {
    reportIconEl.addEventListener('click', () => {
        const currentQuestion = questionData[currentIndex];
        const questionType = isPastPaper ? 'past_paper' : 'regular';
        // Navigate to report page
        window.location.href = `/report/${questionType}/${currentQuestion.id}/`;
    });
}

function typesetMath() {
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
}

// Back button handler
const backBtn = document.getElementById('back-btn');
if (backBtn) {
    backBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Try to construct the paper selection URL from current URL
        const currentPath = window.location.pathname;
        // URL pattern: /mcq/{chapter_slug}/{paper_type}/
        const pathParts = currentPath.split('/').filter(part => part);
        
        if (pathParts.length >= 2 && pathParts[0] === 'mcq') {
            // Extract chapter_slug (second part)
            const chapterSlug = pathParts[1];
            // Navigate to paper selection page
            window.location.href = `/chapter/${chapterSlug}/`;
        } else {
            // Fallback to dashboard if URL pattern doesn't match
            window.location.href = '/dashboard/';
        }
    });
}

renderQuestion();
