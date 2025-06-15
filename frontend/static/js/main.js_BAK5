// 最適化処理（非同期対応版）
async function runOptimizationTest() {
    try {
        console.log('最適化テスト開始');
        updateStatus('🚀 最適化処理を開始しています...', 'info');
        
        // 最適化開始
        const startResponse = await fetch('/api/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        
        if (!startResponse.ok) {
            throw new Error(`最適化開始エラー: ${startResponse.status}`);
        }
        
        const startResult = await startResponse.json();
        console.log('最適化開始:', startResult);
        
        // 結果をポーリングで取得
        await pollOptimizationStatus();
        
    } catch (error) {
        console.error('❌ 最適化エラー:', error);
        updateStatus(`❌ 最適化エラー: ${error.message}`, 'error');
    }
}

// 最適化状態をポーリング
async function pollOptimizationStatus() {
    const maxAttempts = 30; // 最大30回（30秒）
    let attempts = 0;
    
    const pollInterval = setInterval(async () => {
        try {
            attempts++;
            
            const response = await fetch('/api/optimization-status');
            const status = await response.json();
            
            console.log(`状態確認 ${attempts}:`, status);
            
            if (!status.running) {
                clearInterval(pollInterval);
                
                if (status.result && status.result.success) {
                    updateStatus('✅ 最適化が完了しました！', 'success');
                    displayOptimizationResult(status.result);
                } else if (status.error) {
                    updateStatus(`❌ 最適化エラー: ${status.error}`, 'error');
                } else {
                    updateStatus('❌ 最適化が失敗しました', 'error');
                }
            } else {
                updateStatus(`🔄 最適化中... (${status.progress}%)`, 'info');
            }
            
            if (attempts >= maxAttempts) {
                clearInterval(pollInterval);
                updateStatus('⏰ 最適化がタイムアウトしました', 'error');
            }
            
        } catch (error) {
            console.error('状態確認エラー:', error);
            clearInterval(pollInterval);
            updateStatus(`❌ 状態確認エラー: ${error.message}`, 'error');
        }
    }, 1000); // 1秒間隔
}