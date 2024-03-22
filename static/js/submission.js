document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        var word = document.getElementById('wordInput').value;
        var csrfToken = document.querySelector('input[name="csrf_token"]').value;

        fetch('/check_word', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            },
            body: JSON.stringify({ 'word': word })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.isValid) {
                console.log("Correct!");
                document.getElementById('wordInput').value = '';
            } else {
                console.log("Nope!");
                alert(data.reason);
            }
            document.getElementById('score').textContent = data.score;
            document.getElementById('letters').textContent = data.letters;
            document.getElementById('wordsLeft').textContent = data.attemptsLeft;

            if (data.gameOver) {
                alert(`Game over! You have received ${data.score} score.`);
                window.location.href = homeUrl;
            }
        }).catch(error => {
            console.error('Fetch error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
