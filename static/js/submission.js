document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        var word = document.getElementById('wordInput').value;
        fetch('/check_word', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'word': word })
        })
        .then(response => response.json())
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
        });
    });
});
