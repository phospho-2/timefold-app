// TimefoldAI カスタマイズ機能 JavaScript

const CUSTOMIZE_API = '/api/customize';
let currentConfig = {};

// カスタマイズパネルを開く
function openCustomizePanel() {
    console.log('🔧 カスタマイズパネルを開きます');
    const modal = document.getElementById('customizeModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('visible');
        modal.style.display = 'block';
        
        loadCurrentConfig();
        loadCurrentSubjects();
        loadCurrentTeachers();
        
        console.log('✅ カスタマイズパネル表示完了');
    } else {
        console.error('❌ customizeModal要素が見つかりません');
        alert('カスタマイズパネルの表示に失敗しました');
    }
}

// カスタマイズパネルを閉じる
function closeCustomizePanel() {
    console.log('🔧 カスタマイズパネルを閉じます');
    const modal = document.getElementById('customizeModal');
    if (modal) {
        modal.classList.remove('visible');
        modal.classList.add('hidden');
        modal.style.display = 'none';
    }
}

// カスタマイズタブの切り替え
function showCustomizeTab(tabName, clickedElement = null) {
    document.querySelectorAll('.customize-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.customize-tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    if (clickedElement) {
        clickedElement.classList.add('active');
    }
}

// 現在の設定を読み込み
async function loadCurrentConfig() {
    try {
        const response = await fetch(`${CUSTOMIZE_API}/config`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const config = await response.json();
        currentConfig = config;
        
        document.getElementById('startHour').value = config.start_hour;
        document.getElementById('endHour').value = config.end_hour;
        document.getElementById('lessonDuration').value = config.lesson_duration;
        document.getElementById('breakDuration').value = config.break_duration;
        document.getElementById('schoolName').value = config.school_name;
        
        console.log('📊 現在の設定読み込み完了:', config);
        
    } catch (error) {
        console.error('設定読み込みエラー:', error);
        showMessage('設定の読み込みに失敗しました', 'error');
    }
}

// 時間設定のプレビュー
async function previewTimeSettings() {
    const tempConfig = {
        start_hour: parseInt(document.getElementById('startHour').value),
        end_hour: parseInt(document.getElementById('endHour').value),
        lesson_duration: parseInt(document.getElementById('lessonDuration').value),
        break_duration: parseInt(document.getElementById('breakDuration').value)
    };
    
    try {
        console.log('📋 プレビュー設定:', tempConfig);
        
        const response = await fetch(`${CUSTOMIZE_API}/preview-timeslots`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(tempConfig)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const previewSlots = await response.json();
        console.log('📅 プレビュー結果:', previewSlots);
        
        displayPreview(previewSlots);
        
        // プレビュータブに切り替え（event.target エラー修正）
        showCustomizeTab('preview');
        document.querySelectorAll('.customize-tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        const previewButton = document.querySelector('[onclick*="preview"]');
        if (previewButton) {
            previewButton.classList.add('active');
        }
        
        showMessage('✅ プレビューを表示しました', 'success');
        
    } catch (error) {
        console.error('プレビュー生成エラー:', error);
        displayPreview([]);
        showMessage('設定プレビューを表示します', 'info');
    }
}

// プレビュー表示
function displayPreview(timeslots) {
    const previewContent = document.getElementById('previewContent');
    
    if (!timeslots || timeslots.length === 0) {
        const startHour = parseInt(document.getElementById('startHour').value);
        const endHour = parseInt(document.getElementById('endHour').value);
        const lessonDuration = parseInt(document.getElementById('lessonDuration').value);
        const breakDuration = parseInt(document.getElementById('breakDuration').value);
        
        const totalMinutes = (endHour - startHour) * 60;
        const slotDuration = lessonDuration + breakDuration;
        const slotsPerDay = Math.floor((totalMinutes - 60) / slotDuration);
        
        previewContent.innerHTML = `
            <h4>📅 時間設定プレビュー</h4>
            <div class="preview-info">
                <p><strong>開始時刻:</strong> ${startHour}:00</p>
                <p><strong>終了時刻:</strong> ${endHour}:00</p>
                <p><strong>授業時間:</strong> ${lessonDuration}分</p>
                <p><strong>休憩時間:</strong> ${breakDuration}分</p>
                <p><strong>1日のコマ数:</strong> 約${slotsPerDay}コマ</p>
                <p><strong>週間総コマ数:</strong> 約${slotsPerDay * 5}コマ</p>
            </div>
            <p style="color: #f39c12; margin-top: 15px;">💡 設定を保存すると、実際の時間枠が生成されます。</p>
        `;
        return;
    }
    
    const days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'];
    const dayNames = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日'];
    
    let html = `
        <h4>📅 新しい時間割構成プレビュー</h4>
        <p>総時間枠数: <strong>${timeslots.length}個</strong> (1日平均: <strong>${Math.round(timeslots.length / 5)}コマ</strong>)</p>
        <div class="preview-grid">
    `;
    
    days.forEach((day, index) => {
        const daySlots = timeslots.filter(slot => slot.day_of_week === day);
        html += `<div class="preview-day"><h4>${dayNames[index]}</h4>`;
        daySlots.forEach(slot => {
            html += `<div class="preview-slot">${slot.period_name}<br>${slot.start_time}-${slot.end_time}</div>`;
        });
        html += '</div>';
    });
    
    html += '</div>';
    previewContent.innerHTML = html;
}

// 時間設定を保存
async function saveTimeSettings() {
    const configData = {
        start_hour: parseInt(document.getElementById('startHour').value),
        end_hour: parseInt(document.getElementById('endHour').value),
        lesson_duration: parseInt(document.getElementById('lessonDuration').value),
        break_duration: parseInt(document.getElementById('breakDuration').value),
        school_name: document.getElementById('schoolName').value
    };
    
    try {
        const response = await fetch(`${CUSTOMIZE_API}/config`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(configData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showMessage('✅ 設定が保存されました！時間枠が更新されます。', 'success');
            setTimeout(() => {
                refreshData();
            }, 1000);
            await loadCurrentConfig();
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
        
    } catch (error) {
        console.error('設定保存エラー:', error);
        showMessage('設定の保存に失敗しました', 'error');
    }
}

// 現在の科目一覧を読み込み（強制キャッシュクリア）
async function loadCurrentSubjects() {
    try {
        const response = await fetch(`/api/subjects?_t=${Date.now()}`); // キャッシュ回避
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const subjects = await response.json();
        
        console.log('📚 科目データ読み込み:', subjects);
        
        const html = subjects.map(subject => `
            <div class="item-card">
                <div class="item-info">
                    <strong>${subject.name}</strong> (${subject.code})
                    <br><small>${subject.category} - 週${subject.weekly_hours}時間</small>
                </div>
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteSubject(${subject.id})">🗑️</button>
                </div>
            </div>
        `).join('');
        
        document.getElementById('currentSubjects').innerHTML = html;
        
    } catch (error) {
        console.error('科目読み込みエラー:', error);
        document.getElementById('currentSubjects').innerHTML = '<p>科目の読み込みに失敗しました</p>';
    }
}

// 科目を追加
async function addSubject() {
    const subjectData = {
        name: document.getElementById('newSubjectName').value,
        code: document.getElementById('newSubjectCode').value,
        category: document.getElementById('subjectCategory').value,
        weekly_hours: parseInt(document.getElementById('weeklyHours').value),
        description: document.getElementById('subjectDescription').value || `${document.getElementById('newSubjectName').value}の授業`
    };
    
    if (!subjectData.name || !subjectData.code) {
        showMessage('科目名と科目コードは必須です', 'error');
        return;
    }
    
    try {
        console.log('📚 科目追加データ:', subjectData);
        
        const response = await fetch(`${CUSTOMIZE_API}/subject`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(subjectData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log('📚 科目追加結果:', result);
        
        if (result.status === 'success') {
            showMessage('✅ ' + result.message, 'success');
            
            document.getElementById('newSubjectName').value = '';
            document.getElementById('newSubjectCode').value = '';
            document.getElementById('subjectDescription').value = '';
            
            // 強制的にリスト更新
            await loadCurrentSubjects();
            
            setTimeout(() => {
                refreshData();
            }, 1500);
            
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
        
    } catch (error) {
        console.error('科目追加エラー:', error);
        showMessage('科目の追加に失敗しました', 'error');
    }
}

// 科目を削除
async function deleteSubject(subjectId) {
    if (!confirm('この科目を削除しますか？')) {
        return;
    }
    
    try {
        const response = await fetch(`${CUSTOMIZE_API}/subject?id=${subjectId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showMessage('✅ ' + result.message, 'success');
            await loadCurrentSubjects();
            setTimeout(() => {
                refreshData();
            }, 1000);
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
        
    } catch (error) {
        console.error('科目削除エラー:', error);
        showMessage('科目の削除に失敗しました', 'error');
    }
}

// 現在の教師一覧を読み込み（強制キャッシュクリア）
async function loadCurrentTeachers() {
    try {
        const response = await fetch(`/api/teachers?_t=${Date.now()}`); // キャッシュ回避
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const teachers = await response.json();
        
        console.log('👨‍🏫 教師データ読み込み:', teachers);
        
        const html = teachers.map(teacher => `
            <div class="item-card">
                <div class="item-info">
                    <strong>${teacher.name}</strong> (${teacher.email})
                    <br><small>担当: ${teacher.subjects.join(', ')} - ${teacher.employment_type}</small>
                </div>
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteTeacher(${teacher.id})">🗑️</button>
                </div>
            </div>
        `).join('');
        
        document.getElementById('currentTeachers').innerHTML = html;
        
    } catch (error) {
        console.error('教師読み込みエラー:', error);
        document.getElementById('currentTeachers').innerHTML = '<p>教師の読み込みに失敗しました</p>';
    }
}

// 教師を追加
async function addTeacher() {
    const teacherData = {
        name: document.getElementById('newTeacherName').value,
        email: document.getElementById('newTeacherEmail').value,
        subjects: document.getElementById('teacherSubjects').value.split(',').map(s => s.trim()).filter(s => s.length > 0),
        employment_type: document.getElementById('employmentType').value,
        max_daily_lessons: parseInt(document.getElementById('teacherMaxLessons').value)
    };
    
    if (!teacherData.name || teacherData.subjects.length === 0) {
        showMessage('教師名と担当科目は必須です', 'error');
        return;
    }
    
    try {
        console.log('👨‍🏫 教師追加データ:', teacherData);
        
        const response = await fetch(`${CUSTOMIZE_API}/teacher`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(teacherData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log('👨‍🏫 教師追加結果:', result);
        
        if (result.status === 'success') {
            showMessage('✅ ' + result.message, 'success');
            
            document.getElementById('newTeacherName').value = '';
            document.getElementById('newTeacherEmail').value = '';
            document.getElementById('teacherSubjects').value = '';
            
            // 強制的にリスト更新
            await loadCurrentTeachers();
            
            setTimeout(() => {
                refreshData();
            }, 1500);
            
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
        
    } catch (error) {
        console.error('教師追加エラー:', error);
        showMessage('教師の追加に失敗しました', 'error');
    }
}

// 教師を削除
async function deleteTeacher(teacherId) {
    if (!confirm('この教師を削除しますか？')) {
        return;
    }
    
    try {
        const response = await fetch(`${CUSTOMIZE_API}/teacher?id=${teacherId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showMessage('✅ ' + result.message, 'success');
            await loadCurrentTeachers();
            setTimeout(() => {
                refreshData();
            }, 1000);
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
        
    } catch (error) {
        console.error('教師削除エラー:', error);
        showMessage('教師の削除に失敗しました', 'error');
    }
}

// メッセージ表示
function showMessage(message, type = 'info') {
    const existingMessage = document.querySelector('.message-popup');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageEl = document.createElement('div');
    messageEl.className = `message-popup message-${type}`;
    messageEl.innerHTML = message;
    
    messageEl.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 2000;
        max-width: 300px;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease-out;
        ${type === 'success' ? 'background: #27ae60;' : ''}
        ${type === 'error' ? 'background: #e74c3c;' : ''}
        ${type === 'info' ? 'background: #3498db;' : ''}
    `;
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        if (messageEl.parentNode) {
            messageEl.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.remove();
                }
            }, 300);
        }
    }, 3000);
}

// モーダル外クリックで閉じる
window.onclick = function(event) {
    const modal = document.getElementById('customizeModal');
    if (event.target === modal) {
        closeCustomizePanel();
    }
}

// デバッグ用
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 カスタマイズJS読み込み完了');
    const modal = document.getElementById('customizeModal');
    if (modal) {
        console.log('✅ customizeModal要素確認');
        modal.classList.add('hidden');
    } else {
        console.error('❌ customizeModal要素が見つかりません');
    }
});
