document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('messageForm').addEventListener('submit', function(e) {
        e.preventDefault();
        var content = document.getElementById('messageContent').value;
        var csrfToken = document.querySelector('input[name="csrf_token"]').value;
        
        fetch('/post_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({'content': content}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                console.error(data.error);
            }
        });
    });
});
