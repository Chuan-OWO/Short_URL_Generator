function deletelog(id) {
    if(confirm(`確定要刪除編號為 ${id} 的資料嗎?`)){
        fetch(`/delete/${id}`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                location.reload();  // 重新載入頁面
            } else {
                console.error('刪除失敗');
            }
        })
        .catch(error => {
            console.error('刪除失敗', error);
        });
    }
}